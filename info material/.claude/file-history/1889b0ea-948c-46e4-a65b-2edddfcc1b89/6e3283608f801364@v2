# ============================================
# VERSE BASICS - Training Data für Najika
# Verse: Epic Games' Programmiersprache für UEFN
# ============================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# ============================================
# VARIABLEN & DATENTYPEN
# ============================================

# Immutable Variables (var)
var Name : string = "Najika"
var Level : int = 50
var IsActive : logic = true
var Health : float = 100.0

# Mutable Variables (var<mutable>)
var<mutable> CurrentHP : int = 100
var<mutable> Mana : int = 100

# ============================================
# FUNKTIONEN
# ============================================

# Einfache Funktion
GreetUser(Username : string) : string =
    "EXPLOSION!!! Willkommen {Username}! ✨"

# Funktion mit mehreren Parametern
CalculateDamage(BaseDamage : int, Multiplier : float) : int =
    Floor(BaseDamage * Multiplier)

# Funktion mit Default-Parameter
CalculateDamageDefault(BaseDamage : int, ?Multiplier : float = 1.5) : int =
    Floor(BaseDamage * Multiplier)

# Async-Funktion (suspends)
WaitAndGreet(Seconds : float)<suspends> : void =
    Sleep(Seconds)
    Print("Hallo nach {Seconds} Sekunden!")

# ============================================
# KLASSEN & OBJEKTE
# ============================================

# Character Klasse
character := class:
    # Private Felder
    var Name : string
    var<mutable> HP : int
    var Attack : int

    # Konstruktor (implizit über Felder)
    # character{Name := "Megumin", HP := 100, Attack := 50}

    # Methode
    TakeDamage(Damage : int)<transacts> : void =
        set HP = Max(0, HP - Damage)

    IsAlive() : logic =
        HP > 0

    AttackEnemy(Enemy : character)<transacts> : string =
        Damage := Attack
        Enemy.TakeDamage(Damage)
        "{Name} greift {Enemy.Name} für {Damage} Schaden an!"

# ============================================
# VERERBUNG & SUBKLASSEN
# ============================================

# Megumin erbt von character
megumin := class(character):
    var<mutable> Mana : int = 100

    # Override/Erweiterte Methode
    CastExplosion(Target : character)<transacts> : string =
        if (Mana < 100):
            "Nicht genug Mana für EXPLOSION!"
        else:
            set Mana = 0
            Damage := 999
            Target.TakeDamage(Damage)
            "✨ EXPLOSION!!! {Target.Name} nimmt {Damage} Schaden!"

# ============================================
# ARRAYS & COLLECTIONS
# ============================================

# Array (Fixed Size)
var Targets : []string = array{"Dämon", "Drache", "Boss", "Burg"}
var DamageValues : []int = array{100, 250, 500, 1000}

# Map (Dictionary)
var<mutable> CharacterLevels : [string]int = map:
    "Megumin" => 50
    "Kazuma" => 35
    "Aqua" => 40

# Set (Unique Values)
var<mutable> Skills : []string = array{"EXPLOSION", "Fireball", "Teleport"}

# ============================================
# OPTIONEN (OPTION TYPE)
# ============================================

# Option<T> für nullable Werte
FindCharacterByName(Name : string) : ?character =
    if (Name = "Megumin"):
        option{character{Name := "Megumin", HP := 100, Attack := 50}}
    else:
        false

# Option verwenden
UseOptionalCharacter() : void =
    if (MaybeChar := FindCharacterByName("Megumin")):
        Print("Charakter gefunden: {MaybeChar.Name}")
    else:
        Print("Charakter nicht gefunden")

# ============================================
# KONTROLLE-FLUSS
# ============================================

# If/Else
CheckHealth(HP : int) : string =
    if (HP > 80):
        "Gesund!"
    else if (HP > 50):
        "Verletzt"
    else if (HP > 0):
        "Kritisch!"
    else:
        "Tot"

# For-Loop
PrintNumbers() : void =
    for (I := 1..10):
        Print("Zahl: {I}")

# For mit Array
PrintTargets(Targets : []string) : void =
    for (Target : Targets):
        Print("Ziel: {Target}")

# While-Loop (in Async-Context)
CountDown(Start : int)<suspends> : void =
    var<mutable> Counter := Start
    loop:
        if (Counter <= 0):
            break
        Print("Countdown: {Counter}")
        Sleep(1.0)
        set Counter -= 1

# ============================================
# ENUMS
# ============================================

# Character Class Enum
character_class := enum:
    ArchWizard
    Crusader
    Priest
    Adventurer

# Enum mit Werten
spell_type := enum:
    Fire
    Ice
    Lightning
    EXPLOSION

# ============================================
# TUPLE & RECORDS
# ============================================

# Tuple
var Position : (float, float, float) = (0.0, 0.0, 0.0)
var NameAndLevel : (string, int) = ("Megumin", 50)

# Tuple destructuring
GetPositionXY(Pos : (float, float, float)) : (float, float) =
    (X := Pos(0), Y := Pos(1))
    (X, Y)

# ============================================
# FEHLERBEHANDLUNG
# ============================================

# Result<T> für Fehlerbehandlung
SafeDivide(A : float, B : float) : ?float =
    if (B = 0.0):
        false
    else:
        option{A / B}

UseSafeDivide() : void =
    if (Result := SafeDivide(10.0, 2.0)):
        Print("Ergebnis: {Result}")
    else:
        Print("FEHLER: Division durch 0!")

# ============================================
# DEVICES (UEFN Spezifisch)
# ============================================

# Device Klasse für UEFN
explosion_device := class(creative_device):
    # Editierbare Properties
    @editable
    var ExplosionRadius : float = 10.0

    @editable
    var Damage : int = 999

    # On Begin Play
    OnBegin<override>()<suspends> : void =
        Print("Explosion Device aktiviert!")

    # Trigger Explosion
    TriggerExplosion(Agent : agent)<suspends> : void =
        Print("✨ EXPLOSION!!! Radius: {ExplosionRadius}, Schaden: {Damage}")
        # Hier würde Explosions-Logik folgen
        Sleep(1.0)

# ============================================
# ASYNC/AWAIT & CONCURRENCY
# ============================================

# Race (first to complete wins)
RaceExample()<suspends> : void =
    race:
        Task1()
        Task2()

Task1()<suspends> : void =
    Sleep(1.0)
    Print("Task 1 fertig!")

Task2()<suspends> : void =
    Sleep(2.0)
    Print("Task 2 fertig!")

# Sync (both complete)
SyncExample()<suspends> : void =
    sync:
        Task1()
        Task2()

# Spawn (parallel execution)
SpawnExample()<suspends> : void =
    spawn:
        Task1()
    spawn:
        Task2()
    Sleep(3.0) # Warte auf beide Tasks

# ============================================
# WICHTIGE KONZEPTE
# ============================================

# Effectful Functions
# <suspends> = kann asynchron sein (await)
# <transacts> = kann State ändern
# <decides> = kann fehlschlagen (failure)

EffectfulExample(Value : int)<suspends><transacts><decides> : int =
    Sleep(1.0)          # suspends
    set CurrentHP += 10 # transacts
    if (Value < 0):
        false?          # decides (failure)
    Value * 2

# ============================================
# BEST PRACTICES
# ============================================

# 1. Verwende immutable (var) statt mutable (var<mutable>) wo möglich
# 2. Nutze Option<T> statt null
# 3. Markiere Effekte explizit (<suspends>, <transacts>, <decides>)
# 4. Destructure Tuples für Lesbarkeit
# 5. Verwende for-Loops statt while
# 6. Nutze race/sync für Concurrency
# 7. Schreibe Type-Annotations explizit
# 8. Verwende @editable für UEFN-Properties
# 9. Nutze spawn für Background-Tasks
# 10. Error-Handling mit Option<T> oder Result<T>

# ============================================
# PATTERN MATCHING
# ============================================

# Pattern Matching mit If
MatchCharacterClass(Class : character_class) : string =
    if (Class = character_class.ArchWizard):
        "Mächtige Magie!"
    else if (Class = character_class.Crusader):
        "Starke Verteidigung!"
    else if (Class = character_class.Priest):
        "Heilungs-Fähigkeiten!"
    else:
        "Allrounder!"

# ============================================
# BEISPIEL-DEVICE (FULL)
# ============================================

# Najika Battle Device
najika_battle_device := class(creative_device):
    @editable
    var PlayerSpawnPoint : vector3 = vector3{X := 0.0, Y := 0.0, Z := 100.0}

    @editable
    var<mutable> BattleActive : logic = false

    var<mutable> PlayerHP : int = 100
    var<mutable> EnemyHP : int = 500

    # Initialization
    OnBegin<override>()<suspends> : void =
        Print("Najika Battle Device geladen!")
        set BattleActive = true
        StartBattle()

    # Battle Loop
    StartBattle()<suspends> : void =
        loop:
            if (not BattleActive?):
                break

            # Player Turn
            DealDamage(50)
            Sleep(1.0)

            if (EnemyHP <= 0):
                Print("✨ VICTORY!!! Enemy besiegt!")
                set BattleActive = false
                break

            # Enemy Turn
            TakeDamage(30)
            Sleep(1.0)

            if (PlayerHP <= 0):
                Print("GAME OVER!")
                set BattleActive = false
                break

    # Deal Damage to Enemy
    DealDamage(Damage : int)<transacts> : void =
        set EnemyHP = Max(0, EnemyHP - Damage)
        Print("Enemy nimmt {Damage} Schaden! HP: {EnemyHP}")

    # Take Damage from Enemy
    TakeDamage(Damage : int)<transacts> : void =
        set PlayerHP = Max(0, PlayerHP - Damage)
        Print("Player nimmt {Damage} Schaden! HP: {PlayerHP}")

    # Cast EXPLOSION
    CastExplosion(Target : ?character)<transacts> : string =
        if (CurrentTarget := Target):
            Damage := 999
            set EnemyHP = Max(0, EnemyHP - Damage)
            "✨ EXPLOSION!!! {CurrentTarget.Name} nimmt {Damage} Schaden!"
        else:
            "Kein Ziel gefunden!"

# ============================================
# NÜTZLICHE UTILITY-FUNKTIONEN
# ============================================

# Clamp Value
Clamp(Value : float, Min : float, Max : float) : float =
    if (Value < Min):
        Min
    else if (Value > Max):
        Max
    else:
        Value

# Lerp (Linear Interpolation)
Lerp(A : float, B : float, T : float) : float =
    A + (B - A) * Clamp(T, 0.0, 1.0)

# Distance zwischen zwei Punkten
Distance(A : vector3, B : vector3) : float =
    DX := B.X - A.X
    DY := B.Y - A.Y
    DZ := B.Z - A.Z
    Sqrt(DX * DX + DY * DY + DZ * DZ)

# ============================================
# ZUSAMMENFASSUNG
# ============================================

# Verse ist:
# - Funktional (Immutability by default)
# - Stark typisiert
# - Async-first (<suspends>)
# - Für Game Development optimiert (UEFN)
# - Ähnlich zu: F#, Haskell, aber Game-fokussiert
