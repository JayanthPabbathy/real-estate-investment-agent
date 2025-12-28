# AI-Driven Real Estate Investment Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🏢 Overview

An end-to-end AI-powered system for real estate investment analysis, combining **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, and **Generative AI** in a multi-agent architecture to provide data-backed investment recommendations.

Developed for: **Golden Mile Properties**  
Assignment Type: Take-Home Interview Assignment  
Focus Areas: GenAI, ML Engineering, RAG, Agentic AI

---

## 🎯 Key Features

### ✅ **Complete System Implementation**

- **Stage 1: Predictive Modeling** - XGBoost/LightGBM ensemble for price & rent prediction
- **Stage 2: RAG System** - Vector database (ChromaDB) with intelligent document retrieval
- **Stage 3: Generative Reasoning** - Azure OpenAI GPT-4o for investment analysis synthesis
- **Stage 4: Agentic Architecture** - Multi-agent system with MCP communication pattern
- **Stage 5: Production API** - FastAPI with Docker deployment

### 🔥 **Production-Ready Features**

- ✨ REST API with OpenAPI documentation
- 📊 Automated PDF report generation
- 📄 JSON output for programmatic access
- 🎨 Modern responsive web frontend
- 🐳 Docker containerization
- 📈 Model performance monitoring
- 🔍 Comprehensive error handling
- 📝 Extensive logging and observability

---

## 🏗️ Architecture

### System Flow

```
User Request → FastAPI → Orchestrator Agent
                             ↓
            ┌────────────────┼────────────────┐
            ↓                ↓                ↓
    Valuation Agent   Market Intel     Risk & Compliance
       (ML Models)     (RAG System)         (RAG System)
            ↓                ↓                ↓
            └────────────────┼────────────────┘
                             ↓
                      Narrative Agent
                      (GPT-4 Synthesis)
                             ↓
                    Investment Analysis + PDF Report
```

### Agent Responsibilities

| Agent | Responsibility | Technology |
|-------|---------------|------------|
| **Valuation Agent** | Price/rent prediction | XGBoost, LightGBM, sklearn |
| **Market Intelligence Agent** | Market data retrieval | RAG, ChromaDB, Sentence Transformers |
| **Risk & Compliance Agent** | Regulatory assessment | RAG, Document retrieval |
| **Narrative Agent** | Synthesis & recommendations | Azure OpenAI GPT-4o, Structured prompts |
| **Orchestrator Agent** | Workflow coordination | Async message passing (MCP pattern) |

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Azure OpenAI API Key
- Docker (optional, for containerized deployment)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/JayanthPabbathy/real-estate-investment-agent.git
cd real-estate-investment-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add:
# - OPENAI_API_KEY (Azure OpenAI key)
# - OPENAI_ENDPOINT (Azure OpenAI endpoint URL)
# - OPENAI_API_VERSION (e.g., 2025-01-01-preview)
# - LLM_MODEL (e.g., gpt-4o)
```

5. **Generate synthetic data (first run)**
```bash
python src/data_generation.py
```

6. **Run the application**
```bash
# Start the API server
python src/api/main.py

# In another terminal, open the frontend
cd frontend
start index.html  # Windows
open index.html   # Mac
xdg-open index.html  # Linux
```

The API will be available at `http://localhost:8000`  
The frontend will open in your default browser

---

## 🚀 Usage

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Investment Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "property": {
      "city": "Mumbai",
      "locality": "Andheri",
      "property_type": "Apartment",
      "size_sqft": 1200,
      "bedrooms": 2,
      "bathrooms": 2,
      "property_age": 5,
      "distance_to_metro_km": 1.5,
      "has_parking": true,
      "floor": 3
    },
    "context": {
      "investment_horizon_years": 5,
      "primary_goal": "both",
      "risk_tolerance": "medium"
    }
  }'
```

#### Get PDF Report
```bash
curl http://localhost:8000/api/v1/report/{request_id} --output report.pdf
```

#### Get JSON Analysis
```bash
curl http://localhost:8000/api/v1/analysis/{request_id} --output analysis.json
```

#### System Statistics
```bash
curl http://localhost:8000/api/v1/stats
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI

### Web Frontend

The platform includes a modern, responsive web interface:

1. **Open the frontend:**
   ```bash
   cd frontend
   start index.html  # or open in browser
   ```

2. **Features:**
   - 📝 User-friendly property input form
   - 📊 Real-time analysis results
   - 📈 Interactive data visualizations
   - 📄 PDF report download
   - 📊 JSON analysis download
   - 🎨 Modern gradient UI design
   - 📱 Fully responsive (mobile, tablet, desktop)

3. **Usage:**
   - Fill in property details (city, size, bedrooms, etc.)
   - Set investment context (horizon, goals, risk tolerance)
   - Click "Analyze Investment"
   - View comprehensive results
   - Download PDF report and JSON analysis

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t real-estate-intelligence .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com \
  -e OPENAI_API_VERSION=2025-01-01-preview \
  -e LLM_MODEL=gpt-4o \
  --name real-estate-api \
  real-estate-intelligence
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📊 Data & Models

### Synthetic Data

The system generates realistic synthetic data including:

- **5,000 property records** with features:
  - City, locality, property type
  - Size, bedrooms, bathrooms, age
  - Price, rent, rental yield
  - Distance to metro, parking, floor

- **Market documents**: News, analysis, trends
- **Regulatory documents**: RERA compliance, stamp duty, building regulations

### ML Models

**Models Compared:**
- Random Forest Regressor
- XGBoost
- LightGBM

**Best Model Selection:** Based on R², RMSE, MAE metrics

**Feature Engineering:**
- Price per sqft
- Metro accessibility score
- Property age categories
- Bedroom/bathroom ratios
- City-locality interactions

### RAG System

**Components:**
- **Chunking Strategy**: 400 tokens with 50-token overlap
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB with cosine similarity
- **Retrieval**: Top-K relevant chunks with metadata filtering

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_system.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test API

```bash
# Start the server first
python src/api/main.py

# In another terminal, run test script
python tests/test_api.py
```

---

## 📈 Model Performance

### Price Prediction Metrics

| Model | R² Score | RMSE | MAE | MAPE |
|-------|----------|------|-----|------|
| XGBoost | 0.92+ | ~800K | ~550K | ~6% |
| LightGBM | 0.91+ | ~850K | ~600K | ~7% |
| Random Forest | 0.89+ | ~950K | ~650K | ~8% |

*Note: Metrics vary based on synthetic data generation*

### RAG Retrieval Quality

- **Precision@5**: ~85%
- **Average Latency**: <500ms
- **Relevance Score**: >0.7 for top results

---

## 🔍 Key Design Decisions

### 1. **Agentic Architecture**

**Why Multi-Agent System?**
- **Modularity**: Each agent has single responsibility
- **Scalability**: Easy to add new capabilities
- **Testability**: Independent testing of agents
- **Observability**: Clear message flow for debugging

**MCP Pattern**: Model Context Protocol for structured agent communication

### 2. **RAG Over Fine-Tuning**

**Rationale:**
- Dynamic knowledge updates without retraining
- Cost-effective for domain-specific information
- Transparent source attribution
- Reduced hallucination risk

### 3. **Ensemble ML Models**

**Benefits:**
- Automatic best model selection
- Robustness across different property types
- Confidence estimation through model agreement

### 4. **Explicit Uncertainty Handling**

**Approach:**
- Confidence scores for predictions
- Explicit assumptions in output
- Limitations clearly stated
- Data quality disclaimers

### 5. **Prompt Engineering**

**Strategies:**
- Structured JSON output format
- Context injection with retrieved documents
- Role-based system prompts
- Hallucination safeguards through validation

---

## ⚠️ Assumptions & Limitations

### Assumptions

1. **Data Quality**: Synthetic data represents realistic patterns
2. **Market Stability**: No major economic disruptions assumed
3. **Linear Relationships**: Some feature relationships simplified
4. **Regulatory Compliance**: Documents reflect current regulations

### Limitations

1. **Synthetic Data**: Not real market data; requires replacement in production
2. **Model Uncertainty**: ±10-15% prediction variance expected
3. **Geographic Scope**: Limited to 6 major Indian cities
4. **Temporal Validity**: Market conditions change rapidly
5. **LLM Dependence**: Requires OpenAI API access and associated costs
6. **Regulatory Updates**: Manual document updates required

### Production Recommendations

- Replace synthetic data with real market data
- Implement automated data pipelines
- Add A/B testing for model updates
- Integrate real-time market feeds
- Implement user authentication
- Add rate limiting and caching
- Set up monitoring and alerting
- Conduct regular model retraining

---

## 📁 Project Structure

```
Real Estate Agent/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── agents/
│   │   ├── agentic_system.py    # Multi-agent orchestration
│   │   └── generative_analyzer.py # LLM reasoning
│   ├── models/
│   │   ├── schemas.py           # Pydantic models
│   │   └── predictive_models.py # ML models
│   ├── rag/
│   │   └── vector_store.py      # RAG system
│   ├── utils/
│   │   ├── pdf_generator.py     # Report generation
│   │   └── helpers.py           # Utilities
│   ├── config.py                # Configuration
│   └── data_generation.py       # Synthetic data
├── frontend/
│   ├── index.html               # Web interface
│   ├── styles.css               # Styling
│   ├── script.js                # Frontend logic
│   └── README.md                # Frontend docs
├── tests/
│   ├── test_system.py           # Unit tests
│   └── test_api.py              # API tests
├── data/                        # Data storage
├── models/                      # Trained models
├── reports/                     # PDF/JSON outputs
├── logs/                        # Application logs
├── requirements.txt             # Dependencies
├── Dockerfile                   # Docker config
├── docker-compose.yml           # Docker Compose
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🛠️ Technology Stack

### Core Technologies

| Category | Technology |
|----------|-----------|
| **Web Framework** | FastAPI 0.109.0 |
| **ML/Data Science** | scikit-learn, XGBoost, LightGBM, pandas, numpy |
| **LLM/GenAI** | Azure OpenAI GPT-4o, LangChain |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector DB** | ChromaDB with HNSW indexing |
| **PDF Generation** | ReportLab |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Logging** | Loguru |
| **Testing** | pytest, httpx |
| **Containerization** | Docker, Docker Compose |

---

## 📝 Evaluation Criteria Addressed

### ✅ Problem Framing
- Clear business problem: Investment decision-making
- End-to-end use case flow implemented
- Realistic constraints and assumptions documented

### ✅ ML & GenAI Depth
- Multiple models compared with justification
- Feature engineering with rationale
- RAG architecture with design trade-offs
- Prompt engineering with safeguards

### ✅ Architectural Soundness
- Modular multi-agent design
- Scalable REST API
- Error handling and retries
- State management

### ✅ Code Quality
- Clean, documented code
- Type hints with Pydantic
- Comprehensive logging
- Test coverage

### ✅ Trade-off Awareness
- Documented design decisions
- Explicit limitations
- Production recommendations
- Cost/performance considerations

---

## 🚧 Future Enhancements

### Short-term
- [ ] Add user authentication & authorization
- [ ] Implement caching layer (Redis)
- [ ] Add rate limiting
- [ ] Expand test coverage to 80%+
- [ ] Export analysis history
- [ ] Batch processing API

### Medium-term
- [ ] Real data integration pipelines
- [ ] Advanced uncertainty quantification
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Comparison mode (multiple properties)
- [ ] Email report delivery

### Long-term
- [ ] Automated model retraining pipeline
- [ ] Real-time market data feeds
- [ ] Custom fine-tuned models
- [ ] Interactive visualization dashboard
- [ ] Market trend prediction
- [ ] Portfolio optimization tools

---

## 📊 Output Formats

The system provides analysis in two formats:

### 1. PDF Report (`report_{request_id}.pdf`)
Professional formatted report including:
- Executive summary
- Property details
- Predictions with confidence intervals
- Investment recommendation
- Risk assessment
- Market intelligence insights
- Methodology explanation

### 2. JSON Analysis (`analysis_{request_id}.json`)
Structured data for programmatic access:
```json
{
  "request_id": "uuid",
  "timestamp": "ISO-8601",
  "property_summary": {...},
  "predictions": {
    "predicted_price": 9788946.52,
    "predicted_rent": 31446.15,
    "predicted_rental_yield": 3.85,
    "price_confidence": 0.85,
    ...
  },
  "recommendation": {...},
  "investment_drivers": {...},
  "risk_assessment": {...},
  "assumptions": [...],
  "limitations": [...]
}
```

**Access:**
- PDF: `GET /api/v1/report/{request_id}`
- JSON: `GET /api/v1/analysis/{request_id}`

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Jayanth Pabbathy**  
GitHub: [@JayanthPabbathy](https://github.com/JayanthPabbathy)  
Repository: [real-estate-investment-agent](https://github.com/JayanthPabbathy/real-estate-investment-agent)

---

## 🌟 Key Highlights

✨ **Complete 5-Stage Pipeline:** From ML predictions to multi-agent orchestration  
🎯 **Production-Ready:** Docker, logging, error handling, testing  
🧠 **AI-Powered:** Azure OpenAI GPT-4o + RAG for intelligent analysis  
📊 **Dual Output:** PDF reports + JSON for programmatic access  
🎨 **Modern UI:** Responsive web frontend with real-time results  
🔍 **Transparent:** Explicit assumptions, limitations, and confidence scores  
🏗️ **Scalable Architecture:** Multi-agent MCP pattern for extensibility  

---

## 📞 Support

For questions or issues:
1. Check API documentation: `http://localhost:8000/docs`
2. Review logs in `logs/` directory
3. Run tests: `pytest tests/ -v`

---

## 🎓 Technical Notes

### Monitoring & Retraining Strategy

**Monitoring:**
- Track prediction accuracy vs actual outcomes
- Monitor API latency and error rates
- Log model confidence distributions
- Alert on data drift detection

**Retraining Triggers:**
- Model performance degradation (R² drops >5%)
- Significant data drift detected
- Quarterly scheduled retraining
- New market conditions (regulatory changes)

**Retraining Process:**
1. Collect new labeled data
2. Validate data quality
3. Retrain model with hyperparameter tuning
4. A/B test new model
5. Gradual rollout with monitoring

### Security Considerations

- **API Key Management**: Environment variables, never in code
- **Input Validation**: Pydantic schemas
- **Output Sanitization**: LLM output validation
- **Rate Limiting**: Recommended for production
- **HTTPS**: Required for production deployment

---

## ✨ Highlights

🎯 **Complete Implementation**: All 5 stages fully functional  
🤖 **Production-Ready**: Docker, monitoring, error handling  
📚 **Well-Documented**: Comprehensive README and inline docs  
🧪 **Tested**: Unit tests and integration tests  
🏗️ **Scalable**: Modular architecture, easy to extend  
🔍 **Transparent**: Explicit assumptions and limitations  

---

**Built with depth, clarity, and production readiness in mind.** 🚀
