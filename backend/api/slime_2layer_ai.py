"""
Slime-KI 2-Layer System - Persönlichkeit vs Game Skills
========================================================

EBENE 1 (KI-Persönlichkeit): PERSISTENT
- Erinnerungen bleiben
- Wissen über Bosse bleibt
- Strategien bekannt
- Persönlichkeit gleich

EBENE 2 (Spiel-Skills): RESET BEI TOD
- Zauber-Erkennung bei 0
- Skills vergessen
- Muss neu lernen
- Training von vorne

Features:
- Memory System für Persönlichkeit
- Boss Knowledge bleibt
- Form-Copy System (5% Chance, 80% Stats)
- Schnelleres Re-Learning (weil KI weiß was wichtig ist)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from backend.utils import handle_errors

router = APIRouter(prefix="/api/slime-ai", tags=["slime_ai"])


# ==================== ENUMS ====================

class BossWeakness(str, Enum):
    """Boss weakness types"""
    MAGIC = "magic"
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    WATER = "water"
    EARTH = "earth"
    WIND = "wind"
    LIGHT = "light"
    DARK = "dark"


# ==================== MODELS ====================

class BossKnowledge(BaseModel):
    """Boss knowledge in AI memory"""
    boss_id: str
    boss_name: str
    weakness: BossWeakness
    strategy: str
    notes: List[str] = []
    learned_at: datetime
    times_defeated: int = 0


class PersonalityMemory(BaseModel):
    """Persistent personality memory (EBENE 1)"""
    slime_id: int
    owner_id: int
    personality_traits: List[str] = []  # z.B. ["mutig", "strategisch", "vorsichtig"]
    boss_knowledge: Dict[str, BossKnowledge] = {}
    general_memories: List[str] = []
    battle_strategies: Dict[str, str] = {}
    created_at: datetime
    last_death: Optional[datetime] = None
    death_count: int = 0


class GameSkills(BaseModel):
    """Game skills (EBENE 2 - RESET BEI TOD)"""
    slime_id: int
    spell_recognition: Dict[str, int] = {}  # spell_id → level (0-100)
    combat_skills: Dict[str, float] = {}  # skill_id → proficiency (0.0-1.0)
    learned_abilities: List[str] = []
    training_progress: Dict[str, int] = {}  # ability_id → progress (0-100)
    current_level: int = 1
    current_xp: int = 0
    reset_count: int = 0
    last_reset: Optional[datetime] = None


class FormCopy(BaseModel):
    """Copied enemy form"""
    form_id: str
    original_name: str
    original_stats: Dict[str, int]  # HP, ATK, DEF, etc.
    slime_stats: Dict[str, int]  # 80% of original
    weakness: Optional[BossWeakness] = None
    strength: Optional[str] = None
    copied_at: datetime
    times_trained_against: int = 0


# ==================== STORAGE ====================

PERSONALITY_MEMORIES: Dict[int, PersonalityMemory] = {}
GAME_SKILLS: Dict[int, GameSkills] = {}
FORM_COPIES: Dict[int, List[FormCopy]] = {}  # slime_id → list of forms


# ==================== HELPERS ====================

def calculate_relearning_speed(personality: PersonalityMemory, skill_id: str) -> float:
    """
    Calculate relearning speed bonus based on AI memory

    Returns multiplier (1.0 = normal, 2.0 = 2x faster)
    """
    # Base speed
    speed = 1.0

    # Bonus if AI remembers using this skill before
    if skill_id in personality.battle_strategies:
        speed += 0.5  # +50% faster

    # Bonus based on death count (more experienced AI)
    speed += min(personality.death_count * 0.1, 0.5)  # +10% per death, max +50%

    return speed


def copy_form_stats(original_stats: Dict[str, int]) -> Dict[str, int]:
    """Copy stats at 80% of original"""
    return {
        stat: int(value * 0.8)
        for stat, value in original_stats.items()
    }


# ==================== PERSONALITY ENDPOINTS (EBENE 1) ====================

@router.post("/personality/create")
@handle_errors()
async def create_personality(slime_id: int, owner_id: int):
    """
    Create personality memory for new slime

    This is EBENE 1 - persists through deaths
    """
    if slime_id in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=400,
            detail="Slime hat bereits eine Persönlichkeit!"
        )

    personality = PersonalityMemory(
        slime_id=slime_id,
        owner_id=owner_id,
        created_at=datetime.now()
    )

    PERSONALITY_MEMORIES[slime_id] = personality

    return {
        "success": True,
        "slime_id": slime_id,
        "message": "✅ Slime-KI Persönlichkeit erstellt!",
        "personality": personality.dict()
    }


@router.post("/personality/learn-boss")
@handle_errors()
async def learn_boss_weakness(
    slime_id: int,
    boss_id: str,
    boss_name: str,
    weakness: BossWeakness,
    strategy: str,
    notes: List[str] = []
):
    """
    Slime AI learns boss weakness (PERMANENT!)

    Example:
    {
        "slime_id": 1,
        "boss_id": "stein_golem",
        "boss_name": "Stein-Golem",
        "weakness": "magic",
        "strategy": "Nutze Feuer-Magie, vermeide physische Angriffe",
        "notes": ["Langsam aber hohe DEF", "Schwacher Punkt im Rücken"]
    }
    """
    if slime_id not in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht gefunden! Erstelle zuerst Persönlichkeit."
        )

    personality = PERSONALITY_MEMORIES[slime_id]

    # Create or update boss knowledge
    knowledge = BossKnowledge(
        boss_id=boss_id,
        boss_name=boss_name,
        weakness=weakness,
        strategy=strategy,
        notes=notes,
        learned_at=datetime.now()
    )

    if boss_id in personality.boss_knowledge:
        # Update existing knowledge
        knowledge.times_defeated = personality.boss_knowledge[boss_id].times_defeated + 1

    personality.boss_knowledge[boss_id] = knowledge

    return {
        "success": True,
        "slime_id": slime_id,
        "boss_id": boss_id,
        "message": f"✅ Slime-KI hat {boss_name} Schwäche gelernt!",
        "knowledge": knowledge.dict(),
        "ai_message": f"Ich merke mir: {boss_name} ist schwach gegen {weakness.value}!"
    }


@router.get("/personality/recall-boss")
@handle_errors()
async def recall_boss_weakness(slime_id: int, boss_id: str):
    """
    Slime AI recalls boss weakness from memory

    Returns knowledge even after death/reset!
    """
    if slime_id not in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht gefunden!"
        )

    personality = PERSONALITY_MEMORIES[slime_id]

    if boss_id not in personality.boss_knowledge:
        return {
            "success": False,
            "slime_id": slime_id,
            "boss_id": boss_id,
            "message": "Slime-KI hat keine Erinnerung an diesen Boss.",
            "ai_message": "Ich kenne diesen Gegner noch nicht..."
        }

    knowledge = personality.boss_knowledge[boss_id]

    return {
        "success": True,
        "slime_id": slime_id,
        "boss_id": boss_id,
        "knowledge": knowledge.dict(),
        "ai_message": f"Ich erinnere mich: {knowledge.boss_name} ist schwach gegen {knowledge.weakness.value}! {knowledge.strategy}"
    }


@router.post("/personality/add-memory")
@handle_errors()
async def add_personality_memory(slime_id: int, memory: str):
    """
    Add general memory to AI personality

    Example: "Kampf gegen Drache war schwer", "Owner bevorzugt defensive Strategie"
    """
    if slime_id not in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht gefunden!"
        )

    personality = PERSONALITY_MEMORIES[slime_id]
    personality.general_memories.append(memory)

    return {
        "success": True,
        "slime_id": slime_id,
        "memory": memory,
        "message": "✅ Erinnerung gespeichert!",
        "ai_message": "Ich merke mir das..."
    }


# ==================== GAME SKILLS ENDPOINTS (EBENE 2) ====================

@router.post("/skills/create")
@handle_errors()
async def create_game_skills(slime_id: int):
    """
    Create game skills for slime

    This is EBENE 2 - RESETS bei Tod!
    """
    skills = GameSkills(
        slime_id=slime_id
    )

    GAME_SKILLS[slime_id] = skills

    return {
        "success": True,
        "slime_id": slime_id,
        "message": "✅ Spiel-Skills erstellt!",
        "skills": skills.dict()
    }


@router.post("/skills/reset")
@handle_errors()
async def reset_game_skills(slime_id: int):
    """
    Reset game skills (bei Tod)

    EBENE 1 (Persönlichkeit) bleibt!
    EBENE 2 (Skills) wird resettet!
    """
    if slime_id not in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht gefunden!"
        )

    if slime_id not in GAME_SKILLS:
        raise HTTPException(
            status_code=404,
            detail="Spiel-Skills nicht gefunden!"
        )

    # Update personality memory (BLEIBT!)
    personality = PERSONALITY_MEMORIES[slime_id]
    personality.last_death = datetime.now()
    personality.death_count += 1

    # Reset game skills
    old_skills = GAME_SKILLS[slime_id]
    new_skills = GameSkills(
        slime_id=slime_id,
        reset_count=old_skills.reset_count + 1,
        last_reset=datetime.now()
    )

    GAME_SKILLS[slime_id] = new_skills

    return {
        "success": True,
        "slime_id": slime_id,
        "death_count": personality.death_count,
        "reset_count": new_skills.reset_count,
        "message": "💀 Character gestorben - Skills zurückgesetzt!",
        "ai_message": "Ich habe Erinnerungen vom letzten Besitzer... aber ich muss Skills neu lernen!",
        "personality_intact": True,
        "skills_reset": True
    }


@router.post("/skills/train")
@handle_errors()
async def train_skill(
    slime_id: int,
    skill_id: str,
    progress_points: int = 1
):
    """
    Train a skill

    Lernt schneller wenn AI es kennt (EBENE 1 hilft EBENE 2!)
    """
    if slime_id not in GAME_SKILLS:
        raise HTTPException(
            status_code=404,
            detail="Spiel-Skills nicht gefunden!"
        )

    if slime_id not in PERSONALITY_MEMORIES:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht gefunden!"
        )

    skills = GAME_SKILLS[slime_id]
    personality = PERSONALITY_MEMORIES[slime_id]

    # Calculate relearning speed
    speed_multiplier = calculate_relearning_speed(personality, skill_id)
    actual_progress = int(progress_points * speed_multiplier)

    # Update training progress
    current_progress = skills.training_progress.get(skill_id, 0)
    new_progress = min(current_progress + actual_progress, 100)
    skills.training_progress[skill_id] = new_progress

    # Learn skill when 100%
    learned = False
    if new_progress >= 100 and skill_id not in skills.learned_abilities:
        skills.learned_abilities.append(skill_id)
        learned = True

    ai_message = None
    if speed_multiplier > 1.0:
        ai_message = "Das kommt mir bekannt vor! Ich lerne schneller!"

    return {
        "success": True,
        "slime_id": slime_id,
        "skill_id": skill_id,
        "progress": new_progress,
        "learned": learned,
        "speed_multiplier": speed_multiplier,
        "ai_message": ai_message
    }


# ==================== FORM-COPY SYSTEM ====================

@router.post("/form/copy")
@handle_errors()
async def copy_enemy_form(
    slime_id: int,
    enemy_id: str,
    enemy_name: str,
    original_stats: Dict[str, int],
    weakness: Optional[BossWeakness] = None,
    strength: Optional[str] = None
):
    """
    Copy enemy form (5% chance after battle)

    Slime imitates enemy at 80% stats

    Example:
    {
        "slime_id": 1,
        "enemy_id": "stein_golem",
        "enemy_name": "Stein-Golem",
        "original_stats": {"HP": 500, "ATK": 50, "DEF": 200},
        "weakness": "magic",
        "strength": "physical"
    }
    """
    # 5% chance
    import random
    if random.random() > 0.05:
        return {
            "success": False,
            "slime_id": slime_id,
            "message": "Form-Copy fehlgeschlagen!",
            "ai_message": "Ich konnte die Form nicht kopieren..."
        }

    # Copy at 80%
    slime_stats = copy_form_stats(original_stats)

    form = FormCopy(
        form_id=enemy_id,
        original_name=enemy_name,
        original_stats=original_stats,
        slime_stats=slime_stats,
        weakness=weakness,
        strength=strength,
        copied_at=datetime.now()
    )

    # Store
    if slime_id not in FORM_COPIES:
        FORM_COPIES[slime_id] = []

    FORM_COPIES[slime_id].append(form)

    return {
        "success": True,
        "slime_id": slime_id,
        "form": form.dict(),
        "message": f"✅ Form kopiert: {enemy_name}!",
        "ai_message": f"Ich habe {enemy_name} Form kopiert! Lass uns damit trainieren!"
    }


@router.get("/form/list")
@handle_errors()
async def list_copied_forms(slime_id: int):
    """List all copied forms for training"""
    forms = FORM_COPIES.get(slime_id, [])

    return {
        "success": True,
        "slime_id": slime_id,
        "forms": [f.dict() for f in forms],
        "count": len(forms)
    }


@router.post("/form/train-against")
@handle_errors()
async def train_against_form(slime_id: int, form_id: str):
    """
    Train against copied form (SAFE!)

    Learn enemy patterns without risk
    """
    if slime_id not in FORM_COPIES:
        raise HTTPException(
            status_code=404,
            detail="Keine kopierten Formen gefunden!"
        )

    forms = FORM_COPIES[slime_id]
    form = next((f for f in forms if f.form_id == form_id), None)

    if not form:
        raise HTTPException(
            status_code=404,
            detail=f"Form {form_id} nicht gefunden!"
        )

    form.times_trained_against += 1

    return {
        "success": True,
        "slime_id": slime_id,
        "form": form.dict(),
        "message": f"✅ Training gegen {form.original_name} gestartet!",
        "ai_message": f"Lass uns gegen meine {form.original_name}-Form trainieren!",
        "tips": [
            f"Schwach gegen: {form.weakness.value if form.weakness else 'unbekannt'}",
            f"Stark gegen: {form.strength if form.strength else 'unbekannt'}"
        ]
    }


# ==================== STATUS ENDPOINTS ====================

@router.get("/status")
@handle_errors()
async def get_slime_ai_status(slime_id: int):
    """
    Get complete 2-layer status

    Shows both personality (persistent) and skills (reset)
    """
    if slime_id not in PERSONALITY_MEMORIES or slime_id not in GAME_SKILLS:
        raise HTTPException(
            status_code=404,
            detail="Slime-KI nicht vollständig initialisiert!"
        )

    personality = PERSONALITY_MEMORIES[slime_id]
    skills = GAME_SKILLS[slime_id]
    forms = FORM_COPIES.get(slime_id, [])

    return {
        "success": True,
        "slime_id": slime_id,
        "ebene_1_personality": {
            "death_count": personality.death_count,
            "boss_knowledge_count": len(personality.boss_knowledge),
            "memories_count": len(personality.general_memories),
            "status": "✅ PERSISTENT"
        },
        "ebene_2_skills": {
            "current_level": skills.current_level,
            "learned_abilities_count": len(skills.learned_abilities),
            "reset_count": skills.reset_count,
            "last_reset": skills.last_reset,
            "status": "⚠️ RESETS BEI TOD"
        },
        "form_copies": {
            "count": len(forms),
            "forms": [f.original_name for f in forms]
        }
    }