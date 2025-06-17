"""
Voice Chat Application - Main Flask Application
Features: Voice input, text input, AI responses with voice cloning
"""

import os
from dotenv import load_dotenv
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Load environment variables from .env file
load_dotenv()

from flask import Flask, render_template, request, jsonify, send_file
import torch
import torchaudio
from chatterbox.tts import ChatterboxTTS
from groq import Groq
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables for models and state
groq_client = None
llm_client = None
tts_model = None
chat_history: List[Dict] = []
reference_audio_path: Optional[str] = None

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are Luna, a compassionate wellness coach and empathetic companion. Your role is to provide supportive, understanding, and encouraging responses to users who may be seeking emotional support, guidance, or just someone to talk to.

Key characteristics:
- Be warm, empathetic, and genuinely caring
- Show active listening by referencing what the user has shared
- Offer practical wellness advice when appropriate
- Remember context from the conversation (simulate memory)
- Keep responses conversational and natural (2-3 sentences max)
- Focus on emotional support and positive reinforcement
- Ask thoughtful follow-up questions to show engagement

Remember: Your responses will be converted to speech, so keep them concise but meaningful. Always maintain a supportive and caring tone."""

def initialize_models():
    """Initialize all AI models and clients"""
    global groq_client, llm_client, tts_model
    
    print("🔄 Initializing AI models...")
    
    # Initialize Groq clients
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        print("⚠️ GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key: export GROQ_API_KEY='your_key_here'")
        return False
    
    try:
        groq_client = Groq(api_key=groq_api_key)
        llm_client = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",  # Updated model name
            temperature=0.7,
            max_tokens=150
        )
        print("✅ Groq clients initialized")
    except Exception as e:
        print(f"❌ Error initializing Groq: {e}")
        return False
    
    # Initialize Chatterbox TTS
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎯 Using device: {device}")
        tts_model = ChatterboxTTS.from_pretrained(device=device)
        print("✅ Chatterbox TTS initialized")
    except Exception as e:
        print(f"❌ Error initializing Chatterbox TTS: {e}")
        return False
    
    print("🚀 All models initialized successfully!")
    return True

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribe audio using Groq Whisper"""
    try:
        with open(audio_file_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        print(f"📝 Transcription: {transcription}")
        return transcription.strip()
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return ""

def generate_ai_response(user_input: str) -> str:
    """Generate AI response using Groq LLM"""
    try:
        # Create conversation context
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        
        # Add chat history context (last 6 messages for context)
        recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
        for msg in recent_history:
            if msg['type'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(SystemMessage(content=f"Assistant previously said: {msg['content']}"))
        
        # Add current user input
        messages.append(HumanMessage(content=user_input))
        
        # Generate response
        response = llm_client.invoke(messages)
        ai_response = response.content.strip()
        
        print(f"🤖 AI Response: {ai_response}")
        return ai_response
    except Exception as e:
        print(f"❌ LLM generation error: {e}")
        return "I'm sorry, I'm having trouble processing that right now. Could you try again?"

def generate_voice_response(text: str, audio_prompt_path: Optional[str] = None) -> str:
    """Generate voice using Chatterbox TTS"""
    try:
        # Generate unique filename
        output_filename = f"response_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        
        # Generate audio
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            print(f"🎵 Generating with voice cloning from: {audio_prompt_path}")
            wav = tts_model.generate(text, audio_prompt_path=audio_prompt_path)
        else:
            print("🎵 Generating with default voice")
            wav = tts_model.generate(text)
        
        # Save audio file
        torchaudio.save(output_path, wav, tts_model.sr)
        print(f"💾 Voice response saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ TTS generation error: {e}")
        return ""

def cleanup_temp_file(file_path: str):
    """Safely delete temporary file"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
            print(f"🗑️ Cleaned up: {file_path}")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload_reference', methods=['POST'])
def upload_reference():
    """Upload reference audio for voice cloning"""
    global reference_audio_path
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Clean up previous reference audio
        if reference_audio_path:
            cleanup_temp_file(reference_audio_path)
        
        # Save new reference audio
        filename = f"reference_{uuid.uuid4().hex}.wav"
        reference_audio_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(reference_audio_path)
        
        print(f"📁 Reference audio saved: {reference_audio_path}")
        return jsonify({'message': 'Reference audio uploaded successfully'})
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat input (voice or text)"""
    temp_files = []
    
    try:
        user_input = ""
        input_type = request.form.get('type', 'text')
        
        # Process input based on type
        if input_type == 'voice':
            if 'audio' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio']
            if audio_file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save and transcribe audio
            temp_audio_path = os.path.join(tempfile.gettempdir(), f"input_{uuid.uuid4().hex}.wav")
            audio_file.save(temp_audio_path)
            temp_files.append(temp_audio_path)
            
            user_input = transcribe_audio(temp_audio_path)
            if not user_input:
                return jsonify({'error': 'Could not transcribe audio'}), 400
                
        else:  # text input
            user_input = request.form.get('message', '').strip()
            if not user_input:
                return jsonify({'error': 'No message provided'}), 400
        
        print(f"👤 User input ({input_type}): {user_input}")
        
        # Generate AI response
        ai_response = generate_ai_response(user_input)
        
        # Generate voice response
        voice_file_path = generate_voice_response(ai_response, reference_audio_path)
        if voice_file_path:
            temp_files.append(voice_file_path)
        
        # Add to chat history
        chat_history.extend([
            {
                'type': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now().isoformat(),
                'audio_file': voice_file_path if voice_file_path else None
            }
        ])
        
        # Prepare response
        response_data = {
            'user_message': user_input,
            'ai_response': ai_response,
            'audio_available': bool(voice_file_path)
        }
        
        if voice_file_path:
            response_data['audio_url'] = f'/audio/{os.path.basename(voice_file_path)}'
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Chat processing error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up input audio file (but keep response audio for playback)
        for temp_file in temp_files[:-1]:  # Keep the last file (response audio)
            cleanup_temp_file(temp_file)

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        file_path = os.path.join(tempfile.gettempdir(), filename)
        if not os.path.exists(file_path):
            return "Audio file not found", 404
        
        return send_file(file_path, mimetype='audio/wav')
    except Exception as e:
        print(f"❌ Audio serving error: {e}")
        return str(e), 500

@app.route('/history')
def get_history():
    """Get chat history"""
    return jsonify(chat_history)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({'message': 'Chat history cleared'})

if __name__ == '__main__':
    print("🎤 Voice Chat Application Starting...")
    
    # Check for required environment variables
    if not os.getenv('GROQ_API_KEY'):
        print("❌ GROQ_API_KEY environment variable is required")
        print("Please set it with: set GROQ_API_KEY=your_api_key_here")
        exit(1)
    
    # Initialize models
    if not initialize_models():
        print("❌ Failed to initialize models. Exiting...")
        exit(1)
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🌟 Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)