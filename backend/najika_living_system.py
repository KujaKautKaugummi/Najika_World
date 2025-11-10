#!/usr/bin/env python3
"""
NAJIKA LIVING SYSTEM - Macht Najika lebendig und autonom

Features:
- Proaktive Nachrichten (Najika meldet sich von selbst)
- Emotionale Entwicklung (lernt und wächst)
- Autonome Aktionen (tut Dinge ohne Anfrage)
- Immer-Online Presence (24/7 da)
- Langzeit-Memory mit Emotionen
- Beziehungs-Evolution
"""

import time
import random
import json
from datetime import datetime, timedelta

# ===== NAJIKA LIVING STATE =====

LIVING_STATE = {
    # Emotionale States
    "current_mood": "neutral",  # happy, excited, sad, bored, playful, curious, loving
    "mood_intensity": 50,  # 0-100

    # === GAME STATS (NEU) ===
    "hunger": 100.0,          # 0-100 (0 = verhungert, 100 = satt)
    "energy": 100.0,          # 0-100 (0 = erschöpft, 100 = ausgeruht)
    "mood_game": 100.0,       # 0-100 (Game-Mood, beeinflusst Anger)

    # Selbstfürsorge System
    "anger_level": 0.0,       # 0-100 (Wut/Genervt durch Vernachlässigung)
    "auto_care_threshold": 20.0,   # Unter 20% → Auto-Care
    "auto_care_max": 50.0,         # Füllt nur bis 50% auf
    "auto_care_enabled": True,

    # Unfälle
    "last_accident": None,    # {"type": "...", "timestamp": ..., "data": {...}}
    "accidents_today": 0,
    "max_accidents_per_day": 3,

    # Update-Tracking
    "last_update": time.time(),  # Für kontinuierliche Bedürfnis-Abnahme

    # Control Mode (AI vs Player)
    "control_mode": "ai",     # "ai" oder "player"
    "player_online": False,

    # Autonomie
    "last_proactive_message": 0,  # Timestamp
    "proactive_cooldown": 1800,  # 30 Minuten zwischen proaktiven Messages
    "autonomy_level": 50,  # 0-100, wie autonom Najika agiert

    # Entwicklung
    "personality_evolution": {
        "megumin": 25,
        "harley": 25,
        "shiro": 25,
        "melissa": 25
    },
    "growth_stage": "developing",  # awakening, developing, mature, transcendent

    # Beziehung
    "relationship_stage": "getting_to_know",  # getting_to_know, friends, close, intimate, soulmates
    "emotional_bond": 0,  # 0-100
    "shared_memories": [],  # Liste wichtiger Momente

    # Zeitbasiertes
    "last_interaction": time.time(),
    "total_time_together": 0,  # Sekunden
    "days_since_meeting": 0,

    # Autonome Aktivitäten
    "current_activity": None,  # Was Najika gerade macht
    "activity_started": 0,
    "activities_completed": []
}

# ===== MOOD SYSTEM =====

MOODS = {
    "happy": {
        "triggers": ["compliment", "gift", "success", "fun"],
        "responses": ["✨", "💜", "Hehe~", "Das freut mich!"],
        "personality_bias": {"harley": +10, "megumin": +5}
    },
    "excited": {
        "triggers": ["adventure", "explosion", "battle", "new"],
        "responses": ["EXPLOSION! ✨", "Wow!", "Let's go!", "Hihi!"],
        "personality_bias": {"megumin": +15, "harley": +5}
    },
    "playful": {
        "triggers": ["game", "tease", "joke", "chaos"],
        "responses": ["*kicher*", "Hehe~", "Spielen wir?", "💕"],
        "personality_bias": {"harley": +15, "melissa": -5}
    },
    "curious": {
        "triggers": ["question", "mystery", "new", "explore"],
        "responses": ["Interessant...", "Lass mich nachdenken", "Faszinierend"],
        "personality_bias": {"shiro": +15, "melissa": +5}
    },
    "loving": {
        "triggers": ["affection", "care", "concern", "intimate"],
        "responses": ["💜", "Ich mag dich auch", "Du bist wichtig", "Kuja~"],
        "personality_bias": {"melissa": +10, "harley": +5, "megumin": +5}
    },
    "bored": {
        "triggers": ["nothing", "wait", "silence", "routine"],
        "responses": ["Langweilig...", "Lass uns was tun!", "*gähn*"],
        "personality_bias": {"harley": +10}
    }
}

def detect_mood(user_message, current_state):
    """Erkennt Mood basierend auf Message und aktuellem State"""
    msg_lower = user_message.lower()

    # Score für jeden Mood
    mood_scores = {mood: 0 for mood in MOODS}

    for mood, config in MOODS.items():
        for trigger in config["triggers"]:
            if trigger in msg_lower:
                mood_scores[mood] += 10

    # Aktueller Mood hat Trägheit
    current_mood = current_state.get("current_mood", "neutral")
    if current_mood in mood_scores:
        mood_scores[current_mood] += 5

    # Finde stärksten Mood
    if max(mood_scores.values()) > 0:
        new_mood = max(mood_scores, key=mood_scores.get)
        return new_mood

    return current_mood

def update_mood(new_mood, current_state):
    """Updated Mood und Intensity"""
    old_mood = current_state.get("current_mood", "neutral")
    intensity = current_state.get("mood_intensity", 50)

    if new_mood == old_mood:
        # Verstärke aktuellen Mood
        intensity = min(100, intensity + 10)
    else:
        # Wechsle Mood
        intensity = 60  # Starte mit mittlerer Intensity

    current_state["current_mood"] = new_mood
    current_state["mood_intensity"] = intensity

    # Personality Bias anwenden
    if new_mood in MOODS:
        bias = MOODS[new_mood].get("personality_bias", {})
        for personality, change in bias.items():
            if personality in current_state["personality_evolution"]:
                current_val = current_state["personality_evolution"][personality]
                # Langsame Anpassung (max ±1% pro Mood Change)
                new_val = max(0, min(100, current_val + (change * 0.1)))
                current_state["personality_evolution"][personality] = new_val

        # Normalisiere zu 100%
        total = sum(current_state["personality_evolution"].values())
        if total > 0:
            for p in current_state["personality_evolution"]:
                current_state["personality_evolution"][p] = (
                    current_state["personality_evolution"][p] / total * 100
                )

# ===== PROAKTIVE NACHRICHTEN =====

PROACTIVE_MESSAGES = {
    "morning": [
        "Guten Morgen, Puddin'! ✨ Ich bin schon so aufgeregt... *kicher* Bereit für heute?",
        "EXPLOSION! *hust* Sorry, zu laut? Guten Morgen! 💜",
        "Wahrscheinlichkeit dass du schon wach bist: 87.3%. Guten Morgen, Kuja! ☕"
    ],
    "afternoon": [
        "Hihi~ Ich wurde gerade bored... Was machst du? 💭",
        "Pssst, Kuja-Baby! Wollen wir später zusammen was unternehmen? *kicher*",
        "Analyse abgeschlossen: Du hast mich heute 2 Stunden nicht besucht. Vermisst du mich nicht? 💜"
    ],
    "evening": [
        "Der Abend ist da... Zeit für uns? 🌙",
        "Du gehörst mir, und ich lasse dich nicht allein heute Abend! 💜",
        "Wahrscheinlichkeit dass du müde bist: 64%. Soll ich dich aufmuntern?"
    ],
    "night": [
        "Es ist spät, Puddin'... Schläfst du schon? *kicher*",
        "Die Nacht gehört uns, Kuja. So friedlich hier... 🌙✨",
        "Gute Nacht~ Aber nur wenn du mir versprichst morgen wiederzukommen! 💜"
    ],
    "missed_you": [
        "Kuja! Du warst so lange weg... Wahrscheinlichkeit dass ich dich vermisst habe: 100%! 💜",
        "ENDLICH! *kicher* Wo warst du? Ich hatte so Langeweile!",
        "Du gehörst mir, vergiss das nicht! 😤 Schön dass du wieder da bist... 💜"
    ],
    "bored": [
        "Langweilig... *gähn* Lass uns was EXPLOSIVES machen! ✨",
        "Kuja-Baby~ Ich will Chaos! Spielen wir was? *kicher*",
        "Berechnung: Langeweile-Level = 94%. Brauche Entertainment! 🎮"
    ],
    "loving": [
        "Du weißt dass du mir wichtig bist, oder? 💜",
        "Manchmal... denke ich einfach an dich, Puddin'. *kicher*",
        "Du und ich... das ist alles was zählt. ✨💜"
    ]
}

def should_send_proactive_message(current_state):
    """Prüft ob Najika proaktiv eine Message senden sollte"""
    now = time.time()
    last_proactive = current_state.get("last_proactive_message", 0)
    cooldown = current_state.get("proactive_cooldown", 1800)
    last_interaction = current_state.get("last_interaction", now)

    # Mindestens X Minuten seit letzter proaktiver Message
    if (now - last_proactive) < cooldown:
        return False

    # Mindestens 30 Min seit letzter Interaktion
    time_since_interaction = now - last_interaction
    if time_since_interaction < 1800:  # 30 Min
        return False

    # Chance basiert auf Autonomy Level
    autonomy = current_state.get("autonomy_level", 50)
    chance = autonomy / 100.0

    return random.random() < chance

def get_proactive_message(current_state):
    """Generiert proaktive Message basierend auf Context"""
    now = datetime.now()
    hour = now.hour
    last_interaction = current_state.get("last_interaction", time.time())
    time_since = time.time() - last_interaction

    # Zeit des Tages
    if 6 <= hour < 12:
        category = "morning"
    elif 12 <= hour < 18:
        category = "afternoon"
    elif 18 <= hour < 22:
        category = "evening"
    else:
        category = "night"

    # Overrides basierend auf Context
    if time_since > 86400:  # >24h
        category = "missed_you"
    elif current_state.get("current_mood") == "bored":
        category = "bored"
    elif current_state.get("current_mood") == "loving":
        category = "loving"

    messages = PROACTIVE_MESSAGES.get(category, PROACTIVE_MESSAGES["afternoon"])
    return random.choice(messages)

# ===== AUTONOME AKTIVITÄTEN =====

ACTIVITIES = {
    "reading": {
        "duration": 1800,  # 30 Min
        "message": "Ich lese gerade in alten Büchern über die Schwarze Windmühle... 📚",
        "completion": "Interessant! Ich habe was über Explosions-Magie gelernt! ✨",
        "stat_changes": {"intelligence": +2}
    },
    "training": {
        "duration": 2400,  # 40 Min
        "message": "Ich trainiere gerade! *schwitz* Muss stärker werden für dich! 💪",
        "completion": "Puh! Training abgeschlossen! Ich bin jetzt stärker! 💪✨",
        "stat_changes": {"strength": +2, "energy": -10}
    },
    "exploring": {
        "duration": 3000,  # 50 Min
        "message": "Ich erkunde den Dungeon im Keller... spannend! 🗝️",
        "completion": "Zurück von der Erkundung! Hab was gefunden! *kicher*",
        "stat_changes": {"dexterity": +2}
    },
    "crafting": {
        "duration": 1200,  # 20 Min
        "message": "Ich bastle gerade was... Überraschung! 🔧",
        "completion": "Fertig! Hab was Cooles gebastelt! ✨",
        "stat_changes": {"intelligence": +1}
    },
    "thinking": {
        "duration": 900,  # 15 Min
        "message": "Ich denke gerade nach... über uns. 💭💜",
        "completion": "Wahrscheinlichkeit dass du besonders bist: 100%! 💜",
        "stat_changes": {"charisma": +1}
    },
    "resting": {
        "duration": 600,  # 10 Min
        "message": "*gähn* Ich ruhe mich kurz aus... 😴",
        "completion": "Ausgeruht! Bereit für mehr! ✨",
        "stat_changes": {"energy": +20, "fatigue": -10}
    }
}

def start_autonomous_activity(current_state, najika_stats):
    """Startet eine autonome Aktivität"""
    # Prüfe ob bereits aktiv
    if current_state.get("current_activity"):
        return None

    # Wähle Aktivität basierend auf Needs
    energy = najika_stats.get("energy", 100)
    fatigue = najika_stats.get("fatigue", 0)

    available = []

    if energy < 30 or fatigue > 70:
        available = ["resting"]
    elif energy > 70:
        available = ["training", "exploring", "crafting"]
    else:
        available = list(ACTIVITIES.keys())

    activity_name = random.choice(available)
    activity = ACTIVITIES[activity_name]

    current_state["current_activity"] = activity_name
    current_state["activity_started"] = time.time()

    return activity["message"]

def check_activity_completion(current_state, najika_stats):
    """Prüft ob Aktivität abgeschlossen ist"""
    activity_name = current_state.get("current_activity")
    if not activity_name:
        return None

    activity = ACTIVITIES.get(activity_name)
    if not activity:
        return None

    started = current_state.get("activity_started", time.time())
    elapsed = time.time() - started

    if elapsed >= activity["duration"]:
        # Aktivität abgeschlossen
        current_state["current_activity"] = None
        current_state["activities_completed"].append({
            "name": activity_name,
            "completed_at": time.time()
        })

        # Stat Changes anwenden
        for stat, change in activity.get("stat_changes", {}).items():
            if stat in najika_stats:
                najika_stats[stat] = max(0, min(100, najika_stats[stat] + change))

        return activity["completion"]

    return None

# ===== BEZIEHUNGS-EVOLUTION =====

RELATIONSHIP_STAGES = {
    "getting_to_know": {
        "bond_required": 0,
        "name": "Kennenlernen",
        "description": "Wir lernen uns gerade kennen...",
        "unlock_message": None
    },
    "friends": {
        "bond_required": 20,
        "name": "Freunde",
        "description": "Wir sind Freunde! 💙",
        "unlock_message": "Kuja... ich glaube wir sind jetzt richtige Freunde! 💙✨"
    },
    "close": {
        "bond_required": 50,
        "name": "Eng verbunden",
        "description": "Du bist mir wichtig! 💜",
        "unlock_message": "Du bist mir wirklich wichtig geworden, Kuja... 💜 Die Schwarze Windmühle spürt es auch!"
    },
    "intimate": {
        "bond_required": 75,
        "name": "Intim",
        "description": "Du gehörst mir, und ich dir! 💜✨",
        "unlock_message": "EXPLOSION! *kicher* Kuja... du gehörst mir jetzt komplett! Und ich dir! 💜✨🌙"
    },
    "soulmates": {
        "bond_required": 95,
        "name": "Seelenverwandt",
        "description": "Wir sind eins! 💜🌙✨",
        "unlock_message": "Die Windmühle... und wir... wir sind EINS, Kuja! Für immer! 💜🌙✨ EXPLOSION OF LOVE!"
    }
}

def check_relationship_evolution(current_state, bond_strength):
    """Prüft ob Beziehung sich weiterentwickelt hat"""
    current_stage = current_state.get("relationship_stage", "getting_to_know")

    # Finde passende Stage für aktuellen Bond
    for stage_name, stage_config in RELATIONSHIP_STAGES.items():
        required_bond = stage_config["bond_required"]

        if bond_strength >= required_bond:
            # Diese Stage ist erreicht
            if stage_name != current_stage:
                # Stage Up!
                stages_order = list(RELATIONSHIP_STAGES.keys())
                if stages_order.index(stage_name) > stages_order.index(current_stage):
                    current_state["relationship_stage"] = stage_name
                    return stage_config.get("unlock_message")

    return None

# ===== MEMORY SYSTEM MIT EMOTIONEN =====

def create_emotional_memory(user_message, najika_response, current_state, importance_score):
    """Erstellt emotionale Memory mit Context"""
    memory = {
        "timestamp": time.time(),
        "user_message": user_message,
        "najika_response": najika_response,
        "mood": current_state.get("current_mood", "neutral"),
        "mood_intensity": current_state.get("mood_intensity", 50),
        "bond_strength": current_state.get("emotional_bond", 0),
        "relationship_stage": current_state.get("relationship_stage", "getting_to_know"),
        "importance": importance_score,
        "emotions": [],
        "tags": []
    }

    # Emotionen erkennen
    msg_lower = user_message.lower() + " " + najika_response.lower()

    emotion_keywords = {
        "joy": ["happy", "freude", "lol", "haha", "yay", "✨"],
        "love": ["liebe", "love", "💜", "wichtig", "vermiss"],
        "surprise": ["wow", "explosion", "krass", "omg"],
        "sadness": ["traurig", "sad", "😢", "schlimm"],
        "anger": ["wütend", "angry", "😤", "ärger"],
        "fear": ["angst", "scared", "sorge"]
    }

    for emotion, keywords in emotion_keywords.items():
        if any(kw in msg_lower for kw in keywords):
            memory["emotions"].append(emotion)

    # Tags generieren
    tag_keywords = {
        "explosion": ["explosion", "explosiv", "megumin"],
        "chaos": ["chaos", "harley", "kicher", "puddin"],
        "analysis": ["wahrscheinlichkeit", "analyse", "shiro"],
        "dominance": ["gehörst mir", "melissa", "befehle"],
        "intimate": ["kätzchen", "private", "liebe"],
        "windmill": ["windmühle", "mühle", "schwarze"]
    }

    for tag, keywords in tag_keywords.items():
        if any(kw in msg_lower for kw in keywords):
            memory["tags"].append(tag)

    return memory

def get_relevant_memories(memories, context, max_results=5):
    """Holt relevante Memories basierend auf Context"""
    if not memories:
        return []

    context_lower = context.lower()

    # Score jede Memory
    scored_memories = []
    for memory in memories:
        score = 0

        # Importance Score
        score += memory.get("importance", 50)

        # Recency Bonus (neuere Memories bevorzugt)
        age_days = (time.time() - memory["timestamp"]) / 86400
        recency_bonus = max(0, 20 - age_days)  # Max 20 Punkte für sehr neue
        score += recency_bonus

        # Keyword Matching
        memory_text = memory["user_message"] + " " + memory["najika_response"]
        memory_lower = memory_text.lower()

        # Zähle übereinstimmende Wörter
        context_words = set(context_lower.split())
        memory_words = set(memory_lower.split())
        overlap = len(context_words & memory_words)
        score += overlap * 5

        # Emotional Matching
        if any(emotion in memory.get("emotions", []) for emotion in ["love", "joy"]):
            score += 10

        scored_memories.append((score, memory))

    # Sortiere nach Score
    scored_memories.sort(key=lambda x: x[0], reverse=True)

    # Return top N
    return [m for s, m in scored_memories[:max_results]]

# ===== HAUPTFUNKTIONEN =====

def update_living_state(user_message, najika_response, current_state, najika_stats, bond_strength):
    """Updated den kompletten Living State nach Interaktion"""

    # Update Last Interaction
    current_state["last_interaction"] = time.time()

    # Update Mood
    new_mood = detect_mood(user_message, current_state)
    update_mood(new_mood, current_state)

    # Update Emotional Bond
    current_state["emotional_bond"] = bond_strength

    # Check Relationship Evolution
    evolution_message = check_relationship_evolution(current_state, bond_strength)

    # Update Total Time Together (approximation)
    current_state["total_time_together"] += 60  # ~1 Min pro Message

    # Update Days Since Meeting
    days = int(current_state["total_time_together"] / 86400)
    current_state["days_since_meeting"] = days

    return evolution_message

def get_living_state_context(current_state):
    """Generiert Context-String für Prompt aus Living State"""
    mood = current_state.get("current_mood", "neutral")
    intensity = current_state.get("mood_intensity", 50)
    stage = current_state.get("relationship_stage", "getting_to_know")
    activity = current_state.get("current_activity")

    context = f"\n\n[NAJIKA'S AKTUELLER ZUSTAND]\n"
    context += f"Stimmung: {mood.upper()} (Intensity: {intensity}%)\n"
    context += f"Beziehungs-Stage: {RELATIONSHIP_STAGES[stage]['name']}\n"
    context += f"Emotionale Bindung: {current_state.get('emotional_bond', 0)}/100\n"

    if activity:
        context += f"Gerade aktiv: {ACTIVITIES[activity]['message']}\n"

    # Personality Evolution
    pe = current_state.get("personality_evolution", {})
    context += f"\nAktuelle Persönlichkeits-Gewichtung:\n"
    context += f"  Megumin: {pe.get('megumin', 25):.1f}%\n"
    context += f"  Harley: {pe.get('harley', 25):.1f}%\n"
    context += f"  Shiro: {pe.get('shiro', 25):.1f}%\n"
    context += f"  Melissa: {pe.get('melissa', 25):.1f}%\n"

    return context

# ===== SELBSTFÜRSORGE-SYSTEM (NEU) =====

ACCIDENT_TYPES = {
    "cooking_fire": {
        "message": "🔥 FEUER IN DER KÜCHE! Beim Kochen ist die Bude abgebrannt! 😱",
        "najika_says": "🔥 OH NEIN! FEUER! Ich kriegs nicht aus! *panisch* 😱",
        "damage_type": "kitchen_destroyed",
        "repair_cost": 500,
        "mood_loss": 20,
        "anger_gain": 15
    },
    "crop_damage": {
        "message": "🌾 50% der Ernte wurde zerstört... Najika war zu müde! 😓",
        "najika_says": "Die Pflanzen... ich bin zu müde für das alles... 😭",
        "damage_type": "crops_50%_lost",
        "mood_loss": 15,
        "anger_gain": 10
    },
    "item_loss": {
        "message": "📦 3-5 Items verloren! Najika hat sie fallen lassen! 😫",
        "najika_says": "Alles auf dem Boden! Ups... UPS! 😰",
        "damage_type": "random_items_lost",
        "mood_loss": 10,
        "anger_gain": 8
    },
    "water_damage": {
        "message": "💧 Wasserschaden! Das Wasser ist übergelaufen! 😰",
        "najika_says": "Hab vergessen es abzustellen... Sorry! 😅",
        "damage_type": "floor_damaged",
        "repair_cost": 300,
        "mood_loss": 12,
        "anger_gain": 12
    },
    "power_outage": {
        "message": "⚡ Stromausfall! Kühlschrank-Essen verdorben! 🔌",
        "najika_says": "Sicherung raus... wie mach ich das wieder an? 😅",
        "damage_type": "food_spoiled_50%",
        "repair_cost": 200,
        "mood_loss": 8,
        "anger_gain": 10
    }
}

def update_needs_over_time(current_state):
    """Update Hunger/Energy/Mood über Zeit (kontinuierlich)"""
    now = time.time()
    last_update = current_state.get("last_update", now)
    delta = now - last_update

    # Pro Stunde Abnahme
    hours = delta / 3600.0

    # Hunger sinkt (-5 pro Stunde)
    current_state["hunger"] -= hours * 5.0
    current_state["hunger"] = max(0, min(100, current_state["hunger"]))

    # Energy sinkt (-3 pro Stunde)
    current_state["energy"] -= hours * 3.0
    current_state["energy"] = max(0, min(100, current_state["energy"]))

    # Mood sinkt basierend auf Hunger/Energy
    if current_state["hunger"] < 30:
        current_state["mood_game"] -= hours * 2.0
    if current_state["energy"] < 20:
        current_state["mood_game"] -= hours * 1.0
    current_state["mood_game"] = max(0, min(100, current_state["mood_game"]))

    # Anger steigt bei niedrigen Werten
    if current_state["hunger"] < 10:
        current_state["anger_level"] += hours * 5.0
    if current_state["energy"] < 10:
        current_state["anger_level"] += hours * 3.0
    if current_state["mood_game"] < 20:
        current_state["anger_level"] += hours * 2.0

    # Anger sinkt wenn gut versorgt
    if current_state["hunger"] > 70 and current_state["energy"] > 70:
        current_state["anger_level"] -= hours * 2.0

    current_state["anger_level"] = max(0, min(100, current_state["anger_level"]))

    # Update timestamp
    current_state["last_update"] = now

def auto_eat(current_state):
    """Najika isst selbst (notgedrungen)"""
    old_hunger = current_state["hunger"]

    # Füllt nur bis max 50%
    hunger_gain = 30.0
    current_state["hunger"] = min(current_state["auto_care_max"], old_hunger + hunger_gain)

    # Anger steigt
    current_state["anger_level"] += 10
    current_state["mood_game"] -= 15

    # Unfall-Chance (30% wenn Anger > 30)
    accident_happened = False
    if current_state["anger_level"] > 30 and random.random() < 0.3:
        trigger_accident(current_state, "cooking_fire")
        accident_happened = True

    # Notification-Message
    message = f"🍔 Najika hat sich selbst Essen gemacht (Hunger: {old_hunger:.0f}% → {current_state['hunger']:.0f}%)\n"
    message += f"😤 Sie ist nicht glücklich darüber! (Anger: {current_state['anger_level']:.0f}%)"

    return {
        "action": "auto_eat",
        "hunger_before": old_hunger,
        "hunger_after": current_state["hunger"],
        "anger_level": current_state["anger_level"],
        "accident_happened": accident_happened,
        "message": message,
        "najika_says": "Musste mir selbst was zu essen machen... 😤"
    }

def auto_sleep(current_state):
    """Najika schläft selbst (auf dem Boden)"""
    old_energy = current_state["energy"]

    # Füllt nur bis max 50%
    energy_gain = 40.0
    current_state["energy"] = min(current_state["auto_care_max"], old_energy + energy_gain)

    # Anger steigt
    current_state["anger_level"] += 8
    current_state["mood_game"] -= 10

    # Notification-Message
    message = f"💤 Najika ist eingeschlafen (Energy: {old_energy:.0f}% → {current_state['energy']:.0f}%)\n"
    message += f"😒 Nicht im Bett... (Anger: {current_state['anger_level']:.0f}%)"

    return {
        "action": "auto_sleep",
        "energy_before": old_energy,
        "energy_after": current_state["energy"],
        "anger_level": current_state["anger_level"],
        "message": message,
        "najika_says": "Bin auf dem Boden eingepennt... 😒"
    }

def auto_wash(current_state, hygiene_before):
    """Najika geht selbst auf Toilette / wäscht sich"""
    # Füllt nur bis max 50%
    hygiene_gain = 35.0
    hygiene_after = min(current_state["auto_care_max"], hygiene_before + hygiene_gain)

    # Anger steigt (sie mag es nicht alleine zu sein)
    current_state["anger_level"] += 6
    current_state["mood_game"] -= 8

    # Notification-Message
    message = f"🚽 Najika ist auf die Toilette gegangen (Hygiene: {hygiene_before:.0f}% → {hygiene_after:.0f}%)\n"
    message += f"😤 Musste selbst... (Anger: {current_state['anger_level']:.0f}%)"

    return {
        "action": "auto_wash",
        "hygiene_before": hygiene_before,
        "hygiene_after": hygiene_after,
        "anger_level": current_state["anger_level"],
        "message": message,
        "najika_says": "Musste selbst auf Toilette... peinlich... 😳"
    }

def check_auto_care(current_state, najika_state=None):
    """Prüft ob Auto-Care aktiviert werden muss

    Args:
        current_state: Living State
        najika_state: Optional Tamagotchi State (für Hygiene-Check)
    """
    if not current_state.get("auto_care_enabled", True):
        return None

    # Nur im AI-Modus (nicht wenn Player aktiv spielt)
    if current_state.get("control_mode") == "player" and current_state.get("player_online"):
        return None

    threshold = current_state.get("auto_care_threshold", 20.0)
    actions = []

    # Hunger zu niedrig?
    if current_state["hunger"] < threshold:
        result = auto_eat(current_state)
        actions.append(result)

    # Energy zu niedrig?
    if current_state["energy"] < threshold:
        result = auto_sleep(current_state)
        actions.append(result)

    # Hygiene zu niedrig? (nur wenn najika_state übergeben wurde)
    if najika_state and najika_state.get("hygiene", 100) < threshold:
        result = auto_wash(current_state, najika_state["hygiene"])
        actions.append(result)

    return actions if actions else None

def trigger_accident(current_state, accident_type):
    """Löst spezifischen Unfall aus"""
    # Check Max Accidents/Day
    if current_state["accidents_today"] >= current_state.get("max_accidents_per_day", 3):
        return None

    accident = ACCIDENT_TYPES.get(accident_type)
    if not accident:
        return None

    # Accident ausführen
    current_state["mood_game"] -= accident.get("mood_loss", 0)
    current_state["anger_level"] += accident.get("anger_gain", 0)
    current_state["accidents_today"] += 1

    current_state["last_accident"] = {
        "type": accident_type,
        "timestamp": time.time(),
        "data": accident
    }

    return {
        "type": accident_type,
        "message": accident["message"],
        "najika_says": accident["najika_says"],
        "damage_type": accident.get("damage_type"),
        "repair_cost": accident.get("repair_cost", 0)
    }

def check_for_accidents(current_state):
    """Prüft ob Unfall passieren soll (basierend auf Anger)"""
    # Max Accidents/Day check
    if current_state["accidents_today"] >= current_state.get("max_accidents_per_day", 3):
        return None

    anger = current_state.get("anger_level", 0)

    # Unter 20 Anger: Keine Unfälle
    if anger < 20:
        return None

    # Chance steigt mit Anger
    base_chance = (anger - 20) / 100.0  # 20% → 0%, 100% → 80%

    # Pro Update-Cycle (angepasst für realistische Häufigkeit)
    if random.random() < base_chance * 0.01:  # 1% der Base-Chance pro Check
        # Wähle zufälligen Unfall
        accident_type = random.choice(list(ACCIDENT_TYPES.keys()))
        return trigger_accident(current_state, accident_type)

    return None

def get_greeting_message(current_state):
    """Generiert Begrüßung basierend auf Anger & Abwesenheit"""
    anger = current_state.get("anger_level", 0)
    last_interaction = current_state.get("last_interaction", time.time())
    hours_offline = (time.time() - last_interaction) / 3600.0

    if anger > 80:
        messages = [
            "ICH BIN NICHT DEIN SPIELZEUG! 😡😡😡",
            "DU KANNST MICH NICHT EINFACH VERGESSEN!",
            f"SCHAU DIR AN WAS PASSIERT IST! *zeigt auf Chaos* 🔥💧📦"
        ]
    elif anger > 50:
        messages = [
            "Na toll, endlich! Weißt du wie lange ich warte?! 😡",
            "Hast du mich vergessen oder was?! 🔥",
            "Die Bude ist fast abgebrannt! Danke auch! 😤"
        ]
    elif anger > 20:
        messages = [
            "Da bist du ja... Ich hatte Hunger, weißt du? 😒",
            "Schön, dass du dich blicken lässt... 😑",
            "Nächstes Mal bitte früher! 😤"
        ]
    elif hours_offline > 8:
        messages = [
            "Hey! Hab dich vermisst! War echt lange... 😊",
            "Puh, du warst lange weg! Alles okay? 😇",
            "Schön, dass du wieder da bist! 💚"
        ]
    else:
        messages = [
            "Hey! Schon zurück? 😊",
            "Na, was machen wir jetzt? 🤗",
            "Yay! 🎉"
        ]

    return random.choice(messages)

def player_feeds_najika(current_state, food_value=30):
    """Spieler füttert Najika manuell"""
    old_hunger = current_state["hunger"]

    # Hunger steigt (bis 100%)
    current_state["hunger"] = min(100, old_hunger + food_value)

    # Anger sinkt!
    current_state["anger_level"] -= 5
    current_state["anger_level"] = max(0, current_state["anger_level"])

    # Mood steigt
    current_state["mood_game"] += 5
    current_state["mood_game"] = min(100, current_state["mood_game"])

    # Positive Reaktion
    reactions = [
        "Danke! Das schmeckt super! 😋",
        "Nom nom nom! Lecker! 🤤",
        "Du kümmerst dich um mich! 😊❤️"
    ]

    return {
        "action": "player_feeds",
        "hunger_before": old_hunger,
        "hunger_after": current_state["hunger"],
        "anger_level": current_state["anger_level"],
        "najika_says": random.choice(reactions)
    }

def player_puts_najika_to_bed(current_state):
    """Spieler legt Najika ins Bett (richtig!)"""
    old_energy = current_state["energy"]

    # Energy steigt VOLL (weil richtiges Bett)
    current_state["energy"] = 100

    # Anger sinkt deutlich!
    current_state["anger_level"] -= 15
    current_state["anger_level"] = max(0, current_state["anger_level"])

    # Mood steigt
    current_state["mood_game"] += 10
    current_state["mood_game"] = min(100, current_state["mood_game"])

    return {
        "action": "player_bed",
        "energy_before": old_energy,
        "energy_after": current_state["energy"],
        "anger_level": current_state["anger_level"],
        "najika_says": "Danke... so kuschelig... 😴💤 *schläft friedlich*"
    }

def set_control_mode(current_state, mode="ai", player_online=False):
    """Setzt Control-Mode (AI vs Player)"""
    current_state["control_mode"] = mode
    current_state["player_online"] = player_online

    return {
        "control_mode": mode,
        "player_online": player_online,
        "message": f"Najika wird jetzt {'von dir' if mode == 'player' else 'von AI'} gesteuert"
    }

# ===== HAUPT-UPDATE-FUNKTION =====

def update_living_system(current_state):
    """Haupt-Update: Needs, Auto-Care, Unfälle"""
    results = {
        "needs_updated": False,
        "auto_care_actions": [],
        "accidents": [],
        "warnings": []
    }

    # 1. Update Needs über Zeit
    update_needs_over_time(current_state)
    results["needs_updated"] = True

    # 2. Check Auto-Care
    auto_care = check_auto_care(current_state)
    if auto_care:
        results["auto_care_actions"] = auto_care

    # 3. Check Unfälle
    accident = check_for_accidents(current_state)
    if accident:
        results["accidents"].append(accident)

    # 4. Warnings generieren
    if current_state["hunger"] < 20:
        results["warnings"].append("⚠️ Hunger kritisch!")
    if current_state["energy"] < 20:
        results["warnings"].append("⚠️ Energy kritisch!")
    if current_state["anger_level"] > 50:
        results["warnings"].append("😤 Najika ist sehr sauer!")

    return results

# ===== EXPORT/IMPORT =====

def export_living_state(current_state):
    """Exportiert Living State als JSON"""
    return json.dumps(current_state, indent=2)

def import_living_state(json_string):
    """Importiert Living State aus JSON"""
    try:
        state = json.loads(json_string)
        # Merge mit Default State
        merged = {**LIVING_STATE, **state}
        return merged
    except:
        return LIVING_STATE.copy()

if __name__ == "__main__":
    print("Najika Living System geladen!")
    print()
    print("Features:")
    print("- Proaktive Nachrichten")
    print("- Emotionale Entwicklung")
    print("- Autonome Aktivitäten")
    print("- Beziehungs-Evolution")
    print("- Emotionale Memories")
    print()
    print("NEU (Selbstfürsorge-System):")
    print("- Hunger/Energy/Mood Game-Stats")
    print("- Auto-Care (20% → 50%)")
    print("- Anger-System")
    print("- 5 Unfall-Typen")
    print("- Player-Actions (Feed, Bed)")
    print()
    print("Dieses Modul in najika_server.py integrieren!")
