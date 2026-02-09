# NAJIKA TRAINING SESSION

**Datum:** 2026-01-20 (Tuesday)
**Zeit:** 12:00-13:00
**Woche:** 11
**Gesamt-Stunden:** 446

================================================================================

## FOCUS: Code-Kata Praxis 2

### AUFGABEN FÜR DIESE STUNDE:

1. Neue Kata oder Variante
2. Implementiere in C#
3. Implementiere in Rust
4. Performance-Vergleich
5. Best Solution dokumentieren

================================================================================

## CODE-KATA RESSOURCE:

# NAJIKA CODE-KATAS - DAILY TRAINING

**ZWECK:** Taegliche kleine Uebungen (15-30 Min)
**FORMAT:** Problem → Loesung in allen 3 Sprachen

================================================================================

## WOCHE 1: GRUNDLAGEN

### TAG 1: FizzBuzz
**Problem:**
Zahlen 1-100:
- Teilbar durch 3: "Fizz"
- Teilbar durch 5: "Buzz"
- Teilbar durch beide: "FizzBuzz"
- Sonst: Zahl

**Python Loesung:**
```python
for i in range(1, 101):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

### TAG 2: Palindrom-Check
**Problem:** Pruefe ob String ein Palindrom ist

**Python:**
```python
def is_palindrome(s: str) -> bool:
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]
```

### TAG 3: Fibonacci
**Problem:** Fibonacci-Folge bis N

**Python (Generator):**
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

### TAG 4: Array Rotation
**Problem:** Rotiere Array um K Positionen

**Python:**
```python
def rotate(arr: list, k: int) -> list:
    k = k % len(arr)  # Handle k > len
    return arr[-k:] + arr[:-k]
```

### TAG 5: Zwei-Summen Problem
**Problem:** Finde 2 Zahlen die zusammen Target ergeben

**Python (O(n)):**
```python
def two_sum(nums: list[int], target: int) -> tuple:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None
```

## WOCHE 2: DATENSTRUKTUREN

### TAG 6: Stack Implementation
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop() if self.items else None
    
    def peek(self):
        return self.items[-1] if self.items else None
```

### TAG 7: Queue Implementation
```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        return self.items.popleft() if self.items else None
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

**Nächste Session:** Heute 13:00-14:00
