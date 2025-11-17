#!/bin/bash

# Najika World - Deployment Script
# Usage: ./scripts/deploy.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if environment is provided
if [ -z "$1" ]; then
    log_error "Environment not specified"
    echo "Usage: $0 [development|staging|production]"
    exit 1
fi

ENVIRONMENT=$1

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    log_error "Invalid environment: $ENVIRONMENT"
    echo "Valid environments: development, staging, production"
    exit 1
fi

log_info "Starting deployment to $ENVIRONMENT environment..."

# ============================================================================
# Pre-deployment Checks
# ============================================================================

log_info "Running pre-deployment checks..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose is not installed"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env.$ENVIRONMENT" ]; then
    log_warn ".env.$ENVIRONMENT file not found, using .env"
    if [ ! -f ".env" ]; then
        log_error ".env file not found"
        exit 1
    fi
    ENV_FILE=".env"
else
    ENV_FILE=".env.$ENVIRONMENT"
fi

log_info "Using environment file: $ENV_FILE"

# ============================================================================
# Backup
# ============================================================================

if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Creating backup..."

    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # Backup database
    docker-compose exec -T postgres pg_dump -U najika najika_world > "$BACKUP_DIR/database.sql"

    # Backup volumes
    docker run --rm -v najika_world_postgres_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/postgres_data.tar.gz /data
    docker run --rm -v najika_world_redis_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/redis_data.tar.gz /data

    log_info "Backup created at $BACKUP_DIR"
fi

# ============================================================================
# Pull Latest Code
# ============================================================================

log_info "Pulling latest code..."

if [ "$ENVIRONMENT" = "production" ]; then
    git fetch --all
    git checkout main
    git pull origin main
elif [ "$ENVIRONMENT" = "staging" ]; then
    git fetch --all
    git checkout develop
    git pull origin develop
else
    log_warn "Skipping git pull for development environment"
fi

# ============================================================================
# Build and Deploy
# ============================================================================

log_info "Building Docker images..."

docker-compose --env-file "$ENV_FILE" build

log_info "Stopping existing containers..."

docker-compose --env-file "$ENV_FILE" down

log_info "Starting containers..."

docker-compose --env-file "$ENV_FILE" up -d

# ============================================================================
# Database Migrations
# ============================================================================

log_info "Running database migrations..."

docker-compose --env-file "$ENV_FILE" exec -T backend python -m alembic upgrade head

# ============================================================================
# Health Checks
# ============================================================================

log_info "Waiting for services to start..."

sleep 10

log_info "Running health checks..."

# Check backend health
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$BACKEND_HEALTH" = "200" ]; then
    log_info "Backend health check: OK"
else
    log_error "Backend health check: FAILED (HTTP $BACKEND_HEALTH)"
    exit 1
fi

# Check frontend
FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)

if [ "$FRONTEND_HEALTH" = "200" ]; then
    log_info "Frontend health check: OK"
else
    log_error "Frontend health check: FAILED (HTTP $FRONTEND_HEALTH)"
    exit 1
fi

# ============================================================================
# Cleanup
# ============================================================================

log_info "Cleaning up..."

docker system prune -f

# ============================================================================
# Post-deployment Tasks
# ============================================================================

if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Running post-deployment tasks..."

    # Clear cache
    docker-compose exec -T redis redis-cli FLUSHALL

    # Restart workers
    docker-compose restart celery_worker celery_beat

    log_info "Post-deployment tasks complete"
fi

# ============================================================================
# Summary
# ============================================================================

log_info "Deployment to $ENVIRONMENT completed successfully!"

echo ""
echo "Services:"
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend: http://localhost"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""

log_info "View logs with: docker-compose logs -f"

# ============================================================================
# Rollback Function (optional)
# ============================================================================

rollback() {
    log_warn "Rolling back deployment..."

    if [ -z "$BACKUP_DIR" ]; then
        log_error "No backup found to rollback to"
        exit 1
    fi

    # Restore database
    docker-compose exec -T postgres psql -U najika najika_world < "$BACKUP_DIR/database.sql"

    # Restore volumes
    docker run --rm -v najika_world_postgres_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar xzf /backup/postgres_data.tar.gz -C /
    docker run --rm -v najika_world_redis_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar xzf /backup/redis_data.tar.gz -C /

    log_info "Rollback complete"
}

# Trap errors and offer rollback
trap 'log_error "Deployment failed!"; read -p "Rollback? (y/n) " -n 1 -r; echo; if [[ $REPLY =~ ^[Yy]$ ]]; then rollback; fi' ERR
