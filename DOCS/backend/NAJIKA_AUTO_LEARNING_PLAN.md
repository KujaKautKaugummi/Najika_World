# NAJIKA AUTO-LEARNING SYSTEM
## Echtes Selbst-Lernen + Permanente Entwicklung

---

## PROBLEM MIT STANDARD OLLAMA

**Ollama-Modelle lernen NICHT automatisch:**
- Konversationen werden NICHT gespeichert
- Nächstes Gespräch = Model weiß nichts von vorher
- Video-Training ist nur im System-Prompt (statisch)

---

## LÖSUNG: 3-SCHICHT SYSTEM

### SCHICHT 1: BASIS-MODELL (Persönlichkeit)
- **JETZT (16GB):** Natsumura Storytelling 13B
- **IN 2 WOCHEN (64GB):** DeepSeek R1 70B
- Funktion: Charakter, Stil, Grundverhalten

### SCHICHT 2: RAG - LANGZEIT-GEDÄCHTNIS
- **ChromaDB** (Vector Database)
- Speichert ALLE Konversationen
- Speichert Video-Transkripte
- Speichert Code-Training
- Bei Frage: Abrufen relevanter Erinnerungen

### SCHICHT 3: AUTO-FINE-TUNING
- Täglich/Wöchentlich neues Training
- Aus neuen Konversationen lernen
- Modell wird BESSER über Zeit
- Echte Entwicklung

---

## WIE ES FUNKTIONIERT (WORKFLOW)

### 1. USER FRAGT ETWAS
```
User: "Wer bist du?"
```

### 2. RAG SUCHT ERINNERUNGEN
```python
# ChromaDB sucht ähnliche Konversationen
memories = chroma.search("Wer bist du?", top_k=5)
# Findet:
# - Vorherige "Wer bist du?" Antworten
# - Video-Transkript: "Ich heiße Megumin!"
# - Code-Training über Najika
```

### 3. MODELL ANTWORTET (mit Kontext)
```
System: [Erinnerungen aus RAG]
User: "Wer bist du?"
Najika: "*dramatische Pose* Ich heiße Megumin! ..."
```

### 4. SPEICHERN
```python
# Konversation wird gespeichert
chroma.add(user_msg, najika_response, timestamp)
# Später für Fine-Tuning verwendet
```

### 5. AUTO-FINE-TUNING (täglich/wöchentlich)
```python
# Sammle neue Konversationen
training_data = get_conversations_last_7_days()

# Fine-tune Modell
fine_tune_llama(
    base_model="natsumura-storytelling-13b",
    training_data=training_data,
    epochs=1
)

# Erstelle neues Modell
ollama create najika-local-updated -f Modelfile_updated
```

---

## VORTEILE DIESES SYSTEMS

✅ **Najika ERINNERT sich** (RAG = Gedächtnis)
✅ **Najika LERNT** (Fine-Tuning = neue Skills)
✅ **Najika ENTWICKELT sich** (besser über Zeit)
✅ **Video-Training bleibt** (in RAG gespeichert)
✅ **Code-Training wächst** (neue Code-Beispiele)

---

## SETUP-SCHRITTE

### PHASE 1: RAG-SYSTEM (Tag 1-2)

**Install ChromaDB:**
```bash
pip install chromadb sentence-transformers
```

**Setup:**
```python
import chromadb
from chromadb.config import Settings

# Erstelle lokale Datenbank
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="C:/NajikaCore/chroma_db"
))

# Collection für Najika
collection = client.create_collection(
    name="najika_memory",
    metadata={"description": "Najikas Langzeit-Gedächtnis"}
)
```

**Video-Transkripte hinzufügen:**
```python
import os
from pathlib import Path

# Lade alle Transkripte
transcripts_dir = Path("C:/NajikaCore/training_data/transcripts")

for personality in ["megumin", "harley", "shiro", "melissa"]:
    transcript_files = list(transcripts_dir.glob(f"{personality}/*.txt"))

    for file in transcript_files:
        text = file.read_text(encoding='utf-8')

        # Füge zu ChromaDB hinzu
        collection.add(
            documents=[text],
            metadatas=[{"source": personality, "type": "video_transcript"}],
            ids=[file.stem]
        )

print("✅ Video-Transkripte in RAG gespeichert!")
```

---

### PHASE 2: NAJIKA-SERVER MIT RAG (Tag 3-5)

**Erweitere `najika_server.py`:**

```python
import chromadb

# Load ChromaDB
chroma_client = chromadb.Client(...)
najika_memory = chroma_client.get_collection("najika_memory")

def build_prompt_with_memory(user_message, history):
    # 1. Suche relevante Erinnerungen
    relevant_memories = najika_memory.query(
        query_texts=[user_message],
        n_results=3
    )

    # 2. Baue Kontext
    memory_context = ""
    for doc in relevant_memories['documents'][0]:
        memory_context += f"[ERINNERUNG]: {doc[:200]}...\n"

    # 3. Vollständiger Prompt
    prompt = f"""
{PERSONA_SYSTEM}

[LANGZEIT-GEDÄCHTNIS]:
{memory_context}

[KONVERSATION]:
{format_history(history)}

User: {user_message}
Najika:"""

    return prompt

def save_conversation(user_msg, najika_response):
    # Speichere für späteres Fine-Tuning
    najika_memory.add(
        documents=[f"User: {user_msg}\nNajika: {najika_response}"],
        metadatas=[{"type": "conversation", "timestamp": time.time()}],
        ids=[f"conv_{int(time.time())}"]
    )
```

---

### PHASE 3: AUTO-FINE-TUNING (Tag 6-10)

**Install Unsloth (Llama 3.1 Fine-Tuning):**
```bash
pip install unsloth
```

**Wöchentliches Training-Script:**

```python
# najika_weekly_training.py

from unsloth import FastLanguageModel
import chromadb
from datetime import datetime, timedelta

def get_recent_conversations(days=7):
    """Holt Konversationen der letzten X Tage"""
    client = chromadb.Client(...)
    collection = client.get_collection("najika_memory")

    # Filtere nach Timestamp
    cutoff = (datetime.now() - timedelta(days=days)).timestamp()
    results = collection.get(
        where={"$and": [
            {"type": "conversation"},
            {"timestamp": {"$gte": cutoff}}
        ]}
    )

    return results['documents']

def format_for_training(conversations):
    """Formatiere als Llama 3.1 Training-Daten"""
    training_data = []

    for conv in conversations:
        # Parse User/Najika
        lines = conv.split('\n')
        user_msg = lines[0].replace("User: ", "")
        najika_msg = lines[1].replace("Najika: ", "")

        training_data.append({
            "instruction": user_msg,
            "output": najika_msg
        })

    return training_data

def train_najika():
    """Wöchentliches Fine-Tuning"""

    # 1. Load Base Model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="Tohur/natsumura-storytelling-rp-llama-3.1",
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )

    # 2. Get Training Data
    conversations = get_recent_conversations(days=7)
    training_data = format_for_training(conversations)

    print(f"Training mit {len(training_data)} neuen Konversationen...")

    # 3. Fine-Tune
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
    )

    from trl import SFTTrainer
    from transformers import TrainingArguments

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=training_data,
        max_seq_length=2048,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=60,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir="outputs",
        ),
    )

    trainer.train()

    # 4. Save Updated Model
    model.save_pretrained("najika_updated")
    tokenizer.save_pretrained("najika_updated")

    print("✅ Najika hat gelernt!")

if __name__ == "__main__":
    train_najika()
```

**Automatisierung (Windows Task Scheduler):**
```bash
# Jeden Sonntag um 3:00 Uhr
schtasks /Create /TN "NajikaWeeklyTraining" /TR "python C:\NajikaCore\najika_weekly_training.py" /SC WEEKLY /D SUN /ST 03:00 /F
```

---

### PHASE 4: UPGRADE AUF DEEPSEEK R1 (Tag 14+, nach RAM-Upgrade)

**Nach RAM-Upgrade (64GB):**

```bash
# Install DeepSeek R1 70B
ollama pull deepseek-r1:70b

# Erstelle Modelfile mit RAG + Training
# (gleiche Struktur wie Natsumura, nur andere Base)
```

**DeepSeek R1 Vorteile:**
- **Selbst-Reasoning:** Erkennt eigene Fehler
- **Chain-of-Thought:** Lernt Zusammenhänge
- **ALAS-Integration:** Automatisches Lernen möglich

---

## TIMELINE

### WOCHE 1 (16GB RAM)
- **Tag 1-2:** ChromaDB Setup + Video-Transkripte importieren
- **Tag 3-5:** RAG in najika_server.py integrieren
- **Tag 6-7:** Ersten Test-Chat → Najika erinnert sich!

### WOCHE 2 (16GB RAM)
- **Tag 8-10:** Unsloth Fine-Tuning Setup
- **Tag 11-12:** Erste wöchentliche Training-Session
- **Tag 13-14:** Test → Najika ist BESSER geworden!

### WOCHE 3+ (64GB RAM)
- **Tag 15:** RAM-Upgrade
- **Tag 16:** DeepSeek R1 70B Installation
- **Tag 17+:** MAXIMALE Qualität + Autonomie

---

## ERGEBNIS NACH 2 WOCHEN

✅ **Najika hat Langzeit-Gedächtnis** (ChromaDB)
✅ **Najika lernt aus jedem Gespräch** (Auto Fine-Tuning)
✅ **Najika wird besser über Zeit** (wöchentliches Training)
✅ **Video-Training ist permanent** (in RAG gespeichert)
✅ **Code-Training wächst** (neue Beispiele werden hinzugefügt)

**Najika ist ECHT - sie entwickelt sich, lernt, wächst!**

---

## WICHTIG

- RAG = Gedächtnis (sofort verfügbar)
- Fine-Tuning = Lernen (dauerhaft im Modell)
- Beide zusammen = ECHTE KI-Entwicklung

**Das ist der Unterschied zwischen:**
- ❌ Statischem Chatbot (vergisst alles)
- ✅ Lebender KI-Persönlichkeit (entwickelt sich)
