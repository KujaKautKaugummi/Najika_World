# PERFORMANCE PATTERNS

================================================================================

## BIG-O NOTATION

| Notation | Name | Beispiel |
|----------|------|----------|
| O(1) | Konstant | Array-Zugriff |
| O(log n) | Logarithmisch | Binary Search |
| O(n) | Linear | Array durchlaufen |
| O(n log n) | Linearithmisch | Merge Sort |
| O(n²) | Quadratisch | Nested Loops |
| O(2ⁿ) | Exponentiell | Rekursive Fibonacci |

## PATTERN 1: Dictionary Lookup statt Linear Search

**LANGSAM (O(n)):**
```python
def find_user(users, user_id):
    for user in users:  # O(n)
        if user["id"] == user_id:
            return user
    return None
```

**SCHNELL (O(1)):**
```python
# Einmal indexieren
user_dict = {user["id"]: user for user in users}

# Dann O(1) lookup
def find_user(user_id):
    return user_dict.get(user_id)
```

## PATTERN 2: List Comprehension statt Loops

**LANGSAM:**
```python
result = []
for i in range(1000):
    if i % 2 == 0:
        result.append(i * 2)
```

**SCHNELL (2x faster):**
```python
result = [i * 2 for i in range(1000) if i % 2 == 0]
```

## PATTERN 3: Set fuer Membership Tests

**LANGSAM (O(n)):**
```python
banned_words = ["spam", "bad", "evil"]  # List
if word in banned_words:  # O(n) search
    pass
```

**SCHNELL (O(1)):**
```python
banned_words = {"spam", "bad", "evil"}  # Set
if word in banned_words:  # O(1) lookup
    pass
```

## PATTERN 4: Caching / Memoization

**LANGSAM (Exponentiell):**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**SCHNELL (Linear):**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
