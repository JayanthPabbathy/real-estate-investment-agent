"""
Configuration Management Module
Handles all application settings and environment variables
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Info
    APP_NAME: str = "Real Estate Investment Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # OpenAI Configuration (Azure OpenAI)
    OPENAI_API_KEY: str
    OPENAI_ENDPOINT: str = ""
    OPENAI_API_VERSION: str = "2025-01-01-preview"
    LLM_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
    
    # Vector Database
    VECTOR_DB_TYPE: str = "chromadb"
    VECTOR_DB_PATH: str = "./data/vector_db"
    COLLECTION_NAME: str = "real_estate_docs"
    EMBEDDING_DIMENSION: int = 1536
    
    # Model Configuration
    MODEL_CACHE_DIR: str = "./models"
    CONFIDENCE_THRESHOLD: float = 0.7
    TOP_K_RETRIEVAL: int = 5
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["*"]
    
    # Paths
    DATA_DIR: Path = Path("./data")
    OUTPUT_DIR: Path = Path("./outputs")
    REPORTS_DIR: Path = Path("./reports")
    LOGS_DIR: Path = Path("./logs")
    
    # Synthetic Data Generation
    SYNTHETIC_DATA_SIZE: int = 5000
    
    # Additional optional settings from .env
    VECTOR_DB_COLLECTION: str = "real_estate_docs"
    SYNTHETIC_DATA_PATH: str = "./data/properties.csv"
    MARKET_DOCS_PATH: str = "./data/market_docs"
    REGULATORY_DOCS_PATH: str = "./data/regulatory_docs"
    MODEL_PATH: str = "./models/predictive_model.pkl"
    SCALER_PATH: str = "./models/scaler.pkl"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env


# Global settings instance
settings = Settings()

# Ensure directories exist
for dir_path in [settings.DATA_DIR, settings.OUTPUT_DIR, 
                 settings.REPORTS_DIR, settings.LOGS_DIR, 
                 Path(settings.MODEL_CACHE_DIR)]:
    dir_path.mkdir(parents=True, exist_ok=True)
