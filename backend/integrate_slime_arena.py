"""
Script to integrate Slime Arena API into najika_server.py
Adds imports and route handlers
"""

import re

SERVER_FILE = "najika_server.py"

# Read current server file
with open(SERVER_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Slime Arena imports after Minigames imports
import_pattern = r"(MINIGAMES_ENABLED = False\s+print\(f\"⚠️  Minigames API nicht verfügbar: {e}\"\))"

slime_arena_import = """

# Import Slime Arena API
try:
    from najika_slime_arena_api import (
        api_start_duel, api_duel_action, api_execute_finisher,
        api_get_leaderboard, api_get_player_stats, api_get_duel_history as api_get_slime_history,
        api_register_tournament, api_get_finishers, api_get_active_duel
    )
    SLIME_ARENA_ENABLED = True
    print("✅ Slime Arena API aktiviert")
except ImportError as e:
    SLIME_ARENA_ENABLED = False
    print(f"⚠️  Slime Arena API nicht verfügbar: {e}")"""

# Check if already added
if "SLIME_ARENA_ENABLED" not in content:
    content = re.sub(import_pattern, r"\1" + slime_arena_import, content)
    print("[OK] Added Slime Arena imports")
else:
    print("[SKIP] Slime Arena imports already exist")

# 2. Add GET routes (find a good insertion point after existing APIs)
get_routes_pattern = r"(# ===== DICE MONSTERS API \(GET\) =====.*?self\.wfile\.write\(json\.dumps\({\"error\": str\(e\)}\)\.encode\(\)\); return)"

slime_arena_get_routes = """

            # ===== SLIME ARENA API (GET) =====
            if SLIME_ARENA_ENABLED:
                if self.path == "/api/slime-arena/finishers":
                    try:
                        result = api_get_finishers()
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path == "/api/slime-arena/leaderboard":
                    try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(self.path)
                        params = parse_qs(parsed.query)
                        limit = int(params.get("limit", [100])[0])
                        result = api_get_leaderboard(limit)
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path.startswith("/api/slime-arena/stats/"):
                    try:
                        player_id = int(self.path.split("/")[-1])
                        result = api_get_player_stats(player_id)
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path.startswith("/api/slime-arena/history/"):
                    try:
                        player_id = int(self.path.split("/")[-1])
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(self.path)
                        params = parse_qs(parsed.query)
                        limit = int(params.get("limit", [20])[0])
                        result = api_get_slime_history(player_id, limit)
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path.startswith("/api/slime-arena/active/"):
                    try:
                        player_id = int(self.path.split("/")[-1])
                        result = api_get_active_duel(player_id)
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return"""

# Check if already added
if "/api/slime-arena/" not in content:
    content = re.sub(get_routes_pattern, r"\1" + slime_arena_get_routes, content, flags=re.DOTALL)
    print("[OK] Added Slime Arena GET routes")
else:
    print("[SKIP] Slime Arena GET routes already exist")

# 3. Add POST routes (find insertion point after existing POST APIs)
post_routes_pattern = r"(if self\.path==\"/api/dice/roll\":.*?self\.wfile\.write\(json\.dumps\({\"error\": str\(e\)}\)\.encode\(\)\); return)"

slime_arena_post_routes = """

            # ===== SLIME ARENA API (POST) =====
            if SLIME_ARENA_ENABLED:
                if self.path=="/api/slime-arena/start-duel":
                    try:
                        data=json.loads(body.decode("utf-8"))
                        result = api_start_duel(
                            player_id=data.get("player_id", 1),
                            mode=data.get("mode", "normal"),
                            opponent_id=data.get("opponent_id"),
                            is_vs_npc=data.get("is_vs_npc", False),
                            npc_name=data.get("npc_name")
                        )
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        print(f"[SlimeArena] Start Duel Error: {e}")
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path=="/api/slime-arena/action":
                    try:
                        data=json.loads(body.decode("utf-8"))
                        result = api_duel_action(
                            duel_id=data.get("duel_id"),
                            action_type=data.get("action_type"),
                            action_data=data.get("action_data", {})
                        )
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        print(f"[SlimeArena] Action Error: {e}")
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path=="/api/slime-arena/finisher":
                    try:
                        data=json.loads(body.decode("utf-8"))
                        result = api_execute_finisher(
                            duel_id=data.get("duel_id"),
                            finisher_id=data.get("finisher_id"),
                            winner_id=data.get("winner_id")
                        )
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        print(f"[SlimeArena] Finisher Error: {e}")
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return

                if self.path=="/api/slime-arena/tournament/register":
                    try:
                        data=json.loads(body.decode("utf-8"))
                        result = api_register_tournament(
                            player_id=data.get("player_id", 1),
                            entry_fee=data.get("entry_fee", 500)
                        )
                        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps(result).encode()); return
                    except Exception as e:
                        print(f"[SlimeArena] Tournament Error: {e}")
                        self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode()); return"""

# Check if already added
if "slime-arena/start-duel" not in content:
    content = re.sub(post_routes_pattern, r"\1" + slime_arena_post_routes, content, flags=re.DOTALL)
    print("[OK] Added Slime Arena POST routes")
else:
    print("[SKIP] Slime Arena POST routes already exist")

# Write updated server file
with open(SERVER_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Slime Arena integration complete!")
print("   Backend API: najika_slime_arena_api.py")
print("   Server routes: najika_server.py (updated)")
print("\n[OK] Ready to test!")
