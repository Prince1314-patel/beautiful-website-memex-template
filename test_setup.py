#!/usr/bin/env python3
"""
Test script to verify the Voice Chat Application setup
"""

import sys
import os
from pathlib import Path

def test_dependencies():
    """Test if all required dependencies are available"""
    dependencies = [
        'flask',
        'torch',
        'torchaudio', 
        'groq',
        'langchain',
        'langchain_groq',
        'chatterbox'
    ]
    
    print("🔍 Testing dependencies...")
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run 'uv pip install -r requirements.txt' to install missing packages")
        return False
    
    print("\n✅ All dependencies are available!")
    return True

def test_environment():
    """Test environment variables and configuration"""
    print("\n🔍 Testing environment...")
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("⚠️ GROQ_API_KEY not set (required for full functionality)")
        return False
    else:
        print(f"✅ GROQ_API_KEY is set ({'*' * 10}...)")
        return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js'
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files exist!")
    return True

def test_imports():
    """Test critical imports"""
    print("\n🔍 Testing critical imports...")
    
    try:
        from chatterbox.tts import ChatterboxTTS
        print("✅ ChatterboxTTS import successful")
    except Exception as e:
        print(f"❌ ChatterboxTTS import failed: {e}")
        return False
    
    try:
        from groq import Groq
        print("✅ Groq client import successful")
    except Exception as e:
        print(f"❌ Groq client import failed: {e}")
        return False
    
    try:
        from langchain_groq import ChatGroq
        print("✅ ChatGroq import successful")
    except Exception as e:
        print(f"❌ ChatGroq import failed: {e}")
        return False
    
    print("\n✅ All critical imports successful!")
    return True

def main():
    """Run all tests"""
    print("🎤 Voice Chat Application Setup Test")
    print("=====================================")
    
    tests = [
        test_file_structure,
        test_dependencies,
        test_imports,
        test_environment
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*50)
    if all(results):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the application:")
        print("1. Set GROQ_API_KEY if not already set: set GROQ_API_KEY=your_key")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())