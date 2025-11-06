# Deployment Guide

This guide covers deploying BWW Store to production environments.

## Prerequisites

- Docker and Docker Compose installed
- Access to production server
- Domain name configured
- SSL certificates
- Environment variables configured

## Deployment Options

### 1. Docker Compose Deployment (Recommended for Small-Medium Scale)

#### Step 1: Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/Yoans-Adel/last-bww-store.git
cd last-bww-store
```

#### Step 3: Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with production values
```

**Important Environment Variables:**

```env
NODE_ENV=production
FLASK_ENV=production

# Database
MONGODB_URI=mongodb://username:password@mongodb:27017/bww_store
REDIS_URL=redis://redis:6379

# Security
JWT_SECRET_KEY=<generate-strong-secret>
SECRET_KEY=<generate-strong-secret>

# Social Media
FACEBOOK_APP_ID=<your-app-id>
FACEBOOK_APP_SECRET=<your-app-secret>
WHATSAPP_ACCESS_TOKEN=<your-token>
```

#### Step 4: Deploy

```bash
# Build and start services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Step 5: Setup SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 2. Kubernetes Deployment (For Large Scale)

#### Prerequisites
- Kubernetes cluster (EKS, GKE, AKS, or self-hosted)
- kubectl configured
- Helm installed

#### Step 1: Create Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-backend
  template:
    metadata:
      labels:
        app: python-backend
    spec:
      containers:
      - name: python-backend
        image: your-registry/bww-python-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URI
          valueFrom:
            secretKeyRef:
              name: bww-secrets
              key: database-uri
```

#### Step 2: Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace bww-store

# Create secrets
kubectl create secret generic bww-secrets \
  --from-env-file=.env \
  -n bww-store

# Deploy
kubectl apply -f k8s/ -n bww-store

# Check status
kubectl get pods -n bww-store
```

### 3. Cloud Platform Deployment

#### AWS Deployment

**Using ECS (Elastic Container Service)**

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create ECR repositories
aws ecr create-repository --repository-name bww-python-backend
aws ecr create-repository --repository-name bww-nodejs-backend
aws ecr create-repository --repository-name bww-frontend

# Build and push images
$(aws ecr get-login --no-include-email)
docker-compose build
docker tag bww-python-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/bww-python-backend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/bww-python-backend:latest
```

#### Google Cloud Platform

**Using Google Cloud Run**

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init

# Build and deploy
gcloud builds submit --tag gcr.io/<project-id>/python-backend backend/python
gcloud run deploy python-backend --image gcr.io/<project-id>/python-backend --platform managed
```

#### Microsoft Azure

**Using Azure Container Instances**

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name bww-store --location eastus

# Deploy
az container create --resource-group bww-store \
  --name python-backend \
  --image your-registry/bww-python-backend:latest \
  --dns-name-label bww-python \
  --ports 5000
```

## Database Setup

### MongoDB Atlas (Cloud)

1. Create account at mongodb.com
2. Create cluster
3. Create database user
4. Whitelist IP addresses
5. Get connection string
6. Update `.env` with connection string

### Self-Hosted MongoDB

```bash
# Using Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:7.0
```

## Monitoring Setup

### Sentry for Error Tracking

```bash
# Get DSN from sentry.io
# Add to .env
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

### Prometheus & Grafana

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Backup Strategy

### Database Backup

```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"

# MongoDB backup
docker exec mongodb mongodump \
  --out /backup/dump_${DATE} \
  --username admin \
  --password password

# Upload to S3
aws s3 cp ${BACKUP_DIR}/dump_${DATE} \
  s3://bww-backups/mongodb/dump_${DATE} \
  --recursive
```

### Automated Backups with Cron

```bash
# Add to crontab
0 2 * * * /path/to/backup-db.sh
```

## Rollback Procedure

### Using Docker Compose

```bash
# Stop current version
docker-compose down

# Checkout previous version
git checkout <previous-commit>

# Rebuild and start
docker-compose up -d --build
```

### Using Kubernetes

```bash
# Rollback deployment
kubectl rollout undo deployment/python-backend -n bww-store

# Check rollout status
kubectl rollout status deployment/python-backend -n bww-store
```

## Performance Optimization

### Enable Caching

```nginx
# nginx.conf
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Enable Gzip Compression

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### Database Indexing

```javascript
// MongoDB indexes
db.products.createIndex({ name: "text", nameAr: "text" });
db.products.createIndex({ category: 1 });
db.orders.createIndex({ userId: 1, createdAt: -1 });
db.users.createIndex({ email: 1 }, { unique: true });
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong JWT secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable firewall
- [ ] Regular security updates
- [ ] Database access control
- [ ] Environment variables not in code
- [ ] Backup encryption
- [ ] DDoS protection
- [ ] Regular security audits

## Troubleshooting

### Check Service Health

```bash
# Docker
docker-compose ps
docker-compose logs <service-name>

# Kubernetes
kubectl get pods -n bww-store
kubectl logs <pod-name> -n bww-store
```

### Common Issues

**Issue**: Service won't start
```bash
# Check logs
docker-compose logs python-backend

# Check environment
docker-compose config
```

**Issue**: Database connection failed
```bash
# Test connection
docker exec -it mongodb mongo -u admin -p password

# Check network
docker network ls
docker network inspect bww-network
```

**Issue**: High memory usage
```bash
# Check container stats
docker stats

# Limit container resources
docker-compose.yml:
  services:
    python-backend:
      deploy:
        resources:
          limits:
            memory: 512M
```

## Scaling

### Horizontal Scaling

```bash
# Scale specific service
docker-compose up -d --scale python-backend=3

# Kubernetes
kubectl scale deployment python-backend --replicas=5 -n bww-store
```

### Load Balancer Configuration

```nginx
upstream python_backend {
    server python-backend-1:5000;
    server python-backend-2:5000;
    server python-backend-3:5000;
}

server {
    location /api/ {
        proxy_pass http://python_backend;
    }
}
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose up -d --build

# Run migrations if needed
docker-compose exec python-backend python manage.py migrate
```

### Database Migration

```bash
# Python (Flask-Migrate)
docker-compose exec python-backend flask db migrate
docker-compose exec python-backend flask db upgrade

# Node.js (Mongoose)
# Run migration scripts
docker-compose exec nodejs-backend node scripts/migrate.js
```

## Support

For deployment issues:
- Check logs first
- Review environment variables
- Verify network connectivity
- Check resource limits
- Contact support: devops@bwwstore.com
