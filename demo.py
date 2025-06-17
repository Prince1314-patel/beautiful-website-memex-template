#!/usr/bin/env python3
"""
Demo script for the Voice Chat Application
Tests basic functionality without requiring API keys
"""

import os
import tempfile
import torch
from pathlib import Path

def demo_setup_check():
    """Demonstrate the setup verification"""
    print("🎤 Luna Voice Chat Application - Demo Mode")
    print("=" * 50)
    
    # Check if we're in the right directory
    required_files = ['app.py', 'templates/index.html', 'static/style.css']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All core files present")
    
    # Check Python environment
    try:
        import flask
        import torch
        import torchaudio
        print("✅ Core dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    # Check AI libraries
    try:
        from chatterbox.tts import ChatterboxTTS
        print("✅ Chatterbox TTS available")
    except ImportError as e:
        print(f"❌ TTS library issue: {e}")
        return False
    
    return True

def demo_audio_capabilities():
    """Demonstrate audio processing capabilities"""
    print("\n🔊 Testing Audio Capabilities")
    print("-" * 30)
    
    # Check PyTorch audio support
    try:
        import torchaudio
        
        # Create a simple sine wave
        sample_rate = 16000
        duration = 1.0  # seconds
        frequency = 440  # A4 note
        
        t = torch.linspace(0, duration, int(sample_rate * duration))
        waveform = torch.sin(2 * torch.pi * frequency * t).unsqueeze(0)
        
        print(f"✅ Generated test audio: {waveform.shape}")
        
        # Test file I/O
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_file.close()  # Close file handle before using with torchaudio
        torchaudio.save(temp_file.name, waveform, sample_rate)
        
        # Verify file was created
        if os.path.exists(temp_file.name):
            file_size = os.path.getsize(temp_file.name)
            print(f"✅ Audio file saved: {file_size} bytes")
            try:
                os.unlink(temp_file.name)  # Clean up
            except OSError:
                pass  # File cleanup can fail on Windows, that's OK for demo
        else:
            print("❌ Failed to save audio file")
            return False
            
    except Exception as e:
        print(f"❌ Audio processing error: {e}")
        return False
    
    return True

def demo_tts_model():
    """Test TTS model loading (without API calls)"""
    print("\n🤖 Testing TTS Model Loading")
    print("-" * 30)
    
    try:
        from chatterbox.tts import ChatterboxTTS
        
        # Check device availability
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ Using device: {device}")
        
        # Note: We won't actually load the model to avoid long download times
        print("✅ ChatterboxTTS class accessible")
        print("📝 Note: Model loading skipped in demo mode")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS model test failed: {e}")
        return False

def demo_flask_app():
    """Test Flask app structure"""
    print("\n🌐 Testing Flask Application Structure")
    print("-" * 40)
    
    try:
        # Import our app module
        import app
        
        # Check if Flask app is properly configured
        flask_app = app.app
        print(f"✅ Flask app created: {flask_app.name}")
        
        # Check routes
        routes = [rule.rule for rule in flask_app.url_map.iter_rules()]
        expected_routes = ['/', '/chat', '/upload_reference', '/audio/<filename>']
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route registered: {route}")
            else:
                print(f"❌ Missing route: {route}")
                return False
        
        print("✅ All expected routes registered")
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n🚀 Next Steps")
    print("=" * 20)
    print("1. Get a Groq API key from: https://console.groq.com")
    print("2. Set the environment variable:")
    print("   set GROQ_API_KEY=your_api_key_here")
    print("3. Start the application:")
    print("   python app.py")
    print("4. Open your browser to: http://localhost:5000")
    print("\n💡 Features to try:")
    print("   • Upload reference audio for voice cloning")
    print("   • Use voice input (hold microphone button)")
    print("   • Try text chat with the empathetic AI")
    print("   • Listen to AI voice responses")

def main():
    """Run the demo"""
    tests = [
        demo_setup_check,
        demo_audio_capabilities, 
        demo_tts_model,
        demo_flask_app
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 Demo completed successfully!")
        print("✅ Your Luna Voice Chat Application is ready to run")
        show_next_steps()
    else:
        print("❌ Some tests failed. Check the setup instructions.")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())