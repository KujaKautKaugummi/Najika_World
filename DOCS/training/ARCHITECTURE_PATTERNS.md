# ARCHITECTURE PATTERNS

================================================================================

## 1. MVC - Model View Controller

**Verwendet in:** Web Apps, Desktop Apps

```python
# MODEL - Daten
class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

# VIEW - Anzeige
class CharacterView:
    def render(self, character):
        print(f"{character.name}: {character.hp} HP")

# CONTROLLER - Logik
class CharacterController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def take_damage(self, damage):
        self.model.hp -= damage
        self.view.render(self.model)
```

## 2. OBSERVER PATTERN

**Verwendet in:** Event-Systeme, UI Updates

```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer:
    def update(self, event):
        print(f"Received event: {event}")

# Nutzung
subject = Subject()
subject.attach(Observer())
subject.notify("HP_CHANGED")
```

## 3. FACTORY PATTERN

```python
class EnemyFactory:
    @staticmethod
    def create(enemy_type):
        if enemy_type == "rat":
            return Enemy("Rat", hp=10, damage=2)
        elif enemy_type == "skeleton":
            return Enemy("Skeleton", hp=30, damage=5)
        elif enemy_type == "boss":
            return Enemy("Boss", hp=100, damage=20)

# Nutzung
enemy = EnemyFactory.create("skeleton")
```

## 4. SINGLETON PATTERN

```python
class GameState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.score = 0
        return cls._instance

# Immer die gleiche Instanz
state1 = GameState()
state2 = GameState()
print(state1 is state2)  # True
```
