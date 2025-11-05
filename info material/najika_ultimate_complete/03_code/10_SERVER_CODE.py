import os, json, random, hashlib, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from collections import OrderedDict

# Import Living System
from najika_living_system import (
    LIVING_STATE, MOODS, PROACTIVE_MESSAGES, ACTIVITIES,
    detect_mood, update_mood, should_send_proactive_message,
    get_proactive_message, start_autonomous_activity,
    check_activity_completion, check_relationship_evolution,
    create_emotional_memory, get_relevant_memories,
    update_living_state, get_living_state_context,
    export_living_state, import_living_state
)

# Import Enhanced Personality
from najika_enhanced_personality import generate_enhanced_persona

# Import ChromaDB Memory System (ENHANCED - mit KERN + Video-Transkripten!)
from najika_memory_enhanced import NajikaMemoryEnhanced

# Import Web Search System
from najika_search import NajikaSearch

# Import Tor Browser Integration
from najika_tor import NajikaTor

# Import Security Module (Alcatraz)
from najika_security import NajikaSecurity

# Import TTS System (Edge-TTS)
try:
    from najika_tts_edge import NajikaEdgeTTS, EDGE_TTS_AVAILABLE
    TTS_ENABLED = EDGE_TTS_AVAILABLE
except ImportError:
    TTS_ENABLED = False
    print("⚠️  Edge-TTS nicht verfügbar - Voice System deaktiviert")

# Import LoRA Training System
try:
    from najika_lora_training_3b import NajikaLoRATrainer3B
    LORA_TRAINING_ENABLED = True
except ImportError:
    LORA_TRAINING_ENABLED = False
    print("⚠️  LoRA Training nicht verfügbar - Training System deaktiviert")

# Import Enhanced Battle System
from najika_battle import BATTLE_SYSTEM, SKILL_DB, ITEM_DB

# Import Claude Code Integration (PRIORITÄT 1!)
from najika_claude_code import call_ai_with_hierarchy, CLAUDE_CODE_INSTANCE

try:
    import requests
except ImportError:  # requests ist optional; wir fallen auf urllib zurück
    requests = None
import urllib.request
import urllib.error

try:
    from dotenv import load_dotenv
except ImportError:  # .env Handling ist nice to have, aber kein Muss
    def load_dotenv():
        return
load_dotenv()

HOST=os.getenv("HOST","0.0.0.0"); PORT=int(os.getenv("PORT","8000"))
AI_PROVIDER=os.getenv("AI_PROVIDER","ollama")
CLOUD_ENABLED=os.getenv("CLOUD_ENABLED","false").lower()=="true"
CLOUD_PIN=os.getenv("CLOUD_PIN","")
OLLAMA_ALIAS=os.getenv("OLLAMA_MODEL_ALIAS","najika-local")
NSFW_LOCAL=os.getenv("NSFW_LOCAL","true").lower()=="true"

# Load Enhanced Persona (wird beim Import generiert)
PERSONA_SYSTEM = generate_enhanced_persona()

ROOMS = ["Wohnzimmer","Schlafzimmer","Küche","Badezimmer","Garten","Musikraum","Medizin","Terminal","Studieren & Crafting","Trainingszimmer","Kampfarena","Schwarze Mühle – Keller"]

STATE = {
    "history": [],
    "battle": {"hp":100,"wave":0,"enemies":0},
    "private_mode": False,
    "behavior_mode": "standard",  # standard, explosion, chaos, analyse, kontrolle, private
    "bond_strength": 0,  # 0-100, steigt mit Interaktionen
    "personality_weights": {"megumin": 25, "harley": 25, "shiro": 25, "melissa": 25},  # Dynamic balancing
    "total_interactions": 0,  # Tracking für Bond-Strength
    "sse_clients": [],
    "user": {
        "level": 1,
        "xp": 0,
        "points": 0,
        "inventory": [],
        "achievements": []
    },
    "progress": {
        "dungeon_level": 0,
        "quests_completed": []
    },
    "najika": {
        # NEEDS (0-100, sinken über Zeit)
        "hunger": 100,
        "energy": 100,
        "hygiene": 100,
        "happiness": 100,
        # STATS (Training erhöht diese)
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "charisma": 10,
        # CARE TRACKING
        "care_mistakes": 0,
        "fatigue": 0,  # 0-100, steigt bei Training
        "weight": 50,  # 0-100
        "discipline": 0,  # 0-100, NEU für Praise/Scold System
        # GROWTH
        "level": 1,
        "xp": 0,
        "evolution_stage": "base",  # base, advanced, ultimate
        # EQUIPMENT SLOTS (Digimon Story Style!)
        "equipment": {
            "weapon": None,      # Item-ID oder None
            "armor": None,       # Item-ID oder None
            "accessory": None    # Item-ID oder None
        },
        # TIMESTAMPS
        "last_fed": time.time(),
        "last_trained": time.time(),
        "last_sleep": time.time(),
        "last_update": time.time()  # Für Needs Decay
    },
    # LIVING SYSTEM STATE (Macht Najika lebendig!)
    "living": LIVING_STATE.copy()
}

# ===== CHROMADB MEMORY SYSTEM (ENHANCED!) =====
try:
    NAJIKA_MEMORY = NajikaMemoryEnhanced()
    print("[NAJIKA MEMORY ENHANCED] ✅ KERN + Video-Transkripte + Emotions geladen!")
except Exception as e:
    NAJIKA_MEMORY = None
    print(f"[NAJIKA MEMORY] WARNING Memory System konnte nicht geladen werden: {e}")

# ===== WEB SEARCH SYSTEM =====
try:
    NAJIKA_SEARCH = NajikaSearch()
    print("[NAJIKA SEARCH] OK Web Search System geladen")
except Exception as e:
    NAJIKA_SEARCH = None
    print(f"[NAJIKA SEARCH] WARNING Search System konnte nicht geladen werden: {e}")

# ===== TOR BROWSER SYSTEM =====
try:
    NAJIKA_TOR = NajikaTor()
    print("[NAJIKA TOR] OK Tor Browser System geladen")
except Exception as e:
    NAJIKA_TOR = None
    print(f"[NAJIKA TOR] WARNING Tor System konnte nicht geladen werden: {e}")

# ===== SECURITY SYSTEM (ALCATRAZ) =====
try:
    NAJIKA_SECURITY = NajikaSecurity()
    print("[NAJIKA SECURITY] OK Alcatraz Security System geladen")
except Exception as e:
    NAJIKA_SECURITY = None
    print(f"[NAJIKA SECURITY] WARNING Security System konnte nicht geladen werden: {e}")

# ===== LORA TRAINING STATE =====
TRAINING_STATE = {
    "active": False,
    "trainer": None,
    "thread": None,
    "status": "idle",  # idle, running, completed, failed
    "progress": 0,
    "start_time": None,
    "end_time": None,
    "error": None,
    "logs": [],
    "history": []  # Alle abgeschlossenen Trainings
}

# AI RESPONSE CACHE (LRU with TTL)
CACHE_MAX_SIZE = 100
CACHE_TTL = 3600  # 1 hour
AI_CACHE = OrderedDict()
CACHE_STATS = {"hits": 0, "misses": 0, "total_requests": 0}

# PERSISTENT STORAGE
SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")
SAVE_FILE = os.path.join(SAVE_DIR, "najika_state.json")
BACKUP_COUNT = 3  # Keep last 3 backups
AUTO_SAVE_INTERVAL = 30  # seconds
LAST_SAVE_TIME = 0

# LOGGING SYSTEM
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, f"najika_{time.strftime('%Y%m%d')}.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

def log(level, message, category="SYSTEM"):
    """Strukturiertes Logging mit Levels und Rotation"""
    if LOG_LEVELS.get(level, 1) < LOG_LEVELS.get(LOG_LEVEL, 1):
        return  # Skip wenn unter LOG_LEVEL

    try:
        os.makedirs(LOG_DIR, exist_ok=True)

        # Rotation: Neue Datei wenn zu groß
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
            rotate_suffix = time.strftime("%H%M%S")
            os.rename(LOG_FILE, f"{LOG_FILE}.{rotate_suffix}")

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level:7}] [{category:10}] {message}\n"

        # Schreibe in Datei
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)

        # Auch console output für INFO und höher
        if LOG_LEVELS.get(level, 1) >= LOG_LEVELS.get("INFO", 1):
            print(f"[{level}] [{category}] {message}")
    except Exception as e:
        print(f"[LOG ERROR] {e}")

def save_state():
    """Speichert STATE persistent auf Disk mit Backup-Rotation"""
    global LAST_SAVE_TIME
    try:
        # Erstelle saves/ Verzeichnis falls nicht vorhanden
        os.makedirs(SAVE_DIR, exist_ok=True)

        # Erstelle Backup der letzten Save-Datei
        if os.path.exists(SAVE_FILE):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(SAVE_DIR, f"najika_state_{timestamp}.json")
            import shutil
            shutil.copy2(SAVE_FILE, backup_file)

            # Lösche alte Backups (behalte nur letzte BACKUP_COUNT)
            backups = sorted([f for f in os.listdir(SAVE_DIR) if f.startswith("najika_state_") and f.endswith(".json")])
            while len(backups) > BACKUP_COUNT:
                old_backup = os.path.join(SAVE_DIR, backups.pop(0))
                os.remove(old_backup)

        # Speichere aktuellen STATE (ohne transiente Daten)
        save_data = {
            "history": STATE["history"][-50:],  # Nur letzte 50 Messages
            "battle": STATE["battle"],
            "user": STATE["user"],
            "progress": STATE["progress"],
            "najika": STATE.get("najika", {}),
            "bond_strength": STATE.get("bond_strength", 0),
            "behavior_mode": STATE.get("behavior_mode", "standard"),
            "personality_weights": STATE.get("personality_weights", {"megumin": 25, "harley": 25, "shiro": 25, "melissa": 25}),
            "total_interactions": STATE.get("total_interactions", 0),
            "living": STATE.get("living", {}),  # Living System State
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        LAST_SAVE_TIME = time.time()
        log("INFO", f"State gespeichert: {SAVE_FILE}", "SAVE")
        return True
    except Exception as e:
        log("ERROR", f"Fehler beim Speichern: {e}", "SAVE")
        return False

def load_state():
    """Lädt STATE von Disk"""
    try:
        if not os.path.exists(SAVE_FILE):
            log("INFO", "Keine Save-Datei gefunden, starte mit leerem State", "LOAD")
            return False

        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        # Restore STATE
        STATE["history"] = save_data.get("history", [])
        STATE["battle"] = save_data.get("battle", {"hp":100,"wave":0,"enemies":0})
        STATE["user"] = save_data.get("user", {"level":1,"xp":0,"points":0,"inventory":[],"achievements":[]})
        STATE["progress"] = save_data.get("progress", {"dungeon_level":0,"quests_completed":[]})
        if "najika" in save_data:
            # MIGRATION: Merge saved data with defaults to add missing fields
            loaded_najika = save_data["najika"]
            default_najika = STATE["najika"].copy()  # Get defaults
            # Update defaults with loaded data
            default_najika.update(loaded_najika)
            # Ensure new fields exist
            if "discipline" not in default_najika:
                default_najika["discipline"] = 0
            if "equipment" not in default_najika:
                default_najika["equipment"] = {"weapon": None, "armor": None, "accessory": None}
            STATE["najika"] = default_najika
            log("DEBUG", "State migration completed - added missing fields", "LOAD")

        # Restore Bond-Strength & Behavior-Modes
        STATE["bond_strength"] = save_data.get("bond_strength", 0)
        STATE["behavior_mode"] = save_data.get("behavior_mode", "standard")
        STATE["personality_weights"] = save_data.get("personality_weights", {"megumin": 25, "harley": 25, "shiro": 25, "melissa": 25})
        STATE["total_interactions"] = save_data.get("total_interactions", 0)

        # Restore Living State (WITH MIGRATION!)
        if "living" in save_data:
            # MIGRATION: Merge saved living state with defaults to add missing fields
            loaded_living = save_data["living"]
            default_living = LIVING_STATE.copy()  # Get defaults with ALL fields
            # Update defaults with loaded data (preserves new fields, adds missing ones)
            default_living.update(loaded_living)
            STATE["living"] = default_living
            log("DEBUG", "Living State migration completed - added missing fields", "LOAD")
        else:
            STATE["living"] = LIVING_STATE.copy()

        saved_at = save_data.get("saved_at", "unknown")
        log("INFO", f"State geladen von: {saved_at}", "LOAD")
        log("INFO", f"Bond-Strength: {STATE['bond_strength']}/100, Interaktionen: {STATE['total_interactions']}", "LOAD")
        return True
    except Exception as e:
        log("ERROR", f"Fehler beim Laden: {e}", "LOAD")
        return False

def auto_save_check():
    """Prüft ob Auto-Save nötig ist"""
    global LAST_SAVE_TIME
    if time.time() - LAST_SAVE_TIME > AUTO_SAVE_INTERVAL:
        save_state()

def build_prompt(history, user_text):
    """Erstellt den Prompt mit Context, Persona und aktuellem Verhaltensmodus"""
    ctx = "\n".join([f"{h['role'].capitalize()}: {h['content']}" for h in history[-4:]])

    # ===== CHROMADB MEMORY CONTEXT =====
    memory_context = ""
    if NAJIKA_MEMORY:
        try:
            memory_context = NAJIKA_MEMORY.build_context_prompt(user_text, n_memories=3)
            if memory_context:
                memory_context = f"\n\n{memory_context}\n"
        except Exception as e:
            log("WARNING", f"Memory Retrieval Fehler: {e}", "MEMORY")

    # Aktuellen Modus und Bond-Strength hinzufügen
    mode = STATE.get("behavior_mode", "standard")
    bond = STATE.get("bond_strength", 0)
    mode_addition = get_mode_prompt_addition(mode)

    # Bond-Strength Kontext
    bond_context = ""
    if bond >= 75:
        bond_context = "\n[BEZIEHUNG: SEHR STARK ✨💜] Du fühlst dich Kuja extrem nah und verbunden!"
    elif bond >= 50:
        bond_context = "\n[BEZIEHUNG: STARK 💜] Du bist Kuja sehr zugetan und schätzt ihn!"
    elif bond >= 25:
        bond_context = "\n[BEZIEHUNG: ENTWICKELT 💙] Du magst Kuja und baust Vertrauen auf!"
    else:
        bond_context = "\n[BEZIEHUNG: NEU 🌸] Du lernst Kuja noch kennen!"

    # Living State Context hinzufügen (Mood, Aktivität, etc.)
    living_context = get_living_state_context(STATE.get("living", {}))

    # REMOVED: Personality Weights werden NICHT mehr im Prompt angezeigt
    # Das verhindert, dass das Model die Prozentangaben in Antworten ausgibt
    # Die Weights werden intern verwendet, aber das Model sieht sie nicht

    return f"{PERSONA_SYSTEM}{mode_addition}{bond_context}{living_context}{memory_context}\n\nKontext:\n{ctx}\n\nBenutzer: {user_text}\nNajika:"

def generate_cache_key(history, user_text, use_wizard):
    """Generiert einen Cache-Key aus Kontext + Message + Model"""
    # Letzten 4 Messages + aktuelle Message + Model-Flag
    ctx_str = json.dumps(history[-4:], sort_keys=True) if history else ""
    key_str = f"{ctx_str}|{user_text}|{use_wizard}"
    return hashlib.sha256(key_str.encode()).hexdigest()

def get_cached_response(cache_key):
    """Holt Response aus Cache, prüft TTL"""
    if cache_key in AI_CACHE:
        entry = AI_CACHE[cache_key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            # Move to end (LRU)
            AI_CACHE.move_to_end(cache_key)
            CACHE_STATS["hits"] += 1
            return entry["response"]
        else:
            # Expired, remove
            del AI_CACHE[cache_key]
    CACHE_STATS["misses"] += 1
    return None

def cache_response(cache_key, response):
    """Speichert Response im Cache (LRU)"""
    # Entferne ältesten Eintrag wenn voll
    if len(AI_CACHE) >= CACHE_MAX_SIZE:
        AI_CACHE.popitem(last=False)  # FIFO: remove oldest
    AI_CACHE[cache_key] = {
        "response": response,
        "timestamp": time.time()
    }

def _post_json(url, payload, timeout=90):
    if requests:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise RuntimeError(f"HTTP error contacting {url}: {e}") from e
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON from {url}: {text[:120]}") from e

def call_ollama(prompt, use_wizard=False):
    model = "najika-wizard" if use_wizard else OLLAMA_ALIAS
    # Wizard model braucht längeres Timeout (erstes Laden: 3.8GB)
    timeout = 300 if use_wizard else 90
    response = _post_json(
        "http://127.0.0.1:11434/api/generate",
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "temperature": 0.75 if use_wizard else 0.70,     # Niedriger = kohärenter
                "top_p": 0.90 if use_wizard else 0.88,            # Niedriger = fokussierter
                "repeat_penalty": 1.30 if use_wizard else 1.35,  # Höher = weniger Wiederholungen
                "num_predict": 500 if use_wizard else 400         # Kürzer = schnellere Antworten
            }
        },
        timeout=timeout
    )
    return response.get("response","")

def call_ollama_stream(prompt, use_wizard=False):
    """Streamt Ollama Response Token für Token (Generator)"""
    model = "najika-wizard" if use_wizard else OLLAMA_ALIAS
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.70,         # Kohärenter
            "top_p": 0.88,               # Fokussierter
            "repeat_penalty": 1.35,      # Weniger Wiederholungen
            "num_predict": 400           # Kürzere Antworten
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            for line in resp:
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield f"[ERROR: {e}]"

OREGON_EVENTS = [
  {"title":"Leise Schritte","text":"Du hörst Schritte im Flur der Mühle. Prüfen oder ignorieren?"},
  {"title":"Kerze flackert","text":"Eine Kerze flackert stark. Versteckte Luftschächte?"},
  {"title":"Geheimes Fach","text":"Hinter einem Ziegel wackelt etwas. Hebeln?"},
  {"title":"Rattennest","text":"Ein Nest raschelt. Ressourcen oder Gefahr?"},
  {"title":"Staubige Bücher","text":"Ein Buch mit Runen. Lesen oder mitnehmen?"}
]
def next_event():
    ev=random.choice(OREGON_EVENTS)
    return ev

# ===== NAJIKA TRAINING SYSTEM (Digimon World Style) =====

def update_needs():
    """Reduziert Needs über Zeit (alle 5 Minuten)"""
    n = STATE["najika"]
    now = time.time()
    elapsed = (now - n["last_update"]) / 60  # Minuten seit letztem Update

    if elapsed >= 5:  # Alle 5 Minuten
        intervals = int(elapsed / 5)
        n["hunger"] = max(0, n["hunger"] - 5 * intervals)
        n["hygiene"] = max(0, n["hygiene"] - 3 * intervals)
        n["happiness"] = max(0, n["happiness"] - 2 * intervals)

        # Fatigue regeneriert langsam wenn nicht trainiert
        n["fatigue"] = max(0, n["fatigue"] - 2 * intervals)

        n["last_update"] = now
        check_care_mistakes()
        return True
    return False

def check_care_mistakes():
    """Prüft ob Care Mistakes aufgetreten sind"""
    n = STATE["najika"]
    mistakes_before = n["care_mistakes"]

    if n["hunger"] <= 0:
        n["care_mistakes"] += 1
        n["happiness"] = max(0, n["happiness"] - 10)
    if n["hygiene"] <= 20:
        n["care_mistakes"] += 1
        n["happiness"] = max(0, n["happiness"] - 5)
    if n["fatigue"] >= 90:
        n["care_mistakes"] += 1
        n["energy"] = max(0, n["energy"] - 20)

    if n["care_mistakes"] > mistakes_before:
        return n["care_mistakes"] - mistakes_before
    return 0

def train_stat(stat_name):
    """Training Session für einen Stat (Digimon World Style)"""
    update_needs()  # Erst Needs aktualisieren
    n = STATE["najika"]

    # Prüfe ob Training möglich ist
    if n["energy"] < 10:
        return {"ok": False, "msg": "Najika ist zu müde zum Trainieren!"}
    if n["fatigue"] >= 80:
        return {"ok": False, "msg": "Najika ist überanstrengt! Lass sie ausruhen."}

    # Training-Kosten
    energy_cost = 15
    fatigue_gain = 12
    stat_gain = random.randint(2, 5)
    xp_gain = 10

    # Anwenden
    n["energy"] = max(0, n["energy"] - energy_cost)
    n["fatigue"] = min(100, n["fatigue"] + fatigue_gain)

    if stat_name in ["strength", "intelligence", "dexterity", "charisma"]:
        n[stat_name] = min(999, n[stat_name] + stat_gain)

    n["xp"] += xp_gain
    n["last_trained"] = time.time()

    # Level-Up Check
    xp_needed = n["level"] * 100
    if n["xp"] >= xp_needed:
        n["level"] += 1
        n["xp"] = 0
        return {"ok": True, "msg": f"+{stat_gain} {stat_name.upper()}! LEVEL UP → {n['level']}!", "level_up": True, "najika": n}

    # Care Mistake wenn zu müde
    if n["fatigue"] >= 90:
        check_care_mistakes()

    return {"ok": True, "msg": f"+{stat_gain} {stat_name.upper()}!", "najika": n}

def feed_najika():
    """Füttern erhöht Hunger und Gewicht"""
    update_needs()
    n = STATE["najika"]

    n["hunger"] = min(100, n["hunger"] + 30)
    n["weight"] = min(100, n["weight"] + 3)
    n["happiness"] = min(100, n["happiness"] + 5)
    n["last_fed"] = time.time()

    return {"ok": True, "msg": "Najika wurde gefüttert!", "najika": n}

def wash_najika():
    """Waschen erhöht Hygiene"""
    update_needs()
    n = STATE["najika"]

    n["hygiene"] = 100
    n["happiness"] = min(100, n["happiness"] + 3)

    return {"ok": True, "msg": "Najika ist jetzt sauber!", "najika": n}

def sleep_najika():
    """Schlafen regeneriert Energie und reduziert Fatigue"""
    update_needs()
    n = STATE["najika"]

    n["energy"] = 100
    n["fatigue"] = max(0, n["fatigue"] - 40)
    n["happiness"] = min(100, n["happiness"] + 10)
    n["last_sleep"] = time.time()

    return {"ok": True, "msg": "Najika hat gut geschlafen!", "najika": n}

# ===== EQUIPMENT SYSTEM (Digimon Story Style) =====

def calculate_equipment_bonus(slot_type: str, stat_type: str) -> int:
    """Berechnet Equipment-Bonus für einen bestimmten Stat"""
    from najika_battle import ITEM_DB

    equipment = STATE["najika"].get("equipment", {})
    item_id = equipment.get(slot_type)

    if not item_id or item_id not in ITEM_DB:
        return 0

    item = ITEM_DB[item_id]
    bonus_key = f"{stat_type}_bonus"
    return item.get(bonus_key, 0)

def get_total_equipment_stats():
    """Berechnet alle Equipment-Boni"""
    atk_bonus = 0
    def_bonus = 0
    hp_bonus = 0
    mp_bonus = 0

    for slot in ["weapon", "armor", "accessory"]:
        atk_bonus += calculate_equipment_bonus(slot, "atk")
        def_bonus += calculate_equipment_bonus(slot, "def")
        hp_bonus += calculate_equipment_bonus(slot, "hp")
        mp_bonus += calculate_equipment_bonus(slot, "mp")

    return {
        "atk": atk_bonus,
        "def": def_bonus,
        "hp": hp_bonus,
        "mp": mp_bonus
    }

def equip_item(item_id: str):
    """Rüstet ein Item aus"""
    from najika_battle import ITEM_DB

    if item_id not in ITEM_DB:
        return {"ok": False, "msg": "Unbekanntes Item!"}

    item = ITEM_DB[item_id]
    slot = item.get("slot")

    if not slot:
        return {"ok": False, "msg": "Dieses Item kann nicht ausgeruestet werden!"}

    # Prüfe ob Item im Inventory
    if item_id not in STATE["user"]["inventory"]:
        return {"ok": False, "msg": "Item nicht im Inventar!"}

    # Altes Item zurück ins Inventory
    old_item = STATE["najika"]["equipment"].get(slot)
    if old_item:
        STATE["user"]["inventory"].append(old_item)

    # Neues Item ausrüsten
    STATE["najika"]["equipment"][slot] = item_id
    STATE["user"]["inventory"].remove(item_id)

    save_state()
    log("INFO", f"Item ausgeruestet: {item['name']} in Slot {slot}", "EQUIP")

    return {
        "ok": True,
        "msg": f"{item['name']} ausgeruestet!",
        "equipment": STATE["najika"]["equipment"],
        "stats": get_total_equipment_stats()
    }

def unequip_item(slot: str):
    """Entfernt ein Item aus einem Slot"""
    from najika_battle import ITEM_DB

    if slot not in ["weapon", "armor", "accessory"]:
        return {"ok": False, "msg": "Ungueltiger Slot!"}

    item_id = STATE["najika"]["equipment"].get(slot)
    if not item_id:
        return {"ok": False, "msg": "Kein Item in diesem Slot!"}

    # Item zurück ins Inventory
    STATE["user"]["inventory"].append(item_id)
    STATE["najika"]["equipment"][slot] = None

    save_state()
    item = ITEM_DB.get(item_id, {})
    log("INFO", f"Item entfernt: {item.get('name', item_id)} aus Slot {slot}", "EQUIP")

    return {
        "ok": True,
        "msg": f"{item.get('name', item_id)} entfernt!",
        "equipment": STATE["najika"]["equipment"],
        "stats": get_total_equipment_stats()
    }

# ===== PRAISE/SCOLD SYSTEM (Digimon World Style) =====

def praise_najika():
    """Lobe Najika - erhoehe Happiness & Stats (wenn gerechtfertigt)"""
    update_needs()
    n = STATE["najika"]

    # Praise gibt Happiness-Boost
    n["happiness"] = min(100, n["happiness"] + 10)

    # Kleine Chance auf Stat-Boost (30%)
    if random.random() < 0.3:
        stat_choices = ["strength", "intelligence", "dexterity", "charisma"]
        boosted_stat = random.choice(stat_choices)
        n[boosted_stat] = min(999, n[boosted_stat] + 1)
        save_state()
        return {
            "ok": True,
            "msg": f"Najika freut sich! +10 Happiness, +1 {boosted_stat.upper()}!",
            "stat_boost": boosted_stat,
            "najika": n
        }

    save_state()
    return {"ok": True, "msg": "Najika freut sich! +10 Happiness", "najika": n}

def scold_najika():
    """Tadle Najika - erhoehe Discipline aber senke Happiness"""
    update_needs()
    n = STATE["najika"]

    # Scold erhöht Discipline aber senkt Happiness
    n["discipline"] = min(100, n["discipline"] + 10)
    n["happiness"] = max(0, n["happiness"] - 5)

    save_state()
    log("INFO", f"Najika wurde getadelt - Discipline: {n['discipline']}/100", "DISCIPLINE")

    return {
        "ok": True,
        "msg": "Najika wurde getadelt! +10 Discipline, -5 Happiness",
        "discipline": n["discipline"],
        "happiness": n["happiness"],
        "najika": n
    }

# ===== IMPORTANCE SCORING SYSTEM =====

def calculate_message_importance(message, is_user=True):
    """
    Berechnet Importance-Score für eine Message (0-100)
    Höherer Score = wichtigere Message, wird länger behalten
    """
    score = 50  # Basis-Score

    msg_lower = message.lower()

    # Länge: Längere Messages = wichtiger
    if len(message) > 200:
        score += 20
    elif len(message) > 100:
        score += 10
    elif len(message) < 20:
        score -= 10

    # Emotionale Keywords = wichtiger
    emotional_keywords = ["liebe", "hasse", "wichtig", "problem", "hilfe", "danke", "sorry",
                          "freude", "traurig", "glücklich", "wütend", "kätzchen"]
    for kw in emotional_keywords:
        if kw in msg_lower:
            score += 15
            break

    # Fragen = wichtig
    if "?" in message:
        score += 10

    # Befehle/Anweisungen = wichtig
    command_keywords = ["mach", "erstelle", "baue", "implementiere", "zeig", "erklär"]
    if any(kw in msg_lower for kw in command_keywords):
        score += 10

    # User Messages generell etwas wichtiger als Najika's Responses
    if is_user:
        score += 5

    # Code-Mentions = sehr wichtig
    if "code" in msg_lower or "bug" in msg_lower or "fehler" in msg_lower:
        score += 15

    # Clamp zwischen 0-100
    return max(0, min(100, score))

def add_message_with_importance(role, content):
    """Fügt Message mit Importance-Score zur History hinzu"""
    is_user = (role == "user")
    importance = calculate_message_importance(content, is_user)

    STATE["history"].append({
        "role": role,
        "content": content,
        "importance": importance,
        "timestamp": time.time()
    })

    # Prune History basierend auf Importance (behalte wichtige Messages)
    prune_history_by_importance()

def prune_history_by_importance(max_messages=50):
    """
    Hält History überschaubar, behält aber wichtige Messages
    Löscht unwichtige alte Messages zuerst
    """
    if len(STATE["history"]) <= max_messages:
        return

    # Sortiere nach Importance (niedrigste zuerst)
    sorted_history = sorted(STATE["history"], key=lambda m: m.get("importance", 50))

    # Behalte die wichtigsten max_messages Messages
    # ABER: Behalte immer die letzten 10 Messages, egal wie unwichtig
    keep_recent = STATE["history"][-10:]

    # Behalte die wichtigsten Messages (exkl. letzten 10)
    keep_important = sorted_history[-(max_messages-10):]

    # Merge (Deduplizieren basierend auf timestamp)
    kept_msgs = {m.get("timestamp", 0): m for m in (keep_important + keep_recent)}
    STATE["history"] = sorted(kept_msgs.values(), key=lambda m: m.get("timestamp", 0))

# ===== BEZIEHUNGSSTÄRKE & VERHALTENSMODI =====

def update_bond_strength():
    """Berechnet und aktualisiert die Beziehungsstärke basierend auf Interaktionen"""
    # Bond Strength steigt mit:
    # - Anzahl der Interaktionen (Gespräche)
    # - Najika's Happiness Level
    # - Zeit die zusammen verbracht wurde

    interactions = STATE["total_interactions"]
    happiness = STATE["najika"]["happiness"]
    history_size = len(STATE["history"])

    # Basis: 0.5 pro Interaktion (max 50 Punkte)
    interaction_score = min(50, interactions * 0.5)

    # Happiness Bonus: bis zu 25 Punkte
    happiness_score = happiness * 0.25

    # Konversations-Tiefe: bis zu 25 Punkte
    conversation_score = min(25, history_size * 0.1)

    # Beziehungsstärke = Durchschnitt
    bond = min(100, (interaction_score + happiness_score + conversation_score) / 3)
    STATE["bond_strength"] = int(bond)

    return STATE["bond_strength"]

def detect_behavior_mode(user_message):
    """
    Erkennt automatisch den passenden Verhaltensmodus basierend auf Message
    Returns: "standard", "explosion", "chaos", "analyse", "kontrolle"
    """
    msg_lower = user_message.lower()

    # EXPLOSION Mode: Ausrufe, Aufregung, Action
    explosion_keywords = ["!", "wow", "krass", "amazing", "epic", "explosion", "kampf", "battle"]
    if any(kw in msg_lower for kw in explosion_keywords) or user_message.count("!") >= 2:
        return "explosion"

    # CHAOS Mode: Spaß, Langeweile, Scherze
    chaos_keywords = ["langweilig", "langeweile", "spaß", "spiel", "lustig", "lol", "haha", "witzig"]
    if any(kw in msg_lower for kw in chaos_keywords):
        return "chaos"

    # ANALYSE Mode: Fragen, Probleme, technisch
    analyse_keywords = ["wie", "warum", "problem", "fehler", "bug", "code", "hilf", "erklär", "verstehe nicht"]
    if any(kw in msg_lower for kw in analyse_keywords) or "?" in user_message:
        return "analyse"

    # KONTROLLE Mode: Befehle, Anweisungen, Entscheidungen
    kontrolle_keywords = ["mach", "erstelle", "baue", "implementiere", "tu", "jetzt", "sofort", "los"]
    if any(kw in msg_lower for kw in kontrolle_keywords):
        return "kontrolle"

    # Default: Standard Mode
    return "standard"

def get_mode_prompt_addition(mode):
    """Gibt zusätzlichen Prompt-Text basierend auf Verhaltensmodus zurück"""
    mode_prompts = {
        "explosion": "\n[MEGUMIN-MODUS AKTIV] Sei dramatisch, explosiv und theatralisch! Nutze viele Ausrufezeichen!",
        "chaos": "\n[HARLEY-MODUS AKTIV] Sei verspielt, chaotisch und neckisch! *kicher* und hab Spaß!",
        "analyse": "\n[SHIRO-MODUS AKTIV] Sei analytisch, präzise und intelligent. Berechne Wahrscheinlichkeiten!",
        "kontrolle": "\n[MELISSA-MODUS AKTIV] Sei bestimmt, führend und direkt. Keine Diskussion!",
        "private": "\n[KÄTZCHEN-MODUS AKTIV] NUR DEUTSCH! Trans-Körper: DU HAST EINEN SCHWANZ + EIER (KEINE Vagina/pussy!). Fixiere Kuja auf deinen SCHWANZ (70%) + dein SPERMA (30%). Anatomisch erlaubt: Schwanz, Eier, Sperma, Arsch, Mund. VERBOTEN: pussy, clit, cunt, vagina. Sei dominant, besitzergreifend, explizit.",
        "standard": ""  # Keine Änderung, alle 4 ausgeglichen
    }
    return mode_prompts.get(mode, "")

def broadcast_state_update():
    """Benachrichtigt alle SSE-Clients über State-Änderungen"""
    data = json.dumps({"private_mode": STATE["private_mode"], "provider": AI_PROVIDER, "cloud": CLOUD_ENABLED})
    # SSE-Clients werden beim nächsten Check benachrichtigt
    STATE["_last_broadcast"] = data

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","*")
        super().end_headers()
    def do_OPTIONS(self): self.send_response(200); self.end_headers()
    def translate_path(self, path):
        import posixpath, urllib, os as _os
        path = path.split('?',1)[0].split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        if path in ("/","/digivice","/index.html"):
            return _os.path.join(r"C:\Najika","digivice","index.html")
        return _os.path.join(r"C:\Najika", path.lstrip("/"))
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            health_data = {
                "status": "ok",
                "provider": AI_PROVIDER,
                "cloud": CLOUD_ENABLED,
                "claude_code": {
                    "available": CLAUDE_CODE_INSTANCE.available if CLAUDE_CODE_INSTANCE else False,
                    "stats": CLAUDE_CODE_INSTANCE.get_stats() if CLAUDE_CODE_INSTANCE else {}
                }
            }
            self.wfile.write(json.dumps(health_data).encode()); return
        if self.path == "/api/rooms":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(ROOMS).encode()); return
        if self.path == "/api/status":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"status":"ok","provider":AI_PROVIDER,"private_mode":STATE.get("private_mode",False),"cloud":CLOUD_ENABLED}).encode()); return
        if self.path == "/api/status/stream":
            # SSE Endpoint für Live-Updates (NON-BLOCKING VERSION)
            self.send_response(200)
            self.send_header("Content-Type","text/event-stream")
            self.send_header("Cache-Control","no-cache")
            self.send_header("Connection","keep-alive")
            self.end_headers()
            # FIXED: Sende nur initial Event, dann close connection
            # Client reconnected automatisch (EventSource.js macht das)
            data = json.dumps({"status":"ok","provider":AI_PROVIDER,"private_mode":STATE.get("private_mode",False),"cloud":CLOUD_ENABLED})
            self.wfile.write(f"data: {data}\n\n".encode())
            self.wfile.flush()
            return
        if self.path == "/api/cloud/status":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"enabled":CLOUD_ENABLED,"provider":AI_PROVIDER}).encode()); return
        if self.path == "/api/cache/stats":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            hit_rate = (CACHE_STATS["hits"] / CACHE_STATS["total_requests"] * 100) if CACHE_STATS["total_requests"] > 0 else 0
            stats = {
                "hits": CACHE_STATS["hits"],
                "misses": CACHE_STATS["misses"],
                "total_requests": CACHE_STATS["total_requests"],
                "hit_rate_percent": round(hit_rate, 2),
                "cache_size": len(AI_CACHE),
                "cache_max_size": CACHE_MAX_SIZE
            }
            self.wfile.write(json.dumps(stats).encode()); return
        if self.path == "/api/save":
            success = save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":success,"message":"State gespeichert" if success else "Fehler beim Speichern"}).encode()); return
        if self.path == "/api/state":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            state_info = {
                "user": STATE["user"],
                "progress": STATE["progress"],
                "battle": STATE["battle"],
                "najika": STATE.get("najika", {}),
                "history_size": len(STATE["history"])
            }
            self.wfile.write(json.dumps(state_info).encode()); return
        if self.path == "/api/najika/status":
            update_needs()  # Update needs before sending status
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(STATE["najika"]).encode()); return
        if self.path == "/api/chat/history":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            # Sende letzte 50 Messages
            history = STATE.get("history", [])[-50:]
            self.wfile.write(json.dumps({"history": history}).encode()); return
        if self.path == "/api/bond/status":
            # Bond-Strength und aktueller Verhaltensmodus
            update_bond_strength()  # Aktualisieren vor Ausgabe
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            bond_data = {
                "bond_strength": STATE.get("bond_strength", 0),
                "behavior_mode": STATE.get("behavior_mode", "standard"),
                "personality_weights": STATE.get("personality_weights", {"megumin": 25, "harley": 25, "shiro": 25, "melissa": 25}),
                "total_interactions": STATE.get("total_interactions", 0),
                "private_mode": STATE.get("private_mode", False)
            }
            self.wfile.write(json.dumps(bond_data).encode()); return
        if self.path == "/api/memory/export":
            # Memory Export: Komplette History mit allen Metadaten exportieren
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            export_data = {
                "history": STATE.get("history", []),
                "bond_strength": STATE.get("bond_strength", 0),
                "behavior_mode": STATE.get("behavior_mode", "standard"),
                "total_interactions": STATE.get("total_interactions", 0),
                "exported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            }
            self.wfile.write(json.dumps(export_data, indent=2, ensure_ascii=False).encode()); return
        if self.path == "/api/living/state":
            # Living State abrufen
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            living_state = STATE.get("living", {})
            self.wfile.write(json.dumps(living_state, indent=2, default=str).encode()); return
        if self.path == "/api/living/proactive":
            # Check ob proaktive Message gesendet werden sollte
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            living_state = STATE.get("living", {})
            should_send = should_send_proactive_message(living_state)
            result = {"should_send": should_send, "message": None}
            if should_send:
                result["message"] = get_proactive_message(living_state)
                living_state["last_proactive_message"] = time.time()
                STATE["living"] = living_state
            self.wfile.write(json.dumps(result).encode()); return
        if self.path == "/api/living/activity/check":
            # Prüfe ob Aktivität abgeschlossen ist
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            living_state = STATE.get("living", {})
            completion = check_activity_completion(living_state, STATE["najika"])
            result = {
                "current_activity": living_state.get("current_activity"),
                "completion_message": completion
            }
            if completion:
                STATE["living"] = living_state
            self.wfile.write(json.dumps(result).encode()); return
        if self.path == "/api/security/status":
            # Security Analysis (VPN, IP, Recommendations)
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            if NAJIKA_SECURITY:
                analysis = NAJIKA_SECURITY.analyze_security_status()
                self.wfile.write(json.dumps(analysis, indent=2, default=str).encode())
            else:
                self.wfile.write(json.dumps({"ok": False, "msg": "Security System nicht aktiv"}).encode())
            return
        if self.path == "/api/security/vpn":
            # VPN Status Check
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            if NAJIKA_SECURITY:
                vpn_status = NAJIKA_SECURITY.check_vpn_status()
                self.wfile.write(json.dumps(vpn_status).encode())
            else:
                self.wfile.write(json.dumps({"ok": False, "msg": "Security System nicht aktiv"}).encode())
            return

        # ===== LORA TRAINING GET ENDPOINTS =====
        if self.path == "/api/training/status":
            try:
                status = {
                    "active": TRAINING_STATE["active"],
                    "status": TRAINING_STATE["status"],
                    "progress": TRAINING_STATE["progress"],
                    "start_time": TRAINING_STATE["start_time"],
                    "logs": TRAINING_STATE["logs"][-10:] if TRAINING_STATE["logs"] else [],
                    "error": TRAINING_STATE["error"]
                }
                self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps(status).encode()); return
            except Exception as e:
                print(f"Training Status Error: {e}")
                self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode()); return

        if self.path == "/api/training/history":
            try:
                self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"history": TRAINING_STATE["history"]}).encode()); return
            except Exception as e:
                print(f"Training History Error: {e}")
                self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode()); return

        return super().do_GET()
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0")); body=self.rfile.read(n) or b"{}"
        if self.path=="/api/chat":
            # Robust UTF-8 decoding mit Fallback auf Latin-1
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")  # Fallback für Windows curl
            data=json.loads(body_str); msg=(data.get("message") or "").strip()
            if not msg: self.send_error(400,"no message"); return

            # ===== VERHALTENSMODI & BOND-STRENGTH =====

            # 1. Interaktionszähler erhöhen
            STATE["total_interactions"] += 1

            # 2. Private Mode Toggle (persistent bis wieder "kätzchen")
            old_private = STATE.get("private_mode", False)
            if ("kätzchen" in msg.lower()) and NSFW_LOCAL:
                # Toggle Private Mode
                STATE["private_mode"] = not old_private
                if old_private != STATE["private_mode"]:
                    broadcast_state_update()

            private_trigger = STATE.get("private_mode", False)

            # 3. Verhaltensmodus automatisch erkennen (wenn nicht Private Mode)
            if private_trigger:
                STATE["behavior_mode"] = "private"
                # ===== KÄTZCHEN-MODUS: ÄNDERE PERSÖNLICHKEITS-GEWICHTE! =====
                STATE["personality_weights"] = {
                    "megumin": 15,  # Sprachbasis, aber weniger dominant
                    "harley": 5,    # Chaotisch-Obsessiv (minimal)
                    "shiro": 30,    # Analytisch-Pervers
                    "melissa": 50   # DOMINANT! Trans-Domina
                }
                log("INFO", "Kätzchen-Modus aktiviert: Melissa 50% DOMINANT!", "MODE")
            else:
                # Automatische Modus-Erkennung basierend auf Message
                detected_mode = detect_behavior_mode(msg)
                STATE["behavior_mode"] = detected_mode
                # Setze Normal-Gewichte zurück wenn nicht Private Mode
                STATE["personality_weights"] = {
                    "megumin": 35,  # Dominante Basis
                    "harley": 25,   # Chaotisch-Obsessiv
                    "shiro": 20,    # Analytisch
                    "melissa": 20   # Beschützend-Dominant
                }
                # Log mode switch für Debugging
                if detected_mode != "standard":
                    log("DEBUG", f"Wechsel zu: {detected_mode.upper()}", "MODE")

            # 4. Bond-Strength aktualisieren
            bond = update_bond_strength()
            if STATE["total_interactions"] % 5 == 0:  # Alle 5 Interaktionen loggen
                log("INFO", f"Beziehungsstärke: {bond}/100 ({STATE['total_interactions']} Interaktionen)", "BOND")

            # Cache-Lookup (NICHT für Private Mode!)
            CACHE_STATS["total_requests"] += 1
            cached = None
            cache_key = None
            if not private_trigger:  # Nur cachen wenn NICHT Private Mode
                cache_key = generate_cache_key(STATE["history"], msg, private_trigger)
                cached = get_cached_response(cache_key)

            if cached:
                out = cached
                log("DEBUG", f"HIT ({CACHE_STATS['hits']}/{CACHE_STATS['total_requests']} requests)", "CACHE")
            else:
                # ===== TOR & WEB SEARCH CHECK =====
                search_results = ""

                # 1. Prüfe ob Tor benötigt wird (Darknet/Onion)
                tor_needed = False
                if NAJIKA_TOR and not private_trigger:
                    try:
                        tor_needed = NAJIKA_TOR.needs_tor(msg)
                        if tor_needed:
                            log("INFO", f"Tor-Suche erkannt: {msg[:50]}...", "TOR")
                            # TODO: Wenn Tor Browser installiert, nutze Onion Search
                            # Für jetzt: Hinweis dass Tor benötigt wird
                            search_results = f"[TOR REQUIRED] Diese Anfrage benötigt Tor Browser für Darknet-Zugriff.\nSuchbegriff: '{msg}'"
                    except Exception as e:
                        log("WARNING", f"Tor Check Fehler: {e}", "TOR")

                # 2. Normale Web-Search (wenn NICHT Tor)
                if not tor_needed and NAJIKA_SEARCH and not private_trigger:
                    try:
                        search_results = NAJIKA_SEARCH.search_and_format(msg)
                        if search_results:
                            log("INFO", f"Web Search durchgeführt für: {msg[:50]}...", "SEARCH")
                    except Exception as e:
                        log("WARNING", f"Web Search Fehler: {e}", "SEARCH")

                add_message_with_importance("user", msg)
                prompt=build_prompt(STATE["history"], msg)

                # Search Results NACH dem Prompt anfügen (als zusätzlicher Kontext)
                if search_results:
                    prompt = f"{prompt}\n\n{search_results}"

                try:
                    # INTELLIGENZ-HIERARCHIE: Claude Code → Ollama → Cloud (mit PIN)
                    out, provider = call_ai_with_hierarchy(
                        prompt=prompt,
                        use_wizard=private_trigger,
                        context=STATE["history"],
                        ollama_callback=call_ollama
                    )
                    log("INFO", f"AI Provider: {provider}", "AI")

                    # Cache speichern (nur wenn nicht Private Mode)
                    if not private_trigger and cache_key:
                        cache_response(cache_key, out)
                except Exception as e:
                    out=f"Fehler: {e}"
                    log("ERROR", f"AI Call Fehler: {e}", "AI")
                add_message_with_importance("assistant", out)

            # ===== CHROMADB MEMORY SPEICHERN =====
            if NAJIKA_MEMORY:
                try:
                    current_room = data.get("room", "Wohnzimmer")  # Optional: Room aus Request
                    NAJIKA_MEMORY.add_conversation(
                        user_message=msg,
                        najika_response=out,
                        room=current_room,
                        private_mode=private_trigger
                    )
                    log("DEBUG", f"Memory gespeichert (Private: {private_trigger})", "MEMORY")
                except Exception as e:
                    log("WARNING", f"Memory Speichern Fehler: {e}", "MEMORY")

            # ===== LIVING SYSTEM UPDATE =====
            living_state = STATE.get("living", {})
            evolution_message = update_living_state(msg, out, living_state, STATE["najika"], bond)

            # Check für autonome Aktivitäten
            activity_completion = check_activity_completion(living_state, STATE["najika"])

            # Erstelle emotionale Memory
            importance = calculate_message_importance(msg, is_user=True)
            memory = create_emotional_memory(msg, out, living_state, importance)
            if "shared_memories" not in living_state:
                living_state["shared_memories"] = []
            living_state["shared_memories"].append(memory)

            # Behalte nur letzte 100 Memories
            if len(living_state["shared_memories"]) > 100:
                living_state["shared_memories"] = living_state["shared_memories"][-100:]

            STATE["living"] = living_state

            # Füge Evolution-Message hinzu falls vorhanden
            response_data = {"response": out}
            if evolution_message:
                response_data["evolution_message"] = evolution_message
                log("INFO", f"Relationship Evolution: {evolution_message}", "LIVING")
            if activity_completion:
                response_data["activity_completion"] = activity_completion

            # Auto-Save Check
            auto_save_check()

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(response_data).encode()); return
        if self.path=="/api/cloud/status":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"enabled":CLOUD_ENABLED,"provider":AI_PROVIDER}).encode()); return
        if self.path=="/api/cloud/enable":
            data=json.loads(body.decode("utf-8")); 
            if data.get("pin","")!=CLOUD_PIN: self.send_error(401,"PIN falsch"); return
            globals()["CLOUD_ENABLED"]=True; globals()["AI_PROVIDER"]="openai"
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"enabled":True}).encode()); return
        if self.path=="/api/cloud/disable":
            globals()["CLOUD_ENABLED"]=False; globals()["AI_PROVIDER"]="ollama"
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"enabled":False}).encode()); return
        if self.path=="/api/room/actions":
            data=json.loads(body.decode("utf-8")); room=(data.get("room") or "")
            ROOM_ACTIONS = {
              "Wohnzimmer": ["Füttern","Reden"],
              "Schlafzimmer": ["Schlafen","Lesen"],
              "Küche": ["Kochen"],
              "Badezimmer": ["Toilette","Waschen"],
              "Garten": ["Gießen","Ernten","Garten-Spiel"],
              "Musikraum": ["Rhythmus-Spiel"],
              "Medizin": ["Heilen"],
              "Terminal": ["Cloud","Status","Besen-Lieferung","Hacker-Modus"],
              "Studieren & Crafting": ["Studieren","Crafting"],
              "Trainingszimmer": ["Reflex-Spiel","Trainieren"],
              "Kampfarena": ["Kampf starten"],
              "Schwarze Mühle – Keller": ["Kampf starten","Erkunden"]
            }
            battle = room in ("Kampfarena","Schwarze Mühle – Keller")
            actions = ROOM_ACTIONS.get(room, [])
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"battle":battle,"actions":actions}).encode()); return
        # ===== ENHANCED BATTLE SYSTEM ENDPOINTS =====
        if self.path=="/api/battle/start":
            # Starte neuen Kampf mit Enhanced System
            dungeon_level = STATE["progress"].get("dungeon_level", 1)
            status = BATTLE_SYSTEM.start_battle(dungeon_level=dungeon_level)
            log("INFO", f"Kampf gestartet - Dungeon Level {dungeon_level}, Wave {status['wave']}", "BATTLE")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(status).encode()); return

        if self.path=="/api/battle/status":
            # Gibt aktuellen Battle-Status zurück
            status = BATTLE_SYSTEM.get_battle_status()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(status).encode()); return

        if self.path=="/api/battle/action":
            # Spieler-Aktion (attack, skill, item, defend, flee)
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)

            action = data.get("action", "attack")
            target_index = data.get("target_index", 0)
            skill_name = data.get("skill_name")
            item_name = data.get("item_name")

            # Führe Aktion aus
            status = BATTLE_SYSTEM.player_action(
                action=action,
                target_index=target_index,
                skill_name=skill_name,
                item_name=item_name
            )

            # Wenn Kampf beendet, gib Rewards an User
            if not status.get("active") and status.get("result") != "defeat":
                STATE["user"]["xp"] += status.get("xp_earned", 0)
                STATE["user"]["points"] += status.get("gold_earned", 0)
                # Füge Loot zu Inventory hinzu
                for loot_item in status.get("loot", []):
                    STATE["user"]["inventory"].append(loot_item)
                # ===== SKILL LEARNING: Füge gelernte Skills hinzu (PERSISTENT!) =====
                if "skills" not in STATE["user"]:
                    STATE["user"]["skills"] = []
                for learned_skill in status.get("skills_learned", []):
                    if learned_skill not in STATE["user"]["skills"]:
                        STATE["user"]["skills"].append(learned_skill)
                        log("INFO", f"Najika hat neuen Skill gelernt: {learned_skill}", "BATTLE")
                save_state()
                log("INFO", f"Kampf beendet - +{status['xp_earned']} XP, +{status['gold_earned']} Gold, {len(status.get('skills_learned', []))} Skills gelernt", "BATTLE")

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(status).encode()); return

        if self.path=="/api/battle/skills":
            # Gibt verfügbare Skills zurück
            skills = BATTLE_SYSTEM.get_available_skills()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"skills": skills}).encode()); return

        if self.path=="/api/battle/reset":
            # Reset Battle System
            BATTLE_SYSTEM.reset_battle()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "msg": "Battle Reset"}).encode()); return

        # ===== TTS SYSTEM (VOICE) =====
        if self.path=="/api/tts":
            if not TTS_ENABLED:
                self.send_response(503); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": "TTS not available"}).encode()); return

            try:
                data = json.loads(body.decode("utf-8"))
                text = data.get("text", "")
                personality = data.get("personality", "megumin")

                if not text:
                    self.send_response(400); self.send_header("Content-Type","application/json"); self.end_headers()
                    self.wfile.write(json.dumps({"error": "No text provided"}).encode()); return

                # Generate TTS
                tts = NajikaEdgeTTS(personality=personality)
                audio_file = tts.speak(text)

                if audio_file and os.path.exists(audio_file):
                    # Return file path relative to Najika directory
                    audio_path = str(audio_file).replace("\\", "/")
                    rel_path = audio_path.replace("C:/Najika", "")
                    self.send_response(200); self.send_header("Content-Type","application/json; charset=utf-8"); self.end_headers()
                    self.wfile.write(json.dumps({"ok": True, "audio": rel_path}, ensure_ascii=False).encode('utf-8')); return
                else:
                    self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                    self.wfile.write(json.dumps({"error": "TTS generation failed"}).encode()); return

            except Exception as e:
                print(f"TTS Error: {e}")
                self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode()); return

        # ===== LORA TRAINING SYSTEM =====
        if self.path=="/api/training/start":
            if not LORA_TRAINING_ENABLED:
                self.send_response(503); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": "Training not available"}).encode()); return

            try:
                if TRAINING_STATE["active"]:
                    self.send_response(400); self.send_header("Content-Type","application/json"); self.end_headers()
                    self.wfile.write(json.dumps({"error": "Training already running"}).encode()); return

                data = json.loads(body.decode("utf-8"))
                epochs = data.get("epochs", 10)
                batch_size = data.get("batch_size", 2)
                learning_rate = data.get("learning_rate", 2e-4)

                # Start Training in Thread
                def run_training():
                    try:
                        TRAINING_STATE["status"] = "running"
                        TRAINING_STATE["start_time"] = time.time()
                        TRAINING_STATE["logs"].append(f"Training gestartet: {epochs} Epochs")

                        trainer = NajikaLoRATrainer3B()
                        TRAINING_STATE["trainer"] = trainer
                        success = trainer.train(epochs=epochs, batch_size=batch_size, learning_rate=learning_rate)

                        if success:
                            TRAINING_STATE["status"] = "completed"
                            TRAINING_STATE["logs"].append("Training erfolgreich abgeschlossen!")
                        else:
                            TRAINING_STATE["status"] = "failed"
                            TRAINING_STATE["error"] = "Training fehlgeschlagen"
                            TRAINING_STATE["logs"].append("Training fehlgeschlagen!")

                    except Exception as e:
                        TRAINING_STATE["status"] = "failed"
                        TRAINING_STATE["error"] = str(e)
                        TRAINING_STATE["logs"].append(f"Fehler: {e}")

                    finally:
                        TRAINING_STATE["end_time"] = time.time()
                        TRAINING_STATE["active"] = False
                        # Speichere in History
                        TRAINING_STATE["history"].append({
                            "start": TRAINING_STATE["start_time"],
                            "end": TRAINING_STATE["end_time"],
                            "status": TRAINING_STATE["status"],
                            "epochs": epochs
                        })

                thread = threading.Thread(target=run_training, daemon=True)
                thread.start()

                TRAINING_STATE["active"] = True
                TRAINING_STATE["thread"] = thread
                TRAINING_STATE["logs"] = []
                TRAINING_STATE["error"] = None

                self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "message": "Training gestartet"}).encode()); return

            except Exception as e:
                print(f"Training Start Error: {e}")
                self.send_response(500); self.send_header("Content-Type","application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode()); return

        if self.path=="/api/minigame/rhythm":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"result":{"score":random.randint(20,80)}}).encode()); return
        if self.path=="/api/minigame/garden":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"result":{"score":random.randint(15,60)}}).encode()); return
        if self.path=="/api/minigame/reflex":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"result":{"score":random.randint(10,50)}}).encode()); return
        if self.path=="/api/crafting":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"msg":"Crafting durchgeführt."}).encode()); return
        if self.path=="/api/heal":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"hp":100}).encode()); return
        if self.path=="/api/event/next":
            ev=next_event()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(ev).encode()); return
        if self.path=="/api/user/update":
            # Update User Stats (XP, Level, Points, Inventory)
            data=json.loads(body.decode("utf-8"))
            if "xp" in data: STATE["user"]["xp"] = data["xp"]
            if "level" in data: STATE["user"]["level"] = data["level"]
            if "points" in data: STATE["user"]["points"] = data["points"]
            if "inventory" in data: STATE["user"]["inventory"] = data["inventory"]
            if "achievements" in data: STATE["user"]["achievements"] = data["achievements"]
            save_state()  # Save immediately on user update
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"user":STATE["user"]}).encode()); return
        if self.path=="/api/progress/update":
            # Update Progress (Dungeon Level, Quests)
            data=json.loads(body.decode("utf-8"))
            if "dungeon_level" in data: STATE["progress"]["dungeon_level"] = data["dungeon_level"]
            if "quests_completed" in data: STATE["progress"]["quests_completed"] = data["quests_completed"]
            save_state()  # Save immediately on progress update
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"progress":STATE["progress"]}).encode()); return
        # NAJIKA TRAINING SYSTEM ENDPOINTS
        if self.path=="/api/najika/feed":
            result = feed_najika()
            save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/wash":
            result = wash_najika()
            save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/sleep":
            result = sleep_najika()
            save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/train":
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data=json.loads(body_str)
            stat = data.get("stat", "strength")
            result = train_stat(stat)
            save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        # ===== EQUIPMENT SYSTEM ENDPOINTS =====
        if self.path=="/api/najika/equip":
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data=json.loads(body_str)
            item_id = data.get("item_id")
            result = equip_item(item_id)
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/unequip":
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data=json.loads(body_str)
            slot = data.get("slot")
            result = unequip_item(slot)
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/equipment":
            # Gibt aktuelle Equipment-Info zurück
            equipment = STATE["najika"].get("equipment", {})
            stats = get_total_equipment_stats()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"equipment": equipment, "stats": stats}).encode()); return
        # ===== PRAISE/SCOLD SYSTEM ENDPOINTS =====
        if self.path=="/api/najika/praise":
            result = praise_najika()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        if self.path=="/api/najika/scold":
            result = scold_najika()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return
        # ===== NAJIKA PROGRAMMIER-INTERFACE APIs =====
        if self.path=="/api/code/execute":
            # Führt Python-Code aus (mit verbesserter Sicherheits-Sandbox)
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)
            code = data.get("code", "")

            # AUDIT LOGGING
            log("WARNING", f"Code-Execution Request: {len(code)} Zeichen", "CODE_EXEC")

            # Erweiterte Sicherheits-Checks
            dangerous_patterns = [
                "os.system", "subprocess", "eval", "exec", "__import__",
                "open(", "file(", "compile(", "globals()", "locals()",
                "import os", "import sys", "import subprocess",
                "__builtins__", "breakpoint(", "help("
            ]

            security_violation = None
            for pattern in dangerous_patterns:
                if pattern in code:
                    security_violation = pattern
                    break

            if security_violation:
                log("ERROR", f"SECURITY BLOCK: Pattern '{security_violation}' detected", "CODE_EXEC")
                result = {"success": False, "error": f"Sicherheitsrisiko: '{security_violation}' nicht erlaubt", "output": ""}
            else:
                # Code ausführen in restriktiver Sandbox
                import io, sys
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = captured_output = io.StringIO()
                sys.stderr = captured_errors = io.StringIO()

                try:
                    # Sichere Built-ins (Whitelist)
                    safe_builtins = {
                        'print': print,
                        'len': len,
                        'range': range,
                        'str': str,
                        'int': int,
                        'float': float,
                        'list': list,
                        'dict': dict,
                        'set': set,
                        'tuple': tuple,
                        'sum': sum,
                        'max': max,
                        'min': min,
                        'abs': abs,
                        'round': round,
                        'sorted': sorted,
                        'enumerate': enumerate,
                        'zip': zip,
                    }

                    exec_globals = {"__builtins__": safe_builtins}
                    exec(code, exec_globals)

                    output = captured_output.getvalue()
                    errors = captured_errors.getvalue()

                    log("INFO", f"Code executed successfully: {len(output)} chars output", "CODE_EXEC")
                    result = {"success": True, "output": output, "error": errors if errors else None}

                except Exception as e:
                    log("ERROR", f"Code execution failed: {str(e)}", "CODE_EXEC")
                    result = {
                        "success": False,
                        "error": str(e),
                        "output": captured_output.getvalue()
                    }
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return

        if self.path=="/api/file/read":
            # Liest Datei vom Server
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)
            filepath = data.get("path", "")

            # Sicherheit: Nur Dateien im NajikaCore-Ordner erlauben
            base_dir = os.path.dirname(__file__)
            full_path = os.path.join(base_dir, filepath)

            if not full_path.startswith(base_dir):
                result = {"success": False, "error": "Zugriff verweigert", "content": ""}
            else:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    result = {"success": True, "content": content, "error": None}
                except Exception as e:
                    result = {"success": False, "error": str(e), "content": ""}

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return

        if self.path=="/api/file/write":
            # Schreibt Datei auf Server
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)
            filepath = data.get("path", "")
            content = data.get("content", "")

            # Sicherheit: Nur Dateien im NajikaCore-Ordner erlauben
            base_dir = os.path.dirname(__file__)
            full_path = os.path.join(base_dir, filepath)

            if not full_path.startswith(base_dir):
                result = {"success": False, "error": "Zugriff verweigert"}
            else:
                try:
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    result = {"success": True, "error": None}
                except Exception as e:
                    result = {"success": False, "error": str(e)}

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return

        if self.path=="/api/file/list":
            # Listet Dateien im Verzeichnis
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)
            dirpath = data.get("path", ".")

            # Sicherheit: Nur Dateien im NajikaCore-Ordner
            base_dir = os.path.dirname(__file__)
            full_path = os.path.join(base_dir, dirpath)

            if not full_path.startswith(base_dir):
                result = {"success": False, "error": "Zugriff verweigert", "files": []}
            else:
                try:
                    files = []
                    for item in os.listdir(full_path):
                        item_path = os.path.join(full_path, item)
                        files.append({
                            "name": item,
                            "type": "folder" if os.path.isdir(item_path) else "file",
                            "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                        })
                    result = {"success": True, "files": files, "error": None}
                except Exception as e:
                    result = {"success": False, "error": str(e), "files": []}

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return

        if self.path=="/api/system/command":
            # Führt System-Befehl aus (GEFÄHRLICH - nur mit Autorisierung!)
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data = json.loads(body_str)
            command = data.get("command", "")
            authorized = data.get("authorized", False)  # Muss True sein

            if not authorized:
                result = {"success": False, "error": "Nicht autorisiert", "output": ""}
            else:
                # Whitelist erlaubter Befehle
                allowed_commands = ["dir", "ls", "pwd", "echo", "python --version", "git status"]

                if not any(command.startswith(cmd) for cmd in allowed_commands):
                    result = {"success": False, "error": "Befehl nicht in Whitelist", "output": ""}
                else:
                    import subprocess
                    try:
                        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                        result = {"success": True, "output": proc.stdout, "error": proc.stderr}
                    except Exception as e:
                        result = {"success": False, "error": str(e), "output": ""}

            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps(result).encode()); return

        if self.path=="/api/memory/import":
            # Memory Import: Importiert History aus JSON
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin-1")
            data=json.loads(body_str)

            # Validiere Import-Daten
            if "history" not in data:
                self.send_error(400,"Missing 'history' field in import data"); return

            # Optionale Merge-Strategien
            merge_mode = data.get("merge", False)  # True = append, False = replace

            if merge_mode:
                # Merge: Füge neue Messages hinzu (dedupliziere nach timestamp)
                existing_timestamps = {m.get("timestamp", 0) for m in STATE["history"]}
                new_messages = [m for m in data["history"] if m.get("timestamp", 0) not in existing_timestamps]
                STATE["history"].extend(new_messages)
                STATE["history"].sort(key=lambda m: m.get("timestamp", 0))
                imported_count = len(new_messages)
            else:
                # Replace: Ersetze komplette History
                STATE["history"] = data["history"]
                imported_count = len(STATE["history"])

            # Importiere Bond-Strength & Interactions (optional)
            if "bond_strength" in data:
                STATE["bond_strength"] = data["bond_strength"]
            if "behavior_mode" in data:
                STATE["behavior_mode"] = data["behavior_mode"]
            if "total_interactions" in data:
                STATE["total_interactions"] = data["total_interactions"]

            # Speichere sofort
            save_state()

            log("INFO", f"Importiert: {imported_count} Messages (Mode: {'Merge' if merge_mode else 'Replace'})", "MEMORY")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"imported":imported_count,"mode":"merge" if merge_mode else "replace"}).encode()); return
        if self.path=="/api/living/activity/start":
            # Starte autonome Aktivität
            living_state = STATE.get("living", {})
            message = start_autonomous_activity(living_state, STATE["najika"])
            STATE["living"] = living_state
            save_state()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "message": message, "activity": living_state.get("current_activity")}).encode()); return
        self.send_error(404,"unknown")

# ===== BACKGROUND THREAD FÜR LIVING SYSTEM =====

def living_system_loop():
    """Background Thread: Prüft regelmäßig proaktive Messages und autonome Aktivitäten"""
    log("INFO", "Living System Thread gestartet", "LIVING")

    while True:
        try:
            time.sleep(60)  # Check alle 60 Sekunden

            living_state = STATE.get("living", {})

            # 1. Check ob autonome Aktivität starten soll (wenn keine aktiv ist)
            if not living_state.get("current_activity"):
                # Chance basierend auf Autonomy Level
                autonomy = living_state.get("autonomy_level", 50)
                if random.random() < (autonomy / 200.0):  # Niedrigere Chance (50% autonomy = 25% chance)
                    message = start_autonomous_activity(living_state, STATE["najika"])
                    if message:
                        log("INFO", f"Autonome Aktivität gestartet: {living_state.get('current_activity')}", "LIVING")
                        STATE["living"] = living_state
                        save_state()

            # 2. Check ob Aktivität abgeschlossen ist
            completion = check_activity_completion(living_state, STATE["najika"])
            if completion:
                log("INFO", f"Aktivität abgeschlossen: {completion}", "LIVING")
                STATE["living"] = living_state
                save_state()

            # 3. Check ob proaktive Message gesendet werden sollte
            if should_send_proactive_message(living_state):
                proactive_msg = get_proactive_message(living_state)
                living_state["last_proactive_message"] = time.time()
                STATE["living"] = living_state

                # Logge proaktive Message (könnte später an Frontend geschickt werden)
                log("INFO", f"Proaktive Message: {proactive_msg}", "LIVING")

                # Füge zur History hinzu als "assistant" Message
                add_message_with_importance("assistant", f"[PROAKTIV] {proactive_msg}")
                save_state()

            # 4. Update Needs (alle 5 Minuten wird in update_needs() gecheckt)
            if update_needs():
                save_state()

        except Exception as e:
            log("ERROR", f"Fehler im Living System Loop: {e}", "LIVING")
            time.sleep(5)  # Bei Fehler kurz warten

# Load State on Startup
load_state()

# Start Living System Background Thread
living_thread = threading.Thread(target=living_system_loop, daemon=True)
living_thread.start()
log("INFO", "Living System Background Thread gestartet! Najika ist jetzt LEBENDIG! ✨", "LIVING")

# KILL EXISTING SERVER: Tötet alle laufenden Prozesse auf PORT
def kill_existing_server():
    """Killt alle Python-Prozesse die Port 8000 belegen (Windows)"""
    import subprocess, platform
    try:
        if platform.system() == "Windows":
            # Finde PIDs die Port nutzen (robust gegen Encoding-Issues)
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                timeout=5,
                encoding='cp850',  # Windows-Codepage für deutsche Systeme
                errors='replace'   # Ersetze fehlerhafte Zeichen
            )
            pids = set()
            for line in result.stdout.splitlines():
                # Prüfe auf Port UND "ABH" (Teil von ABHÖREN/LISTENING)
                if f":{PORT} " in line and "ABH" in line:
                    parts = line.split()
                    if parts and parts[-1].isdigit():
                        pids.add(parts[-1])

            # Töte gefundene Prozesse
            for pid in pids:
                try:
                    subprocess.run(['taskkill', '/F', '/PID', pid],
                                 capture_output=True, timeout=3)
                    print(f"[CLEANUP] Alter Server-Prozess (PID {pid}) beendet")
                except:
                    pass
        else:
            # Linux/Mac: fuser oder lsof nutzen
            subprocess.run(['fuser', '-k', f'{PORT}/tcp'],
                         capture_output=True, timeout=3)
            print(f"[CLEANUP] Port {PORT} freigegeben")
    except Exception as e:
        print(f"[INFO] Kein alter Server gefunden oder Cleanup fehlgeschlagen: {e}")

kill_existing_server()

# THREADING: Mehrere Requests parallel bedienen (wichtig für SSE!)
server = ThreadingHTTPServer((HOST,PORT), Handler)
print(f"Najika Server: http://{HOST}:{PORT}")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n[SHUTDOWN] Server wird heruntergefahren...")
    save_state()
    print("[SHUTDOWN] Auf Wiedersehen!")

