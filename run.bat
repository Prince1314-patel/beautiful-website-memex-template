@echo off
echo 🎤 Starting Luna Voice Chat Assistant
echo ===================================

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if GROQ_API_KEY is set
if "%GROQ_API_KEY%"=="" (
    echo ❌ GROQ_API_KEY environment variable is not set.
    echo Please set your API key: set GROQ_API_KEY=your_api_key_here
    echo Get your API key from: https://console.groq.com
    pause
    exit /b 1
)

echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 🚀 Starting application...
echo Open your browser and navigate to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py