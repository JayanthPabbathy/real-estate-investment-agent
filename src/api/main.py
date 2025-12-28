"""
Stage 5: FastAPI Application
REST API for investment intelligence system
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
import uuid
from datetime import datetime
from loguru import logger
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from models.schemas import (
    InvestmentRequest, InvestmentResponse, HealthResponse,
    PredictionOutput, InvestmentDrivers, RiskAssessment,
    InvestmentRecommendation, RetrievedDocument
)
from models.predictive_models import PredictiveModel
from rag.vector_store import setup_rag_system
from agents.generative_analyzer import GenerativeAnalyzer
from agents.agentic_system import AgenticSystem
from utils.pdf_generator import InvestmentReportGenerator
from data_generation import SyntheticDataGenerator

# Global instances
predictive_model = None
rag_system = None
generative_analyzer = None
agentic_system = None
report_generator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global predictive_model, rag_system, generative_analyzer, agentic_system, report_generator
    
    logger.info("Starting application initialization...")
    
    # Setup logging
    logger.add(
        settings.LOGS_DIR / "api_{time}.log",
        rotation="1 day",
        retention="7 days",
        level=settings.LOG_LEVEL
    )
    
    # Generate data if not exists
    if not (settings.DATA_DIR / "properties_data.csv").exists():
        logger.info("Generating synthetic data...")
        generator = SyntheticDataGenerator(n_samples=settings.SYNTHETIC_DATA_SIZE)
        generator.save_datasets(settings.DATA_DIR)
    
    # Load or train predictive models
    model_path = Path(settings.MODEL_CACHE_DIR)
    predictive_model = PredictiveModel()
    
    if (model_path / "price_model.joblib").exists():
        logger.info("Loading existing models...")
        predictive_model.load_model(model_path)
    else:
        logger.info("Training new models...")
        import pandas as pd
        df = pd.read_csv(settings.DATA_DIR / "properties_data.csv")
        predictive_model.train_ensemble(df)
        predictive_model.save_model(model_path)
    
    # Setup RAG system
    logger.info("Setting up RAG system...")
    rag_system = setup_rag_system(
        settings.DATA_DIR,
        Path(settings.VECTOR_DB_PATH)
    )
    
    # Initialize generative analyzer
    logger.info("Initializing generative analyzer...")
    generative_analyzer = GenerativeAnalyzer(
        api_key=settings.OPENAI_API_KEY,
        endpoint=settings.OPENAI_ENDPOINT,
        api_version=settings.OPENAI_API_VERSION,
        model=settings.LLM_MODEL,
        temperature=settings.OPENAI_TEMPERATURE
    )
    
    # Initialize agentic system
    logger.info("Initializing agentic system...")
    agentic_system = AgenticSystem(
        predictive_model=predictive_model,
        rag_system=rag_system,
        generative_analyzer=generative_analyzer
    )
    
    # Initialize report generator
    report_generator = InvestmentReportGenerator(settings.REPORTS_DIR)
    
    logger.info("Application initialization completed successfully")
    
    yield
    
    # Cleanup
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Driven Real Estate Investment Intelligence Platform",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Real Estate Investment Intelligence Platform",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.now(),
        models_loaded=predictive_model is not None,
        vector_db_status="connected" if rag_system is not None else "disconnected"
    )


@app.post("/api/v1/analyze", response_model=InvestmentResponse, tags=["Analysis"])
async def analyze_investment(request: InvestmentRequest, background_tasks: BackgroundTasks):
    """
    Analyze investment opportunity
    
    This endpoint performs comprehensive investment analysis using:
    - ML models for price/rent prediction
    - RAG for market intelligence
    - Generative AI for reasoning
    - Multi-agent orchestration
    """
    
    try:
        # Generate request ID
        request_id = request.request_id or str(uuid.uuid4())
        logger.info(f"Processing investment analysis request: {request_id}")
        
        # Convert property data to dict
        property_data = {
            'city': request.property.city.value,
            'locality': request.property.locality,
            'property_type': request.property.property_type.value,
            'size_sqft': request.property.size_sqft,
            'bedrooms': request.property.bedrooms,
            'bathrooms': request.property.bathrooms,
            'property_age': request.property.property_age,
            'distance_to_metro_km': request.property.distance_to_metro_km or 5.0,
            'has_parking': request.property.has_parking,
            'floor': request.property.floor or 0,
            'price': 0,  # Will be predicted
            'monthly_rent': 0  # Will be predicted
        }
        
        # Convert investment context
        investment_context = {
            'investment_horizon_years': request.context.investment_horizon_years,
            'primary_goal': request.context.primary_goal,
            'risk_tolerance': request.context.risk_tolerance
        }
        
        # Execute agentic analysis
        result = await agentic_system.analyze_investment(
            property_data=property_data,
            investment_context=investment_context
        )
        
        # Extract results
        predictions = result.get('predictions')
        analysis = result.get('analysis')
        retrieved_docs = result.get('retrieved_documents', [])
        
        # Validate results
        if not predictions:
            logger.error("No predictions returned from agentic system")
            raise HTTPException(status_code=500, detail="Failed to generate predictions")
        
        if not analysis:
            logger.error("No analysis returned from agentic system")
            raise HTTPException(status_code=500, detail="Failed to generate analysis")
        
        logger.debug(f"Predictions: {predictions}")
        logger.debug(f"Analysis keys: {list(analysis.keys()) if analysis else 'None'}")
        
        # Format retrieved documents
        formatted_docs = [
            RetrievedDocument(
                doc_id=doc['metadata']['doc_id'],
                title=doc['metadata']['title'],
                content=doc['content'],
                relevance_score=doc.get('relevance_score', 0.0),
                category=doc['metadata'].get('category', 'unknown'),
                source='vector_db'
            )
            for doc in retrieved_docs[:5]
        ]
        
        # Create response
        response = InvestmentResponse(
            request_id=request_id,
            timestamp=datetime.now(),
            property_summary={
                'city': property_data['city'],
                'locality': property_data['locality'],
                'property_type': property_data['property_type'],
                'size_sqft': property_data['size_sqft'],
                'bedrooms': property_data['bedrooms'],
                'property_age': property_data['property_age']
            },
            predictions=PredictionOutput(**predictions),
            investment_drivers=InvestmentDrivers(
                positive_drivers=analysis.get('positive_drivers', []),
                negative_drivers=analysis.get('negative_drivers', []),
                market_sentiment=analysis.get('market_sentiment', 'Neutral'),
                location_score=analysis.get('location_score', 5.0),
                infrastructure_score=analysis.get('infrastructure_score', 5.0)
            ),
            risk_assessment=RiskAssessment(
                risk_level=analysis.get('risk_level', 'medium'),
                risk_factors=analysis.get('risk_factors', []),
                mitigation_strategies=analysis.get('mitigation_strategies', []),
                regulatory_compliance_score=analysis.get('regulatory_compliance_score', 0.7)
            ),
            recommendation=InvestmentRecommendation(
                recommendation=analysis.get('recommendation', 'Hold'),
                confidence_score=analysis.get('confidence_score', 0.5),
                reasoning=analysis.get('reasoning', 'Analysis completed'),
                expected_appreciation_3yr=analysis.get('expected_appreciation_3yr'),
                expected_appreciation_5yr=analysis.get('expected_appreciation_5yr'),
                expected_roi=analysis.get('expected_roi')
            ),
            retrieved_documents=formatted_docs,
            assumptions=analysis.get('assumptions', []),
            limitations=analysis.get('limitations', [])
        )
        
        # Generate PDF report in background
        report_filename = f"report_{request_id}.pdf"
        
        def generate_report():
            report_data = {
                'request_id': request_id,
                'property_summary': response.property_summary,
                'predictions': predictions,
                'recommendation': {
                    'recommendation': response.recommendation.recommendation,
                    'confidence_score': response.recommendation.confidence_score,
                    'reasoning': response.recommendation.reasoning,
                    'expected_appreciation_3yr': response.recommendation.expected_appreciation_3yr,
                    'expected_appreciation_5yr': response.recommendation.expected_appreciation_5yr,
                    'expected_roi': response.recommendation.expected_roi
                },
                'investment_drivers': {
                    'positive_drivers': response.investment_drivers.positive_drivers,
                    'negative_drivers': response.investment_drivers.negative_drivers
                },
                'risk_assessment': {
                    'risk_level': response.risk_assessment.risk_level,
                    'risk_factors': response.risk_assessment.risk_factors,
                    'mitigation_strategies': response.risk_assessment.mitigation_strategies,
                    'regulatory_compliance_score': response.risk_assessment.regulatory_compliance_score
                },
                'assumptions': response.assumptions,
                'limitations': response.limitations
            }
            report_generator.generate_report(report_data, report_filename)
        
        background_tasks.add_task(generate_report)
        response.report_url = f"/api/v1/report/{request_id}"
        
        logger.info(f"Investment analysis completed: {request_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/report/{request_id}", tags=["Reports"])
async def get_report(request_id: str):
    """Download PDF report"""
    
    report_file = settings.REPORTS_DIR / f"report_{request_id}.pdf"
    
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=report_file,
        media_type="application/pdf",
        filename=f"investment_report_{request_id}.pdf"
    )


@app.get("/api/v1/stats", tags=["Statistics"])
async def get_stats():
    """Get system statistics"""
    
    vector_stats = rag_system.vector_store.get_collection_stats()
    
    return {
        "model_metrics": predictive_model.metrics if hasattr(predictive_model, 'metrics') else {},
        "vector_db": vector_stats,
        "reports_generated": len(list(settings.REPORTS_DIR.glob("*.pdf")))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
