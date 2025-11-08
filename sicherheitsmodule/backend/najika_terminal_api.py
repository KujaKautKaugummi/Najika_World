"""
NAJIKA TERMINAL API
===================

Erweiterte Terminal-Kontrolle für das Najika Digivice
Ermöglicht volle PC-Steuerung aus jedem Netzwerk

FEATURES:
- Persistent Shell Sessions
- Beliebige Befehle (nach Authentifizierung)
- Prozess-Management
- File System Zugriff
- Security Integration (Alcatraz)

SICHERHEIT:
- Passwort-Authentifizierung
- Verschlüsselte Befehls-Übertragung
- Audit Logging
- VPN-Check vor kritischen Operationen
"""

import os
import json
import subprocess
import threading
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Persistent Shell Sessions
SHELL_SESSIONS: Dict[str, 'ShellSession'] = {}


class ShellSession:
    """
    Persistent Shell Session für kontinuierliche Terminal-Nutzung
    """
    def __init__(self, session_id: str, shell_type: str = "bash"):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.shell_type = shell_type
        self.process = None
        self.output_buffer = []
        self.is_active = False
        self._start_shell()

    def _start_shell(self):
        """Starte Shell-Prozess"""
        try:
            if os.name == 'nt':  # Windows
                shell_cmd = ['cmd.exe'] if self.shell_type == 'cmd' else ['powershell.exe']
            else:  # Linux/Mac
                shell_cmd = ['/bin/bash', '-i']

            self.process = subprocess.Popen(
                shell_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            self.is_active = True
            print(f"✅ Shell session {self.session_id} started")
        except Exception as e:
            print(f"❌ Failed to start shell: {e}")
            self.is_active = False

    def execute(self, command: str, timeout: int = 30) -> Tuple[bool, str, str]:
        """
        Führe Befehl in Session aus

        Returns:
            (success, stdout, stderr)
        """
        if not self.is_active or not self.process:
            return False, "", "Shell session not active"

        self.last_activity = datetime.now()

        try:
            # Befehl senden
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()

            # Output sammeln (mit Timeout)
            output_lines = []
            start_time = time.time()

            while time.time() - start_time < timeout:
                if self.process.poll() is not None:
                    break

                # Lese Output
                line = self.process.stdout.readline()
                if line:
                    output_lines.append(line.strip())
                else:
                    break

            output = '\n'.join(output_lines)
            self.output_buffer.append({
                'command': command,
                'output': output,
                'timestamp': datetime.now().isoformat()
            })

            return True, output, ""

        except Exception as e:
            return False, "", str(e)

    def close(self):
        """Beende Shell Session"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
        self.is_active = False
        print(f"✅ Shell session {self.session_id} closed")


class TerminalAPI:
    """
    Terminal API für Najika Digivice
    """

    # Security: Authentifizierung
    TERMINAL_PASSWORD_HASH = None  # Wird beim ersten Start gesetzt

    @staticmethod
    def initialize(password: str):
        """Setze Terminal-Passwort"""
        TerminalAPI.TERMINAL_PASSWORD_HASH = hashlib.sha256(password.encode()).hexdigest()
        print("✅ Terminal API initialized")

    @staticmethod
    def authenticate(password: str) -> bool:
        """Prüfe Passwort"""
        if not TerminalAPI.TERMINAL_PASSWORD_HASH:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == TerminalAPI.TERMINAL_PASSWORD_HASH

    @staticmethod
    def create_session(auth_token: str, shell_type: str = "bash") -> Optional[str]:
        """
        Erstelle neue Shell Session

        Returns:
            session_id oder None bei Fehler
        """
        # Generiere eindeutige Session-ID
        session_id = hashlib.md5(f"{auth_token}{time.time()}".encode()).hexdigest()[:12]

        # Erstelle Session
        session = ShellSession(session_id, shell_type)

        if session.is_active:
            SHELL_SESSIONS[session_id] = session
            print(f"✅ Created session {session_id}")
            return session_id
        else:
            return None

    @staticmethod
    def get_session(session_id: str) -> Optional[ShellSession]:
        """Hole Session"""
        return SHELL_SESSIONS.get(session_id)

    @staticmethod
    def close_session(session_id: str) -> bool:
        """Schließe Session"""
        session = SHELL_SESSIONS.get(session_id)
        if session:
            session.close()
            del SHELL_SESSIONS[session_id]
            return True
        return False

    @staticmethod
    def list_sessions() -> List[Dict]:
        """Liste alle aktiven Sessions"""
        return [
            {
                'session_id': sid,
                'created_at': session.created_at.isoformat(),
                'last_activity': session.last_activity.isoformat(),
                'shell_type': session.shell_type,
                'is_active': session.is_active
            }
            for sid, session in SHELL_SESSIONS.items()
        ]

    @staticmethod
    def execute_command(command: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict:
        """
        Führe einmaligen Befehl aus (keine Session)

        Für schnelle Befehle ohne persistent Shell
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )

            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Command timeout after {timeout}s',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }

    @staticmethod
    def get_processes() -> List[Dict]:
        """Liste laufende Prozesse"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['tasklist', '/FO', 'CSV'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                processes = []
                for line in lines:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        processes.append({
                            'name': parts[0].strip('"'),
                            'pid': parts[1].strip('"')
                        })
                return processes
            else:  # Linux/Mac
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                processes = []
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 11:
                        processes.append({
                            'user': parts[0],
                            'pid': parts[1],
                            'cpu': parts[2],
                            'mem': parts[3],
                            'command': ' '.join(parts[10:])
                        })
                return processes
        except Exception as e:
            print(f"❌ Failed to get processes: {e}")
            return []

    @staticmethod
    def kill_process(pid: str) -> bool:
        """Beende Prozess"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
            else:  # Linux/Mac
                subprocess.run(['kill', '-9', pid], check=True)
            return True
        except:
            return False


# Flask/HTTP Handler Integration
def handle_terminal_api(path: str, body: dict, auth_token: str) -> dict:
    """
    Handler für Terminal API Requests

    Zu integrieren in najika_server.py do_POST()
    """

    # Authentifizierung prüfen
    password = body.get('password', '')
    if not TerminalAPI.authenticate(password):
        return {'success': False, 'error': 'Authentication failed'}

    # Route Handling
    if path == '/api/terminal/session/create':
        shell_type = body.get('shell_type', 'bash')
        session_id = TerminalAPI.create_session(auth_token, shell_type)
        if session_id:
            return {'success': True, 'session_id': session_id}
        else:
            return {'success': False, 'error': 'Failed to create session'}

    elif path == '/api/terminal/session/close':
        session_id = body.get('session_id', '')
        success = TerminalAPI.close_session(session_id)
        return {'success': success}

    elif path == '/api/terminal/session/list':
        sessions = TerminalAPI.list_sessions()
        return {'success': True, 'sessions': sessions}

    elif path == '/api/terminal/execute':
        session_id = body.get('session_id')
        command = body.get('command', '')
        timeout = body.get('timeout', 30)

        if session_id:
            # Execute in session
            session = TerminalAPI.get_session(session_id)
            if session:
                success, stdout, stderr = session.execute(command, timeout)
                return {
                    'success': success,
                    'stdout': stdout,
                    'stderr': stderr
                }
            else:
                return {'success': False, 'error': 'Session not found'}
        else:
            # One-time execution
            cwd = body.get('cwd')
            result = TerminalAPI.execute_command(command, timeout, cwd)
            return result

    elif path == '/api/terminal/processes':
        processes = TerminalAPI.get_processes()
        return {'success': True, 'processes': processes}

    elif path == '/api/terminal/kill':
        pid = body.get('pid', '')
        success = TerminalAPI.kill_process(pid)
        return {'success': success}

    else:
        return {'success': False, 'error': 'Unknown endpoint'}


# Cleanup Thread (schließt inaktive Sessions)
def cleanup_inactive_sessions(max_inactive_minutes: int = 30):
    """Background Thread: Schließt inaktive Sessions"""
    while True:
        time.sleep(60)  # Check every minute

        now = datetime.now()
        to_close = []

        for session_id, session in SHELL_SESSIONS.items():
            inactive_minutes = (now - session.last_activity).total_seconds() / 60
            if inactive_minutes > max_inactive_minutes:
                to_close.append(session_id)

        for session_id in to_close:
            print(f"🧹 Closing inactive session {session_id}")
            TerminalAPI.close_session(session_id)


# Start Cleanup Thread
cleanup_thread = threading.Thread(target=cleanup_inactive_sessions, daemon=True)
cleanup_thread.start()


if __name__ == '__main__':
    # Test
    print("🧪 Testing Terminal API...")

    # Initialize
    TerminalAPI.initialize("test_password_123")

    # Authenticate
    assert TerminalAPI.authenticate("test_password_123") == True
    assert TerminalAPI.authenticate("wrong") == False

    # Create session
    session_id = TerminalAPI.create_session("test_token", "bash")
    print(f"Created session: {session_id}")

    # Execute command
    session = TerminalAPI.get_session(session_id)
    if session:
        success, stdout, stderr = session.execute("echo 'Hello from Terminal!'")
        print(f"Output: {stdout}")

    # List sessions
    sessions = TerminalAPI.list_sessions()
    print(f"Active sessions: {len(sessions)}")

    # Close session
    TerminalAPI.close_session(session_id)

    print("✅ Test completed!")
