"""
NAJIKA TEMPERATUR-SYSTEM
Regionsbasierte Temperatur-Mechaniken

Features:
- Spieler-Körpertemperatur (0-100)
- Regions-Basistemperaturen
- Tag/Nacht Zyklen
- Wetter-Effekte
- Kleidungs-Resistenzen
- Food-Buffs für Temperatur
- HP/Stamina-Effekte bei Extremen
"""

import time
import random
from typing import Dict, Optional, Tuple

# ===== REGION TEMPERATURES =====
# Basierend auf NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md
REGIONS = {
    # REGION 1: Heiße Dünen (Western/Desert)
    "heisse_duenen": {
        "name": "Heiße Dünen",
        "base_temp": 40,
        "day_variance": 15,     # Bis zu 55°C am Tag!
        "night_variance": -20,  # Runter auf 20°C nachts
        "biome": "desert",
        "danger_level": 2,      # Hohe Gefahr
        "slime_color": "dusty_gold"
    },
    # REGION 2: Samtmoos-Tiefwald (mit Dampf-Hain Stadt)
    "samtmoos_tiefwald": {
        "name": "Samtmoos-Tiefwald",
        "base_temp": 22,
        "day_variance": 6,      # +6 am Tag
        "night_variance": -4,   # -4 in der Nacht
        "biome": "forest",
        "danger_level": 0,      # Keine Temp-Gefahr (mild!)
        "slime_color": "moss_green"
    },
    # REGION 3: Salzwind-Küste (mit Salzige Bucht)
    "salzwind_kueste": {
        "name": "Salzwind-Küste",
        "base_temp": 25,
        "day_variance": 5,
        "night_variance": -3,
        "biome": "coast",
        "danger_level": 0,
        "slime_color": "ocean_blue"
    },
    # REGION 4: Blitzebene (Highland/Storms)
    "blitzebene": {
        "name": "Blitzebene",
        "base_temp": 18,
        "day_variance": 8,
        "night_variance": -10,
        "biome": "highland",
        "danger_level": 1,      # Leichte Kälte nachts
        "slime_color": "lightning_purple"
    },
    # REGION 5: Grünschlamm-Sumpf (Hexen-Gebiet)
    "gruenschlamm_sumpf": {
        "name": "Grünschlamm-Sumpf",
        "base_temp": 30,
        "day_variance": 3,
        "night_variance": -2,
        "biome": "swamp",
        "danger_level": 1,
        "humidity": 90,         # Schwül!
        "slime_color": "midnight_black"
    },
    # REGION 6: Reich der Drei (Kälte/Frost/Eis + Nekromantie)
    "reich_der_drei": {
        "name": "Reich der Drei - Kälte Frost Eis",
        "base_temp": -15,
        "day_variance": 5,
        "night_variance": -10,
        "biome": "ice",
        "danger_level": 3,      # SEHR gefährlich!
        "slime_color": "crystal_white",
        "elements": ["kaelte", "frost", "eis"]
    },
    # REGION 7: Magmaströme (Vulkan-Region)
    "magmastroeme": {
        "name": "Magmaströme",
        "base_temp": 50,
        "day_variance": 10,
        "night_variance": -5,
        "biome": "volcanic",
        "danger_level": 3,      # SEHR gefährlich!
        "slime_color": "molten_red"
    },
    # REGION 8: Tiefenhöhlen (Underground - unter Samtmoos)
    "tiefenhoehlen": {
        "name": "Tiefenhöhlen",
        "base_temp": 15,        # Konstant kühl unter der Erde
        "day_variance": 0,      # Kein Tag/Nacht unter der Erde
        "night_variance": 0,
        "biome": "caves",
        "danger_level": 1,
        "underground": True,
        "slime_color": "deep_purple"
    },
    # ENDGAME: Götterfels (Hub - Safe Zone)
    "goetterfels": {
        "name": "Götterfels",
        "base_temp": 20,        # Angenehm
        "day_variance": 3,
        "night_variance": -2,
        "biome": "mountain",
        "danger_level": 0,      # Safe Zone!
        "safe_zone": True
    }
}

# ===== CLOTHING SYSTEM =====
CLOTHING = {
    # Leichte Kleidung
    "cloth_robe": {
        "name": "Stoffrobe",
        "heat_resist": 10,
        "cold_resist": -5,
        "slot": "body"
    },
    "desert_robe": {
        "name": "Wüstenrobe",
        "heat_resist": 40,
        "cold_resist": -20,
        "slot": "body"
    },
    "summer_dress": {
        "name": "Sommerkleid",
        "heat_resist": 25,
        "cold_resist": -15,
        "slot": "body"
    },

    # Schwere Kleidung
    "fur_coat": {
        "name": "Pelzmantel",
        "heat_resist": -30,
        "cold_resist": 50,
        "slot": "body"
    },
    "winter_armor": {
        "name": "Winterrüstung",
        "heat_resist": -40,
        "cold_resist": 60,
        "slot": "body"
    },
    "ice_cloak": {
        "name": "Eismantel",
        "heat_resist": -20,
        "cold_resist": 45,
        "slot": "body"
    },

    # Magische Kleidung
    "gothic_lolita_enchanted": {
        "name": "Verzaubertes Gothic-Lolita Kleid",
        "heat_resist": 20,
        "cold_resist": 20,
        "slot": "body",
        "special": "najika_adaptive"  # Passt sich an!
    },
    "elemental_robe": {
        "name": "Elementarrobe",
        "heat_resist": 35,
        "cold_resist": 35,
        "slot": "body"
    },

    # Kopfbedeckung
    "straw_hat": {
        "name": "Strohhut",
        "heat_resist": 15,
        "cold_resist": -10,
        "slot": "head"
    },
    "fur_hood": {
        "name": "Fellkapuze",
        "heat_resist": -10,
        "cold_resist": 25,
        "slot": "head"
    },
    "megumin_hat": {
        "name": "Megumins Hexenhut",
        "heat_resist": 10,
        "cold_resist": 10,
        "slot": "head"
    }
}

# ===== FOOD BUFFS =====
TEMP_FOOD = {
    "fire_pepper": {
        "name": "Feuerpfeffer",
        "effect": "warming",
        "strength": 15,
        "duration": 300,  # 5 Minuten
        "description": "Wärmt von innen"
    },
    "ice_berry": {
        "name": "Eisbeere",
        "effect": "cooling",
        "strength": 15,
        "duration": 300,
        "description": "Kühlt den Körper"
    },
    "spicy_stew": {
        "name": "Scharfer Eintopf",
        "effect": "warming",
        "strength": 25,
        "duration": 600,  # 10 Minuten
        "description": "Hält lange warm"
    },
    "frozen_dessert": {
        "name": "Gefrorenes Dessert",
        "effect": "cooling",
        "strength": 25,
        "duration": 600,
        "description": "Erfrischend kalt"
    },
    "elemental_elixir": {
        "name": "Elementar-Elixier",
        "effect": "immunity",
        "strength": 100,
        "duration": 180,  # 3 Minuten
        "description": "Immun gegen Temperatur"
    },
    "hot_cocoa": {
        "name": "Heißer Kakao",
        "effect": "warming",
        "strength": 20,
        "duration": 240,
        "description": "Gemütlich warm"
    },
    "mint_tea": {
        "name": "Minztee",
        "effect": "cooling",
        "strength": 20,
        "duration": 240,
        "description": "Erfrischend kühl"
    }
}


class TemperatureSystem:
    def __init__(self):
        self.player_temp = 37.0  # Normale Körpertemperatur
        self.target_temp = 37.0
        self.current_region = "samtmoos_tiefwald"  # Start im milden Wald
        self.time_of_day = 12  # 0-24 Stunden
        self.weather = "clear"

        # Ausrüstung
        self.equipped_clothing = {
            "head": None,
            "body": "cloth_robe"
        }

        # Aktive Buffs
        self.active_buffs = []  # { type, strength, end_time }

        # Status
        self.is_overheating = False
        self.is_freezing = False
        self.hp_drain_rate = 0
        self.stamina_drain_rate = 0

        print("[TEMP] Temperatur-System initialisiert")

    def update(self, delta_time: float = 1.0) -> Dict:
        """
        Haupt-Update-Loop (sollte jede Sekunde aufgerufen werden)

        Returns:
            Dict mit Status-Updates
        """
        # 1. Berechne Umgebungstemperatur
        env_temp = self._calculate_environment_temp()

        # 2. Berechne effektive Temperatur (mit Kleidung/Buffs)
        effective_temp = self._calculate_effective_temp(env_temp)

        # 3. Passe Spieler-Temperatur an
        self._adjust_player_temp(effective_temp, delta_time)

        # 4. Berechne Effekte
        effects = self._calculate_effects()

        # 5. Aktualisiere Buffs
        self._update_buffs()

        return {
            "player_temp": round(self.player_temp, 1),
            "env_temp": round(env_temp, 1),
            "effective_temp": round(effective_temp, 1),
            "is_overheating": self.is_overheating,
            "is_freezing": self.is_freezing,
            "hp_drain": self.hp_drain_rate,
            "stamina_drain": self.stamina_drain_rate,
            "effects": effects,
            "region": REGIONS[self.current_region]["name"],
            "danger_level": REGIONS[self.current_region]["danger_level"]
        }

    def _calculate_environment_temp(self) -> float:
        """Berechnet die aktuelle Umgebungstemperatur"""
        region = REGIONS[self.current_region]
        base = region["base_temp"]

        # Tag/Nacht Zyklus (6-18 = Tag)
        if 6 <= self.time_of_day <= 18:
            time_factor = region["day_variance"]
            # Peak um 14 Uhr
            hour_factor = 1 - abs(self.time_of_day - 14) / 8
        else:
            time_factor = region["night_variance"]
            # Kälteste Zeit um 4 Uhr
            if self.time_of_day < 6:
                hour_factor = 1 - abs(self.time_of_day - 4) / 6
            else:
                hour_factor = 1 - abs(self.time_of_day - 28) / 6

        temp = base + (time_factor * hour_factor)

        # Wetter-Effekte
        if self.weather == "rain":
            temp -= 5
        elif self.weather == "storm":
            temp -= 10
        elif self.weather == "heatwave":
            temp += 10
        elif self.weather == "blizzard":
            temp -= 15

        # Chaotische Regionen
        if region.get("chaotic"):
            temp += random.uniform(-10, 10)

        return temp

    def _calculate_effective_temp(self, env_temp: float) -> float:
        """Berechnet die gefühlte Temperatur mit Kleidung/Buffs"""
        effective = env_temp

        # Kleidungs-Resistenzen
        total_heat_resist = 0
        total_cold_resist = 0

        for slot, item_id in self.equipped_clothing.items():
            if item_id and item_id in CLOTHING:
                item = CLOTHING[item_id]
                total_heat_resist += item.get("heat_resist", 0)
                total_cold_resist += item.get("cold_resist", 0)

                # Spezial: Najika-Kleidung passt sich an
                if item.get("special") == "najika_adaptive":
                    if env_temp > 35:
                        total_heat_resist += 15
                    elif env_temp < 10:
                        total_cold_resist += 15

        # Wende Resistenzen an
        if env_temp > 37:  # Heiß
            resistance_factor = total_heat_resist / 100
            effective = env_temp - (env_temp - 37) * resistance_factor
        elif env_temp < 37:  # Kalt
            resistance_factor = total_cold_resist / 100
            effective = env_temp + (37 - env_temp) * resistance_factor

        # Buff-Effekte
        for buff in self.active_buffs:
            if buff["type"] == "warming":
                effective += buff["strength"] * 0.5
            elif buff["type"] == "cooling":
                effective -= buff["strength"] * 0.5
            elif buff["type"] == "immunity":
                effective = 37  # Perfekte Temperatur

        return effective

    def _adjust_player_temp(self, effective_temp: float, delta_time: float):
        """Passt die Spieler-Körpertemperatur an"""
        # Temperatur bewegt sich langsam Richtung Umgebung
        diff = effective_temp - self.player_temp
        adjustment = diff * 0.02 * delta_time  # 2% pro Sekunde

        self.player_temp += adjustment

        # Clamp zwischen 30 und 44 (tödliche Grenzen)
        self.player_temp = max(30, min(44, self.player_temp))

    def _calculate_effects(self) -> list:
        """Berechnet Status-Effekte basierend auf Temperatur"""
        effects = []

        # Überhitzung (>40°C)
        if self.player_temp > 40:
            self.is_overheating = True
            severity = (self.player_temp - 40) / 4  # 0-1 basierend auf 40-44

            self.stamina_drain_rate = severity * 5  # Bis zu 5/s
            effects.append(f"🔥 Überhitzung! (-{self.stamina_drain_rate:.1f} Stamina/s)")

            if self.player_temp > 42:
                self.hp_drain_rate = severity * 2  # Bis zu 2/s
                effects.append(f"☠️ Hitzeschlag! (-{self.hp_drain_rate:.1f} HP/s)")
        else:
            self.is_overheating = False

        # Unterkühlung (<34°C)
        if self.player_temp < 34:
            self.is_freezing = True
            severity = (34 - self.player_temp) / 4  # 0-1 basierend auf 30-34

            self.stamina_drain_rate = severity * 3  # Bis zu 3/s
            effects.append(f"❄️ Unterkühlung! (-{self.stamina_drain_rate:.1f} Stamina/s)")
            effects.append(f"🐢 Bewegung verlangsamt ({int(severity * 30)}%)")

            if self.player_temp < 32:
                self.hp_drain_rate = severity * 2
                effects.append(f"☠️ Erfrierung! (-{self.hp_drain_rate:.1f} HP/s)")
        else:
            self.is_freezing = False

        # Normale Temperatur
        if not self.is_overheating and not self.is_freezing:
            self.hp_drain_rate = 0
            self.stamina_drain_rate = 0
            if 36 <= self.player_temp <= 38:
                effects.append("✅ Optimale Körpertemperatur")

        return effects

    def _update_buffs(self):
        """Entfernt abgelaufene Buffs"""
        current_time = time.time()
        self.active_buffs = [
            buff for buff in self.active_buffs
            if buff["end_time"] > current_time
        ]

    # ===== PUBLIC API =====

    def change_region(self, region_id: str) -> bool:
        """Wechselt die Region"""
        if region_id not in REGIONS:
            return False

        self.current_region = region_id
        print(f"[TEMP] Region gewechselt: {REGIONS[region_id]['name']}")
        return True

    def set_time(self, hour: int):
        """Setzt die Tageszeit (0-23)"""
        self.time_of_day = hour % 24

    def advance_time(self, hours: float):
        """Lässt Zeit vergehen"""
        self.time_of_day = (self.time_of_day + hours) % 24

    def set_weather(self, weather: str):
        """Setzt das Wetter"""
        valid = ["clear", "rain", "storm", "heatwave", "blizzard", "fog"]
        if weather in valid:
            self.weather = weather
            print(f"[TEMP] Wetter: {weather}")

    def equip_clothing(self, item_id: str) -> bool:
        """Rüstet Kleidung aus"""
        if item_id not in CLOTHING:
            return False

        item = CLOTHING[item_id]
        self.equipped_clothing[item["slot"]] = item_id
        print(f"[TEMP] Ausgerüstet: {item['name']}")
        return True

    def unequip_clothing(self, slot: str) -> bool:
        """Entfernt Kleidung"""
        if slot in self.equipped_clothing:
            self.equipped_clothing[slot] = None
            return True
        return False

    def consume_food(self, food_id: str) -> Dict:
        """Konsumiert Temperatur-Essen"""
        if food_id not in TEMP_FOOD:
            return {"success": False, "message": "Unbekanntes Item"}

        food = TEMP_FOOD[food_id]
        end_time = time.time() + food["duration"]

        self.active_buffs.append({
            "type": food["effect"],
            "strength": food["strength"],
            "end_time": end_time,
            "name": food["name"]
        })

        return {
            "success": True,
            "message": f"{food['name']} konsumiert! {food['description']}",
            "effect": food["effect"],
            "duration": food["duration"]
        }

    def get_region_info(self, region_id: str = None) -> Dict:
        """Gibt Informationen über eine Region zurück"""
        rid = region_id or self.current_region
        if rid not in REGIONS:
            return None

        region = REGIONS[rid]
        return {
            "id": rid,
            "name": region["name"],
            "base_temp": region["base_temp"],
            "biome": region["biome"],
            "danger_level": region["danger_level"],
            "recommended_gear": self._get_recommended_gear(rid)
        }

    def _get_recommended_gear(self, region_id: str) -> list:
        """Empfiehlt Ausrüstung für eine Region"""
        region = REGIONS[region_id]
        recommendations = []

        if region["base_temp"] > 35:
            recommendations.append("Wüstenrobe oder Leichte Kleidung")
            recommendations.append("Eisbeeren oder Gefrorenes Dessert")
        elif region["base_temp"] < 10:
            recommendations.append("Pelzmantel oder Winterrüstung")
            recommendations.append("Feuerpfeffer oder Scharfer Eintopf")
        else:
            recommendations.append("Normale Kleidung ausreichend")

        if region["danger_level"] >= 3:
            recommendations.append("⚠️ GEFÄHRLICH! Elementar-Elixier empfohlen!")

        return recommendations

    def get_status(self) -> Dict:
        """Gibt den kompletten Temperatur-Status zurück"""
        return {
            "player_temp": round(self.player_temp, 1),
            "region": self.current_region,
            "region_name": REGIONS[self.current_region]["name"],
            "time_of_day": self.time_of_day,
            "weather": self.weather,
            "clothing": self.equipped_clothing,
            "active_buffs": [
                {
                    "name": b.get("name", b["type"]),
                    "remaining": round(b["end_time"] - time.time(), 0)
                }
                for b in self.active_buffs
            ],
            "is_overheating": self.is_overheating,
            "is_freezing": self.is_freezing
        }


# ===== SINGLETON INSTANCE =====
TEMPERATURE_SYSTEM = None


def get_temperature_system() -> TemperatureSystem:
    """Gibt die Singleton-Instanz zurück"""
    global TEMPERATURE_SYSTEM
    if TEMPERATURE_SYSTEM is None:
        TEMPERATURE_SYSTEM = TemperatureSystem()
    return TEMPERATURE_SYSTEM


# ===== API FUNCTIONS (für Server-Integration) =====

def api_update_temperature() -> Dict:
    """API: Update und Status abrufen"""
    return get_temperature_system().update()


def api_change_region(region_id: str) -> Dict:
    """API: Region wechseln"""
    success = get_temperature_system().change_region(region_id)
    return {
        "success": success,
        "status": get_temperature_system().get_status()
    }


def api_consume_food(food_id: str) -> Dict:
    """API: Essen konsumieren"""
    return get_temperature_system().consume_food(food_id)


def api_equip_clothing(item_id: str) -> Dict:
    """API: Kleidung ausrüsten"""
    success = get_temperature_system().equip_clothing(item_id)
    return {
        "success": success,
        "status": get_temperature_system().get_status()
    }


def api_get_status() -> Dict:
    """API: Status abrufen"""
    return get_temperature_system().get_status()


def api_get_all_regions() -> Dict:
    """API: Alle Regionen abrufen"""
    return {
        region_id: get_temperature_system().get_region_info(region_id)
        for region_id in REGIONS.keys()
    }


# ===== TEST =====
if __name__ == "__main__":
    temp_sys = get_temperature_system()

    print("\n=== TEMPERATUR-SYSTEM TEST ===\n")

    # Test verschiedene Regionen (aktuelle Namen aus regions.json)
    for region_id in ["samtmoos_tiefwald", "heisse_duenen", "reich_der_drei"]:
        temp_sys.change_region(region_id)
        temp_sys.player_temp = 37.0  # Reset

        print(f"\n--- {REGIONS[region_id]['name']} ---")
        for _ in range(5):
            status = temp_sys.update(5)  # 5 Sekunden simulieren
            print(f"  Env: {status['env_temp']}°C | Player: {status['player_temp']}°C | Effects: {status['effects']}")

    print("\n=== TEST ABGESCHLOSSEN ===")
