@echo off
echo 🎤 Voice Chat Application Setup
echo ================================

echo.
echo 📦 Creating virtual environment...
uv venv

echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 📥 Installing dependencies...
uv pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To run the application:
echo 1. Set your Groq API key: set GROQ_API_KEY=your_api_key_here
echo 2. Run: python app.py
echo.
echo 📝 Note: You need a Groq API key from https://console.groq.com
echo.
pause