"""
Najika Hybrid Signal Server

This server handles messaging between Digivice devices:
- Direct P2P routing for trusted circle (via Tailscale)
- Relay server for public users
- User discovery and online status
- Message queuing for offline users

Architecture:
- Trusted devices (8 Digivices): Direct P2P preferred, relay as fallback
- Public users: Always via relay
- End-to-End encryption maintained (server can't read messages)

Features:
- WebSocket for real-time messaging
- HTTP REST API for user management
- Message queue for offline delivery
- Online status tracking
"""

import json
import asyncio
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import threading

# Web server
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# WebSocket (for real-time messaging)
try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False
    print("⚠️ Warning: websockets not installed. Real-time messaging will not work.")
    print("Install with: pip install websockets")


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class User:
    """Digivice user"""
    user_id: str
    device_name: str
    is_trusted: bool  # In the trusted circle of 8?
    tailscale_ip: Optional[str]
    created_at: datetime
    last_seen: datetime
    is_online: bool = False
    websocket: Optional[WebSocketServerProtocol] = None

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'device_name': self.device_name,
            'is_trusted': self.is_trusted,
            'tailscale_ip': self.tailscale_ip,
            'last_seen': self.last_seen.isoformat(),
            'is_online': self.is_online,
        }


@dataclass
class QueuedMessage:
    """Message waiting for offline user"""
    message_id: str
    from_user: str
    to_user: str
    encrypted_message: Dict
    timestamp: datetime
    attempts: int = 0
    max_attempts: int = 10

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'from_user': self.from_user,
            'to_user': self.to_user,
            'encrypted_message': self.encrypted_message,
            'timestamp': self.timestamp.isoformat(),
            'attempts': self.attempts,
        }


# ============================================================
# SIGNAL SERVER
# ============================================================

class SignalServer:
    """Hybrid Signal server for Digivice messaging"""

    def __init__(self):
        # User registry
        self.users: Dict[str, User] = {}
        self.users_lock = threading.Lock()

        # Message queue (for offline users)
        self.message_queue: Dict[str, List[QueuedMessage]] = defaultdict(list)
        self.queue_lock = threading.Lock()

        # Active WebSocket connections
        self.websockets: Dict[str, WebSocketServerProtocol] = {}

        # Trusted circle (the 8 Digivices)
        self.trusted_circle: Set[str] = set()

        # Stats
        self.stats = {
            'total_messages': 0,
            'direct_p2p': 0,
            'relayed': 0,
            'queued': 0,
        }

    # ============================================================
    # USER MANAGEMENT
    # ============================================================

    def register_user(
        self,
        user_id: str,
        device_name: str,
        is_trusted: bool = False,
        tailscale_ip: Optional[str] = None,
    ) -> User:
        """Register a new user"""
        with self.users_lock:
            if user_id in self.users:
                # Update existing user
                user = self.users[user_id]
                user.device_name = device_name
                user.is_trusted = is_trusted
                user.tailscale_ip = tailscale_ip
                user.last_seen = datetime.now()
            else:
                # Create new user
                user = User(
                    user_id=user_id,
                    device_name=device_name,
                    is_trusted=is_trusted,
                    tailscale_ip=tailscale_ip,
                    created_at=datetime.now(),
                    last_seen=datetime.now(),
                )
                self.users[user_id] = user

            if is_trusted:
                self.trusted_circle.add(user_id)

            print(f"✅ User registered: {device_name} ({user_id}) - Trusted: {is_trusted}")
            return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def update_online_status(self, user_id: str, is_online: bool):
        """Update user's online status"""
        with self.users_lock:
            user = self.users.get(user_id)
            if user:
                user.is_online = is_online
                user.last_seen = datetime.now()

    def get_online_users(self) -> List[User]:
        """Get all online users"""
        return [u for u in self.users.values() if u.is_online]

    # ============================================================
    # MESSAGE ROUTING
    # ============================================================

    def route_message(
        self,
        from_user_id: str,
        to_user_id: str,
        encrypted_message: Dict,
    ) -> Dict:
        """
        Route a message with automatic mode selection:
        1. Direct P2P (if both in trusted circle)
        2. Relay via server (if public user or P2P unavailable)
        3. Queue (if recipient offline)
        """
        self.stats['total_messages'] += 1

        from_user = self.get_user(from_user_id)
        to_user = self.get_user(to_user_id)

        if not to_user:
            return {
                'success': False,
                'error': 'Recipient not found',
                'mode': 'error'
            }

        # Check if both users are in trusted circle
        both_trusted = (
            from_user_id in self.trusted_circle and
            to_user_id in self.trusted_circle
        )

        # Check if recipient is online
        if not to_user.is_online:
            # Queue message for offline delivery
            return self._queue_message(from_user_id, to_user_id, encrypted_message)

        # Attempt direct P2P if both trusted and have Tailscale IPs
        if both_trusted and to_user.tailscale_ip:
            # For P2P, just return the Tailscale IP
            # The client will attempt direct connection
            self.stats['direct_p2p'] += 1
            return {
                'success': True,
                'mode': 'direct_p2p',
                'tailscale_ip': to_user.tailscale_ip,
                'message': 'Use direct P2P connection'
            }

        # Fallback to relay
        return self._relay_message(from_user_id, to_user_id, encrypted_message)

    def _relay_message(
        self,
        from_user_id: str,
        to_user_id: str,
        encrypted_message: Dict,
    ) -> Dict:
        """Relay message via server"""
        to_user = self.get_user(to_user_id)

        if not to_user or not to_user.is_online:
            return self._queue_message(from_user_id, to_user_id, encrypted_message)

        # Send via WebSocket if connected
        if to_user_id in self.websockets:
            websocket = self.websockets[to_user_id]
            try:
                # Send message asynchronously
                message_data = {
                    'type': 'message',
                    'from': from_user_id,
                    'message': encrypted_message,
                    'timestamp': datetime.now().isoformat(),
                }

                # Schedule send (WebSocket is async)
                asyncio.create_task(
                    websocket.send(json.dumps(message_data))
                )

                self.stats['relayed'] += 1
                return {
                    'success': True,
                    'mode': 'relay',
                    'message': 'Message relayed via server'
                }
            except Exception as e:
                print(f"❌ Relay error: {e}")
                return self._queue_message(from_user_id, to_user_id, encrypted_message)

        # No WebSocket connection, queue message
        return self._queue_message(from_user_id, to_user_id, encrypted_message)

    def _queue_message(
        self,
        from_user_id: str,
        to_user_id: str,
        encrypted_message: Dict,
    ) -> Dict:
        """Queue message for offline delivery"""
        with self.queue_lock:
            message_id = hashlib.md5(
                f"{from_user_id}{to_user_id}{time.time()}".encode()
            ).hexdigest()

            queued_msg = QueuedMessage(
                message_id=message_id,
                from_user=from_user_id,
                to_user=to_user_id,
                encrypted_message=encrypted_message,
                timestamp=datetime.now(),
            )

            self.message_queue[to_user_id].append(queued_msg)
            self.stats['queued'] += 1

            print(f"📥 Message queued for {to_user_id} (queue size: {len(self.message_queue[to_user_id])})")

            return {
                'success': True,
                'mode': 'queued',
                'message': 'Recipient offline, message queued',
                'message_id': message_id,
            }

    def get_queued_messages(self, user_id: str) -> List[QueuedMessage]:
        """Get all queued messages for a user"""
        with self.queue_lock:
            messages = self.message_queue.get(user_id, [])
            # Clear queue
            if user_id in self.message_queue:
                del self.message_queue[user_id]
            return messages

    # ============================================================
    # WEBSOCKET MANAGEMENT
    # ============================================================

    async def handle_websocket(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket connection"""
        user_id = None

        try:
            # First message should be authentication
            auth_msg = await websocket.recv()
            auth_data = json.loads(auth_msg)

            if auth_data.get('type') != 'auth':
                await websocket.close(1008, "Authentication required")
                return

            user_id = auth_data.get('user_id')
            # TODO: Add proper authentication here

            # Register WebSocket
            self.websockets[user_id] = websocket
            self.update_online_status(user_id, True)

            print(f"✅ WebSocket connected: {user_id}")

            # Send queued messages
            queued = self.get_queued_messages(user_id)
            for msg in queued:
                await websocket.send(json.dumps({
                    'type': 'message',
                    'from': msg.from_user,
                    'message': msg.encrypted_message,
                    'timestamp': msg.timestamp.isoformat(),
                    'queued': True,
                }))

            # Keep connection alive
            async for message in websocket:
                data = json.loads(message)

                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))

                elif data.get('type') == 'send_message':
                    # Handle message send
                    to_user = data.get('to')
                    encrypted_msg = data.get('message')
                    result = self.route_message(user_id, to_user, encrypted_msg)
                    await websocket.send(json.dumps(result))

        except Exception as e:
            print(f"⚠️ WebSocket error: {e}")

        finally:
            # Cleanup
            if user_id:
                if user_id in self.websockets:
                    del self.websockets[user_id]
                self.update_online_status(user_id, False)
                print(f"❌ WebSocket disconnected: {user_id}")

    # ============================================================
    # STATS
    # ============================================================

    def get_stats(self) -> Dict:
        """Get server statistics"""
        return {
            **self.stats,
            'total_users': len(self.users),
            'trusted_users': len(self.trusted_circle),
            'online_users': len(self.get_online_users()),
            'queued_messages': sum(len(q) for q in self.message_queue.values()),
        }


# ============================================================
# HTTP REQUEST HANDLER
# ============================================================

# Global server instance
signal_server = SignalServer()


class SignalHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for Signal server REST API"""

    def _send_json(self, data: Dict, status_code: int = 200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/health':
            self._send_json({'status': 'ok'})

        elif self.path == '/api/stats':
            self._send_json(signal_server.get_stats())

        elif self.path.startswith('/api/users/'):
            # Get user status
            parts = self.path.split('/')
            if len(parts) >= 4:
                user_id = parts[3]
                if parts[4] == 'status':
                    user = signal_server.get_user(user_id)
                    if user:
                        self._send_json({
                            'online': user.is_online,
                            'last_seen': user.last_seen.isoformat(),
                        })
                    else:
                        self._send_json({'error': 'User not found'}, 404)

        elif self.path == '/api/users/online':
            online_users = signal_server.get_online_users()
            self._send_json({
                'users': [u.to_dict() for u in online_users]
            })

        else:
            self._send_json({'error': 'Not found'}, 404)

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        if self.path == '/api/users/register':
            # Register user
            user = signal_server.register_user(
                user_id=data.get('user_id'),
                device_name=data.get('device_name'),
                is_trusted=data.get('is_trusted', False),
                tailscale_ip=data.get('tailscale_ip'),
            )
            self._send_json({'success': True, 'user': user.to_dict()})

        elif self.path == '/api/messenger/relay':
            # Relay message
            result = signal_server.route_message(
                from_user_id=data.get('from'),
                to_user_id=data.get('to'),
                encrypted_message=data.get('message'),
            )
            self._send_json(result)

        elif self.path == '/api/messenger/receive':
            # Direct P2P receive endpoint (for Tailscale direct connections)
            to_user_id = data.get('to')
            encrypted_msg = data.get('message')

            # Add to queue or deliver immediately if online
            user = signal_server.get_user(to_user_id)
            if user and user.is_online and to_user_id in signal_server.websockets:
                # Send via WebSocket
                websocket = signal_server.websockets[to_user_id]
                asyncio.create_task(
                    websocket.send(json.dumps({
                        'type': 'message',
                        'from': data.get('from', 'unknown'),
                        'message': encrypted_msg,
                        'timestamp': datetime.now().isoformat(),
                    }))
                )
                self._send_json({'success': True, 'mode': 'delivered'})
            else:
                # Queue
                signal_server._queue_message(
                    from_user_id=data.get('from', 'unknown'),
                    to_user_id=to_user_id,
                    encrypted_message=encrypted_msg,
                )
                self._send_json({'success': True, 'mode': 'queued'})

        else:
            self._send_json({'error': 'Not found'}, 404)


# ============================================================
# SERVER STARTUP
# ============================================================

def run_http_server(port: int = 9000):
    """Run HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SignalHTTPHandler)
    print(f"🌐 HTTP Server running on port {port}")
    httpd.serve_forever()


async def run_websocket_server(port: int = 9001):
    """Run WebSocket server"""
    if not HAS_WEBSOCKETS:
        print("❌ WebSocket server unavailable (websockets module not installed)")
        return

    async with websockets.serve(signal_server.handle_websocket, "0.0.0.0", port):
        print(f"🔌 WebSocket Server running on port {port}")
        await asyncio.Future()  # Run forever


def main():
    """Start both HTTP and WebSocket servers"""
    print("=" * 60)
    print("NAJIKA HYBRID SIGNAL SERVER")
    print("=" * 60)
    print("Features:")
    print("  - Direct P2P routing for trusted circle")
    print("  - Relay server for public users")
    print("  - Message queuing for offline users")
    print("=" * 60)

    # Start HTTP server in thread
    http_thread = threading.Thread(target=run_http_server, args=(9000,), daemon=True)
    http_thread.start()

    # Start WebSocket server
    if HAS_WEBSOCKETS:
        asyncio.run(run_websocket_server(9001))
    else:
        print("⚠️ Running in HTTP-only mode")
        http_thread.join()


if __name__ == "__main__":
    main()
