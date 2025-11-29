# Broadcast Management System

A complete three-tier broadcast notification management system built with Flask (Backend), React (Web Frontend), and Flutter (Mobile App).

## 📋 Project Overview

The Broadcast Management System allows users to:
- Create and manage broadcast messages
- Send broadcasts to multiple users
- Receive push notifications on mobile devices
- Track delivery status of broadcasts
- Manage user accounts with authentication

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Broadcast Management System              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐  ┌─────────────────────────────────┐ │
│  │   Web Frontend   │  │    Mobile App                   │ │
│  │   (React.js)     │  │    (Flutter)                    │ │
│  │                  │  │                                 │ │
│  │ - Dashboard      │  │ - Login/Signup                  │ │
│  │ - Create/Send    │  │ - Notification Center           │ │
│  │ - Broadcast Mgmt │  │ - Push Notifications (FCM)      │ │
│  └────────┬─────────┘  └────────────┬────────────────────┘ │
│           │                        │                       │
│           └────────────┬───────────┘                       │
│                        │ HTTP/REST API                     │
│                        ▼                                   │
│          ┌─────────────────────────────────┐              │
│          │   Flask Backend API             │              │
│          │   (Port 5000)                   │              │
│          │                                 │              │
│          │ - Authentication (JWT)          │              │
│          │ - CRUD Operations               │              │
│          │ - Push Notifications (Firebase) │              │
│          │ - User Management               │              │
│          └────────────┬────────────────────┘              │
│                       │                                   │
│          ┌────────────┴────────────┐                      │
│          ▼                         ▼                      │
│    ┌──────────────┐         ┌─────────────────┐          │
│    │  PostgreSQL  │         │ Firebase Cloud  │          │
│    │  Database    │         │ Messaging (FCM) │          │
│    │  (Port 5432) │         │                 │          │
│    └──────────────┘         └─────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Project Structure

```
broadcast-management-system/
├── backend/                          # Flask Backend API
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── models/
│   │   │   └── __init__.py          # SQLAlchemy models (User, Broadcast, Notification)
│   │   ├── routes/
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   └── broadcasts.py        # Broadcast CRUD endpoints
│   │   └── utils/
│   │       └── __init__.py          # Firebase push notification service
│   ├── app.py                        # Flask application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   ├── docker-compose.yml            # PostgreSQL + Flask services
│   └── .env.example                  # Environment variables template
│
├── frontend/                         # React Web Frontend
│   ├── public/
│   │   └── index.html               # HTML entry point
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js             # Login form
│   │   │   ├── Signup.js            # Signup form
│   │   │   └── Auth.css             # Auth styles
│   │   ├── pages/
│   │   │   ├── Dashboard.js         # Main dashboard
│   │   │   └── Dashboard.css        # Dashboard styles
│   │   ├── services/
│   │   │   └── api.js               # API client service
│   │   ├── App.js                   # Main app component
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   ├── package.json                  # NPM dependencies
│   └── README.md                     # Frontend documentation
│
├── mobile/                           # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart                # App entry point
│   │   ├── screens/
│   │   │   ├── login_screen.dart    # Login screen
│   │   │   ├── signup_screen.dart   # Signup screen
│   │   │   └── home_screen.dart     # Notifications list
│   │   ├── services/
│   │   │   ├── api_service.dart     # API client
│   │   │   └── notification_service.dart # FCM handler
│   │   └── models/
│   │       ├── user.dart            # User model
│   │       └── broadcast.dart       # Broadcast model
│   ├── pubspec.yaml                  # Flutter dependencies
│   ├── android/                      # Android native configuration
│   ├── ios/                          # iOS native configuration
│   └── README.md                     # Mobile app documentation
│
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- Flutter SDK (for mobile development)
- Docker & Docker Compose
- PostgreSQL (or use Docker)
- Firebase account (for push notifications)

### 1. Backend Setup (Flask + PostgreSQL)

#### Using Docker (Recommended)

```bash
cd backend

# Create .env file from example
cp .env.example .env

# Build and start services
docker-compose up --build
```

The backend will be available at `http://localhost:5000`

#### Manual Setup (Without Docker)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and configure database
cp .env.example .env
# Edit .env with your PostgreSQL connection details

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Run development server
python app.py
```

### 2. Web Frontend Setup (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Mobile App Setup (Flutter)

```bash
cd mobile

# Get Flutter dependencies
flutter pub get

# Configure Firebase:
# - Place google-services.json in android/app/
# - Place GoogleService-Info.plist in ios/Runner/

# Run on emulator or device
flutter run
```

## 📚 API Documentation

### Authentication Endpoints

#### Signup
```
POST /api/auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}

Response: 201 Created
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": { ... },
  "access_token": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### Get Current User
```
GET /api/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Broadcast Endpoints

#### Create Broadcast
```
POST /api/broadcasts
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "System Maintenance",
  "message": "System maintenance scheduled for tonight at 10 PM"
}

Response: 201 Created
{
  "message": "Broadcast created successfully",
  "broadcast": {
    "id": 1,
    "title": "System Maintenance",
    "message": "System maintenance...",
    "creator_id": 1,
    "status": "draft",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### List Broadcasts
```
GET /api/broadcasts?page=1&per_page=10&status=draft
Authorization: Bearer {access_token}

Response: 200 OK
{
  "broadcasts": [ ... ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

#### Get Broadcast
```
GET /api/broadcasts/{id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "title": "...",
  "message": "...",
  "status": "draft",
  "notifications": [ ... ]
}
```

#### Update Broadcast
```
PUT /api/broadcasts/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "message": "Updated message content"
}

Response: 200 OK
```

#### Delete Broadcast
```
DELETE /api/broadcasts/{id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "message": "Broadcast deleted successfully"
}
```

#### Send Broadcast
```
POST /api/broadcasts/{id}/send
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "target_users": [2, 3, 4]  // Optional, if not provided sends to all users
}

Response: 200 OK
{
  "message": "Broadcast sent successfully",
  "broadcast": { ... },
  "send_result": {
    "status": "success",
    "sent_count": 3
  }
}
```

#### Get User Notifications
```
GET /api/broadcasts/notifications/all?page=1&per_page=10
Authorization: Bearer {access_token}

Response: 200 OK
{
  "notifications": [
    {
      "id": 1,
      "broadcast_id": 1,
      "user_id": 1,
      "status": "sent",
      "created_at": "2024-01-15T10:30:00",
      "broadcast": { ... }
    }
  ],
  "total": 15,
  "pages": 2,
  "current_page": 1
}
```

## 🔐 Security

### Best Practices Implemented

1. **Password Hashing**: Uses Werkzeug for secure password hashing
2. **JWT Authentication**: Stateless token-based authentication
3. **CORS**: Configured for secure cross-origin requests
4. **Environment Variables**: Sensitive data stored in `.env`
5. **Database Indexes**: Optimized queries with proper indexing

### Production Checklist

- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Use environment-specific configurations
- [ ] Enable CSRF protection
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Regular security audits

## 📱 Push Notification Setup

### Firebase Configuration

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Create a new project
   - Enable Cloud Messaging

2. **Backend Configuration**:
   ```bash
   # Download service account JSON from Firebase Console
   # Settings > Service Accounts > Generate new private key
   
   cp /path/to/firebase-service-account.json backend/
   ```

3. **Android Configuration**:
   ```bash
   # Download google-services.json from Firebase Console
   cp google-services.json mobile/android/app/
   ```

4. **iOS Configuration**:
   ```bash
   # Download GoogleService-Info.plist from Firebase Console
   cp GoogleService-Info.plist mobile/ios/Runner/
   ```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Broadcasts Table
```sql
CREATE TABLE broadcasts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    creator_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    sent_at TIMESTAMP
);
```

### Notifications Table
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    broadcast_id INTEGER NOT NULL REFERENCES broadcasts(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    fcm_token TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    sent_at TIMESTAMP,
    error_message TEXT
);
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run tests (if test suite is added)
pytest

# Check code quality
pylint app/
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build
```

### Mobile Testing
```bash
cd mobile

# Run tests
flutter test

# Build for production
flutter build apk      # Android
flutter build ios      # iOS
```

## 📈 Performance Optimization

1. **Database**:
   - Indexed foreign keys
   - Query pagination
   - Connection pooling

2. **Frontend**:
   - Code splitting
   - Lazy loading
   - Caching

3. **Backend**:
   - Request throttling
   - Response compression
   - Database query optimization

## 🐛 Troubleshooting

### Backend Issues

**Issue**: "Connection refused" to PostgreSQL
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart services
docker-compose restart
```

**Issue**: JWT token invalid
- Ensure `JWT_SECRET_KEY` is set correctly
- Token may be expired (tokens expire after 1 hour by default)

### Frontend Issues

**Issue**: CORS errors
- Ensure backend is running on correct port
- Check proxy setting in `package.json`

**Issue**: Blank screen
- Check browser console for errors
- Verify API connection in Network tab

### Mobile Issues

**Issue**: Notifications not received
- Verify Firebase setup
- Check FCM token in device logs
- Ensure app has notification permissions

## 📝 API Response Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request |
| 401  | Unauthorized |
| 404  | Not Found |
| 409  | Conflict (e.g., user exists) |
| 500  | Server Error |

## 🚢 Deployment

### Docker Deployment

```bash
# Build production image
docker build -t broadcast-api:latest backend/

# Run with docker-compose
docker-compose -f docker-compose.yml up -d
```

### Cloud Deployment (AWS, GCP, Azure)

1. Set up managed database (RDS, Cloud SQL)
2. Configure environment variables
3. Deploy using CI/CD pipeline
4. Set up monitoring and logging
5. Configure auto-scaling

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check individual README files in each directory

## 📄 License

This project is provided as-is for educational purposes.

## 🔗 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Flutter Documentation](https://flutter.dev/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Introduction](https://jwt.io/introduction)

---

**Last Updated**: January 2024
**Version**: 1.0.0
