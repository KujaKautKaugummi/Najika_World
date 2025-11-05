"""
PYTHON BASICS - Training Data für Najika
Grundlegende Python-Konzepte und Syntax
"""

# ============================================
# VARIABLEN & DATENTYPEN
# ============================================

# Zahlen
number = 42
pi = 3.14159
is_active = True

# Strings
name = "Najika"
greeting = f"Hallo, ich bin {name}!"

# Listen
explosion_targets = ["Dämon", "Drache", "Boss", "Burg"]
damage_values = [100, 250, 500, 1000]

# Dictionaries
character = {
    "name": "Megumin",
    "level": 50,
    "class": "Arch Wizard",
    "specialty": "EXPLOSION"
}

# ============================================
# FUNKTIONEN
# ============================================

def greet_user(username):
    """Begrüßt einen User"""
    return f"EXPLOSION!!! Willkommen {username}! ✨"

def calculate_damage(base_damage, multiplier=1.5):
    """Berechnet Schadenswert"""
    return int(base_damage * multiplier)

def read_file(file_path):
    """Liest eine Datei"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "FEHLER: Datei nicht gefunden!"

def write_file(file_path, content):
    """Schreibt eine Datei"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Datei gespeichert: {file_path}"

# ============================================
# KLASSEN (OOP)
# ============================================

class Character:
    """Charakter-Klasse"""

    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def take_damage(self, damage):
        """Nimmt Schaden"""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def is_alive(self):
        """Prüft ob Charakter lebt"""
        return self.hp > 0

    def attack_enemy(self, enemy):
        """Greift Gegner an"""
        damage = self.attack
        enemy.take_damage(damage)
        return f"{self.name} greift {enemy.name} für {damage} Schaden an!"

class Megumin(Character):
    """Megumin - EXPLOSION-Spezialistin"""

    def __init__(self):
        super().__init__("Megumin", hp=100, attack=50)
        self.mana = 100

    def cast_explosion(self, target):
        """Wirkt EXPLOSION-Zauber"""
        if self.mana < 100:
            return "Nicht genug Mana für EXPLOSION!"

        self.mana = 0
        damage = 999
        target.take_damage(damage)
        return f"✨ EXPLOSION!!! {target.name} nimmt {damage} Schaden!"

# ============================================
# LIST COMPREHENSIONS & LAMBDA
# ============================================

# List Comprehension
squares = [x**2 for x in range(10)]
even_numbers = [x for x in range(20) if x % 2 == 0]

# Lambda-Funktionen
double = lambda x: x * 2
is_even = lambda x: x % 2 == 0

# Map/Filter/Reduce
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# ============================================
# ERROR HANDLING
# ============================================

def safe_divide(a, b):
    """Division mit Error-Handling"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "FEHLER: Division durch 0!"
    except TypeError:
        return "FEHLER: Ungültiger Datentyp!"
    finally:
        print("Division abgeschlossen")

# ============================================
# DATEIEN & PFADE
# ============================================

from pathlib import Path

def list_files(directory):
    """Listet Dateien in Verzeichnis"""
    path = Path(directory)

    if not path.exists():
        return []

    files = []
    for item in path.iterdir():
        if item.is_file():
            files.append(item.name)

    return files

# ============================================
# JSON-VERARBEITUNG
# ============================================

import json

def save_to_json(data, file_path):
    """Speichert Daten als JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_from_json(file_path):
    """Lädt Daten aus JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ============================================
# ASYNC/AWAIT (Fortgeschritten)
# ============================================

import asyncio

async def async_task(name, delay):
    """Asynchrone Task"""
    print(f"Task {name} startet...")
    await asyncio.sleep(delay)
    print(f"Task {name} fertig!")
    return f"Ergebnis von {name}"

async def main():
    """Führt mehrere Tasks parallel aus"""
    results = await asyncio.gather(
        async_task("A", 1),
        async_task("B", 2),
        async_task("C", 0.5)
    )
    return results

# ============================================
# WICHTIGE TIPPS
# ============================================

"""
PYTHON BEST PRACTICES:

1. Verwende sprechende Variablennamen
2. Schreibe Docstrings für Funktionen
3. Nutze Type Hints (ab Python 3.5):
   def greet(name: str) -> str:
       return f"Hallo {name}"

4. Verwende List Comprehensions statt Loops (wenn möglich)
5. Error-Handling mit try/except
6. Nutze 'with' für File-Operations
7. Vermeide globale Variablen
8. Schreibe Tests (unittest, pytest)
9. Formatiere Code mit black/autopep8
10. Nutze virtuelle Environments (venv, conda)
"""

# ============================================
# BEISPIEL-USAGE
# ============================================

if __name__ == "__main__":
    # Teste Funktionen
    print(greet_user("Kuja"))
    print(calculate_damage(100))

    # Teste Klassen
    megumin = Megumin()
    enemy = Character("Dämon", hp=500, attack=30)
    print(megumin.cast_explosion(enemy))

    # Teste List Comprehension
    print("Gerade Zahlen:", even_numbers)
