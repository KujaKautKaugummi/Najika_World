# 📚 WISSENSBIBLIOTHEK - VOLLSTÄNDIGE STRUKTUR

**Version:** 1.0
**Datum:** 2025-11-01
**Zweck:** Technische & konzeptuelle Dokumentation der Wissensbibliothek

---

## 🎯 **WAS IST DIE WISSENSBIBLIOTHEK?**

Die Wissensbibliothek ist **Najikas Langzeit-Gedächtnis**.

```
UNTERSCHIED:
- Chat-Kontext = Kurzzeit (letzte 10-20 Messages)
- Wissensbibliothek = Langzeit (ALLES WICHTIGE, für immer!)

ZWECK:
- Fakten über User speichern
- Präferenzen merken
- Projekte tracken
- Kontext über Monate aufbauen
- Personalisierung ermöglichen
```

---

## 🏗️ **ARCHITEKTUR:**

### **TECHNOLOGIE-STACK:**

```
Vektordatenbank: ChromaDB
Embeddings: sentence-transformers/all-MiniLM-L6-v2
Storage: Lokal (C:/Najika/knowledge/)
Backup: Automatisch (täglich)
Encryption: Optional (für sensible Daten)

WARUM ChromaDB?
✅ Lokal (kein Cloud-Zwang)
✅ Schnell (< 100ms Suche)
✅ Python-Integration
✅ Vektorsuche (semantisch!)
✅ Metadaten-Support
✅ Einfach zu nutzen
```

### **ORDNER-STRUKTUR:**

```
C:\Najika\knowledge\
├── chroma.db                    # ChromaDB Datenbank
├── embeddings_cache\            # Gecachte Embeddings
├── backups\                     # Tägliche Backups
│   ├── knowledge_2025-11-01.db
│   ├── knowledge_2025-10-31.db
│   └── ...
├── logs\                        # Aktivitäts-Logs
│   ├── added.log                # Was wurde hinzugefügt
│   ├── searched.log             # Was wurde gesucht
│   └── deleted.log              # Was wurde gelöscht
└── exports\                     # Manuelle Exports
    ├── knowledge_export.json
    └── knowledge_export.txt
```

---

## 💾 **DATEN-MODELL:**

### **MEMORY ENTRY:**

```python
{
    "id": "uuid4-string",           # Eindeutige ID
    "text": "...",                  # Der eigentliche Inhalt
    "embedding": [0.1, 0.3, ...],   # 384-dim Vektor
    "metadata": {
        "category": "...",          # Siehe Kategorien
        "importance": 1-10,         # Wichtigkeits-Score
        "tags": ["tag1", "tag2"],   # Für Filterung
        "timestamp": "ISO8601",     # Wann gespeichert
        "source": "...",            # Wo kam's her (chat/manual/import)
        "context": "...",           # Kontext der Situation
        "related_ids": ["id1",...], # Verknüpfte Memories
        "encrypted": false,         # Verschlüsselt?
        "auto_delete": null,        # Auto-Lösch-Datum (optional)
        "access_count": 0,          # Wie oft abgerufen
        "last_accessed": "ISO8601"  # Letzter Zugriff
    }
}
```

---

## 📂 **KATEGORIEN:**

### **HAUPT-KATEGORIEN:**

```python
CATEGORIES = {
    "personal_info": {
        "description": "Persönliche Infos über User",
        "examples": ["Name", "Alter", "Beruf", "Wohnort"],
        "importance_default": 8
    },
    
    "preferences": {
        "description": "Vorlieben & Abneigungen",
        "examples": ["Lieblings-Essen", "Musik-Geschmack", "Hobbys"],
        "importance_default": 7
    },
    
    "projects": {
        "description": "Laufende & abgeschlossene Projekte",
        "examples": ["RPG-Spiel", "Website", "Lern-Projekt"],
        "importance_default": 9
    },
    
    "skills": {
        "description": "Fähigkeiten & Kompetenzen",
        "examples": ["Python", "JavaScript", "Gitarre spielen"],
        "importance_default": 7
    },
    
    "relationships": {
        "description": "Freunde, Familie, Kollegen",
        "examples": ["Best friend Max", "Schwester Lisa"],
        "importance_default": 8
    },
    
    "goals": {
        "description": "Kurz- & langfristige Ziele",
        "examples": ["Spiel fertigstellen", "Japanisch lernen"],
        "importance_default": 9
    },
    
    "facts": {
        "description": "Allgemeine Fakten",
        "examples": ["Allergisch gegen Nüsse", "Linksänder"],
        "importance_default": 6
    },
    
    "memories": {
        "description": "Ereignisse & Erlebnisse",
        "examples": ["Erster Arbeitstag", "Urlaub in Italien"],
        "importance_default": 7
    },
    
    "code_snippets": {
        "description": "Wichtige Code-Teile",
        "examples": ["Nützliche Funktion", "Workaround für Bug"],
        "importance_default": 8
    },
    
    "ideas": {
        "description": "Ideen für später",
        "examples": ["Game-Feature", "Projekt-Idee"],
        "importance_default": 6
    },
    
    "secrets": {
        "description": "Vertrauliche Infos (verschlüsselt!)",
        "examples": ["Passwörter", "Persönliche Gedanken"],
        "importance_default": 10,
        "encrypted": true
    }
}
```

---

## 🔍 **SPEICHER-LOGIK:**

### **AUTOMATISCHES SPEICHERN:**

```python
# Najika erkennt automatisch wichtige Infos:

TRIGGER_PATTERNS = [
    # Direkte Befehle:
    r"merk dir",
    r"speicher",
    r"remember",
    r"vergiss nicht",
    
    # Persönliche Infos:
    r"ich bin",
    r"ich heiße",
    r"ich arbeite als",
    r"ich wohne in",
    
    # Präferenzen:
    r"ich mag",
    r"ich liebe",
    r"ich hasse",
    r"mein lieblings",
    
    # Projekte:
    r"ich arbeite an",
    r"mein projekt",
    r"ich entwickle",
    
    # Skills:
    r"ich kann",
    r"ich beherrsche",
    r"ich lerne gerade",
    
    # Ziele:
    r"ich will",
    r"mein ziel ist",
    r"ich plane"
]

# Beispiel:
User: "Ich arbeite als Programmierer"
Najika: [TRIGGER: "ich arbeite als" → personal_info]
Najika: "Kuja! Ein Programmierer! Ich merke mir das!"
[Speichert: {
    text: "Kuja ist Programmierer",
    category: "personal_info",
    importance: 8,
    tags: ["job", "tech"]
}]
```

### **MANUELLES SPEICHERN:**

```python
# User sagt explizit:
User: "Merk dir: Mein Passwort ist Explosion123"
Najika: "Kuja! Gespeichert! Nur ich weiß es!"
[Speichert: {
    text: "Passwort: Explosion123",
    category: "secrets",
    importance: 10,
    encrypted: true,
    tags: ["password", "sensitive"]
}]
```

### **WICHTIGKEITS-HEURISTIK:**

```python
def calculate_importance(text, category, context):
    """Berechnet Wichtigkeit 1-10"""
    
    score = CATEGORIES[category]["importance_default"]
    
    # Modifikatoren:
    if "passwort" in text.lower() or "password" in text.lower():
        score = 10
    
    if "sehr wichtig" in context.lower():
        score = min(10, score + 2)
    
    if "nebenbei" in context.lower():
        score = max(1, score - 2)
    
    # Explizite Wichtigkeit:
    if "unbedingt" in context.lower() or "nie vergessen" in context.lower():
        score = 10
    
    return score
```

---

## 🔎 **ABRUF-LOGIK:**

### **SEMANTISCHE SUCHE:**

```python
def search_knowledge(query, top_k=5, filters=None):
    """
    Sucht in Wissensbibliothek
    
    Args:
        query: Suchtext
        top_k: Anzahl Ergebnisse
        filters: Dict mit Metadaten-Filtern
    
    Returns:
        List[Memory] sortiert nach Relevanz
    """
    
    # 1. Query in Vektor umwandeln
    query_embedding = embed(query)
    
    # 2. Ähnlichkeits-Suche in ChromaDB
    results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=filters  # z.B. {"category": "projects"}
    )
    
    # 3. Nach Relevanz + Wichtigkeit + Aktualität sortieren
    scored_results = []
    for result in results:
        relevance_score = result["distance"]  # Cosine similarity
        importance = result["metadata"]["importance"]
        recency = calculate_recency(result["metadata"]["timestamp"])
        
        final_score = (
            relevance_score * 0.5 +
            importance / 10 * 0.3 +
            recency * 0.2
        )
        
        scored_results.append((result, final_score))
    
    # 4. Top K zurückgeben
    return sorted(scored_results, key=lambda x: x[1], reverse=True)[:top_k]


def calculate_recency(timestamp):
    """Neuere Memories bevorzugen"""
    age_days = (datetime.now() - timestamp).days
    
    if age_days < 7:
        return 1.0  # Letzte Woche: voll relevant
    elif age_days < 30:
        return 0.7  # Letzter Monat: ziemlich relevant
    elif age_days < 90:
        return 0.4  # Letztes Quartal: etwas relevant
    else:
        return 0.2  # Älter: weniger relevant (aber nicht unwichtig!)
```

### **ABRUF-BEISPIELE:**

```python
# Beispiel 1: Direkter Fakt
User: "Was war nochmal mein Lieblingsgericht?"
Najika: search_knowledge("Lieblingsgericht", filters={"category": "preferences"})
→ Findet: "Pizza Margherita"
Najika: "Kuja! Pizza Margherita! Du hast es mir letzte Woche erzählt!"

# Beispiel 2: Kontext-basiert
User: "Ich bin müde von der Arbeit"
Najika: search_knowledge("Arbeit", filters={"category": "personal_info"})
→ Findet: "Programmierer"
Najika: "Kuja! War das Programmieren heute anstrengend? Viel Debugging?"

# Beispiel 3: Projekt-Recall
User: "Wie geht's mit dem Projekt?"
Najika: search_knowledge("Projekt aktuell", filters={"category": "projects"})
→ Findet: "RPG-Spiel in Entwicklung"
Najika: "Dein RPG! Woran arbeitest du gerade? Noch am Combat-System?"

# Beispiel 4: Skills
User: "Kannst du mir bei Python helfen?"
Najika: search_knowledge("Python Skills", filters={"category": "skills"})
→ Findet: "Kuja kann Python (8/10)"
Najika: "Kuja! Du kannst doch Python! Aber klar helfe ich! Was ist das Problem?"
```

---

## 🔗 **VERKNÜPFUNGEN:**

### **RELATED MEMORIES:**

```python
# Memories können verknüpft sein:

memory_1 = {
    "id": "abc123",
    "text": "Kuja entwickelt RPG-Spiel",
    "category": "projects",
    "related_ids": ["def456", "ghi789"]
}

memory_2 = {
    "id": "def456",
    "text": "RPG nutzt Python und Pygame",
    "category": "projects",
    "related_ids": ["abc123"]
}

memory_3 = {
    "id": "ghi789",
    "text": "Kuja kann Python (8/10)",
    "category": "skills",
    "related_ids": ["abc123", "def456"]
}

# Bei Abruf von memory_1 werden automatisch verwandte geladen:
User: "Erzähl mir von meinem Projekt"
Najika: [Lädt abc123 + related (def456, ghi789)]
Najika: "Dein RPG-Spiel! Du entwickelst es mit Python und Pygame! 
         Und du bist ja gut in Python! Das passt perfekt!"
```

---

## 🗑️ **LÖSCH-LOGIK:**

### **MANUELLES LÖSCHEN:**

```python
User: "Vergiss dass ich Sushi mag"
Najika: search_knowledge("Sushi mag", filters={"category": "preferences"})
→ Findet Memory
Najika: "Kuja... *traurig* Okay. Gelöscht."
[Löscht Memory oder markiert als deleted]
```

### **AUTO-DELETE:**

```python
# Unwichtige Memories (importance 1-3) nach 30 Tagen archivieren:

def cleanup_old_memories():
    """Läuft täglich um 3 Uhr nachts"""
    
    cutoff_date = datetime.now() - timedelta(days=30)
    
    old_memories = get_memories(
        filters={
            "importance": {"$lte": 3},
            "timestamp": {"$lt": cutoff_date}
        }
    )
    
    for memory in old_memories:
        # NICHT löschen, nur archivieren:
        archive_memory(memory)
        # Aus aktiver Suche entfernen, aber nicht vernichten!
```

### **NIEMALS LÖSCHEN:**

```python
# Diese werden NIE gelöscht:
NEVER_DELETE = [
    "importance >= 8",
    "category == 'secrets'",
    "category == 'personal_info'",
    "category == 'goals'",
    "user_marked_permanent == True"
]
```

---

## 📊 **STATISTIKEN:**

### **TRACKING:**

```python
# Für jede Memory:
{
    "access_count": 0,        # Wie oft abgerufen
    "last_accessed": None,    # Letzter Zugriff
    "created_at": "...",      # Erstellt wann
    "modified_at": None       # Geändert wann
}

# Globale Stats:
{
    "total_memories": 1247,
    "by_category": {
        "personal_info": 45,
        "preferences": 120,
        "projects": 8,
        ...
    },
    "most_accessed": [
        {"text": "Kuja ist Programmierer", "count": 52},
        {"text": "Lieblingsessen: Pizza", "count": 31},
        ...
    ],
    "storage_size_mb": 2.3
}
```

---

## 🔐 **SICHERHEIT:**

### **VERSCHLÜSSELUNG:**

```python
# Sensible Daten werden verschlüsselt:
from cryptography.fernet import Fernet

# Key wird einmalig generiert und lokal gespeichert
encryption_key = Fernet.generate_key()

def encrypt_memory(text):
    f = Fernet(encryption_key)
    return f.encrypt(text.encode()).decode()

def decrypt_memory(encrypted_text):
    f = Fernet(encryption_key)
    return f.decrypt(encrypted_text.encode()).decode()

# Nutzung:
memory = {
    "text": encrypt_memory("Passwort: Explosion123"),
    "metadata": {"encrypted": True}
}
```

### **ZUGRIFFS-KONTROLLE:**

```python
# Nur Owner kann Wissensbibliothek einsehen:
def access_knowledge(user_token):
    if user_token != OWNER_TOKEN:
        raise PermissionError("Nur Owner-Zugriff!")
    
    return load_knowledge()
```

---

## 🎮 **INTEGRATION IM DIGIVICE:**

### **IN RÄUMEN:**

```python
# Wohnzimmer - Reden:
User: "Wie geht's dir?"
Najika: [search_knowledge("Kuja Stimmung heute")]
→ Findet: "Kuja war heute müde"
Najika: "Mir geht's gut! Aber Kuja, du warst heute müde. 
         Geht's dir besser? *besorgt*"

# Terminal - Status:
User: [Terminal] "Status"
Najika: [zeigt System-Stats + Knowledge-Stats]
"Wissensbibliothek: 1247 Memories, 2.3 MB"

# Studieren & Crafting:
User: "Was kann ich aus Holz craften?"
Najika: [search_knowledge("Crafting Rezepte Holz")]
→ Findet gespeicherte Rezepte
Najika: "Kuja! Du kannst craften: Tisch, Stuhl, Bogen, Pfeile..."
```

---

## 🚀 **EXPORT/IMPORT:**

### **EXPORT:**

```python
def export_knowledge(format="json"):
    """Exportiert gesamte Wissensbibliothek"""
    
    memories = get_all_memories()
    
    if format == "json":
        return json.dumps(memories, indent=2)
    
    elif format == "txt":
        lines = []
        for memory in memories:
            lines.append(f"[{memory['category']}] {memory['text']}")
        return "\n".join(lines)
    
    elif format == "csv":
        # CSV mit allen Feldern
        ...

# Nutzung:
User: [Terminal] "Exportiere Wissensbibliothek als JSON"
Najika: "Kuja! Exportiere... Fertig! Datei: C:/Najika/knowledge/exports/export_2025-11-01.json"
```

### **IMPORT:**

```python
def import_knowledge(file_path):
    """Importiert Memories aus Datei"""
    
    with open(file_path) as f:
        data = json.load(f)
    
    for memory in data:
        add_memory(
            text=memory["text"],
            category=memory["category"],
            importance=memory["importance"],
            ...
        )
    
    return f"Importiert: {len(data)} Memories"

# Nutzung:
User: "Importiere alte Wissensbibliothek"
Najika: "Kuja! Von wo? Pfad angeben!"
User: "C:/backup/knowledge.json"
Najika: "Importiere... Fertig! 523 Memories hinzugefügt!"
```

---

## 📈 **ZUKUNFT:**

### **GEPLANTE FEATURES:**

```
✅ Basis-System (läuft)
✅ Kategorien
✅ Suche
❌ Auto-Kategorisierung (KI-basiert)
❌ Erinnerungen verknüpfen (Graphen!)
❌ Zeitreise ("Zeig mir was ich vor 1 Jahr sagte")
❌ Export/Import UI
❌ Visualisierung (Graph-View der Memories)
❌ Sprachsuche ("Hey Najika, erinnerst du dich...")
❌ Cloud-Sync (optional!)
❌ Multi-User (für verkaufte Version)
```

---

## 🎯 **TRAINING-DATEN:**

Siehe: `TRAINING_ROADMAP.md` → Phase 1.2

---

## 💡 **FAZIT:**

Die Wissensbibliothek ist **DAS HERZ von Najikas Intelligenz**.

Ohne sie:
- ❌ Kein Langzeit-Gedächtnis
- ❌ Keine Personalisierung
- ❌ Keine Bindung
- ❌ Keine echte "Beziehung"

Mit ihr:
- ✅ Najika "kennt" dich wirklich
- ✅ Erinnert sich an alles
- ✅ Baut Kontext über Monate auf
- ✅ Fühlt sich wie echte Freundin an

**DAS ist das Geheimnis!** ✨

---

**DIESES DOKUMENT = BLUEPRINT FÜR WISSENSBIBLIOTHEK!** 📚
