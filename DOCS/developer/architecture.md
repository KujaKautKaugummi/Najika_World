# Najika World - System Architecture

**Version:** 2.0.0
**Last Updated:** 2025-01-17
**Status:** Complete

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Architecture Diagram](#architecture-diagram)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [Database Design](#database-design)
7. [API Design](#api-design)
8. [Training Systems](#training-systems)
9. [World Systems](#world-systems)
10. [Security Architecture](#security-architecture)
11. [Deployment Architecture](#deployment-architecture)

---

## Overview

Najika World is a multi-platform AI gaming ecosystem consisting of:
- **UE5 Mobile Game** - Android game with backend integration
- **Digivice Web Game** - Browser-based 3D world
- **Backend API** - FastAPI-based backend services
- **Training Systems** - AI training and model management
- **Admin Dashboard** - System management interface

### Design Principles

1. **Modularity** - Independent, reusable components
2. **Scalability** - Horizontal scaling support
3. **Security** - JWT auth, HTTPS, input validation
4. **Performance** - LOD, caching, streaming
5. **Maintainability** - Clean code, documentation, tests

---

## System Components

```
Najika World Ecosystem
├── Mobile App (UE5)
│   ├── NajikaBackendClient Plugin
│   ├── NajikaVoiceSystem Plugin
│   └── Game Logic Blueprints
│
├── Web Game (Digivice)
│   ├── Three.js 3D Engine
│   ├── World Systems (Biomes, Weather, LOD)
│   ├── Character System
│   └── UI Components
│
├── Backend (FastAPI)
│   ├── REST API
│   ├── WebSocket Services
│   ├── Database (PostgreSQL/SQLite)
│   ├── Training Services
│   └── Admin Services
│
├── Training Systems
│   ├── LoRA Training
│   ├── Session Training
│   ├── Code Training
│   └── Voice Training
│
└── Infrastructure
    ├── Docker Containers
    ├── Redis Cache
    ├── Nginx Reverse Proxy
    └── CI/CD Pipeline
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐      │
│  │             │   │             │   │              │      │
│  │  UE5 Mobile │   │  Web Game   │   │   Admin      │      │
│  │    Game     │   │  (Digivice) │   │  Dashboard   │      │
│  │             │   │             │   │              │      │
│  └──────┬──────┘   └──────┬──────┘   └──────┬───────┘      │
│         │                 │                  │              │
└─────────┼─────────────────┼──────────────────┼──────────────┘
          │                 │                  │
          │        HTTPS/WebSocket             │
          │                 │                  │
┌─────────┼─────────────────┼──────────────────┼──────────────┐
│         │                 │                  │              │
│  ┌──────▼─────────────────▼──────────────────▼───────┐     │
│  │                                                     │     │
│  │         NGINX REVERSE PROXY / LOAD BALANCER       │     │
│  │                                                     │     │
│  └──────┬──────────────────────────────────────┬──────┘     │
│         │                                      │            │
│         │                                      │            │
├─────────┼──────────────────────────────────────┼────────────┤
│                   APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│         │                                      │            │
│  ┌──────▼──────────┐                  ┌───────▼─────────┐  │
│  │                 │                  │                 │  │
│  │  FastAPI App    │◄────────────────►│  WebSocket      │  │
│  │  (REST API)     │                  │  Server         │  │
│  │                 │                  │                 │  │
│  └──────┬──────────┘                  └─────────────────┘  │
│         │                                                   │
│         │                                                   │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │            BUSINESS LOGIC LAYER                     │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Game       │  │  Training   │  │  Voice     │  │   │
│  │  │  Systems    │  │  Systems    │  │  Systems   │  │   │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Arena      │  │  Admin      │  │  Auth      │  │   │
│  │  │  System     │  │  Services   │  │  Services  │  │   │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  │                                                      │   │
│  └──────┬───────────────────────────────────────┬──────┘   │
│         │                                       │          │
├─────────┼───────────────────────────────────────┼──────────┤
│                    DATA LAYER                              │
├─────────────────────────────────────────────────────────────┤
│         │                                       │          │
│  ┌──────▼──────────┐         ┌────────────────▼────────┐  │
│  │                 │         │                         │  │
│  │   PostgreSQL    │         │     Redis Cache         │  │
│  │   Database      │         │   (Sessions, Jobs)      │  │
│  │                 │         │                         │  │
│  └─────────────────┘         └─────────────────────────┘  │
│                                                            │
│  ┌─────────────────┐         ┌─────────────────────────┐  │
│  │                 │         │                         │  │
│  │  ChromaDB       │         │   File Storage          │  │
│  │  (Memories)     │         │   (Models, Data)        │  │
│  │                 │         │                         │  │
│  └─────────────────┘         └─────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   BACKGROUND SERVICES                       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │              │  │              │  │                 │  │
│  │   Celery     │  │   Training   │  │   Scheduler     │  │
│  │   Worker     │  │   Queue      │  │   (Cron Jobs)   │  │
│  │              │  │              │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### Layer Structure

```
backend/
├── main.py                     # FastAPI App Entry Point
├── config.py                   # Configuration Management
├── database.py                 # Database Connection
│
├── api/                        # API Layer (REST Endpoints)
│   ├── auth.py                 # Authentication
│   ├── game.py                 # Game Systems
│   ├── arena.py                # Nemesis Arena
│   ├── training.py             # Training Jobs
│   ├── voice.py                # Voice Chat
│   └── admin.py                # Admin Functions
│
├── models/                     # Data Models (SQLAlchemy ORM)
│   ├── user.py                 # User Model
│   ├── character.py            # Character Model
│   ├── inventory.py            # Inventory Models
│   └── training.py             # Training Job Models
│
├── services/                   # Business Logic Layer
│   ├── avatar_service.py
│   ├── finisher_system.py
│   ├── nemesis_arena_system.py
│   ├── training_launcher.py
│   ├── training_scheduler.py
│   ├── training_progress_tracker.py
│   ├── unified_training_interface.py
│   ├── voice_service.py
│   └── websocket_manager.py
│
└── alembic/                    # Database Migrations
    ├── env.py
    ├── script.py.mako
    └── versions/
```

### Request Flow

```
1. Client Request
   ↓
2. Nginx (TLS Termination, Load Balancing)
   ↓
3. FastAPI App (Routing, Middleware)
   ↓
4. API Endpoint (Request Validation)
   ↓
5. Service Layer (Business Logic)
   ↓
6. Data Layer (Database, Cache)
   ↓
7. Response (JSON)
```

### Middleware Stack

1. **CORS Middleware** - Cross-origin resource sharing
2. **Authentication Middleware** - JWT validation
3. **Rate Limiting** - API abuse prevention
4. **Compression** - Response compression
5. **Error Handling** - Global exception handling

---

## Frontend Architecture

### Web Game (Digivice)

```
digivice/
├── index.html                  # Entry Point
├── static/
│   ├── js/
│   │   ├── main.js             # Main App
│   │   ├── scene_setup.js      # Three.js Scene
│   │   ├── world_mode_manager.js
│   │   └── ui/                 # UI Components
│   │
│   └── css/
│       └── style.css
│
└── js/
    ├── world/                  # World Systems
    │   ├── biome_system.js
    │   ├── vegetation_system.js
    │   ├── weather_system.js
    │   ├── day_night_cycle.js
    │   ├── city_builder.js
    │   ├── lod_manager.js
    │   ├── region_streaming.js
    │   └── world_systems_integration.js
    │
    ├── character/              # Character Systems
    │   ├── character_controller.js
    │   ├── animation_system.js
    │   └── combat_system.js
    │
    └── utils/
        ├── resource_loader.js
        ├── cache_manager.js
        └── performance_monitor.js
```

### Component Architecture

```
┌─────────────────────────────────────┐
│         Application Core            │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Three.js Scene Manager     │  │
│  └──────────────────────────────┘  │
│           │          │              │
│  ┌────────▼────┐  ┌─▼──────────┐   │
│  │  World      │  │  Character  │   │
│  │  Systems    │  │  Systems    │   │
│  └─────────────┘  └─────────────┘   │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Resource Management        │  │
│  │   - Loader                   │  │
│  │   - Cache                    │  │
│  │   - Streaming                │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Performance Optimization   │  │
│  │   - LOD Manager              │  │
│  │   - Particle Pooling         │  │
│  │   - Audio Pooling            │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│    User     │      │  Character   │      │  Inventory   │
├─────────────┤      ├──────────────┤      ├──────────────┤
│ id (PK)     │─────<│ user_id (FK) │─────<│ character_id │
│ username    │      │ name         │      │ item_id      │
│ email       │      │ species      │      │ quantity     │
│ password    │      │ level        │      │ equipped     │
│ is_admin    │      │ hp           │      └──────────────┘
│ created_at  │      │ attack       │
└─────────────┘      │ defense      │
                     │ created_at   │
                     └──────────────┘

┌──────────────┐      ┌──────────────┐
│ TrainingJob  │      │TrainingProgress│
├──────────────┤      ├──────────────┤
│ id (PK)      │─────<│ job_id (FK)  │
│ user_id (FK) │      │ epoch        │
│ job_name     │      │ step         │
│ type         │      │ loss         │
│ status       │      │ accuracy     │
│ config       │      │ timestamp    │
│ created_at   │      └──────────────┘
│ started_at   │
│ completed_at │
└──────────────┘
```

### Tables

1. **users** - User accounts
2. **characters** - Game characters
3. **inventory_items** - Character inventory
4. **equipment** - Equipped items
5. **training_jobs** - Training job records
6. **training_progress** - Training progress snapshots
7. **sessions** - User sessions
8. **admin_logs** - Admin action logs

---

## API Design

### RESTful Principles

- **Resource-based URLs** - `/api/v1/characters/{id}`
- **HTTP Methods** - GET, POST, PUT, PATCH, DELETE
- **Status Codes** - 200, 201, 400, 401, 404, 500
- **JSON Responses** - Consistent structure
- **Versioning** - `/api/v1/`, `/api/v2/`

### Authentication Flow

```
1. User Login
   POST /api/v1/auth/login
   { "username": "...", "password": "..." }
   ↓
2. Server validates credentials
   ↓
3. Server generates JWT token
   ↓
4. Client receives token
   { "access_token": "eyJ...", "token_type": "bearer" }
   ↓
5. Client includes token in future requests
   Authorization: Bearer eyJ...
   ↓
6. Server validates token on each request
```

### WebSocket Architecture

```
Client                    Server
  │                         │
  ├──── WS Connect ────────>│
  │     /voice/ws/{token}   │
  │                         │
  │<──── Accept ────────────┤
  │                         │
  │──── Binary Audio ──────>│
  │                         │
  │                         ├─── Transcribe (Whisper AI)
  │                         │
  │<──── Transcription ─────┤
  │     { "text": "..." }   │
  │                         │
  │──── Ping ──────────────>│
  │                         │
  │<──── Pong ──────────────┤
  │                         │
```

---

## Training Systems

### Training Pipeline

```
1. User creates training job
   ↓
2. Job added to queue (TrainingScheduler)
   ↓
3. Scheduler launches job (TrainingLauncher)
   ↓
4. Training script executes
   ↓
5. Progress tracked (TrainingProgressTracker)
   ↓
6. Model saved to output directory
   ↓
7. Job marked as completed
```

### Training Types

1. **LoRA Training** - Fine-tune LLMs
2. **Session Training** - Train on chat logs
3. **Code Training** - Train on code repositories
4. **Voice Training** - Voice cloning
5. **Personality Training** - Emotional intelligence

---

## World Systems

### World System Integration

```
┌─────────────────────────────────────┐
│   World Systems Integration         │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │  Biome   │  │Vegetation│        │
│  │  System  │─>│  System  │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │ Weather  │─>│Day/Night │        │
│  │  System  │  │  Cycle   │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │   LOD    │  │ Region   │        │
│  │ Manager  │  │Streaming │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  ┌──────────────────────┐          │
│  │    City Builder      │          │
│  └──────────────────────┘          │
│                                     │
└─────────────────────────────────────┘
```

---

## Security Architecture

### Security Layers

1. **Transport Security** - HTTPS/TLS 1.3
2. **Authentication** - JWT tokens
3. **Authorization** - Role-based access control
4. **Input Validation** - Pydantic models
5. **SQL Injection Prevention** - ORM (SQLAlchemy)
6. **XSS Prevention** - Output encoding
7. **CSRF Protection** - SameSite cookies
8. **Rate Limiting** - API throttling

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "123",
    "username": "najika",
    "is_admin": false,
    "exp": 1705500000
  },
  "signature": "..."
}
```

---

## Deployment Architecture

### Production Stack

```
┌─────────────────────────────────────┐
│          Load Balancer              │
│           (Nginx)                   │
└──────────┬────────────┬─────────────┘
           │            │
    ┌──────▼────┐  ┌───▼──────┐
    │  Backend  │  │  Backend │
    │  Server 1 │  │  Server 2│
    └──────┬────┘  └───┬──────┘
           │            │
    ┌──────▼────────────▼─────┐
    │     PostgreSQL           │
    │   (Primary + Replica)    │
    └──────────────────────────┘
```

### Container Architecture

```
docker-compose.yml
├── nginx           (Reverse Proxy)
├── backend         (FastAPI App x4 workers)
├── postgres        (Database)
├── redis           (Cache & Sessions)
├── celery_worker   (Background Tasks)
└── celery_beat     (Scheduler)
```

---

## Performance Considerations

### Optimization Strategies

1. **Database**
   - Connection pooling
   - Query optimization
   - Indexes on foreign keys

2. **API**
   - Response compression
   - Pagination
   - Caching (Redis)

3. **Frontend**
   - LOD system
   - Particle pooling
   - Audio pooling
   - Resource streaming

4. **Training**
   - GPU utilization
   - Batch processing
   - Progress checkpoints

---

## Monitoring & Logging

### Metrics Collection

- **Application Metrics** - Response times, error rates
- **System Metrics** - CPU, memory, disk, network
- **Database Metrics** - Connections, query times
- **Training Metrics** - Loss, accuracy, GPU usage

### Log Levels

1. **DEBUG** - Detailed diagnostic info
2. **INFO** - General informational messages
3. **WARNING** - Warning messages
4. **ERROR** - Error messages
5. **CRITICAL** - Critical failures

---

## Future Architecture Plans

### Planned Improvements

1. **Microservices** - Split monolith into services
2. **Message Queue** - Add RabbitMQ/Kafka
3. **CDN** - Static asset delivery
4. **Container Orchestration** - Kubernetes
5. **Monitoring** - Prometheus + Grafana
6. **Distributed Tracing** - Jaeger/OpenTelemetry

---

**Architecture Document Version:** 2.0.0
**Last Updated:** 2025-01-17
**Status:** ✅ Complete
