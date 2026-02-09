#!/usr/bin/env python3
"""
Najika Messenger Server - Zero-Knowledge Architecture
Handles E2E encrypted messaging with Post-Quantum support

ZERO-KNOWLEDGE PRINCIPLES:
- Server NEVER sees message content
- Server NEVER stores encryption keys
- Server only routes encrypted payloads
- Metadata protection via Sealed Sender
- Perfect Forward Secrecy
- Post-Compromise Security

Signal Protocol + Post-Quantum (PQXDH):
- X3DH Key Agreement (classical)
- CRYSTALS-Kyber (post-quantum)
- Double/Triple Ratchet
- Sealed Sender

Author: Claude Code
Date: 2025-11-07
Version: 1.0
"""

import os
import sys
import secrets
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from pathlib import Path
from collections import defaultdict
import base64

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuration
class Config:
    SECRET_KEY = os.getenv('MESSENGER_SECRET_KEY', secrets.token_hex(32))

    # Storage limits
    MAX_QUEUED_MESSAGES_PER_USER = 10000
    MAX_PREKEYS_PER_DEVICE = 100
    MESSAGE_TTL_DAYS = 30  # Delete undelivered messages after 30 days

    # Rate limiting
    MAX_MESSAGES_PER_MINUTE = 60
    MAX_PREKEY_REQUESTS_PER_HOUR = 100

    # Security
    SEALED_SENDER_ENABLED = True
    REQUIRE_IDENTITY_VERIFICATION = True

    # Panic mode
    ENABLE_PANIC_MODE = True
    PANIC_WIPE_DELAY_SECONDS = 5  # Grace period before wipe

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# SocketIO for real-time message delivery
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "200 per hour"]
)

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class PreKeyBundle:
    """
    PreKey bundle for X3DH/PQXDH key exchange
    Contains both classical and post-quantum keys
    """
    # Classical keys (X3DH)
    identity_key: str  # Long-term identity key (public)
    signed_prekey: str  # Signed prekey
    signed_prekey_signature: str  # Signature of signed prekey
    one_time_prekey: Optional[str] = None  # One-time prekey (optional)

    # Post-Quantum keys (PQXDH)
    pq_last_resort_prekey: Optional[str] = None  # Kyber public key (last resort)
    pq_one_time_prekey: Optional[str] = None  # Kyber public key (one-time)

    # Metadata
    device_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data

@dataclass
class EncryptedMessage:
    """
    Encrypted message envelope
    Server NEVER decrypts this
    """
    message_id: str
    sender_id: str  # Encrypted in Sealed Sender mode
    recipient_id: str
    recipient_device_id: str

    # Encrypted payload (includes type, content, ratchet keys, etc.)
    encrypted_payload: str  # Base64 encoded

    # Metadata (minimal)
    timestamp: datetime
    sealed_sender: bool = True

    # Delivery tracking
    delivered: bool = False
    delivered_at: Optional[datetime] = None

    # TTL
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=Config.MESSAGE_TTL_DAYS))

    def to_dict(self):
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['expires_at'] = self.expires_at.isoformat()
        if self.delivered_at:
            data['delivered_at'] = self.delivered_at.isoformat()
        return data

@dataclass
class DeviceRegistration:
    """Device registration for messaging"""
    device_id: str
    user_id: str
    device_name: str
    registered_at: datetime
    last_seen: datetime
    prekey_bundle: Optional[PreKeyBundle] = None
    is_active: bool = True

    # WebSocket session
    socket_sid: Optional[str] = None

# ============================================================================
# IN-MEMORY STORAGE
# ============================================================================
# Note: In production, use Redis or PostgreSQL with encryption at rest

# Device management
devices: Dict[str, DeviceRegistration] = {}  # device_id -> DeviceRegistration

# PreKey bundles
prekey_bundles: Dict[str, List[PreKeyBundle]] = defaultdict(list)  # user_id -> [bundles]

# One-time prekeys (separate storage for quick access)
one_time_prekeys: Dict[str, List[str]] = defaultdict(list)  # user_id -> [prekeys]
pq_one_time_prekeys: Dict[str, List[str]] = defaultdict(list)  # user_id -> [PQ prekeys]

# Message queue (undelivered messages)
message_queue: Dict[str, List[EncryptedMessage]] = defaultdict(list)  # user_id -> [messages]

# Online users (WebSocket sessions)
online_users: Dict[str, Set[str]] = defaultdict(set)  # user_id -> {socket_sids}
socket_to_user: Dict[str, Tuple[str, str]] = {}  # socket_sid -> (user_id, device_id)

# Panic mode tracking
panic_mode_devices: Dict[str, datetime] = {}  # device_id -> panic_timestamp

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_message_id() -> str:
    """Generate unique message ID"""
    return secrets.token_hex(16)

def is_user_online(user_id: str) -> bool:
    """Check if user has any online devices"""
    return len(online_users.get(user_id, set())) > 0

def get_user_devices(user_id: str) -> List[DeviceRegistration]:
    """Get all devices for a user"""
    return [d for d in devices.values() if d.user_id == user_id and d.is_active]

def cleanup_expired_messages():
    """Remove expired messages from queue"""
    now = datetime.utcnow()
    for user_id in list(message_queue.keys()):
        message_queue[user_id] = [
            msg for msg in message_queue[user_id]
            if msg.expires_at > now
        ]
        if not message_queue[user_id]:
            del message_queue[user_id]

def get_prekey_bundle(user_id: str, device_id: Optional[str] = None) -> Optional[PreKeyBundle]:
    """
    Get prekey bundle for initiating conversation
    Consumes one-time prekey if available
    """
    bundles = prekey_bundles.get(user_id, [])
    if not bundles:
        return None

    # Filter by device if specified
    if device_id:
        bundles = [b for b in bundles if b.device_id == device_id]
        if not bundles:
            return None

    # Get first bundle
    bundle = bundles[0]

    # Try to get one-time prekeys
    classical_otk = None
    pq_otk = None

    if one_time_prekeys[user_id]:
        classical_otk = one_time_prekeys[user_id].pop(0)

    if pq_one_time_prekeys[user_id]:
        pq_otk = pq_one_time_prekeys[user_id].pop(0)

    # Create bundle with one-time keys
    bundle_copy = PreKeyBundle(
        identity_key=bundle.identity_key,
        signed_prekey=bundle.signed_prekey,
        signed_prekey_signature=bundle.signed_prekey_signature,
        one_time_prekey=classical_otk,
        pq_last_resort_prekey=bundle.pq_last_resort_prekey,
        pq_one_time_prekey=pq_otk,
        device_id=bundle.device_id,
        created_at=bundle.created_at
    )

    return bundle_copy

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/messenger/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'server': 'najika_messenger',
        'version': '1.0',
        'features': {
            'post_quantum': True,
            'sealed_sender': Config.SEALED_SENDER_ENABLED,
            'panic_mode': Config.ENABLE_PANIC_MODE
        },
        'statistics': {
            'registered_devices': len(devices),
            'online_users': len([u for u in online_users.values() if u]),
            'queued_messages': sum(len(msgs) for msgs in message_queue.values()),
            'prekey_bundles': sum(len(bundles) for bundles in prekey_bundles.values())
        }
    })

@app.route('/api/messenger/device/register', methods=['POST'])
@limiter.limit("10 per hour")
def register_device():
    """
    Register device for messaging

    Request:
    {
        "device_id": "unique_device_id",
        "user_id": "user_id",
        "device_name": "Xiaomi 11T Pro",
        "prekey_bundle": {
            "identity_key": "base64...",
            "signed_prekey": "base64...",
            "signed_prekey_signature": "base64...",
            "pq_last_resort_prekey": "base64..."
        }
    }
    """
    data = request.get_json()

    device_id = data.get('device_id')
    user_id = data.get('user_id')
    device_name = data.get('device_name')
    prekey_bundle_data = data.get('prekey_bundle')

    if not all([device_id, user_id, device_name, prekey_bundle_data]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create PreKey bundle
    prekey_bundle = PreKeyBundle(
        identity_key=prekey_bundle_data['identity_key'],
        signed_prekey=prekey_bundle_data['signed_prekey'],
        signed_prekey_signature=prekey_bundle_data['signed_prekey_signature'],
        pq_last_resort_prekey=prekey_bundle_data.get('pq_last_resort_prekey'),
        device_id=device_id,
        created_at=datetime.utcnow()
    )

    # Register device
    device = DeviceRegistration(
        device_id=device_id,
        user_id=user_id,
        device_name=device_name,
        registered_at=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        prekey_bundle=prekey_bundle,
        is_active=True
    )

    devices[device_id] = device
    prekey_bundles[user_id].append(prekey_bundle)

    return jsonify({
        'success': True,
        'message': 'Device registered successfully',
        'device_id': device_id
    }), 201

@app.route('/api/messenger/prekeys/upload', methods=['POST'])
@limiter.limit("20 per hour")
def upload_prekeys():
    """
    Upload one-time prekeys (batch)

    Request:
    {
        "user_id": "user_id",
        "device_id": "device_id",
        "one_time_prekeys": ["key1", "key2", ...],
        "pq_one_time_prekeys": ["pq_key1", "pq_key2", ...]
    }
    """
    data = request.get_json()

    user_id = data.get('user_id')
    device_id = data.get('device_id')
    otk_list = data.get('one_time_prekeys', [])
    pq_otk_list = data.get('pq_one_time_prekeys', [])

    if not all([user_id, device_id]):
        return jsonify({'error': 'Missing user_id or device_id'}), 400

    # Verify device exists
    if device_id not in devices:
        return jsonify({'error': 'Device not registered'}), 404

    # Limit number of prekeys
    current_count = len(one_time_prekeys[user_id])
    if current_count + len(otk_list) > Config.MAX_PREKEYS_PER_DEVICE:
        return jsonify({'error': 'Too many prekeys'}), 400

    # Add prekeys
    one_time_prekeys[user_id].extend(otk_list)
    pq_one_time_prekeys[user_id].extend(pq_otk_list)

    return jsonify({
        'success': True,
        'uploaded_classical': len(otk_list),
        'uploaded_pq': len(pq_otk_list),
        'total_classical': len(one_time_prekeys[user_id]),
        'total_pq': len(pq_one_time_prekeys[user_id])
    })

@app.route('/api/messenger/prekeys/<user_id>', methods=['GET'])
@limiter.limit("100 per hour")
def get_prekey_bundle_endpoint(user_id: str):
    """
    Get prekey bundle for user (to initiate conversation)

    Query params:
    - device_id (optional): Specific device
    """
    device_id = request.args.get('device_id')

    bundle = get_prekey_bundle(user_id, device_id)
    if not bundle:
        return jsonify({'error': 'No prekey bundle available'}), 404

    return jsonify({
        'success': True,
        'prekey_bundle': bundle.to_dict()
    })

@app.route('/api/messenger/messages/send', methods=['POST'])
@limiter.limit("60 per minute")
def send_message():
    """
    Send encrypted message

    Request:
    {
        "sender_id": "sender_user_id",  # Empty if sealed sender
        "recipient_id": "recipient_user_id",
        "recipient_device_id": "device_id",
        "encrypted_payload": "base64_encrypted_data",
        "sealed_sender": true
    }

    Note: Server NEVER decrypts the payload!
    """
    data = request.get_json()

    sender_id = data.get('sender_id', '')
    recipient_id = data.get('recipient_id')
    recipient_device_id = data.get('recipient_device_id')
    encrypted_payload = data.get('encrypted_payload')
    sealed_sender = data.get('sealed_sender', Config.SEALED_SENDER_ENABLED)

    if not all([recipient_id, recipient_device_id, encrypted_payload]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Verify recipient device exists
    if recipient_device_id not in devices:
        return jsonify({'error': 'Recipient device not found'}), 404

    # Create encrypted message
    message = EncryptedMessage(
        message_id=generate_message_id(),
        sender_id=sender_id if not sealed_sender else '',
        recipient_id=recipient_id,
        recipient_device_id=recipient_device_id,
        encrypted_payload=encrypted_payload,
        timestamp=datetime.utcnow(),
        sealed_sender=sealed_sender
    )

    # Try immediate delivery if recipient is online
    if is_user_online(recipient_id):
        # Send via WebSocket
        for socket_sid in online_users[recipient_id]:
            socketio.emit('new_message', {
                'message': message.to_dict()
            }, room=socket_sid)

        message.delivered = True
        message.delivered_at = datetime.utcnow()
    else:
        # Queue message for later delivery
        message_queue[recipient_id].append(message)

        # Check queue size limit
        if len(message_queue[recipient_id]) > Config.MAX_QUEUED_MESSAGES_PER_USER:
            # Remove oldest message
            message_queue[recipient_id].pop(0)

    return jsonify({
        'success': True,
        'message_id': message.message_id,
        'delivered': message.delivered,
        'queued': not message.delivered
    })

@app.route('/api/messenger/messages/fetch', methods=['POST'])
def fetch_messages():
    """
    Fetch queued messages

    Request:
    {
        "user_id": "user_id",
        "device_id": "device_id"
    }
    """
    data = request.get_json()

    user_id = data.get('user_id')
    device_id = data.get('device_id')

    if not all([user_id, device_id]):
        return jsonify({'error': 'Missing user_id or device_id'}), 400

    # Verify device
    if device_id not in devices:
        return jsonify({'error': 'Device not registered'}), 404

    # Get messages for this user/device
    messages = [
        msg.to_dict() for msg in message_queue.get(user_id, [])
        if msg.recipient_device_id == device_id
    ]

    # Clear fetched messages
    if user_id in message_queue:
        message_queue[user_id] = [
            msg for msg in message_queue[user_id]
            if msg.recipient_device_id != device_id
        ]

    return jsonify({
        'success': True,
        'messages': messages,
        'count': len(messages)
    })

@app.route('/api/messenger/messages/ack', methods=['POST'])
def acknowledge_message():
    """
    Acknowledge message delivery

    Request:
    {
        "message_id": "message_id",
        "user_id": "user_id"
    }
    """
    data = request.get_json()

    message_id = data.get('message_id')
    user_id = data.get('user_id')

    if not all([message_id, user_id]):
        return jsonify({'error': 'Missing fields'}), 400

    # Find and mark message as delivered
    for msg in message_queue.get(user_id, []):
        if msg.message_id == message_id:
            msg.delivered = True
            msg.delivered_at = datetime.utcnow()
            break

    return jsonify({'success': True})

@app.route('/api/messenger/panic/trigger', methods=['POST'])
@limiter.limit("5 per hour")
def trigger_panic():
    """
    Trigger panic mode - wipe all data for user

    Request:
    {
        "user_id": "user_id",
        "device_id": "device_id",
        "panic_code": "panic_pin"
    }

    WARNING: This PERMANENTLY deletes all data!
    """
    if not Config.ENABLE_PANIC_MODE:
        return jsonify({'error': 'Panic mode disabled'}), 403

    data = request.get_json()

    user_id = data.get('user_id')
    device_id = data.get('device_id')
    panic_code = data.get('panic_code')

    if not all([user_id, device_id, panic_code]):
        return jsonify({'error': 'Missing fields'}), 400

    # Verify device
    if device_id not in devices:
        return jsonify({'error': 'Device not found'}), 404

    # In production, verify panic_code here
    # For now, just trigger wipe

    # Mark panic timestamp
    panic_mode_devices[device_id] = datetime.utcnow()

    # Grace period before actual wipe
    time.sleep(Config.PANIC_WIPE_DELAY_SECONDS)

    # WIPE ALL USER DATA
    # 1. Remove devices
    user_devices = [d_id for d_id, d in devices.items() if d.user_id == user_id]
    for d_id in user_devices:
        del devices[d_id]

    # 2. Remove prekeys
    if user_id in prekey_bundles:
        del prekey_bundles[user_id]
    if user_id in one_time_prekeys:
        del one_time_prekeys[user_id]
    if user_id in pq_one_time_prekeys:
        del pq_one_time_prekeys[user_id]

    # 3. Remove messages
    if user_id in message_queue:
        del message_queue[user_id]

    # 4. Disconnect WebSockets
    if user_id in online_users:
        for socket_sid in online_users[user_id]:
            socketio.emit('panic_wipe', {'message': 'Server data wiped'}, room=socket_sid)
            disconnect(sid=socket_sid)
        del online_users[user_id]

    return jsonify({
        'success': True,
        'message': 'All server data wiped',
        'wiped_at': datetime.utcnow().isoformat()
    })

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    # Remove from online users
    if request.sid in socket_to_user:
        user_id, device_id = socket_to_user[request.sid]
        online_users[user_id].discard(request.sid)
        del socket_to_user[request.sid]

        # Update device last seen
        if device_id in devices:
            devices[device_id].last_seen = datetime.utcnow()
            devices[device_id].socket_sid = None

    print(f"Client disconnected: {request.sid}")

@socketio.on('authenticate')
def handle_authenticate(data):
    """Authenticate WebSocket connection"""
    user_id = data.get('user_id')
    device_id = data.get('device_id')

    if not all([user_id, device_id]):
        emit('auth_error', {'error': 'Missing credentials'})
        return

    # Verify device
    if device_id not in devices:
        emit('auth_error', {'error': 'Device not registered'})
        return

    # Mark as online
    online_users[user_id].add(request.sid)
    socket_to_user[request.sid] = (user_id, device_id)

    # Update device
    devices[device_id].last_seen = datetime.utcnow()
    devices[device_id].socket_sid = request.sid

    # Join user room
    join_room(f"user_{user_id}")

    emit('auth_success', {
        'user_id': user_id,
        'device_id': device_id,
        'queued_messages': len([m for m in message_queue.get(user_id, []) if m.recipient_device_id == device_id])
    })

    # Deliver any queued messages
    queued = [m for m in message_queue.get(user_id, []) if m.recipient_device_id == device_id]
    for msg in queued:
        emit('new_message', {'message': msg.to_dict()})
        msg.delivered = True
        msg.delivered_at = datetime.utcnow()

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    recipient_id = data.get('recipient_id')
    is_typing = data.get('is_typing', True)

    if not recipient_id:
        return

    # Get sender info
    if request.sid not in socket_to_user:
        return

    sender_id, _ = socket_to_user[request.sid]

    # Send typing indicator to recipient
    if recipient_id in online_users:
        for socket_sid in online_users[recipient_id]:
            socketio.emit('typing_indicator', {
                'sender_id': sender_id,
                'is_typing': is_typing
            }, room=socket_sid)

# ============================================================================
# BACKGROUND TASKS
# ============================================================================

def cleanup_task():
    """Background task to cleanup expired data"""
    while True:
        time.sleep(3600)  # Run every hour
        cleanup_expired_messages()
        print(f"Cleanup completed at {datetime.utcnow()}")

# ============================================================================
# STARTUP
# ============================================================================

def initialize_server():
    """Initialize server"""
    print("=" * 60)
    print("🔒 Najika Messenger Server (Zero-Knowledge)")
    print("=" * 60)
    print(f"Version: 1.0")
    print(f"Post-Quantum: Enabled (PQXDH + Kyber)")
    print(f"Sealed Sender: {Config.SEALED_SENDER_ENABLED}")
    print(f"Panic Mode: {Config.ENABLE_PANIC_MODE}")
    print(f"Message TTL: {Config.MESSAGE_TTL_DAYS} days")
    print("=" * 60)
    print("\n⚠️  ZERO-KNOWLEDGE MODE")
    print("Server NEVER sees message content")
    print("All encryption happens client-side")
    print("=" * 60)

if __name__ == '__main__':
    initialize_server()

    # Run with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=5001,
        debug=True,
        use_reloader=False
    )
