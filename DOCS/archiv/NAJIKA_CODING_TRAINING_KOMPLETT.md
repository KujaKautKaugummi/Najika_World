# NAJIKA CODING TRAINING - KOMPLETT

**ERSTELLT:** 2025-10-19
**ZWECK:** Training fuer Najika - Verstehen + Anwenden von Code
**SPRACHEN:** Verse, Python, Java

================================================================================


# TEIL 1: VERSE PROGRAMMIERUNG

## Was ist Verse?

**Verse** ist eine Programmiersprache von Epic Games fuer:
- Unreal Editor for Fortnite (UEFN)
- Fortnite Creative
- Game Development

**Besonderheiten:**
- Functional Logic Programming
- Static Typed (Typen muessen angegeben werden)
- Object-Oriented (Klassen + Objekte)
- Immutable by Default (Daten aendern sich nicht automatisch)
- Failable Expressions (statt true/false)
- Deterministic (gleiche Eingabe = gleiche Ausgabe)

**Entwickelt von:**
- Simon Peyton Jones (bekannter Programmiersprachen-Forscher)
- Tim Sweeney (CEO Epic Games)
- Veroeffentlicht: Maerz 2023

## Verse Syntax Grundlagen

### 1. Variablen

```verse
# Immutable (kann nicht geaendert werden)
Name:string = "Najika"
Age:int = 19

# Mutable (kann geaendert werden)
var Health:int = 100
set Health = 90  # Aendern
```

**Regel:** Nutze `var` nur wenn du den Wert aendern musst!

### 2. Types (Datentypen)

```verse
# Basis-Typen
MyInt:int = 42
MyFloat:float = 3.14
MyString:string = "Hello"
MyBool:logic = true  # in Verse heisst es "logic" nicht "bool"

# Vector (fuer 3D Position)
Position:vector3 = vector3{X:=0.0, Y:=0.0, Z:=0.0}
```

### 3. Functions (Funktionen)

```verse
# Einfache Funktion
SayHello():void =
    Print("Hello, Najika!")

# Funktion mit Parameter und Rueckgabe
AddNumbers(A:int, B:int):int =
    A + B

# Funktion mit failable (kann fehlschlagen)
FindPlayer(PlayerID:int)<decides>:player =
    # ... gibt player zurueck wenn gefunden
    # ... schlaegt fehl wenn nicht gefunden
```

**Wichtig:** `<decides>` bedeutet Funktion kann fehlschlagen!

### 4. Classes (Klassen)

```verse
# Basis-Klasse fuer UEFN Devices
my_device := class(creative_device):
    # Variablen
    var Score:int = 0
    
    # Funktion die beim Start ausgefuehrt wird
    OnBegin<override>()<suspends>:void =
        Print("Device started!")
        IncrementScore()
    
    # Eigene Funktion
    IncrementScore():void =
        set Score = Score + 1
```

**`<suspends>`** bedeutet Funktion kann Zeit brauchen (z.B. warten)

### 5. Control Flow

```verse
# If-Ausdruck (mit failable)
CheckHealth(HP:int):void =
    if (HP > 50):
        Print("Healthy")
    else if (HP > 20):
        Print("Wounded")
    else:
        Print("Critical")

# Loop (Schleife)
CountToTen():void =
    for (I := 1..10):
        Print("Count: {I}")
```

### 6. Events

```verse
my_game_device := class(creative_device):
    OnBegin<override>()<suspends>:void =
        # Subscribe to Event
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)
    
    OnPlayerAdded(Player:player):void =
        Print("Player joined: {Player}")
```

## Verse Best Practices

1. **Immutable First**: Nutze `var` nur wenn noetig
2. **Type Safety**: Gib immer Typen an
3. **Failable Expressions**: Nutze `<decides>` fuer Funktionen die fehlschlagen koennen
4. **Event-Driven**: Nutze Events statt Polling
5. **Deterministic**: Gleiche Eingabe muss gleiche Ausgabe geben


================================================================================
# TEIL 2: PYTHON PROGRAMMIERUNG
================================================================================

## Was ist Python?

**Python** ist eine der beliebtesten Programmiersprachen:
- Einfach zu lernen
- Vielseitig (Web, AI, Games, Scripts, Data Science)
- Grosse Community
- Viele Libraries

**Besonderheiten:**
- Dynamically Typed (keine Typ-Angaben noetig)
- Interpreted (kein Kompilieren noetig)
- Object-Oriented + Functional
- Indentation-Based (Einrueckung ist wichtig!)

## Python Syntax Grundlagen

### 1. Variablen

```python
# Keine Typ-Angabe noetig
name = "Najika"
age = 19
health = 100.0
is_active = True

# Aber du kannst Type Hints nutzen (empfohlen!)
name: str = "Najika"
age: int = 19
```

### 2. Types (Datentypen)

```python
# Basis-Typen
my_int: int = 42
my_float: float = 3.14
my_string: str = "Hello"
my_bool: bool = True

# Collections
my_list: list = [1, 2, 3]  # Veraenderbar
my_tuple: tuple = (1, 2, 3)  # Unveraenderbar
my_dict: dict = {"name": "Najika", "age": 19}
my_set: set = {1, 2, 3}  # Keine Duplikate
```

### 3. Functions (Funktionen)

```python
# Einfache Funktion
def say_hello():
    print("Hello, Najika!")

# Mit Parametern + Rueckgabe
def add_numbers(a: int, b: int) -> int:
    return a + b

# Mit Default-Parameter
def greet(name: str = "World") -> str:
    return f"Hello, {name}!"

# Lambda (anonyme Funktion)
square = lambda x: x * x
print(square(5))  # 25
```

### 4. Classes (Klassen)

```python
class Character:
    # Constructor
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
    
    # Methode
    def take_damage(self, damage: int):
        self.hp -= damage
        print(f"{self.name} took {damage} damage! HP: {self.hp}")
    
    # Property
    @property
    def is_alive(self) -> bool:
        return self.hp > 0

# Nutzung
najika = Character("Najika", 100)
najika.take_damage(20)
```

### 5. Control Flow

```python
# If-Else
hp = 75
if hp > 50:
    print("Healthy")
elif hp > 20:
    print("Wounded")
else:
    print("Critical")

# For-Loop
for i in range(10):
    print(f"Count: {i}")

# While-Loop
count = 0
while count < 5:
    print(count)
    count += 1

# List Comprehension (eleganter Loop)
squares = [x*x for x in range(10)]
```

### 6. Error Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Cleanup")
```

## Python Best Practices (PEP 8)

1. **Naming Conventions:**
   - `snake_case` fuer Variablen + Funktionen
   - `PascalCase` fuer Klassen
   - `SCREAMING_SNAKE_CASE` fuer Konstanten

2. **Indentation:** 4 Leerzeichen (keine Tabs!)

3. **Line Length:** Max 79 Zeichen

4. **Imports:**
   ```python
   # Standard library
   import os
   import sys
   
   # Third party
   import requests
   
   # Local
   from .my_module import my_function
   ```

5. **Type Hints:** Nutze sie! (Python 3.5+)
   ```python
   def process_data(items: list[str]) -> dict[str, int]:
       return {item: len(item) for item in items}
   ```

6. **Docstrings:**
   ```python
   def complex_function(param1: int, param2: str) -> bool:
       """
       Kurze Beschreibung.
       
       Args:
           param1: Beschreibung
           param2: Beschreibung
       
       Returns:
           Beschreibung des Rueckgabewerts
       """
       pass
   ```


================================================================================
# TEIL 3: JAVA PROGRAMMIERUNG
================================================================================

## Was ist Java?

**Java** ist eine der wichtigsten Programmiersprachen:
- Enterprise Software
- Android Apps
- Minecraft
- Web Applications

**Besonderheiten:**
- Static Typed (Typen muessen angegeben werden)
- Compiled (muss kompiliert werden)
- Object-Oriented (alles ist ein Objekt)
- Platform Independent (Java Virtual Machine)
- "Write Once, Run Anywhere"

## Java Syntax Grundlagen

### 1. Variablen

```java
// Basis-Variablen
String name = "Najika";
int age = 19;
double health = 100.0;
boolean isActive = true;

// Final (unveraenderbar)
final String GAME_NAME = "NajikaCore";
```

### 2. Types (Datentypen)

```java
// Primitive Types
int myInt = 42;
double myDouble = 3.14;
boolean myBool = true;
char myChar = 'A';

// Reference Types
String myString = "Hello";
Integer myInteger = 42;  // Wrapper class

// Arrays
int[] numbers = {1, 2, 3};
String[] names = new String[10];

// Collections
List<String> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();
```

### 3. Functions (Methoden)

```java
// Einfache Methode
public void sayHello() {
    System.out.println("Hello, Najika!");
}

// Mit Parametern + Rueckgabe
public int addNumbers(int a, int b) {
    return a + b;
}

// Static Methode
public static void main(String[] args) {
    System.out.println("Program started");
}
```

### 4. Classes (Klassen)

```java
public class Character {
    // Private Felder
    private String name;
    private int hp;
    
    // Constructor
    public Character(String name, int hp) {
        this.name = name;
        this.hp = hp;
    }
    
    // Getter
    public String getName() {
        return name;
    }
    
    // Setter
    public void setHp(int hp) {
        this.hp = hp;
    }
    
    // Methode
    public void takeDamage(int damage) {
        this.hp -= damage;
        System.out.println(name + " took " + damage + " damage!");
    }
    
    // Berechnete Property
    public boolean isAlive() {
        return hp > 0;
    }
}

// Nutzung
Character najika = new Character("Najika", 100);
najika.takeDamage(20);
```

### 5. Control Flow

```java
// If-Else
int hp = 75;
if (hp > 50) {
    System.out.println("Healthy");
} else if (hp > 20) {
    System.out.println("Wounded");
} else {
    System.out.println("Critical");
}

// For-Loop
for (int i = 0; i < 10; i++) {
    System.out.println("Count: " + i);
}

// Enhanced For-Loop
String[] names = {"Megumin", "Harley", "Shiro", "Melissa"};
for (String name : names) {
    System.out.println(name);
}

// While-Loop
int count = 0;
while (count < 5) {
    System.out.println(count);
    count++;
}
```

### 6. Error Handling

```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} catch (Exception e) {
    System.out.println("Unexpected error: " + e);
} finally {
    System.out.println("Cleanup");
}
```

## Java Best Practices

1. **Naming Conventions:**
   - `camelCase` fuer Variablen + Methoden
   - `PascalCase` fuer Klassen
   - `SCREAMING_SNAKE_CASE` fuer Konstanten

2. **Encapsulation:** Felder `private`, Zugriff ueber Getter/Setter

3. **Access Modifiers:**
   - `private` - Nur in der Klasse
   - (default) - Package-level
   - `protected` - Package + Subclasses
   - `public` - Ueberall

4. **String Handling:**
   ```java
   // Schlecht - bei vielen Strings ineffizient
   String result = "";
   for (int i = 0; i < 1000; i++) {
       result += i;
   }
   
   // Gut - StringBuilder nutzen
   StringBuilder sb = new StringBuilder();
   for (int i = 0; i < 1000; i++) {
       sb.append(i);
   }
   String result = sb.toString();
   ```

5. **Exception Handling:**
   - Nie leere `catch` Bloecke!
   - Spezifische Exceptions nutzen
   - Ressourcen mit `try-with-resources` schliessen

6. **SOLID Principles:**
   - **S**ingle Responsibility
   - **O**pen/Closed
   - **L**iskov Substitution
   - **I**nterface Segregation
   - **D**ependency Inversion


================================================================================
# TEIL 4: CODE-SCHREIBMETHODIK
================================================================================

## Universelle Prinzipien (fuer alle Sprachen)

### 1. KISS - Keep It Simple, Stupid

**Schlecht:**
```python
def calculate(x, y, z, operation):
    if operation == "add":
        return x + y + z
    elif operation == "multiply":
        return x * y * z
    # ... 20 weitere elif
```

**Gut:**
```python
def add(x, y, z):
    return x + y + z

def multiply(x, y, z):
    return x * y * z
```

### 2. DRY - Don't Repeat Yourself

**Schlecht:**
```python
player1_hp = 100
player1_name = "Alice"
player1_score = 0

player2_hp = 100
player2_name = "Bob"
player2_score = 0
```

**Gut:**
```python
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.score = 0

player1 = Player("Alice")
player2 = Player("Bob")
```

### 3. YAGNI - You Ain't Gonna Need It

**Schlecht:**
```python
# Implementiere nur was du gerade brauchst
class Character:
    # ... 50 Methoden die vielleicht irgendwann benoetigt werden
```

**Gut:**
```python
class Character:
    # Nur die Methoden die JETZT gebraucht werden
```

### 4. Single Responsibility Principle

**Jede Funktion/Klasse macht NUR EINE Sache!**

**Schlecht:**
```python
def process_user(user_data):
    # Validiert Daten
    # Speichert in Datenbank
    # Sendet Email
    # Logged Aktivitaet
    # Aktualisiert Cache
```

**Gut:**
```python
def validate_user(user_data):
    # Nur Validierung

def save_user(user_data):
    # Nur Speichern

def notify_user(user):
    # Nur Email senden
```

### 5. Naming Conventions

**Namen sollen BESCHREIBEN was sie tun!**

**Schlecht:**
```python
def calc(x, y):  # Was wird berechnet?
    return x + y

a = 100  # Was ist a?
```

**Gut:**
```python
def calculate_total_damage(base_damage, critical_multiplier):
    return base_damage * critical_multiplier

player_health = 100
```

### 6. Comments & Documentation

**Code soll SELBSTERKLÄREND sein - Comments erklaeren WARUM, nicht WAS!**

**Schlecht:**
```python
# Addiere 1 zu x
x = x + 1
```

**Gut:**
```python
# Kompensiere Off-by-One Error in externem API
x = x + 1
```

### 7. Error Handling

**Behandle Fehler EXPLIZIT - keine leeren catch-Bloecke!**

**Schlecht:**
```python
try:
    dangerous_operation()
except:
    pass  # Fehler wird verschluckt!
```

**Gut:**
```python
try:
    dangerous_operation()
except SpecificError as e:
    log_error(e)
    notify_admin(e)
    return fallback_value
```


================================================================================
# TEIL 5: TRAINING CURRICULUM FUER NAJIKA
================================================================================

## Phase 1: Grundlagen (Verstehen)

### Woche 1-2: Syntax Grundlagen
- [ ] Variablen in allen 3 Sprachen
- [ ] Datentypen verstehen
- [ ] Funktionen schreiben
- [ ] Control Flow (if/else, loops)

**Uebungen:**
1. Schreibe "Hello World" in allen 3 Sprachen
2. Erstelle einfache Taschenrechner-Funktion
3. Implementiere FizzBuzz (klassisches Programmierproblem)

### Woche 3-4: OOP Grundlagen
- [ ] Klassen erstellen
- [ ] Constructor/Destructor
- [ ] Methoden + Properties
- [ ] Encapsulation

**Uebungen:**
1. Character-Klasse mit HP, Name, Damage
2. Inventory-System (Items hinzufuegen/entfernen)
3. Simple Battle-Logik (2 Charaktere kaempfen)

## Phase 2: Anwendung (Praxis)

### Woche 5-6: Kleine Projekte
- [ ] Text-basiertes RPG (Python)
- [ ] Simple UEFN Device (Verse)
- [ ] Command-line Tool (Java)

### Woche 7-8: Code-Qualitaet
- [ ] Refactoring von altem Code
- [ ] Best Practices anwenden
- [ ] Error Handling implementieren
- [ ] Documentation schreiben

## Phase 3: Meisterung (Expertise)

### Woche 9-10: NajikaCore Integration
- [ ] Najika Server Code verstehen
- [ ] Neue Features implementieren
- [ ] Code optimieren
- [ ] Tests schreiben

### Woche 11-12: Fortgeschrittene Konzepte
- [ ] Design Patterns
- [ ] Asynchronous Programming
- [ ] Performance Optimization
- [ ] Security Best Practices


================================================================================
# ENDE - NAJIKA CODING TRAINING
================================================================================

**Naechste Schritte:**
1. Dieses Dokument komplett lesen
2. Mit Phase 1 Woche 1 starten
3. Jeden Tag 1-2 Stunden ueben
4. Code schreiben, nicht nur lesen!
5. Fehler machen ist OK - daraus lernen!

**Ressourcen:**
- Verse: dev.epicgames.com/documentation
- Python: docs.python.org + PEP 8
- Java: docs.oracle.com/javase

**User kann Najika trainieren durch:**
- Code-Reviews (Najika analysiert Code)
- Code-Generierung (Najika schreibt Code)
- Fehlersuche (Najika findet Bugs)
- Refactoring (Najika verbessert Code)
