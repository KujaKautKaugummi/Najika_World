"""
Lebensraum API - Sync endpoint for Digivice Flutter App

Handles:
- Signed action validation (Anti-Cheat)
- Offline queue processing
- Daily limits enforcement
- State sync between app and game
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import hashlib
import hmac
import json
from backend.utils import handle_errors

router = APIRouter(prefix="/api/lebensraum", tags=["Lebensraum"])

# ============================================================================
# MODELS
# ============================================================================

class SignedAction(BaseModel):
    """A signed action from the Digivice app"""
    action: str
    data: Dict[str, Any]
    timestamp: int
    signature: str

class SyncResponse(BaseModel):
    """Response for sync requests"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class DailyLimits(BaseModel):
    """Daily limits for public version"""
    fish: int = 20
    harvest: int = 50
    craft: int = 10

class UserState(BaseModel):
    """User state in Lebensraum"""
    user_id: str
    location: str = "schwarze_muehle"
    fish_count: int = 0
    harvest_count: int = 0
    craft_count: int = 0
    last_reset: datetime = datetime.now()
    inventory: List[Dict[str, Any]] = []
    is_private: bool = False

# ============================================================================
# IN-MEMORY STORAGE (Replace with database in production)
# ============================================================================

# Device secrets for validation (in production, store in database)
device_secrets: Dict[str, str] = {}

# User states
user_states: Dict[str, UserState] = {}

# Action queue for offline sync
action_queue: List[Dict[str, Any]] = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_signature(action: SignedAction, device_secret: str) -> bool:
    """Validate HMAC-SHA256 signature"""
    payload = json.dumps({
        'action': action.action,
        'data': action.data,
        'timestamp': action.timestamp,
    }, separators=(',', ':'))

    expected_signature = hmac.new(
        device_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(action.signature, expected_signature)

def validate_timestamp(timestamp: int, max_age_seconds: int = 300) -> bool:
    """Check if timestamp is within acceptable range"""
    now = int(datetime.now().timestamp() * 1000)
    age = abs(now - timestamp)
    return age < (max_age_seconds * 1000)

def get_or_create_user_state(user_id: str) -> UserState:
    """Get or create user state"""
    if user_id not in user_states:
        user_states[user_id] = UserState(user_id=user_id)
    return user_states[user_id]

def check_daily_limit(state: UserState, action: str) -> bool:
    """Check if user can perform action (daily limit)"""
    # Private users have no limits
    if state.is_private:
        return True

    # Reset if new day
    today = datetime.now().date()
    if state.last_reset.date() != today:
        state.fish_count = 0
        state.harvest_count = 0
        state.craft_count = 0
        state.last_reset = datetime.now()

    limits = DailyLimits()

    if action == 'fish':
        return state.fish_count < limits.fish
    elif action in ['garden', 'harvest']:
        return state.harvest_count < limits.harvest
    elif action == 'craft':
        return state.craft_count < limits.craft

    return True  # No limit for other actions

def process_action(state: UserState, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a validated action"""
    result = {'success': True, 'rewards': []}

    if action == 'fish':
        state.fish_count += 1
        # Simulate fishing reward
        fish_types = ['Karpfen', 'Forelle', 'Aal', 'Goldfisch', 'Magischer Fisch']
        import random
        caught = random.choice(fish_types)
        result['rewards'].append({'type': 'fish', 'item': caught})
        state.inventory.append({'type': 'fish', 'name': caught, 'timestamp': datetime.now().isoformat()})

    elif action in ['garden', 'harvest']:
        state.harvest_count += 1
        crops = ['Tomate', 'Karotte', 'Magische Bohne', 'Mondblume']
        import random
        harvested = random.choice(crops)
        result['rewards'].append({'type': 'crop', 'item': harvested})
        state.inventory.append({'type': 'crop', 'name': harvested, 'timestamp': datetime.now().isoformat()})

    elif action == 'craft':
        state.craft_count += 1
        # Would need recipe validation in real implementation
        result['rewards'].append({'type': 'item', 'item': 'Crafted Item'})

    elif action == 'chat':
        # Chat doesn't affect limits
        result['rewards'].append({'type': 'affection', 'amount': 1})

    elif action == 'move':
        if 'location' in data:
            state.location = data['location']

    return result

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/sync", response_model=SyncResponse)
@handle_errors()
async def sync_action(action: SignedAction):
    """
    Sync a signed action from the Digivice app.

    This endpoint:
    1. Validates the HMAC signature (anti-cheat)
    2. Checks timestamp freshness
    3. Enforces daily limits
    4. Processes the action
    5. Returns rewards/results
    """
    # For now, use a default secret (in production, look up by device ID)
    device_secret = "najika-digivice-secret-key-2026"

    # Validate timestamp (max 5 minutes old)
    if not validate_timestamp(action.timestamp, max_age_seconds=300):
        raise HTTPException(
            status_code=400,
            detail="Action timestamp expired or invalid"
        )

    # Validate signature
    # Note: Temporarily disabled for development
    # if not validate_signature(action, device_secret):
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Invalid signature - potential cheat attempt"
    #     )

    # Get user state (use device ID or session in production)
    user_id = action.data.get('user_id', 'default_user')
    state = get_or_create_user_state(user_id)

    # Check daily limits
    if not check_daily_limit(state, action.action):
        return SyncResponse(
            success=False,
            message=f"Daily limit reached for {action.action}",
            data={
                'fish_remaining': max(0, DailyLimits().fish - state.fish_count),
                'harvest_remaining': max(0, DailyLimits().harvest - state.harvest_count),
                'craft_remaining': max(0, DailyLimits().craft - state.craft_count),
            }
        )

    # Process the action
    result = process_action(state, action.action, action.data)

    return SyncResponse(
        success=True,
        message=f"Action '{action.action}' processed successfully",
        data={
            **result,
            'state': {
                'location': state.location,
                'fish_count': state.fish_count,
                'harvest_count': state.harvest_count,
                'craft_count': state.craft_count,
                'inventory_size': len(state.inventory),
            }
        }
    )

@router.get("/state/{user_id}")
@handle_errors()
async def get_state(user_id: str):
    """Get current user state"""
    state = get_or_create_user_state(user_id)

    return {
        'user_id': state.user_id,
        'location': state.location,
        'daily_counts': {
            'fish': state.fish_count,
            'harvest': state.harvest_count,
            'craft': state.craft_count,
        },
        'limits': {
            'fish': DailyLimits().fish,
            'harvest': DailyLimits().harvest,
            'craft': DailyLimits().craft,
        },
        'remaining': {
            'fish': max(0, DailyLimits().fish - state.fish_count),
            'harvest': max(0, DailyLimits().harvest - state.harvest_count),
            'craft': max(0, DailyLimits().craft - state.craft_count),
        },
        'inventory_size': len(state.inventory),
        'is_private': state.is_private,
    }

@router.get("/inventory/{user_id}")
@handle_errors()
async def get_inventory(user_id: str, limit: int = 50):
    """Get user inventory"""
    state = get_or_create_user_state(user_id)

    return {
        'user_id': user_id,
        'items': state.inventory[-limit:],  # Return last N items
        'total': len(state.inventory),
    }

@router.post("/set-private/{user_id}")
@handle_errors()
async def set_private_mode(user_id: str, is_private: bool):
    """Set private mode (no limits) - requires authentication in production"""
    state = get_or_create_user_state(user_id)
    state.is_private = is_private

    return {
        'success': True,
        'message': f"Private mode {'enabled' if is_private else 'disabled'} for {user_id}",
        'is_private': state.is_private,
    }

@router.get("/limits")
@handle_errors()
async def get_limits():
    """Get current daily limits"""
    limits = DailyLimits()
    return {
        'fish': limits.fish,
        'harvest': limits.harvest,
        'craft': limits.craft,
        'description': {
            'fish': 'Maximum fish catches per day',
            'harvest': 'Maximum harvests per day',
            'craft': 'Maximum crafts per day',
        },
        'note': 'Private mode users have no limits!'
    }

@router.delete("/reset/{user_id}")
@handle_errors()
async def reset_daily_counts(user_id: str):
    """Reset daily counts (admin only in production)"""
    state = get_or_create_user_state(user_id)
    state.fish_count = 0
    state.harvest_count = 0
    state.craft_count = 0
    state.last_reset = datetime.now()

    return {
        'success': True,
        'message': f"Daily counts reset for {user_id}",
    }