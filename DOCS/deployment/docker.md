# Docker Deployment Guide

Complete guide for deploying Najika World using Docker.

---

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/KujaKautKaugummi/Najika_World.git
cd Najika_World
```

### 2. Create Environment File

```bash
cp backend/.env.example backend/.env
```

Edit `.env`:
```env
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://najika:najika_password@db:5432/najika
DEBUG=False
```

### 3. Build and Start

```bash
docker-compose up -d
```

### 4. Access Services

- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Digivice Web Game:** http://localhost:3000
- **PostgreSQL:** localhost:5432

---

## Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: najika_db
    environment:
      POSTGRES_DB: najika
      POSTGRES_USER: najika
      POSTGRES_PASSWORD: najika_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U najika"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis (Caching & Task Queue)
  redis:
    image: redis:7-alpine
    container_name: najika_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # Backend API
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: najika_backend
    environment:
      DATABASE_URL: postgresql://najika:najika_password@db:5432/najika
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: "False"
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app/backend
      - ./models:/app/models
      - ./voice_data:/app/voice_data
      - ./training_data:/app/training_data
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000

  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    container_name: najika_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - ./digivice:/usr/share/nginx/html/digivice
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

---

## Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend /app/backend
COPY models /app/models
COPY voice_data /app/voice_data
COPY training_data /app/training_data

# Create directories
RUN mkdir -p /app/voice_data /app/training_data /app/models

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Backend upstream
    upstream backend {
        server backend:8000;
    }

    # HTTP Server
    server {
        listen 80;
        server_name api.najika.world;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name api.najika.world;

        # SSL Certificates
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL Settings
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;

        # API Routes
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket
        location /api/voice/ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

        # API Docs
        location /docs {
            proxy_pass http://backend;
        }

        # Health Check
        location /health {
            proxy_pass http://backend;
        }
    }

    # Digivice Web Game
    server {
        listen 80;
        server_name najika.world www.najika.world;

        root /usr/share/nginx/html/digivice;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        # Static files
        location /static {
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

---

## Production Deployment

### 1. SSL Certificates

Get Let's Encrypt certificate:

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d api.najika.world -d najika.world
```

Or use existing certificates:

```bash
mkdir -p ssl
cp your_cert.pem ssl/cert.pem
cp your_key.pem ssl/key.pem
```

### 2. Database Backup

```bash
# Backup
docker exec najika_db pg_dump -U najika najika > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i najika_db psql -U najika najika < backup.sql
```

### 3. Automatic Backups

Create `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker exec najika_db pg_dump -U najika najika > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
```

Schedule with cron:
```cron
0 2 * * * /path/to/backup.sh
```

### 4. Monitoring

Add monitoring with Prometheus:

```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
```

---

## Scaling

### Horizontal Scaling (Multiple Backend Instances)

```yaml
# docker-compose.yml
services:
  backend:
    # ... configuration ...
    deploy:
      replicas: 3
```

### Load Balancing with Nginx

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

---

## Environment Variables

Complete list of environment variables:

```env
# Application
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://redis:6379/0

# API
API_PREFIX=/api
CORS_ORIGINS=https://najika.world

# Voice
WHISPER_MODEL=base
TTS_ENGINE=edge

# Training
TRAINING_DATA_DIR=/app/training_data
MODEL_OUTPUT_DIR=/app/models

# Paths
VOICE_DATA_DIR=/app/voice_data
SAVE_DIR=/app/saves
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose build --no-cache backend
docker-compose up -d
```

### Database connection failed

```bash
# Test database connection
docker exec najika_backend python -c "from backend.database import engine; engine.connect()"

# Check database is running
docker exec najika_db psql -U najika -c "SELECT 1"
```

### Out of memory

```bash
# Check memory usage
docker stats

# Increase memory limit
docker-compose up -d --scale backend=1
```

---

## Maintenance

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose build
docker-compose down
docker-compose up -d
```

### Database Migrations

```bash
# Run migrations
docker exec najika_backend alembic upgrade head
```

### Clear Cache

```bash
# Clear Redis cache
docker exec najika_redis redis-cli FLUSHALL
```

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database password
- [ ] Enable SSL/TLS (HTTPS)
- [ ] Configure firewall (UFW/iptables)
- [ ] Set DEBUG=False in production
- [ ] Restrict CORS_ORIGINS
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Automated backups
- [ ] Monitor logs for suspicious activity

---

## Performance Optimization

### 1. Database Connection Pooling

```python
# backend/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### 2. Redis Caching

```python
# Use Redis for session storage
SESSION_TYPE = "redis"
SESSION_REDIS = redis.from_url(REDIS_URL)
```

### 3. CDN for Static Files

Use CloudFlare or AWS CloudFront for:
- Digivice web game assets
- Voice audio files
- Training model downloads

---

## Cost Estimation (AWS/DigitalOcean)

### Small Deployment (< 100 users)

- **EC2 t3.small** (2 vCPU, 2GB RAM): $15/month
- **RDS PostgreSQL** (db.t3.micro): $15/month
- **ElastiCache Redis** (cache.t3.micro): $12/month
- **Total:** ~$42/month

### Medium Deployment (100-1000 users)

- **EC2 t3.medium** (2 vCPU, 4GB RAM): $30/month
- **RDS PostgreSQL** (db.t3.small): $25/month
- **ElastiCache Redis** (cache.t3.small): $20/month
- **Total:** ~$75/month

### Large Deployment (1000+ users)

- **EC2 m5.large** (2 vCPU, 8GB RAM) x 2: $140/month
- **RDS PostgreSQL** (db.m5.large): $100/month
- **ElastiCache Redis** (cache.m5.large): $80/month
- **Load Balancer:** $20/month
- **Total:** ~$340/month

---

**Created:** PHASE 25 - Documentation Consolidation
**Author:** Web Model (Claude Sonnet 4.5)
