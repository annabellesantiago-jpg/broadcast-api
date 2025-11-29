# Development & Deployment Guide

## Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js 16+
- Flutter SDK
- Docker & Docker Compose
- Git

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd broadcast-management-system

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env 2>/dev/null || true

# Edit backend/.env with your settings
```

### Running Services Locally

#### Option 1: Using Docker (Recommended)

```bash
cd backend
docker-compose up --build

# In another terminal, start frontend
cd frontend
npm install
npm start

# In another terminal, start mobile (optional)
cd mobile
flutter run
```

#### Option 2: Manual Setup

**Terminal 1 - PostgreSQL**
```bash
# Install PostgreSQL or run via Docker
docker run --name broadcast-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=broadcast_db \
  -p 5432:5432 \
  postgres:15-alpine
```

**Terminal 2 - Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Terminal 3 - Frontend**
```bash
cd frontend
npm install
npm start
```

**Terminal 4 - Mobile (Optional)**
```bash
cd mobile
flutter run
```

## API Testing

### Using cURL

#### 1. Signup
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Save the access_token from response
TOKEN="your_token_here"
```

#### 3. Create Broadcast
```bash
curl -X POST http://localhost:5000/api/broadcasts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Broadcast",
    "message": "This is a test broadcast message"
  }'
```

#### 4. List Broadcasts
```bash
curl -X GET "http://localhost:5000/api/broadcasts?page=1&per_page=10" \
  -H "Authorization: Bearer $TOKEN"
```

#### 5. Send Broadcast
```bash
curl -X POST http://localhost:5000/api/broadcasts/1/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_users": [2, 3]}'
```

### Using Postman

1. Import the provided Postman collection
2. Set environment variables:
   - `base_url`: http://localhost:5000/api
   - `token`: (obtained from login response)
3. Use pre-made requests to test all endpoints

### Using Insomnia

Similar to Postman - create a workspace and configure requests.

## Building for Production

### Backend

```bash
cd backend

# Build Docker image
docker build -t broadcast-api:latest .

# Push to registry (e.g., Docker Hub)
docker tag broadcast-api:latest your-registry/broadcast-api:latest
docker push your-registry/broadcast-api:latest
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in build/ directory
# Deploy to static hosting (Netlify, Vercel, AWS S3, etc.)
```

### Mobile

#### Android
```bash
cd mobile

# Build APK
flutter build apk

# Output: build/app/outputs/flutter-apk/app-release.apk

# Build App Bundle (for Play Store)
flutter build appbundle

# Output: build/app/outputs/bundle/release/app-release.aab
```

#### iOS
```bash
cd mobile

# Build for iOS
flutter build ios

# Open in Xcode for final configuration
open ios/Runner.xcworkspace
```

## Deployment Platforms

### Backend Deployment

#### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Install dependencies
sudo yum install docker docker-compose
sudo usermod -a -G docker ec2-user

# Clone repo and deploy
git clone <repo>
cd broadcast-management-system/backend
docker-compose up -d
```

#### Google Cloud Run
```bash
# Install gcloud CLI
# Authenticate
gcloud auth login

# Deploy
gcloud run deploy broadcast-api \
  --source . \
  --region us-central1 \
  --platform managed
```

#### Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create broadcast-api

# Set environment variables
heroku config:set JWT_SECRET_KEY=your-secret
heroku config:set DATABASE_URL=postgres://...

# Deploy
git push heroku main
```

### Frontend Deployment

#### Vercel
```bash
npm install -g vercel

cd frontend
vercel
```

#### Netlify
```bash
npm install -g netlify-cli

cd frontend
netlify deploy --prod --dir=build
```

#### AWS S3
```bash
cd frontend
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name --delete

# Configure CloudFront CDN
```

### Mobile Deployment

#### Google Play Store
1. Generate release key
2. Build app bundle
3. Create developer account
4. Submit for review

#### Apple App Store
1. Enroll Apple Developer Program
2. Create App ID and certificates
3. Build iOS archive
4. Submit via App Store Connect

## Environment Variables

### Backend (.env)
```
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=your-jwt-secret-key
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-key.json
```

### Frontend (.env)
```
REACT_APP_API_URL=https://api.yourdomain.com/api
REACT_APP_ENV=production
```

### Mobile (environment.dart or similar)
```dart
const String apiBaseUrl = 'https://api.yourdomain.com/api';
const String firebaseProjectId = 'your-project-id';
```

## Monitoring & Logging

### Backend Monitoring
```bash
# View Docker logs
docker-compose logs -f backend

# SSH into container
docker-compose exec backend bash

# Install monitoring tools
pip install prometheus-client
pip install sentry-sdk
```

### Set up APM (Application Performance Monitoring)
- Sentry for error tracking
- New Relic or DataDog for performance
- ELK Stack for logging

### Database Monitoring
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres

# Check connections
SELECT * FROM pg_stat_activity;

# Check table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker
        run: |
          docker build -t broadcast-api:latest backend/
          docker push ${{ secrets.REGISTRY }}/broadcast-api:latest

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: cd frontend && npm install && npm run build
      - name: Deploy to Vercel
        run: npm install -g vercel && vercel deploy --prod
```

## Performance Optimization

### Backend
- Enable query caching
- Implement database connection pooling
- Use CDN for static files
- Enable gzip compression

### Frontend
- Code splitting and lazy loading
- Image optimization
- Minification and bundling
- Service workers for caching

### Mobile
- Optimize bundle size
- Use lazy loading for images
- Implement efficient state management
- Profile with Flutter DevTools

## Security Hardening

- [ ] Enable HTTPS/TLS everywhere
- [ ] Implement rate limiting
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable DDoS protection
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Implement backup and disaster recovery
- [ ] Set up log aggregation
- [ ] Configure alerts for suspicious activity

## Rollback Procedures

```bash
# Docker
docker-compose pull
docker-compose down
docker-compose up -d

# Git
git revert <commit-hash>
git push

# Database migration rollback
python manage.py migrate <app> <migration-number>
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port or kill process using it |
| Database connection refused | Check PostgreSQL is running and credentials |
| CORS errors | Verify API URL in frontend config |
| Token expired | Implement token refresh mechanism |
| Memory usage high | Profile app, check for memory leaks |
| Slow API responses | Check database queries, add indexes |

## Performance Benchmarks

- Backend API response time: < 200ms
- Frontend load time: < 2s
- Database query time: < 100ms
- Mobile app startup: < 3s

## Support & Maintenance

- Monitor system logs daily
- Review analytics weekly
- Update dependencies monthly
- Security patches: as soon as available
- Full backup: daily
- Database maintenance: weekly
