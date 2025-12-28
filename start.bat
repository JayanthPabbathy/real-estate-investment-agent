@echo off
REM Quick start script for Windows

echo ============================================
echo Real Estate Investment Intelligence Platform
echo ============================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Check for .env file
if not exist ".env" (
    echo Warning: No .env file found. Creating from template...
    copy .env.example .env
    echo Please edit .env and add your OPENAI_API_KEY
    exit /b 1
)

REM Generate data
if not exist "data\properties_data.csv" (
    echo Generating synthetic data...
    python src\data_generation.py
)

REM Train models
if not exist "models\price_model.joblib" (
    echo Training ML models...
    python src\models\predictive_models.py
)

REM Setup vector database
if not exist "data\vector_db" (
    echo Setting up vector database...
    python src\rag\vector_store.py
)

echo.
echo Setup complete!
echo.
echo To start the server:
echo   python src\api\main.py
echo.
echo API will be available at: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo.
pause
