# najika_behavior_hooks.py
# Najika World - USER_DEFINED Behavior Hooks
# Platzhalter-System für Inhalte die das AI nicht generieren kann/soll

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Callable, Any
from enum import Enum
import json
import os
from pathlib import Path

# ==================== HOOK TYPES ====================

class HookType(Enum):
    """Verschiedene Arten von Behavior Hooks"""
    # Animation Hooks
    ANIMATION = "animation"          # Welche Animation abspielen
    GESTURE = "gesture"              # Gesten während Sprechen
    FACIAL = "facial"                # Gesichtsausdruck

    # Sound Hooks
    VOICE_TONE = "voice_tone"        # Tonfall der Stimme
    SOUND_EFFECT = "sound_effect"    # Soundeffekt abspielen

    # Visual Hooks
    PARTICLE = "particle"            # Partikel-Effekte
    CAMERA = "camera"                # Kamera-Bewegung
    LIGHTING = "lighting"            # Beleuchtungsänderung

    # Behavior Hooks
    MOVEMENT = "movement"            # Wie bewegt sie sich
    IDLE = "idle"                    # Idle-Verhalten
    REACTION = "reaction"            # Reaktion auf Events

    # Content Hooks (für Inhalte die AI nicht generiert)
    NSFW = "nsfw"                    # NSFW Beschreibungen
    VIOLENCE = "violence"            # Gewalt-Beschreibungen
    CUSTOM = "custom"                # Frei definierbar

@dataclass
class BehaviorHook:
    """Ein einzelner Behavior Hook"""
    hook_id: str
    hook_type: HookType
    trigger: str                     # Wann wird der Hook ausgelöst
    content: str                     # Der Inhalt/Aktion
    priority: int = 5               # 1-10, höher = wichtiger
    conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "hook_id": self.hook_id,
            "hook_type": self.hook_type.value,
            "trigger": self.trigger,
            "content": self.content,
            "priority": self.priority,
            "conditions": self.conditions,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BehaviorHook":
        return cls(
            hook_id=data["hook_id"],
            hook_type=HookType(data["hook_type"]),
            trigger=data["trigger"],
            content=data["content"],
            priority=data.get("priority", 5),
            conditions=data.get("conditions", {}),
            metadata=data.get("metadata", {})
        )

# ==================== HOOK REGISTRY ====================

class HookRegistry:
    """
    Verwaltet alle USER_DEFINED Hooks.

    Das AI kann Platzhalter wie [USER_DEFINED:animation:happy]
    in seine Antworten einfügen. Diese werden dann durch
    registrierte Hooks ersetzt.
    """

    def __init__(self, hooks_dir: str = None):
        self.hooks: Dict[str, BehaviorHook] = {}
        self.hooks_by_type: Dict[HookType, List[BehaviorHook]] = {
            t: [] for t in HookType
        }
        self.hooks_dir = hooks_dir or self._default_hooks_dir()

        # Standard-Hooks laden
        self._load_default_hooks()

    def _default_hooks_dir(self) -> str:
        """Standard-Verzeichnis für Hook-Definitionen"""
        return str(Path(__file__).parent / "hooks")

    def _load_default_hooks(self):
        """Lädt Standard-Hooks"""
        # Animation Hooks
        self.register(BehaviorHook(
            hook_id="anim_happy",
            hook_type=HookType.ANIMATION,
            trigger="happy",
            content="Anim_Najika_Happy",
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="anim_sad",
            hook_type=HookType.ANIMATION,
            trigger="sad",
            content="Anim_Najika_Sad",
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="anim_excited",
            hook_type=HookType.ANIMATION,
            trigger="excited",
            content="Anim_Najika_Excited",
            priority=6
        ))
        self.register(BehaviorHook(
            hook_id="anim_explosion",
            hook_type=HookType.ANIMATION,
            trigger="explosion",
            content="Anim_Najika_Explosion_Cast",
            priority=10
        ))

        # Gesture Hooks
        self.register(BehaviorHook(
            hook_id="gesture_wave",
            hook_type=HookType.GESTURE,
            trigger="greeting",
            content="Gesture_Wave",
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="gesture_point",
            hook_type=HookType.GESTURE,
            trigger="pointing",
            content="Gesture_Point",
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="gesture_shrug",
            hook_type=HookType.GESTURE,
            trigger="unsure",
            content="Gesture_Shrug",
            priority=5
        ))

        # Voice Tone Hooks
        self.register(BehaviorHook(
            hook_id="voice_excited",
            hook_type=HookType.VOICE_TONE,
            trigger="excited",
            content=json.dumps({"pitch": 1.2, "speed": 1.1, "energy": 0.9}),
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="voice_sad",
            hook_type=HookType.VOICE_TONE,
            trigger="sad",
            content=json.dumps({"pitch": 0.9, "speed": 0.8, "energy": 0.4}),
            priority=5
        ))
        self.register(BehaviorHook(
            hook_id="voice_megumin",
            hook_type=HookType.VOICE_TONE,
            trigger="explosion_mode",
            content=json.dumps({"pitch": 1.3, "speed": 1.0, "energy": 1.0, "dramatic": True}),
            priority=8
        ))

        # Particle Hooks
        self.register(BehaviorHook(
            hook_id="particle_sparkle",
            hook_type=HookType.PARTICLE,
            trigger="happy",
            content="VFX_Sparkle_Happy",
            priority=3
        ))
        self.register(BehaviorHook(
            hook_id="particle_fire",
            hook_type=HookType.PARTICLE,
            trigger="explosion",
            content="VFX_Explosion_Fire",
            priority=10
        ))

        # Idle Hooks
        self.register(BehaviorHook(
            hook_id="idle_bored",
            hook_type=HookType.IDLE,
            trigger="idle_long",
            content="Idle_Bored_LookAround",
            conditions={"idle_time_seconds": 30}
        ))
        self.register(BehaviorHook(
            hook_id="idle_read",
            hook_type=HookType.IDLE,
            trigger="idle_long",
            content="Idle_ReadBook",
            conditions={"idle_time_seconds": 60, "personality": "shiro"}
        ))

    def register(self, hook: BehaviorHook):
        """Registriert einen neuen Hook"""
        self.hooks[hook.hook_id] = hook
        self.hooks_by_type[hook.hook_type].append(hook)

    def unregister(self, hook_id: str):
        """Entfernt einen Hook"""
        if hook_id in self.hooks:
            hook = self.hooks[hook_id]
            self.hooks_by_type[hook.hook_type].remove(hook)
            del self.hooks[hook_id]

    def get(self, hook_id: str) -> Optional[BehaviorHook]:
        """Gibt Hook nach ID zurück"""
        return self.hooks.get(hook_id)

    def find_by_trigger(
        self,
        hook_type: HookType,
        trigger: str,
        context: dict = None
    ) -> Optional[BehaviorHook]:
        """
        Findet passenden Hook für einen Trigger.

        Args:
            hook_type: Art des Hooks
            trigger: Der Trigger-String
            context: Optionaler Kontext für Condition-Matching

        Returns:
            Der beste passende Hook oder None
        """
        candidates = []

        for hook in self.hooks_by_type[hook_type]:
            if hook.trigger == trigger:
                if self._check_conditions(hook, context):
                    candidates.append(hook)

        if not candidates:
            return None

        # Nach Priorität sortieren
        candidates.sort(key=lambda h: h.priority, reverse=True)
        return candidates[0]

    def _check_conditions(self, hook: BehaviorHook, context: dict = None) -> bool:
        """Prüft ob Conditions erfüllt sind"""
        if not hook.conditions:
            return True

        if context is None:
            return True

        for key, required_value in hook.conditions.items():
            if key not in context:
                return False
            if context[key] != required_value:
                return False

        return True

    def resolve_placeholder(self, placeholder: str, context: dict = None) -> str:
        """
        Löst einen [USER_DEFINED:type:trigger] Platzhalter auf.

        Format: [USER_DEFINED:hook_type:trigger]
        Beispiel: [USER_DEFINED:animation:happy]

        Returns:
            Den aufgelösten Content oder den Original-Platzhalter
        """
        if not placeholder.startswith("[USER_DEFINED:"):
            return placeholder

        # Parse Platzhalter
        inner = placeholder[14:-1]  # Entferne [USER_DEFINED: und ]
        parts = inner.split(":")

        if len(parts) < 2:
            return placeholder

        try:
            hook_type = HookType(parts[0])
            trigger = parts[1]
        except ValueError:
            return placeholder

        # Hook suchen
        hook = self.find_by_trigger(hook_type, trigger, context)

        if hook:
            return hook.content
        else:
            return placeholder

    def process_text(self, text: str, context: dict = None) -> str:
        """
        Verarbeitet Text und ersetzt alle USER_DEFINED Platzhalter.
        """
        import re

        pattern = r'\[USER_DEFINED:[^\]]+\]'

        def replacer(match):
            return self.resolve_placeholder(match.group(0), context)

        return re.sub(pattern, replacer, text)

    def save_to_file(self, filepath: str):
        """Speichert alle Hooks in Datei"""
        data = {
            "hooks": [h.to_dict() for h in self.hooks.values()]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filepath: str):
        """Lädt Hooks aus Datei"""
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for hook_data in data.get("hooks", []):
            hook = BehaviorHook.from_dict(hook_data)
            self.register(hook)

# ==================== HOOK TEMPLATES ====================

class HookTemplates:
    """Vordefinierte Hook-Templates für häufige Fälle"""

    @staticmethod
    def create_emotion_animation(emotion: str, animation_name: str) -> BehaviorHook:
        """Erstellt Animation-Hook für Emotion"""
        return BehaviorHook(
            hook_id=f"anim_{emotion}",
            hook_type=HookType.ANIMATION,
            trigger=emotion,
            content=animation_name,
            priority=5
        )

    @staticmethod
    def create_reaction_chain(
        trigger: str,
        animation: str,
        particle: str = None,
        sound: str = None
    ) -> List[BehaviorHook]:
        """Erstellt eine Kette von zusammenhängenden Hooks"""
        hooks = []

        hooks.append(BehaviorHook(
            hook_id=f"chain_{trigger}_anim",
            hook_type=HookType.ANIMATION,
            trigger=trigger,
            content=animation,
            priority=6
        ))

        if particle:
            hooks.append(BehaviorHook(
                hook_id=f"chain_{trigger}_particle",
                hook_type=HookType.PARTICLE,
                trigger=trigger,
                content=particle,
                priority=5
            ))

        if sound:
            hooks.append(BehaviorHook(
                hook_id=f"chain_{trigger}_sound",
                hook_type=HookType.SOUND_EFFECT,
                trigger=trigger,
                content=sound,
                priority=5
            ))

        return hooks

    @staticmethod
    def create_personality_override(
        personality: str,
        voice_settings: dict,
        idle_animation: str
    ) -> List[BehaviorHook]:
        """Erstellt Hooks für eine Persönlichkeit"""
        return [
            BehaviorHook(
                hook_id=f"personality_{personality}_voice",
                hook_type=HookType.VOICE_TONE,
                trigger=f"active_{personality}",
                content=json.dumps(voice_settings),
                priority=7
            ),
            BehaviorHook(
                hook_id=f"personality_{personality}_idle",
                hook_type=HookType.IDLE,
                trigger="idle",
                content=idle_animation,
                conditions={"active_personality": personality},
                priority=6
            )
        ]

# ==================== SINGLETON & API ====================

_hook_registry: Optional[HookRegistry] = None

def get_hook_registry() -> HookRegistry:
    """Gibt die globale Hook-Registry zurück"""
    global _hook_registry
    if _hook_registry is None:
        _hook_registry = HookRegistry()
    return _hook_registry

def resolve_hooks(text: str, context: dict = None) -> str:
    """Löst alle USER_DEFINED Platzhalter in Text auf"""
    registry = get_hook_registry()
    return registry.process_text(text, context)

def get_animation_for_emotion(emotion: str) -> Optional[str]:
    """Gibt Animation für eine Emotion zurück"""
    registry = get_hook_registry()
    hook = registry.find_by_trigger(HookType.ANIMATION, emotion)
    return hook.content if hook else None

def get_voice_settings(mood: str) -> Optional[dict]:
    """Gibt Voice-Settings für eine Stimmung zurück"""
    registry = get_hook_registry()
    hook = registry.find_by_trigger(HookType.VOICE_TONE, mood)
    if hook:
        return json.loads(hook.content)
    return None

# ==================== TEST ====================

if __name__ == "__main__":
    registry = HookRegistry()

    # Test Placeholder Resolution
    test_texts = [
        "Najika springt vor Freude! [USER_DEFINED:animation:happy]",
        "Sie wirkt nachdenklich... [USER_DEFINED:gesture:unsure]",
        "EXPLOSION!!! [USER_DEFINED:animation:explosion] [USER_DEFINED:particle:explosion]",
        "Hallo! [USER_DEFINED:gesture:greeting] Schön dich zu sehen!",
    ]

    print("=" * 60)
    print("NAJIKA BEHAVIOR HOOKS - TEST")
    print("=" * 60)

    for text in test_texts:
        resolved = registry.process_text(text)
        print(f"\nOriginal: {text}")
        print(f"Resolved: {resolved}")

    # Test Hook Lookup
    print("\n" + "=" * 60)
    print("HOOK LOOKUP TEST")
    print("=" * 60)

    emotions = ["happy", "sad", "excited", "explosion"]
    for emotion in emotions:
        hook = registry.find_by_trigger(HookType.ANIMATION, emotion)
        if hook:
            print(f"{emotion}: {hook.content}")
        else:
            print(f"{emotion}: No hook found")

    # Test Voice Settings
    print("\n" + "=" * 60)
    print("VOICE SETTINGS TEST")
    print("=" * 60)

    moods = ["excited", "sad", "explosion_mode"]
    for mood in moods:
        settings = get_voice_settings(mood)
        if settings:
            print(f"{mood}: {settings}")
        else:
            print(f"{mood}: No settings found")
