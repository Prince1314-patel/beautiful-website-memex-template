# Luna - Voice Chat AI Assistant

An interactive AI-powered voice chat application that provides empathetic and supportive conversations. Luna features voice input, text input, and AI responses with voice cloning capabilities.

## Features

### Core Functionality
- **Voice Input**: Click and hold to record voice messages
- **Text Input**: Type messages for text-based conversations  
- **AI Voice Responses**: Get audio responses from the AI assistant
- **Voice Cloning**: Upload reference audio to clone your voice for AI responses
- **Empathetic AI**: Luna is designed as a compassionate wellness coach

### Technical Features
- **Speech-to-Text**: Powered by Groq Whisper large-v3-turbo
- **Language Model**: Uses Groq's Llama-3.3-70B-Versatile for conversations
- **Text-to-Speech**: Chatterbox TTS for high-quality voice synthesis
- **Responsive Design**: Modern, mobile-friendly interface
- **Secure Audio Handling**: Temporary storage with automatic cleanup

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI Models**: 
  - Groq API (Whisper + Llama)
  - Chatterbox TTS for voice synthesis
- **Audio Processing**: PyTorch, TorchAudio

## Quick Start

### Prerequisites
- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com))
- Microphone access for voice input

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd voice_chat_app_architecture
```

2. **Run the setup script**
```bash
setup.bat
```

3. **Set your Groq API key**
```bash
set GROQ_API_KEY=your_api_key_here
```

4. **Start the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

### Manual Setup (Alternative)

```bash
# Create virtual environment
uv venv
.venv\Scripts\activate.bat

# Install dependencies
uv pip install -r requirements.txt

# Set API key and run
set GROQ_API_KEY=your_api_key_here
python app.py
```

## Usage

### Basic Conversation
1. **Voice Input**: Click and hold the microphone button, speak your message, then release
2. **Text Input**: Type your message in the text area and click send
3. **AI Response**: Luna will respond with both text and audio (if voice cloning is enabled)

### Voice Cloning Setup
1. Click the upload area in the "Voice Cloning" section
2. Upload a clear audio file (10+ seconds recommended)
3. Once uploaded, AI responses will use your cloned voice

### Best Practices for Voice Cloning
- Use WAV format audio files
- 24kHz sample rate or higher
- Single speaker, no background noise
- Professional microphone preferred
- 10+ seconds of clear speech

## Architecture

### Components
- **Flask Backend**: Handles API requests, audio processing, and AI integration
- **Web Frontend**: Responsive chat interface with voice recording capabilities
- **AI Integration**: Groq API for STT/LLM, Chatterbox for TTS
- **Security**: Temporary file storage with automatic cleanup

### Data Flow
1. User input (voice/text) → Flask backend
2. Voice transcription (if needed) → Groq Whisper
3. Text processing → Groq Llama LLM
4. Voice synthesis → Chatterbox TTS
5. Response delivery → Frontend playback
6. Cleanup → Temporary files deleted

### Privacy & Security
- Audio files stored temporarily during processing
- Automatic cleanup after response generation
- No persistent storage of conversation history
- Secure API key handling

## Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)

### Model Configuration
- **STT Model**: `whisper-large-v3-turbo`
- **LLM Model**: `llama-3.3-70b-versatile`
- **TTS Model**: Chatterbox (automatic device detection)

## Development

### Project Structure
```
voice_chat_app_architecture/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend template
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── setup.bat            # Setup script
└── README.md           # This file
```

### Adding Features
- **New AI Models**: Extend the model initialization in `app.py`
- **UI Components**: Add to `templates/index.html` and `static/style.css`
- **API Endpoints**: Add new routes in `app.py`

## Troubleshooting

### Common Issues
- **Microphone Access**: Ensure browser permissions are granted
- **API Key Error**: Verify `GROQ_API_KEY` is set correctly
- **Audio Playback**: Check browser audio permissions
- **Model Loading**: Ensure sufficient RAM for Chatterbox TTS

### Performance Tips
- Use GPU acceleration if available (CUDA/ROCm)
- Adjust model parameters for your hardware
- Monitor memory usage with large audio files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the individual component licenses:
- Groq API: Commercial use subject to Groq terms
- Chatterbox TTS: MIT License
- Flask: BSD License

---

🤖 *Generated with [Memex](https://memex.tech)*  
Co-Authored-By: Memex <noreply@memex.tech>
