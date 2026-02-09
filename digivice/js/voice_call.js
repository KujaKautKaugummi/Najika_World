/**
 * NAJIKA VOICE CALL SYSTEM
 * WebRTC Audio Streaming + Whisper STT + Coqui TTS
 */

// Global Voice Call State
let voiceCallActive = false;
let mediaRecorder = null;
let audioStream = null;
let audioContext = null;
let analyser = null;
let visualizerAnimationId = null;
let callStartTime = null;
let callDurationInterval = null;

// Button References
const voiceCallBtn = document.getElementById('voiceCallBtn');
const voiceCallPanel = document.getElementById('voice-call-panel');
const startCallBtn = document.getElementById('start-call-btn');
const endCallBtn = document.getElementById('end-call-btn');
const callStatusText = document.getElementById('call-status-text');
const callDuration = document.getElementById('call-duration');
const callTranscript = document.getElementById('call-transcript');
const callStats = document.getElementById('call-stats');
const sttLatency = document.getElementById('stt-latency');
const ttsLatency = document.getElementById('tts-latency');

// Audio Visualizer Canvas
const visualizerCanvas = document.getElementById('audio-visualizer');
const visualizerCtx = visualizerCanvas ? visualizerCanvas.getContext('2d') : null;

// Toggle Voice Call Panel
if (voiceCallBtn) {
    voiceCallBtn.addEventListener('click', () => {
        if (voiceCallPanel) {
            const isVisible = voiceCallPanel.style.display !== 'none';
            voiceCallPanel.style.display = isVisible ? 'none' : 'block';
        }
    });
}

/**
 * Start Voice Call
 */
async function startVoiceCall() {
    try {
        // Request microphone access
        console.log('[VOICE CALL] Requesting microphone access...');
        callStatusText.textContent = 'Mikrofonzugriff wird angefordert...';

        audioStream = await navigator.mediaDevices.getUserMedia({
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            }
        });

        console.log('[VOICE CALL] Microphone access granted!');
        callStatusText.textContent = 'Verbinde mit Najika...';

        // Call server to start session
        const response = await fetch('http://localhost:8000/api/voice_call/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();
        console.log('[VOICE CALL] Session started:', result);

        if (!result.status || result.status !== 'call_started') {
            throw new Error('Failed to start call session');
        }

        // Setup audio context and analyser for visualizer
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;

        const source = audioContext.createMediaStreamSource(audioStream);
        source.connect(analyser);

        // Setup MediaRecorder for audio streaming
        const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/wav';
        mediaRecorder = new MediaRecorder(audioStream, { mimeType });

        let audioChunks = [];

        mediaRecorder.ondataavailable = async (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            if (audioChunks.length === 0) return;

            const audioBlob = new Blob(audioChunks, { type: mimeType });
            audioChunks = [];

            // Convert to base64
            const reader = new FileReader();
            reader.onloadend = async () => {
                const base64Audio = reader.result.split(',')[1];
                await sendAudioToServer(base64Audio);
            };
            reader.readAsDataURL(audioBlob);
        };

        // Start recording (capture every 3 seconds)
        mediaRecorder.start();
        setInterval(() => {
            if (mediaRecorder && voiceCallActive && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                mediaRecorder.start();
            }
        }, 3000);

        // Update UI
        voiceCallActive = true;
        startCallBtn.style.display = 'none';
        endCallBtn.style.display = 'block';
        callStatusText.textContent = '🎤 Anruf aktiv - Sprechen Sie jetzt!';
        callStatusText.style.color = '#2ecc71';
        callDuration.style.display = 'block';
        callStats.style.display = 'block';
        callTranscript.innerHTML = '<p style="color: #2ecc71; text-align: center;">🎤 Bereit zum Zuhören...</p>';

        // Start call duration timer
        callStartTime = Date.now();
        callDurationInterval = setInterval(() => {
            if (!voiceCallActive) {
                clearInterval(callDurationInterval);
                return;
            }
            const elapsed = Math.floor((Date.now() - callStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const seconds = (elapsed % 60).toString().padStart(2, '0');
            callDuration.textContent = `${minutes}:${seconds}`;
        }, 1000);

        // Start visualizer
        startAudioVisualizer();

        console.log('[VOICE CALL] Call started successfully!');

    } catch (error) {
        console.error('[VOICE CALL] Error starting call:', error);
        callStatusText.textContent = '❌ Fehler: ' + error.message;
        callStatusText.style.color = '#e74c3c';

        // Cleanup on error
        if (audioStream) {
            audioStream.getTracks().forEach(track => track.stop());
            audioStream = null;
        }
    }
}

/**
 * Send audio to server for processing
 */
async function sendAudioToServer(audioBase64) {
    try {
        console.log('[VOICE CALL] Sending audio to server...');

        const response = await fetch('http://localhost:8000/api/voice_call/audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio: audioBase64 })
        });

        const result = await response.json();
        console.log('[VOICE CALL] Server response:', result);

        if (result.error) {
            console.error('[VOICE CALL] Server error:', result.error);
            return;
        }

        // Update transcript with user's speech
        const userText = result.stt?.text;
        if (userText && userText.trim()) {
            addToTranscript('user', userText);
        }

        // Update transcript with Najika's response
        const najikaText = result.text;
        if (najikaText && najikaText.trim()) {
            addToTranscript('najika', najikaText);
        }

        // Play Najika's voice response
        if (result.tts && result.tts.audio_base64) {
            await playAudioResponse(result.tts.audio_base64);
        }

        // Update latency stats
        if (result.stt && result.stt.latency_ms) {
            sttLatency.textContent = `${Math.round(result.stt.latency_ms)} ms`;
        }
        if (result.tts && result.tts.latency_ms) {
            ttsLatency.textContent = `${Math.round(result.tts.latency_ms)} ms`;
        }

    } catch (error) {
        console.error('[VOICE CALL] Error sending audio:', error);
    }
}

/**
 * Add message to transcript
 */
function addToTranscript(speaker, text) {
    if (!callTranscript) return;

    const messageDiv = document.createElement('div');
    messageDiv.style.marginBottom = '10px';
    messageDiv.style.padding = '8px';
    messageDiv.style.borderRadius = '8px';
    messageDiv.style.borderLeft = '3px solid ' + (speaker === 'user' ? '#667eea' : '#ff6b6b');
    messageDiv.style.background = speaker === 'user' ? 'rgba(102, 126, 234, 0.1)' : 'rgba(255, 107, 107, 0.1)';

    const speakerLabel = document.createElement('div');
    speakerLabel.style.fontWeight = 'bold';
    speakerLabel.style.fontSize = '12px';
    speakerLabel.style.marginBottom = '5px';
    speakerLabel.style.color = speaker === 'user' ? '#667eea' : '#ff6b6b';
    speakerLabel.textContent = speaker === 'user' ? '👤 Du' : '💜 Najika';

    const messageText = document.createElement('div');
    messageText.style.fontSize = '14px';
    messageText.style.color = '#eaeaea';
    messageText.textContent = text;

    messageDiv.appendChild(speakerLabel);
    messageDiv.appendChild(messageText);
    callTranscript.appendChild(messageDiv);

    // Auto-scroll to bottom
    callTranscript.scrollTop = callTranscript.scrollHeight;
}

/**
 * Play audio response from base64
 */
async function playAudioResponse(audioBase64) {
    try {
        const audioData = atob(audioBase64);
        const audioArray = new Uint8Array(audioData.length);
        for (let i = 0; i < audioData.length; i++) {
            audioArray[i] = audioData.charCodeAt(i);
        }

        const audioBlob = new Blob([audioArray], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audio = new Audio(audioUrl);
        await audio.play();

        console.log('[VOICE CALL] Playing Najika\'s voice response');

    } catch (error) {
        console.error('[VOICE CALL] Error playing audio:', error);
    }
}

/**
 * End Voice Call
 */
async function endVoiceCall() {
    try {
        console.log('[VOICE CALL] Ending call...');

        // Stop media recorder
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }

        // Stop audio stream
        if (audioStream) {
            audioStream.getTracks().forEach(track => track.stop());
            audioStream = null;
        }

        // Close audio context
        if (audioContext && audioContext.state !== 'closed') {
            await audioContext.close();
            audioContext = null;
        }

        // Stop visualizer
        if (visualizerAnimationId) {
            cancelAnimationFrame(visualizerAnimationId);
            visualizerAnimationId = null;
        }

        // Stop call duration timer
        if (callDurationInterval) {
            clearInterval(callDurationInterval);
            callDurationInterval = null;
        }

        // Call server to end session
        const response = await fetch('http://localhost:8000/api/voice_call/end', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();
        console.log('[VOICE CALL] Session ended:', result);

        // Update UI
        voiceCallActive = false;
        startCallBtn.style.display = 'block';
        endCallBtn.style.display = 'none';
        callStatusText.textContent = 'Anruf beendet';
        callStatusText.style.color = '#aaa';
        callDuration.style.display = 'none';
        callStats.style.display = 'none';

        // Clear visualizer canvas
        if (visualizerCtx && visualizerCanvas) {
            visualizerCtx.clearRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
        }

        // Close panel after 2 seconds
        setTimeout(() => {
            if (voiceCallPanel) {
                voiceCallPanel.style.display = 'none';
            }
        }, 2000);

        console.log('[VOICE CALL] Call ended successfully!');

    } catch (error) {
        console.error('[VOICE CALL] Error ending call:', error);
    }
}

/**
 * Start audio visualizer
 */
function startAudioVisualizer() {
    if (!analyser || !visualizerCtx || !visualizerCanvas) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
        if (!voiceCallActive) {
            cancelAnimationFrame(visualizerAnimationId);
            return;
        }

        visualizerAnimationId = requestAnimationFrame(draw);

        analyser.getByteFrequencyData(dataArray);

        // Clear canvas
        visualizerCtx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        visualizerCtx.fillRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);

        // Draw frequency bars
        const barWidth = (visualizerCanvas.width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            barHeight = (dataArray[i] / 255) * visualizerCanvas.height * 0.8;

            const r = 255;
            const g = 107 + (dataArray[i] / 255) * 50;
            const b = 107 + (dataArray[i] / 255) * 50;

            visualizerCtx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            visualizerCtx.fillRect(x, visualizerCanvas.height - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        }
    }

    draw();
}

// Expose functions globally
window.startVoiceCall = startVoiceCall;
window.endVoiceCall = endVoiceCall;

console.log('[VOICE CALL] Voice Call System loaded!');
