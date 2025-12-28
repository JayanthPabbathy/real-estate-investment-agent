"""
Test Suite for Investment Intelligence Platform
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from models.schemas import PropertyInput, InvestmentContext, City, PropertyType


class TestSchemas:
    """Test Pydantic schemas"""
    
    def test_property_input_valid(self):
        """Test valid property input"""
        property_data = PropertyInput(
            city=City.MUMBAI,
            locality="Andheri",
            property_type=PropertyType.APARTMENT,
            size_sqft=1200,
            bedrooms=2,
            bathrooms=2,
            property_age=5,
            distance_to_metro_km=1.5,
            has_parking=True,
            floor=3
        )
        assert property_data.city == City.MUMBAI
        assert property_data.size_sqft == 1200
    
    def test_investment_context_valid(self):
        """Test valid investment context"""
        context = InvestmentContext(
            investment_horizon_years=5,
            primary_goal="both",
            risk_tolerance="medium",
            budget_range_min=10000000,
            budget_range_max=15000000,
            financing_required=True
        )
        assert context.investment_horizon_years == 5
        assert context.primary_goal == "both"
    
    def test_investment_context_invalid_goal(self):
        """Test invalid primary goal"""
        with pytest.raises(ValueError):
            InvestmentContext(
                investment_horizon_years=5,
                primary_goal="invalid_goal",
                risk_tolerance="medium"
            )


class TestDataGeneration:
    """Test data generation"""
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        from data_generation import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(n_samples=100)
        df = generator.generate_structured_data()
        
        assert len(df) == 100
        assert 'property_id' in df.columns
        assert 'city' in df.columns
        assert 'price' in df.columns
        assert df['price'].min() > 0
    
    def test_market_documents_generation(self):
        """Test market documents generation"""
        from data_generation import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator()
        docs = generator.generate_market_documents()
        
        assert len(docs) > 0
        assert 'doc_id' in docs[0]
        assert 'title' in docs[0]
        assert 'content' in docs[0]


class TestPredictiveModels:
    """Test predictive models"""
    
    def test_feature_engineering(self):
        """Test feature engineering"""
        from models.predictive_models import FeatureEngineering
        import pandas as pd
        
        df = pd.DataFrame([{
            'city': 'Mumbai',
            'locality': 'Andheri',
            'property_type': 'Apartment',
            'size_sqft': 1200,
            'bedrooms': 2,
            'bathrooms': 2,
            'property_age': 5,
            'distance_to_metro_km': 1.5,
            'has_parking': True,
            'floor': 3,
            'price': 12000000,
            'monthly_rent': 40000
        }])
        
        df_engineered = FeatureEngineering.create_features(df)
        
        assert 'price_per_sqft' in df_engineered.columns
        assert 'metro_score' in df_engineered.columns
        assert df_engineered['price_per_sqft'].iloc[0] == 10000


@pytest.mark.asyncio
class TestAgenticSystem:
    """Test agentic system"""
    
    async def test_agent_message_creation(self):
        """Test agent message creation"""
        from agents.agentic_system import Agent, AgentRole, AgentMessage
        
        class DummyAgent(Agent):
            async def process(self, message):
                return self.create_message(
                    receiver=message.sender,
                    message_type="response",
                    payload={"status": "ok"}
                )
        
        agent = DummyAgent(AgentRole.VALUATION)
        
        msg = AgentMessage(
            sender=AgentRole.ORCHESTRATOR,
            receiver=AgentRole.VALUATION,
            message_type="test",
            payload={}
        )
        
        response = await agent.process(msg)
        assert response.sender == AgentRole.VALUATION
        assert response.payload["status"] == "ok"


class TestRAGSystem:
    """Test RAG system"""
    
    def test_document_chunking(self):
        """Test document chunking"""
        from rag.vector_store import DocumentChunker
        
        text = "This is a test. " * 100
        chunks = DocumentChunker.chunk_by_paragraph(text, max_chunk_size=50, overlap=10)
        
        assert len(chunks) > 0
        assert all(len(chunk.split()) <= 60 for chunk in chunks)  # Allow some overflow


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
