# ChromaDB Performance Notes 2026-02-15

**Erstellt von:** SONNET (Claude Sonnet 4.5)
**Scope:** Code-Review der Memory-Implementierungen

---

## 📊 MEMORY-IMPLEMENTIERUNGEN

| Datei | Größe | Zweck |
|-------|-------|-------|
| `najika_memory.py` | 12KB | Basis ChromaDB Memory |
| `najika_memory_enhanced.py` | 17KB | Erweiterte Memory (RAG) |
| `api/memory.py` | 13KB | API Router für Memory |

---

## ⚠️ PERFORMANCE BOTTLENECKS IDENTIFIZIERT

### 1️⃣ **Sequenzielle Collection-Queries** (`najika_memory_enhanced.py:254`)

**Problem:**
```python
def search(self, query, n_results=5):
    # Queried 7 Collections SEQUENZIELL:
    # 1. conversations
    # 2. project_knowledge
    # 3. personalities
    # 4. complete_knowledge
    # 5. md_knowledge
    # 6. wichtige_docs
    # 7. core
```

**Impact:**
- Jede Query = ~50-200ms
- 7 Collections = 350-1400ms TOTAL! 😱
- BLOCKIERT Main-Thread

**Lösung (für später):**
```python
import asyncio

async def search_async(self, query, n_results=5):
    tasks = [
        asyncio.to_thread(self.query_collection, "conversations", query, n_results),
        asyncio.to_thread(self.query_collection, "project_knowledge", query, n_results),
        # ... etc
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Parallel = ~200ms statt 1400ms! ✅
```

### 2️⃣ **Bare except: pass** (Silent Failures)

**Problem:**
```python
try:
    results = self.collection.query(...)
except:  # ❌ Fängt ALLE Exceptions ohne Log!
    pass
```

**Impact:**
- Keine Logs bei Fehlern
- Debugging unmöglich
- Silent Data-Loss

**Lösung:**
```python
except Exception as e:
    logger.error(f"ChromaDB Query failed: {e}")
    # Optional: Fallback oder Re-raise
```

### 3️⃣ **Keine Query-Caching**

**Problem:**
- Gleiche Query mehrfach = mehrfache DB-Calls
- Kein Cache für häufige Queries

**Lösung (für später):**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_query(query: str, n_results: int):
    return self._query_internal(query, n_results)
```

---

## ✅ QUICK WINS (Einfache Optimierungen)

### 1. Exception-Handling verbessern
```python
# backend/najika_memory_enhanced.py Zeile 270, 288, 306, etc.
except:  # ❌
    pass

# Besser:
except Exception as e:  # ✅
    logger.error(f"Collection query failed: {e}")
```

### 2. n_results limitieren
```python
def search(self, query, n_results=5):
    # Maximum enforc en
    n_results = min(n_results, 10)  # Max 10 results
```

### 3. Timeouts hinzufügen
```python
# Bei ChromaDB-Init
client = chromadb.Client(Settings(
    chroma_api_impl="local",
    anonymized_telemetry=False,
    timeout=5.0  # 5 Sekunden Timeout
))
```

---

## 📝 EMPFEHLUNGEN

**P0 - JETZT (SONNET):**
1. ✅ Exception-Handling verbessern (Logger statt pass)
2. ✅ n_results Limits enforc en

**P1 - DIESE WOCHE:**
3. ⬜ Async/Parallel Queries implementieren
4. ⬜ Query-Caching hinzufügen
5. ⬜ Performance-Monitoring (@measure_performance)

**P2 - SPÄTER:**
6. ⬜ ChromaDB Indices optimieren
7. ⬜ Embedding-Cache
8. ⬜ Batch-Processing für große Imports

---

## 🧪 TESTING

**Vor Optimierung:**
```bash
curl -X POST http://localhost:8001/api/memory/search \
  -d '{"query": "Najika Persönlichkeit", "n_results": 5}'

# Erwartete Zeit: ~500-1000ms
```

**Nach Optimierung:**
```bash
# Ziel: < 200ms
```

---

## 📚 REFERENZEN

- ChromaDB Docs: https://docs.trychroma.com/
- FastAPI Async: https://fastapi.tiangolo.com/async/
- Python asyncio: https://docs.python.org/3/library/asyncio.html

---

**Note:** Tiefgreifende Optimierungen brauchen Testing.
SONNET kann Exception-Handling jetzt fixen, große Refactors später!
