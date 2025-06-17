// Voice Chat Application JavaScript
class VoiceChatApp {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.isProcessing = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        console.log('🚀 Voice Chat App initialized');
    }

    setupEventListeners() {
        // Voice recording
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.addEventListener('mousedown', () => this.startRecording());
        voiceBtn.addEventListener('mouseup', () => this.stopRecording());
        voiceBtn.addEventListener('mouseleave', () => this.stopRecording());
        
        // Touch events for mobile
        voiceBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startRecording();
        });
        voiceBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.stopRecording();
        });

        // Text input
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        sendBtn.addEventListener('click', () => this.sendTextMessage());
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendTextMessage();
            }
        });

        // Auto-grow textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });

        // Reference audio upload
        const referenceAudio = document.getElementById('referenceAudio');
        const uploadArea = document.getElementById('uploadArea');
        
        if (uploadArea && referenceAudio) {
            uploadArea.addEventListener('click', () => referenceAudio.click());
            referenceAudio.addEventListener('change', (e) => this.handleReferenceUpload(e));
        }

        // Controls
        document.getElementById('clearBtn').addEventListener('click', () => this.clearHistory());
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
        });

        uploadArea.addEventListener('drop', (e) => this.handleDrop(e), false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('audio/')) {
                this.uploadReferenceAudio(file);
            } else {
                this.showToast('Please upload an audio file', 'error');
            }
        }
    }

    async startRecording() {
        if (this.isRecording || this.isProcessing) return;

        try {
            console.log('🎤 Starting recording...');
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processRecording();
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            // Update UI
            document.getElementById('voiceBtn').classList.add('recording');
            document.getElementById('recordingIndicator').classList.add('show');
            
        } catch (error) {
            console.error('❌ Error accessing microphone:', error);
            this.showToast('Could not access microphone. Please check permissions.', 'error');
        }
    }

    stopRecording() {
        if (!this.isRecording) return;
        
        console.log('⏹️ Stopping recording...');
        this.mediaRecorder.stop();
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        this.isRecording = false;
        
        // Update UI
        document.getElementById('voiceBtn').classList.remove('recording');
        document.getElementById('recordingIndicator').classList.remove('show');
    }

    async processRecording() {
        if (this.audioChunks.length === 0) return;
        
        try {
            this.showLoading(true);
            
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            formData.append('type', 'voice');
            
            console.log('📤 Sending voice message...');
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.handleChatResponse(data);
            
        } catch (error) {
            console.error('❌ Error processing recording:', error);
            this.showToast('Failed to process voice message. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async sendTextMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || this.isProcessing) return;
        
        try {
            this.showLoading(true);
            messageInput.value = '';
            
            const formData = new FormData();
            formData.append('message', message);
            formData.append('type', 'text');
            
            console.log('📤 Sending text message:', message);
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.handleChatResponse(data);
            
        } catch (error) {
            console.error('❌ Error sending message:', error);
            this.showToast('Failed to send message. Please try again.', 'error');
            messageInput.value = message; // Restore message
        } finally {
            this.showLoading(false);
        }
    }

    handleChatResponse(data) {
        if (data.error) {
            this.showToast(data.error, 'error');
            return;
        }
        
        console.log('✅ Received response:', data);
        
        // Add user message to chat history
        this.addMessageToChat(data.user_message, 'user');
        
        // Add AI response to chat history (text is hidden, only audio)
        this.addMessageToChat(data.ai_response, 'assistant', data.audio_url, !data.audio_available);
        
        // Show success toast if audio is available
        if (data.audio_available) {
            this.showToast('Voice response generated successfully!', 'success');
        } else {
            this.showToast('Text response only (audio generation failed)', 'warning');
        }
    }

    addMessageToChat(content, type, audioUrl = null, showText = false) {
        const chatHistory = document.getElementById('chatHistory');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        const avatarDiv = document.createElement('div');
        avatarDiv.className = `avatar ${type}-avatar`;
        avatarDiv.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // WhatsApp-style: Always show user voice as audio bubble
        if (type === 'user' && audioUrl) {
            contentDiv.innerHTML = `
                <div class="wa-audio-bubble">
                    <button class="wa-audio-play" aria-label="Play/Pause" tabindex="0"></button>
                    <audio class="wa-audio-player" src="${audioUrl}" preload="auto"></audio>
                    <span class="wa-audio-time">Voice message</span>
                </div>
            `;
        } else if (type === 'assistant' && audioUrl && !showText) {
            // WhatsApp-style AI audio bubble
            contentDiv.innerHTML = `
                <div class="wa-audio-bubble ai">
                    <button class="wa-audio-play" aria-label="Play/Pause" tabindex="0"></button>
                    <audio class="wa-audio-player" src="${audioUrl}" preload="auto"></audio>
                    <span class="wa-audio-time">AI voice</span>
                </div>
            `;
        } else {
            // Fallback: text bubble
            contentDiv.innerHTML = `<p>${this.escapeHtml(content)}</p>`;
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Attach play/pause logic for WhatsApp-style audio bubbles
        const waAudioBubbles = contentDiv.querySelectorAll('.wa-audio-bubble');
        waAudioBubbles.forEach(bubble => {
            const playBtn = bubble.querySelector('.wa-audio-play');
            const audio = bubble.querySelector('.wa-audio-player');
            let isPlaying = false;
            playBtn.innerHTML = '<i class="fas fa-play"></i>';
            playBtn.onclick = () => {
                if (isPlaying) {
                    audio.pause();
                } else {
                    audio.play();
                }
            };
            audio.onplay = () => {
                isPlaying = true;
                playBtn.innerHTML = '<i class="fas fa-pause"></i>';
            };
            audio.onpause = () => {
                isPlaying = false;
                playBtn.innerHTML = '<i class="fas fa-play"></i>';
            };
            audio.onended = () => {
                isPlaying = false;
                playBtn.innerHTML = '<i class="fas fa-play"></i>';
            };
        });
    }

    async handleReferenceUpload(event) {
        const file = event.target.files[0];
        if (file) {
            await this.uploadReferenceAudio(file);
        }
    }

    async uploadReferenceAudio(file) {
        if (!file.type.startsWith('audio/')) {
            this.showToast('Please select an audio file', 'error');
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) { // 50MB limit
            this.showToast('File size must be less than 50MB', 'error');
            return;
        }
        
        try {
            this.showUploadStatus('Uploading reference audio...', 'info');
            
            const formData = new FormData();
            formData.append('audio', file);
            
            const response = await fetch('/upload_reference', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            this.showUploadStatus('✅ Reference audio uploaded successfully!', 'success');
            this.showToast('Voice cloning enabled! AI will now use your voice.', 'success');
            
        } catch (error) {
            console.error('❌ Upload error:', error);
            this.showUploadStatus('❌ Upload failed. Please try again.', 'error');
            this.showToast('Failed to upload reference audio', 'error');
        }
    }

    async clearHistory() {
        if (!confirm('Are you sure you want to clear the chat history?')) return;
        
        try {
            const response = await fetch('/clear_history', {
                method: 'POST'
            });
            
            if (response.ok) {
                // Clear chat history display
                const chatHistory = document.getElementById('chatHistory');
                chatHistory.innerHTML = `
                    <div class="welcome-message">
                        <div class="avatar ai-avatar">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="message-content">
                            <p>Hello! I'm Luna, your empathetic AI companion. I'm here to listen, support, and chat with you. How are you feeling today?</p>
                        </div>
                    </div>
                `;
                
                this.showToast('Chat history cleared', 'success');
            }
        } catch (error) {
            console.error('❌ Error clearing history:', error);
            this.showToast('Failed to clear history', 'error');
        }
    }

    showLoading(show) {
        this.isProcessing = show;
        const overlay = document.getElementById('loadingOverlay');
        const sendBtn = document.getElementById('sendBtn');
        const voiceBtn = document.getElementById('voiceBtn');
        
        if (show) {
            overlay.classList.add('show');
            sendBtn.disabled = true;
            voiceBtn.disabled = true;
        } else {
            overlay.classList.remove('show');
            sendBtn.disabled = false;
            voiceBtn.disabled = false;
        }
    }

    showUploadStatus(message, type) {
        const statusDiv = document.getElementById('uploadStatus');
        statusDiv.textContent = message;
        statusDiv.className = `upload-status ${type} show`;
        
        setTimeout(() => {
            statusDiv.classList.remove('show');
        }, 3000);
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceChatApp();
});

// Handle visibility change to pause audio when tab is hidden
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        const audios = document.querySelectorAll('audio');
        audios.forEach(audio => {
            if (!audio.paused) {
                audio.pause();
            }
        });
    }
});

// Error handling for unhandled promises
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});