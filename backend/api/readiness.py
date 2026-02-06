# readiness.py
# Najika World - Readiness API Router
# Endpoints für Autonomy-Gate Debugging und Kontrolle

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import sys
import os

# Backend-Pfad hinzufügen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from najika_readiness import (
    get_readiness_gate,
    compute_readiness,
    check_can_act,
    SystemGuard
)

router = APIRouter(prefix="/api/meta", tags=["readiness"])

# ==================== REQUEST MODELS ====================

class StateInput(BaseModel):
    """Input für State-basierte Berechnungen"""
    emotion: Optional[Dict[str, float]] = None
    trust_level: Optional[int] = 1
    user_autonomy_approval: Optional[bool] = None

class ActionCheckInput(BaseModel):
    """Input für Action-Check"""
    action: str
    state: Optional[StateInput] = None

# ==================== RESPONSE MODELS ====================

class ReadinessResponse(BaseModel):
    """Readiness Status Response"""
    score: float
    is_ready: bool
    threshold: float
    autonomy_level: str
    reasons: List[Dict[str, Any]]
    allowed_actions: List[str]

class ActionCheckResponse(BaseModel):
    """Action Check Response"""
    action: str
    allowed: bool
    reason: str
    requires_confirmation: bool
    readiness_score: float
    autonomy_level: str

# ==================== ENDPOINTS ====================

@router.get("/readiness", response_model=ReadinessResponse)
async def get_readiness_status():
    """
    Gibt aktuellen Readiness-Status zurück.

    Nützlich für:
    - UI Badge (Ready/Not Ready Anzeige)
    - Debugging der Autonomy-Gate
    - Monitoring
    """
    gate = get_readiness_gate()

    # Default State wenn keiner gesetzt
    default_state = {
        "emotion": {"joy": 0.5, "fear": 0.0, "anger": 0.0},
        "trust_level": 3,
        "user_autonomy_approval": None
    }

    result = gate.compute_readiness(default_state)

    return ReadinessResponse(
        score=result.score,
        is_ready=result.is_ready,
        threshold=result.threshold,
        autonomy_level=gate.autonomy_level,
        reasons=[
            {
                "category": r.category,
                "description": r.description,
                "impact": r.impact
            }
            for r in result.reasons
        ],
        allowed_actions=gate.get_allowed_actions()
    )

@router.post("/readiness", response_model=ReadinessResponse)
async def compute_readiness_with_state(state: StateInput):
    """
    Berechnet Readiness mit angegebenem State.

    Nützlich für:
    - "Was wäre wenn" Szenarien
    - Testing verschiedener States
    """
    gate = get_readiness_gate()

    state_dict = {
        "emotion": state.emotion or {"joy": 0.5, "fear": 0.0, "anger": 0.0},
        "trust_level": state.trust_level or 1,
        "user_autonomy_approval": state.user_autonomy_approval
    }

    result = gate.compute_readiness(state_dict)

    return ReadinessResponse(
        score=result.score,
        is_ready=result.is_ready,
        threshold=result.threshold,
        autonomy_level=gate.autonomy_level,
        reasons=[
            {
                "category": r.category,
                "description": r.description,
                "impact": r.impact
            }
            for r in result.reasons
        ],
        allowed_actions=gate.get_allowed_actions()
    )

@router.post("/can-act", response_model=ActionCheckResponse)
async def check_action_allowed(input: ActionCheckInput):
    """
    Prüft ob eine bestimmte Aktion erlaubt ist.

    Nützlich für:
    - Vor Ausführung einer Aktion prüfen
    - UI-Buttons aktivieren/deaktivieren
    """
    gate = get_readiness_gate()

    state_dict = {}
    if input.state:
        state_dict = {
            "emotion": input.state.emotion or {"joy": 0.5, "fear": 0.0, "anger": 0.0},
            "trust_level": input.state.trust_level or 1,
            "user_autonomy_approval": input.state.user_autonomy_approval
        }
    else:
        state_dict = {
            "emotion": {"joy": 0.5, "fear": 0.0, "anger": 0.0},
            "trust_level": 3,
            "user_autonomy_approval": None
        }

    result = check_can_act(input.action, state_dict)

    return ActionCheckResponse(
        action=input.action,
        allowed=result["guard"]["allowed"],
        reason=result["guard"]["reason"],
        requires_confirmation=result["guard"]["requires_confirmation"],
        readiness_score=result["readiness"]["score"],
        autonomy_level=result["autonomy_level"]
    )

@router.post("/record-error")
async def record_error(error_type: str = "generic"):
    """
    Registriert einen Fehler im Readiness-System.

    Fehler reduzieren temporär den Readiness-Score.
    """
    gate = get_readiness_gate()
    gate.record_error(error_type)

    return {
        "status": "recorded",
        "error_type": error_type,
        "error_count": gate.error_count
    }

@router.post("/record-interaction")
async def record_interaction():
    """
    Registriert eine User-Interaktion.

    Frische Interaktionen erhöhen den Readiness-Score.
    """
    gate = get_readiness_gate()
    gate.record_interaction()

    return {
        "status": "recorded",
        "last_interaction": gate.last_interaction.isoformat() if gate.last_interaction else None
    }

@router.get("/forbidden-actions")
async def get_forbidden_actions():
    """
    Gibt Liste der immer verbotenen Aktionen zurück.

    Diese Aktionen sind NIEMALS erlaubt, unabhängig vom Readiness-Score.
    """
    return {
        "forbidden": SystemGuard.FORBIDDEN_ACTIONS,
        "requires_confirmation": SystemGuard.REQUIRES_CONFIRMATION
    }

@router.post("/set-threshold")
async def set_readiness_threshold(threshold: float):
    """
    Setzt den Readiness-Threshold.

    Werte:
    - 0.0: Alles erlaubt (gefährlich!)
    - 0.65: Standard
    - 0.9: Sehr streng
    """
    if not 0.0 <= threshold <= 1.0:
        raise HTTPException(
            status_code=400,
            detail="Threshold muss zwischen 0.0 und 1.0 liegen"
        )

    gate = get_readiness_gate()
    gate.threshold = threshold
    gate.state.threshold = threshold

    return {
        "status": "updated",
        "new_threshold": threshold
    }

@router.get("/autonomy-levels")
async def get_autonomy_level_info():
    """
    Erklärt die Autonomie-Level.
    """
    return {
        "levels": {
            "A": {
                "name": "Reaktiv",
                "description": "Reagiert nur auf direkte Befehle",
                "score_range": "< 0.4"
            },
            "B": {
                "name": "Vorschläge",
                "description": "Kann Vorschläge machen, wartet auf Bestätigung",
                "score_range": "0.4 - 0.65"
            },
            "C": {
                "name": "Autonom",
                "description": "Kann eigenständig handeln",
                "score_range": "> 0.65 (threshold)"
            }
        },
        "current_level": get_readiness_gate().autonomy_level
    }
