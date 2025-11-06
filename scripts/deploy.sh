#!/bin/bash

# BWW Store Deployment Script
# Usage: ./deploy.sh [environment]
# Environments: development, staging, production

set -e

ENVIRONMENT=${1:-development}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=================================="
echo "BWW Store Deployment Script"
echo "Environment: $ENVIRONMENT"
echo "=================================="

# Color codes
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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Load environment
load_environment() {
    log_info "Loading environment: $ENVIRONMENT"
    
    ENV_FILE="$PROJECT_ROOT/.env.$ENVIRONMENT"
    if [ -f "$ENV_FILE" ]; then
        log_info "Using environment file: $ENV_FILE"
        cp "$ENV_FILE" "$PROJECT_ROOT/.env"
    elif [ -f "$PROJECT_ROOT/.env" ]; then
        log_warn "Using existing .env file"
    else
        log_error "No environment file found"
        exit 1
    fi
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."
    cd "$PROJECT_ROOT"
    docker-compose build --no-cache
    log_info "Docker images built successfully"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    # Python migrations
    log_info "Running Python migrations..."
    docker-compose exec -T python-backend flask db upgrade || log_warn "Python migrations failed or not needed"
    
    # Node.js migrations (if any)
    log_info "Running Node.js migrations..."
    docker-compose exec -T nodejs-backend node scripts/migrate.js || log_warn "Node.js migrations failed or not needed"
    
    log_info "Migrations completed"
}

# Start services
start_services() {
    log_info "Starting services..."
    cd "$PROJECT_ROOT"
    docker-compose up -d
    log_info "Services started successfully"
}

# Stop services
stop_services() {
    log_info "Stopping services..."
    cd "$PROJECT_ROOT"
    docker-compose down
    log_info "Services stopped successfully"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Wait for services to be ready
    sleep 10
    
    # Check Python backend
    if curl -f http://localhost:5000/ &> /dev/null; then
        log_info "Python backend is healthy"
    else
        log_error "Python backend health check failed"
        return 1
    fi
    
    # Check Node.js backend
    if curl -f http://localhost:3000/ &> /dev/null; then
        log_info "Node.js backend is healthy"
    else
        log_error "Node.js backend health check failed"
        return 1
    fi
    
    log_info "All services are healthy"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."
    
    BACKUP_DIR="$PROJECT_ROOT/backups"
    mkdir -p "$BACKUP_DIR"
    
    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/mongodb_backup_${DATE}.archive"
    
    docker-compose exec -T mongodb mongodump --archive > "$BACKUP_FILE"
    
    log_info "Database backup created: $BACKUP_FILE"
}

# Rollback
rollback() {
    log_error "Deployment failed. Rolling back..."
    
    # Stop new version
    stop_services
    
    # Restore from backup if exists
    LATEST_BACKUP=$(ls -t "$PROJECT_ROOT/backups"/mongodb_backup_*.archive 2>/dev/null | head -n1)
    if [ -n "$LATEST_BACKUP" ]; then
        log_info "Restoring database from: $LATEST_BACKUP"
        docker-compose exec -T mongodb mongorestore --archive < "$LATEST_BACKUP"
    fi
    
    # Checkout previous version (if in git)
    if [ -d "$PROJECT_ROOT/.git" ]; then
        log_info "Checking out previous git version..."
        git checkout HEAD~1
    fi
    
    # Start services
    start_services
    
    log_error "Rollback completed"
}

# Main deployment flow
main() {
    check_prerequisites
    load_environment
    
    # Production requires backup
    if [ "$ENVIRONMENT" = "production" ]; then
        backup_database
    fi
    
    # Build and deploy
    if build_images && start_services && run_migrations && health_check; then
        log_info "=================================="
        log_info "Deployment completed successfully!"
        log_info "=================================="
        log_info "Services:"
        log_info "  - Frontend: http://localhost"
        log_info "  - Python API: http://localhost:5000"
        log_info "  - Node.js API: http://localhost:3000"
        log_info "=================================="
    else
        log_error "Deployment failed"
        if [ "$ENVIRONMENT" = "production" ]; then
            rollback
        fi
        exit 1
    fi
}

# Handle script arguments
case "$1" in
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 5
        start_services
        ;;
    logs)
        docker-compose logs -f
        ;;
    status)
        docker-compose ps
        ;;
    backup)
        backup_database
        ;;
    *)
        main
        ;;
esac
