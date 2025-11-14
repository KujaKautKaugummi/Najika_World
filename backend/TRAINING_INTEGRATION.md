# Training System Integration

**Status:** ✅ Complete (PHASE 20)
**Version:** 1.0

---

## Overview

The training system integration connects existing training scripts with the new FastAPI backend, providing a unified interface for managing AI training jobs.

### Integrated Training Types

1. **LoRA Training** (`najika_lora_training.py`)
   - Fine-tunes language models with LoRA adapters
   - Uses ChromaDB conversations as training data
   - Optimized for RTX 3060 Ti (8GB VRAM)

2. **Session Training** (`NAJIKA_SESSION_TRAINING.py`)
   - Imports Claude Code sessions
   - Builds training data from conversation history

3. **Code Training** (`NAJIKA_CODE_TRAINING.py`)
   - Learns from project code structure
   - Improves code generation capabilities

4. **Voice Training** (`NAJIKA_VIDEO_TO_VOICE_TRAINING.py`)
   - Processes video/audio for voice cloning
   - Creates TTS training data

5. **Personality Training** (`najika_emotional_intelligence_training.py`)
   - Trains emotional intelligence
   - Enhances personality traits

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           API Router (/api/training)                   │ │
│  │  - Create job      - Start job      - Monitor progress │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐ │
│  │        Training Launcher Service                       │ │
│  │  - Job management   - Script integration   - Logging   │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                  │
    ┌────▼───────┐                    ┌────▼─────────┐
    │  Database  │                    │   Training   │
    │  (SQLite/  │                    │   Scripts    │
    │ PostgreSQL)│                    │ (existing)   │
    └────────────┘                    └──────────────┘
```

---

## Usage

### 1. Create Training Job

**POST** `/api/training/jobs`

```json
{
  "job_name": "LoRA Training - Weekly Update",
  "training_type": "lora",
  "description": "Train on recent conversations",
  "config": {
    "base_model": "unsloth/Meta-Llama-3.1-8B-Instruct",
    "num_epochs": 3,
    "learning_rate": 0.0002,
    "batch_size": 4,
    "min_samples": 50
  }
}
```

**Response:**

```json
{
  "id": 1,
  "job_name": "LoRA Training - Weekly Update",
  "training_type": "lora",
  "status": "pending",
  "progress": 0.0,
  "created_at": "2025-01-14T12:00:00"
}
```

### 2. Start Training Job

**POST** `/api/training/jobs/1/start`

**Response:**

```json
{
  "success": true,
  "message": "Training started in background"
}
```

### 3. Monitor Progress

**GET** `/api/training/jobs/1/progress`

**Response:**

```json
[
  {
    "epoch": null,
    "step": null,
    "loss": null,
    "message": "Started lora training",
    "logged_at": "2025-01-14T12:00:01"
  },
  {
    "epoch": null,
    "step": null,
    "loss": null,
    "message": "Preparing training data...",
    "logged_at": "2025-01-14T12:00:05"
  },
  {
    "epoch": 1,
    "step": 10,
    "loss": 2.345,
    "message": "Training in progress...",
    "logged_at": "2025-01-14T12:05:00"
  }
]
```

### 4. Check Job Status

**GET** `/api/training/jobs/1`

**Response:**

```json
{
  "id": 1,
  "job_name": "LoRA Training - Weekly Update",
  "training_type": "lora",
  "status": "completed",
  "progress": 100.0,
  "output_model_path": "/path/to/model",
  "metrics": {
    "final_loss": 0.234,
    "training_time": "45m"
  },
  "created_at": "2025-01-14T12:00:00",
  "started_at": "2025-01-14T12:00:01",
  "completed_at": "2025-01-14T12:45:30"
}
```

---

## Training Configuration

### LoRA Training

```python
{
  "base_model": "unsloth/Meta-Llama-3.1-8B-Instruct",
  "num_epochs": 3,           # Number of training epochs
  "learning_rate": 0.0002,   # Learning rate
  "batch_size": 4,           # Batch size (adjust for GPU memory)
  "min_samples": 50,         # Minimum training samples required
  "lora_r": 16,              # LoRA rank (optional)
  "lora_alpha": 32           # LoRA alpha (optional)
}
```

### Session Training

```python
{
  "session_path": "/path/to/session.json",  # Optional specific session
  "max_sessions": 100,                       # Maximum sessions to import
  "filter_by_date": "2025-01-01"            # Optional date filter
}
```

### Code Training

```python
{
  "project_path": "/path/to/project",   # Optional specific project
  "languages": ["python", "javascript"], # Filter by languages
  "max_files": 1000                      # Maximum files to process
}
```

### Voice Training

```python
{
  "video_path": "/path/to/video.mp4",   # Video file to process
  "speaker_name": "Najika",              # Speaker identification
  "language": "de"                       # Language code
}
```

---

## Training Launcher Service

The `TrainingLauncher` service (`backend/services/training_launcher.py`) provides:

### Features

- ✅ **Unified Interface** - Single API for all training types
- ✅ **Background Execution** - Non-blocking training in threads
- ✅ **Progress Tracking** - Real-time progress updates
- ✅ **Error Handling** - Graceful error recovery and logging
- ✅ **Script Integration** - Wraps existing training scripts
- ✅ **Database Persistence** - Stores jobs and progress

### Methods

#### `launch_training()`

```python
training_launcher.launch_training(
    job_id=1,
    training_type="lora",
    config={"num_epochs": 3},
    db=db_session
)
```

Launches a training job in a background thread.

#### `_run_lora_training()`

Executes LoRA training by:
1. Creating `NajikaLoRATrainer` instance
2. Preparing training data from ChromaDB
3. Running training loop
4. Saving model output
5. Updating job status

#### `_run_session_training()`, `_run_code_training()`, etc.

Execute other training types as subprocesses for compatibility with existing scripts.

---

## Database Schema

### TrainingJob Model

```python
class TrainingJob:
    id: int
    user_id: int
    job_name: str
    training_type: str  # lora, session, code, voice, personality
    description: str
    status: str         # pending, running, completed, failed, cancelled
    progress: float     # 0.0 - 100.0
    config: dict        # Training configuration
    output_model_path: str
    metrics: dict       # Training metrics (loss, accuracy, etc.)
    error_message: str
    created_at: datetime
    started_at: datetime
    completed_at: datetime
```

### TrainingProgress Model

```python
class TrainingProgress:
    id: int
    job_id: int
    epoch: int
    step: int
    loss: float
    accuracy: float
    message: str
    log_level: str      # info, warning, error
    logged_at: datetime
```

---

## Integration with Existing Scripts

### LoRA Training

**Before:**
```bash
python backend/najika_lora_training.py
```

**After:**
```bash
curl -X POST http://localhost:8000/api/training/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"job_name": "LoRA Training", "training_type": "lora"}'
```

### Benefits

1. **Web Interface** - Control training via HTTP API
2. **Progress Tracking** - Real-time updates in database
3. **Multi-User** - Multiple users can run training jobs
4. **Job History** - Complete history of all training runs
5. **Error Recovery** - Automatic error logging and recovery

---

## Testing

### 1. Create Test Job

```bash
curl -X POST http://localhost:8000/api/training/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "Test LoRA Training",
    "training_type": "lora",
    "config": {
      "num_epochs": 1,
      "batch_size": 2
    }
  }'
```

### 2. Start Job

```bash
curl -X POST http://localhost:8000/api/training/jobs/1/start \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Monitor Progress

```bash
# Get job status
curl http://localhost:8000/api/training/jobs/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get progress logs
curl http://localhost:8000/api/training/jobs/1/progress \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Error Handling

### Common Errors

1. **Training Script Not Found**
   - **Cause:** Script path incorrect
   - **Solution:** Check `training_launcher.scripts` dictionary

2. **Insufficient Training Data**
   - **Cause:** Not enough samples in ChromaDB
   - **Solution:** Import more sessions or lower `min_samples`

3. **GPU Out of Memory**
   - **Cause:** Batch size too large
   - **Solution:** Reduce `batch_size` in config

4. **Import Errors**
   - **Cause:** Missing dependencies
   - **Solution:** Install requirements: `pip install -r requirements.txt`

### Error Logs

All errors are logged in:
- Database: `TrainingProgress` table
- Console: Printed to stdout
- Job status: Updated to "failed" with error message

---

## Future Enhancements (Post-PHASE 20)

### Planned Features

- [ ] **Celery Integration** - Distributed task queue for scaling
- [ ] **GPU Scheduling** - Queue jobs to prevent OOM errors
- [ ] **Model Registry** - Version control for trained models
- [ ] **Web Dashboard** - React UI for training management
- [ ] **Training Presets** - Pre-configured training templates
- [ ] **Auto-Training** - Scheduled automatic training
- [ ] **Training Metrics** - Advanced metrics visualization
- [ ] **Model Comparison** - A/B testing for models

---

## File Structure

```
backend/
├── services/
│   ├── __init__.py
│   └── training_launcher.py         # NEW: Unified training interface
│
├── api/
│   └── training.py                   # UPDATED: Now uses training_launcher
│
├── models/
│   └── training.py                   # Training job & progress models
│
├── najika_lora_training.py          # Existing script (wrapped)
├── NAJIKA_SESSION_TRAINING.py       # Existing script (wrapped)
├── NAJIKA_CODE_TRAINING.py          # Existing script (wrapped)
├── NAJIKA_VIDEO_TO_VOICE_TRAINING.py # Existing script (wrapped)
└── TRAINING_INTEGRATION.md          # This file
```

---

## Summary

**PHASE 20: Training System Integration** successfully:

- ✅ Created unified `TrainingLauncher` service
- ✅ Integrated 5 existing training scripts
- ✅ Updated `/api/training` to use launcher
- ✅ Added background job execution
- ✅ Implemented progress tracking
- ✅ Preserved existing script functionality

**Total Lines:** ~1,500

**Next Phase:** PHASE 21 - Voice & TTS Integration

---

**Created:** PHASE 20
**Author:** Web Model (Claude Sonnet 4.5)
