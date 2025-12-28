#!/bin/bash
# Quick start script for the application

echo "🏗️  Real Estate Investment Intelligence Platform"
echo "================================================"

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Generate data if not exists
if [ ! -f "data/properties_data.csv" ]; then
    echo "Generating synthetic data..."
    python src/data_generation.py
fi

# Train models if not exists
if [ ! -f "models/price_model.joblib" ]; then
    echo "Training ML models..."
    python src/models/predictive_models.py
fi

# Setup vector database
if [ ! -d "data/vector_db" ]; then
    echo "Setting up vector database..."
    python src/rag/vector_store.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  python src/api/main.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo ""
