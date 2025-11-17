# Najika World - Deployment Guide

Complete guide for deploying Najika World to production.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Database Migrations](#database-migrations)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Storage: 20 GB
- OS: Ubuntu 20.04+ / Debian 11+

**Recommended (Production):**
- CPU: 4+ cores
- RAM: 8+ GB
- Storage: 100+ GB SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

```bash
# Docker & Docker Compose
docker --version  # 20.10+
docker-compose --version  # 2.0+

# Git
git --version  # 2.25+

# Optional
nginx --version  # For reverse proxy
certbot --version  # For SSL certificates
```

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/KujaKautKaugummi/Najika_World.git
cd Najika_World
```

### 2. Configure Environment Variables

```bash
# Create environment file
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**

```bash
# Database
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://najika:${POSTGRES_PASSWORD}@postgres:5432/najika_world

# Redis
REDIS_PASSWORD=your_redis_password_here
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0

# Security
SECRET_KEY=your_secret_key_minimum_32_characters
JWT_SECRET=your_jwt_secret_minimum_32_characters

# API
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Celery
CELERY_BROKER_URL=redis://:${REDIS_PASSWORD}@redis:6379/1
CELERY_RESULT_BACKEND=redis://:${REDIS_PASSWORD}@redis:6379/1

# Optional: Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Generate Secure Keys:**

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Generate JWT_SECRET
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Create Directories

```bash
mkdir -p logs data models backups
chmod 755 logs data models backups
```

---

## Docker Deployment

### Quick Start

```bash
# Deploy with one command
./scripts/deploy.sh production
```

### Manual Docker Deployment

#### Step 1: Build Images

```bash
docker-compose build
```

#### Step 2: Start Services

```bash
docker-compose up -d
```

#### Step 3: Run Migrations

```bash
docker-compose exec backend python -m alembic upgrade head
```

#### Step 4: Verify Deployment

```bash
# Check all services are running
docker-compose ps

# Check logs
docker-compose logs -f

# Health check
curl http://localhost:8000/health
```

### Docker Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Restart service
docker-compose restart [service_name]

# Execute command in container
docker-compose exec backend [command]

# View resource usage
docker stats

# Prune unused resources
docker system prune -a
```

---

## Manual Deployment

### Backend (Python/FastAPI)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost/najika_world"
export SECRET_KEY="your-secret-key"

# 4. Run migrations
python -m alembic upgrade head

# 5. Start server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend (Static Files)

```bash
# Serve with Nginx
sudo cp -r digivice/* /var/www/najika-frontend/

# Or with Python
python -m http.server 8080 --directory digivice/
```

### Database (PostgreSQL)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql

CREATE DATABASE najika_world;
CREATE USER najika WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE najika_world TO najika;
\q

# Run migrations
python -m alembic upgrade head
```

### Redis

```bash
# Install Redis
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Secure Redis
sudo nano /etc/redis/redis.conf
# Add: requirepass your_redis_password

sudo systemctl restart redis-server
```

---

## CI/CD Pipeline

### GitHub Actions

Pipeline automatically runs on:
- **CI (Continuous Integration)**: Every push/PR
- **CD (Continuous Deployment)**: Git tags (v1.0.0)

#### Trigger Deployment

```bash
# 1. Update version
git tag -a v1.0.0 -m "Release version 1.0.0"

# 2. Push tag
git push origin v1.0.0

# 3. GitHub Actions will:
#    - Run tests
#    - Build Docker image
#    - Push to registry
#    - Deploy to production
#    - Create GitHub release
```

#### Manual Workflow Trigger

```bash
# Go to GitHub Actions tab
# Select workflow
# Click "Run workflow"
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pytest tests/

build:
  stage: build
  script:
    - docker build -t najika-world .

deploy:
  stage: deploy
  script:
    - ./scripts/deploy.sh production
  only:
    - tags
```

---

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from models
docker-compose exec backend python -m alembic revision --autogenerate -m "Add new table"

# Create empty migration
docker-compose exec backend python -m alembic revision -m "Custom migration"
```

### Applying Migrations

```bash
# Upgrade to latest
docker-compose exec backend python -m alembic upgrade head

# Upgrade to specific version
docker-compose exec backend python -m alembic upgrade abc123

# Downgrade one version
docker-compose exec backend python -m alembic downgrade -1

# Show current version
docker-compose exec backend python -m alembic current
```

### Migration Best Practices

1. **Always test migrations** on staging first
2. **Backup database** before running migrations
3. **Review auto-generated migrations** - they may need adjustments
4. **Make migrations reversible** - implement downgrade()
5. **Use transactions** for data migrations

---

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost/

# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Filter by timestamp
docker-compose logs --since 2024-01-01T00:00:00 backend
```

### Metrics

```bash
# System resources
docker stats

# Database connections
docker-compose exec postgres psql -U najika -c "SELECT count(*) FROM pg_stat_activity;"

# Redis stats
docker-compose exec redis redis-cli INFO
```

### Monitoring Tools

**Recommended:**
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Sentry** - Error tracking
- **Uptime Robot** - Uptime monitoring

---

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check logs
docker-compose logs [service_name]

# Check container status
docker-compose ps

# Rebuild container
docker-compose up -d --build [service_name]
```

#### 2. Database Connection Errors

```bash
# Check if Postgres is running
docker-compose ps postgres

# Check connection
docker-compose exec backend psql $DATABASE_URL -c "SELECT 1;"

# Reset database
docker-compose down
docker volume rm najika_world_postgres_data
docker-compose up -d
```

#### 3. Migration Fails

```bash
# Rollback to previous version
docker-compose exec backend python -m alembic downgrade -1

# Check current version
docker-compose exec backend python -m alembic current

# Force to specific version (dangerous!)
docker-compose exec backend python -m alembic stamp [revision]
```

#### 4. Out of Disk Space

```bash
# Remove unused Docker resources
docker system prune -a -f

# Remove old logs
find logs/ -name "*.log" -mtime +30 -delete

# Clean backups
find backups/ -mtime +90 -delete
```

#### 5. High CPU/Memory Usage

```bash
# Check resource usage
docker stats

# Restart heavy services
docker-compose restart backend celery_worker

# Scale down workers
docker-compose up -d --scale celery_worker=1
```

---

## Rollback Procedures

### Automatic Rollback

```bash
# Deployment script includes automatic rollback on failure
./scripts/deploy.sh production
# On error, answer "y" when prompted for rollback
```

### Manual Rollback

#### 1. Rollback Code

```bash
# Checkout previous version
git log --oneline
git checkout [previous_commit_hash]

# Rebuild and restart
docker-compose up -d --build
```

#### 2. Rollback Database

```bash
# Stop services
docker-compose down

# Restore from backup
docker-compose exec -T postgres psql -U najika najika_world < backups/[backup_file].sql

# Restart services
docker-compose up -d
```

#### 3. Rollback Docker Image

```bash
# Use previous image
docker-compose pull ghcr.io/kujakautkaugummi/najika_world:v1.0.0
docker-compose up -d
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Disable root SSH login
- [ ] Enable automatic security updates
- [ ] Regular backups scheduled
- [ ] Monitor error logs
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Configure CORS properly

---

## Performance Optimization

### Backend

```python
# Increase workers
uvicorn backend.main:app --workers 4

# Enable caching
@app.get("/api/data")
@cache(expire=300)
async def get_data():
    ...
```

### Database

```sql
-- Add indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_character_user_id ON characters(user_id);

-- Analyze tables
ANALYZE users;
ANALYZE characters;
```

### Frontend

```javascript
// Enable compression
// Add to nginx.conf
gzip on;
gzip_types text/css application/javascript;

// Lazy load images
<img loading="lazy" src="image.jpg">
```

---

## Backup Strategy

### Automated Backups

```bash
# Add to crontab
0 2 * * * /opt/najika_world/scripts/backup.sh

# Backup script
#!/bin/bash
BACKUP_DIR="/backups/$(date +\%Y\%m\%d)"
mkdir -p $BACKUP_DIR
docker-compose exec -T postgres pg_dump -U najika najika_world > $BACKUP_DIR/db.sql
```

### Backup Retention

- **Daily backups**: Keep 7 days
- **Weekly backups**: Keep 4 weeks
- **Monthly backups**: Keep 6 months

---

## Support

- **Documentation**: https://docs.najika.world
- **Issues**: https://github.com/KujaKautKaugummi/Najika_World/issues
- **Discord**: https://discord.gg/najika

---

**Last Updated:** 2025-01-17
**Version:** 1.0.0
