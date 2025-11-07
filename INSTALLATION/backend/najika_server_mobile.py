#!/usr/bin/env python3
"""
Najika Mobile Server Extension
Extends the main Najika server with mobile-specific APIs

This server handles:
- Mobile app authentication
- Connection management (local/Cloudflare detection)
- Mobile-specific API endpoints
- Integration with Messenger server
- Push notifications
- Device management

Author: Claude Code
Date: 2025-11-07
Version: 1.0
"""

import os
import sys
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import argon2

# Import base server functionality
# Note: This will be dynamically imported from main server
# sys.path.append(str(Path(__file__).parent.parent / 'SERVER'))
# from najika_server import app as base_app, NajikaServer

# Configuration
class Config:
    SECRET_KEY = os.getenv('NAJIKA_SECRET_KEY', secrets.token_hex(32))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    JWT_EXPIRATION_HOURS = 24 * 7  # 7 days
    MAX_DEVICES_PER_USER = 3
    MESSENGER_SERVER_URL = 'http://localhost:5001'

    # Security
    ENABLE_RATE_LIMITING = True
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30

    # Connection detection
    LOCAL_NETWORK_PREFIX = '192.168.'  # Adjust to your network
    CLOUDFLARE_HEADER = 'CF-Connecting-IP'

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Password hasher (Argon2)
ph = argon2.PasswordHasher()

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Device:
    """Mobile device registration"""
    device_id: str
    device_name: str
    device_type: str  # android, ios
    user_id: str
    registered_at: datetime
    last_seen: datetime
    push_token: Optional[str] = None
    public_key: Optional[str] = None
    is_active: bool = True

@dataclass
class Session:
    """User session"""
    session_id: str
    user_id: str
    device_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    connection_type: str  # local, cloudflare, tailscale

# ============================================================================
# IN-MEMORY STORAGE (for now - will be replaced with database)
# ============================================================================

# In production, these should be in SQLite/PostgreSQL
devices: Dict[str, Device] = {}
sessions: Dict[str, Session] = {}
users: Dict[str, Dict] = {}  # user_id -> {username, password_hash, etc.}
login_attempts: Dict[str, List[datetime]] = {}

# ============================================================================
# AUTHENTICATION
# ============================================================================

def create_jwt_token(user_id: str, device_id: str) -> str:
    """Create JWT token for authenticated session"""
    payload = {
        'user_id': user_id,
        'device_id': device_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token: str) -> Optional[Dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def check_rate_limit(identifier: str) -> Tuple[bool, Optional[int]]:
    """Check if identifier (IP or user) has exceeded login attempts"""
    if identifier not in login_attempts:
        login_attempts[identifier] = []

    # Remove old attempts
    cutoff = datetime.utcnow() - timedelta(minutes=Config.LOCKOUT_DURATION_MINUTES)
    login_attempts[identifier] = [
        attempt for attempt in login_attempts[identifier]
        if attempt > cutoff
    ]

    if len(login_attempts[identifier]) >= Config.MAX_LOGIN_ATTEMPTS:
        # Calculate remaining lockout time
        oldest_attempt = min(login_attempts[identifier])
        unlock_time = oldest_attempt + timedelta(minutes=Config.LOCKOUT_DURATION_MINUTES)
        remaining_seconds = int((unlock_time - datetime.utcnow()).total_seconds())
        return False, remaining_seconds

    return True, None

def detect_connection_type(request) -> str:
    """Detect if connection is local, Cloudflare, or Tailscale"""
    # Check for Cloudflare
    if request.headers.get(Config.CLOUDFLARE_HEADER):
        return 'cloudflare'

    # Check for Tailscale (100.x.x.x range)
    remote_ip = request.remote_addr
    if remote_ip.startswith('100.'):
        return 'tailscale'

    # Check for local network
    if remote_ip.startswith(Config.LOCAL_NETWORK_PREFIX) or remote_ip == '127.0.0.1':
        return 'local'

    return 'unknown'

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/mobile/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'server': 'najika_mobile',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/mobile/connection/detect', methods=['GET'])
def detect_connection():
    """
    Detect connection type for client

    Client calls this to determine if it should use:
    - Local connection (fastest)
    - Cloudflare Tunnel
    - Tailscale
    """
    connection_type = detect_connection_type(request)

    # Provide appropriate endpoint URLs
    endpoints = {
        'local': f'http://{request.host}',
        'cloudflare': 'https://najika.yourdomain.com',
        'tailscale': f'http://{request.remote_addr}:8000'
    }

    return jsonify({
        'connection_type': connection_type,
        'recommended_endpoint': endpoints.get(connection_type, endpoints['cloudflare']),
        'client_ip': request.remote_addr,
        'all_endpoints': endpoints
    })

@app.route('/api/mobile/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
def register_device():
    """
    Register new mobile device

    Request:
    {
        "username": "najika_user",
        "password": "secure_password",
        "device_name": "Xiaomi 11T Pro",
        "device_type": "android",
        "device_id": "unique_device_id",
        "public_key": "device_public_key"
    }
    """
    data = request.get_json()

    # Validate input
    required_fields = ['username', 'password', 'device_name', 'device_type', 'device_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']
    device_id = data['device_id']

    # Check rate limiting
    allowed, remaining = check_rate_limit(request.remote_addr)
    if not allowed:
        return jsonify({
            'error': 'Too many registration attempts',
            'retry_after_seconds': remaining
        }), 429

    # Check if user exists
    user_id = None
    if username in [u.get('username') for u in users.values()]:
        return jsonify({'error': 'Username already exists'}), 409

    # Create new user
    user_id = secrets.token_hex(16)
    password_hash = ph.hash(password)

    users[user_id] = {
        'username': username,
        'password_hash': password_hash,
        'created_at': datetime.utcnow(),
        'device_count': 0
    }

    # Register device
    device = Device(
        device_id=device_id,
        device_name=data['device_name'],
        device_type=data['device_type'],
        user_id=user_id,
        registered_at=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        push_token=data.get('push_token'),
        public_key=data.get('public_key'),
        is_active=True
    )

    devices[device_id] = device
    users[user_id]['device_count'] += 1

    # Create JWT token
    token = create_jwt_token(user_id, device_id)

    return jsonify({
        'success': True,
        'user_id': user_id,
        'device_id': device_id,
        'token': token,
        'expires_at': (datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)).isoformat()
    }), 201

@app.route('/api/mobile/auth/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    """
    Login with existing credentials

    Request:
    {
        "username": "najika_user",
        "password": "secure_password",
        "device_id": "unique_device_id"
    }
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    device_id = data.get('device_id')

    if not all([username, password, device_id]):
        return jsonify({'error': 'Missing credentials'}), 400

    # Check rate limiting
    allowed, remaining = check_rate_limit(request.remote_addr)
    if not allowed:
        return jsonify({
            'error': 'Too many login attempts',
            'retry_after_seconds': remaining
        }), 429

    # Find user
    user_id = None
    for uid, user_data in users.items():
        if user_data['username'] == username:
            user_id = uid
            break

    if not user_id:
        login_attempts[request.remote_addr].append(datetime.utcnow())
        return jsonify({'error': 'Invalid credentials'}), 401

    # Verify password
    try:
        ph.verify(users[user_id]['password_hash'], password)
    except argon2.exceptions.VerifyMismatchError:
        login_attempts[request.remote_addr].append(datetime.utcnow())
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check if device exists
    if device_id not in devices:
        return jsonify({'error': 'Device not registered'}), 404

    # Verify device belongs to user
    if devices[device_id].user_id != user_id:
        return jsonify({'error': 'Device does not belong to user'}), 403

    # Update device last seen
    devices[device_id].last_seen = datetime.utcnow()

    # Create JWT token
    token = create_jwt_token(user_id, device_id)

    # Create session
    session_id = secrets.token_hex(16)
    session = Session(
        session_id=session_id,
        user_id=user_id,
        device_id=device_id,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        ip_address=request.remote_addr,
        connection_type=detect_connection_type(request)
    )
    sessions[session_id] = session

    return jsonify({
        'success': True,
        'user_id': user_id,
        'device_id': device_id,
        'token': token,
        'session_id': session_id,
        'expires_at': session.expires_at.isoformat(),
        'connection_type': session.connection_type
    })

@app.route('/api/mobile/auth/verify', methods=['POST'])
def verify_token():
    """Verify JWT token validity"""
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'error': 'No token provided'}), 400

    payload = verify_jwt_token(token)
    if not payload:
        return jsonify({'valid': False, 'error': 'Invalid or expired token'}), 401

    return jsonify({
        'valid': True,
        'user_id': payload['user_id'],
        'device_id': payload['device_id'],
        'expires_at': datetime.fromtimestamp(payload['exp']).isoformat()
    })

@app.route('/api/mobile/devices', methods=['GET'])
def list_devices():
    """List all devices for authenticated user"""
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401

    token = auth_header.split(' ')[1]
    payload = verify_jwt_token(token)
    if not payload:
        return jsonify({'error': 'Invalid token'}), 401

    user_id = payload['user_id']

    # Get all devices for this user
    user_devices = [
        asdict(device) for device in devices.values()
        if device.user_id == user_id
    ]

    return jsonify({'devices': user_devices})

@app.route('/api/mobile/server/info', methods=['GET'])
def server_info():
    """Get server information and capabilities"""
    return jsonify({
        'server_name': 'Najika Mobile Server',
        'version': '1.0',
        'features': {
            'messenger': True,
            'video_calls': True,
            'voice_calls': True,
            'avatar_mode': True,
            'post_quantum': True,
            'panic_button': True,
            'sealed_sender': True
        },
        'security': {
            'encryption': 'E2E (Signal Protocol + Post-Quantum)',
            'metadata_protection': 'Sealed Sender',
            'server_knowledge': 'Zero-Knowledge',
            'forward_secrecy': True
        },
        'connection_methods': ['local', 'cloudflare', 'tailscale'],
        'messenger_server': Config.MESSENGER_SERVER_URL
    })

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connection_status', {'status': 'connected', 'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('authenticate')
def handle_authenticate(data):
    """Authenticate WebSocket connection"""
    token = data.get('token')
    if not token:
        emit('auth_error', {'error': 'No token provided'})
        return

    payload = verify_jwt_token(token)
    if not payload:
        emit('auth_error', {'error': 'Invalid token'})
        return

    # Store user info in session
    g.user_id = payload['user_id']
    g.device_id = payload['device_id']

    # Join user room for targeted messages
    join_room(f"user_{payload['user_id']}")

    emit('auth_success', {
        'user_id': payload['user_id'],
        'device_id': payload['device_id']
    })

@socketio.on('ping')
def handle_ping():
    """Keep-alive ping"""
    emit('pong', {'timestamp': datetime.utcnow().isoformat()})

# ============================================================================
# STARTUP
# ============================================================================

def initialize_server():
    """Initialize server on startup"""
    print("=" * 60)
    print("🚀 Najika Mobile Server Starting...")
    print("=" * 60)
    print(f"Version: 1.0")
    print(f"JWT Expiration: {Config.JWT_EXPIRATION_HOURS} hours")
    print(f"Rate Limiting: {'Enabled' if Config.ENABLE_RATE_LIMITING else 'Disabled'}")
    print(f"Messenger Server: {Config.MESSENGER_SERVER_URL}")
    print("=" * 60)

if __name__ == '__main__':
    initialize_server()

    # Run with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
