# NAJIKA TRAINING SESSION

**Datum:** 2025-10-26 (Sunday)
**Zeit:** 10:00-11:00
**Woche:** 1
**Gesamt-Stunden:** 31

================================================================================

## FOCUS: Refactoring 1

### AUFGABEN FÜR DIESE STUNDE:

1. Nimm alten Code
2. Identifiziere Code-Smells
3. Refactore
4. Dokumentiere Änderungen
5. Erkläre WARUM besser

================================================================================

## REFACTORING RESSOURCE:

# COMMON PITFALLS - TYPISCHE FEHLER

================================================================================

## PYTHON PITFALLS

### 1. Mutable Default Arguments
**FALSCH:**
```python
def add_item(item, items=[]):  # GEFAHR!
    items.append(item)
    return items

# Alle Aufrufe teilen sich die GLEICHE Liste!
add_item(1)  # [1]
add_item(2)  # [1, 2] - UUPS!
```

**RICHTIG:**
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Late Binding Closures
**FALSCH:**
```python
functions = []
for i in range(3):
    functions.append(lambda: i)

# Alle geben 2 zurueck!
[f() for f in functions]  # [2, 2, 2]
```

**RICHTIG:**
```python
functions = []
for i in range(3):
    functions.append(lambda i=i: i)  # Default-Wert!

[f() for f in functions]  # [0, 1, 2]
```

### 3. Modifying List While Iterating
**FALSCH:**
```python
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # UEBERSPRINGT Elemente!
```

**RICHTIG:**
```python
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
```

## JAVA PITFALLS

### 1. String Comparison mit ==
**FALSCH:**
```java
String a = "hello";
String b = new String("hello");
if (a == b) {  // false! Vergleicht Referenzen!
```

**RICHTIG:**
```java
if (a.equals(b)) {  // true! Vergleicht Inhalt
```

### 2. NullPointerException
**FALSCH:**
```java
String name = null;
int length = name.length();  // CRASH!
```

**RICHTIG:**
```java
String name = null;
int length = (name != null) ? name.length() : 0;

// Oder Java 8+:
int length = Optional.ofNullable(name)
    .map(String::length)
    .orElse(0);
```


================================================================================
# ABSCHLUSS DIESER SESSION
================================================================================

**Wenn Session abgeschlossen:**
```bash
python C:/NajikaCore/najika_complete_training_session.py
```

**Das macht:**
1. Markiert diese Session als erledigt
2. Updated Gesamt-Stunden Counter
3. Speichert Progress

**Nächste Session:** Heute 11:00-12:00
