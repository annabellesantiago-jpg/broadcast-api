@echo off
REM Broadcast Management System - Quick Start Script (Windows)

echo.
echo 🚀 Broadcast Management System - Quick Start
echo =============================================
echo.

REM Check prerequisites
echo ✓ Checking prerequisites...

where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker.
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose not found. Please install Docker Compose.
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js.
    exit /b 1
)

echo ✓ All prerequisites found!
echo.

REM Create .env file if it doesn't exist
if not exist backend\.env (
    echo 📝 Creating backend\.env...
    copy backend\.env.example backend\.env
    echo ⚠️  Please update backend\.env with your settings
)

echo.
echo 🔨 Building services...
cd backend
docker-compose build

echo.
echo 🚀 Starting services...
docker-compose up -d

REM Wait for backend to be ready
echo ⏳ Waiting for backend to be ready...
timeout /t 5 /nobreak

cd ..

echo.
echo 📦 Installing frontend dependencies...
cd frontend
call npm install

echo.
echo ✓ All services started successfully!
echo.
echo 📍 Access points:
echo    - Backend API:     http://localhost:5000
echo    - Frontend (React): http://localhost:3000
echo.
echo 🎯 Next steps:
echo    1. Start frontend: cd frontend ^&^& npm start
echo    2. Open http://localhost:3000 in your browser
echo    3. Create an account or login
echo.
echo 📚 Documentation:
echo    - Main README:     ./README.md
echo    - Firebase Setup:  ./FIREBASE_SETUP.md
echo    - Deployment:      ./DEPLOYMENT.md
echo    - Testing:         ./TESTING.md
echo.
echo 💡 Tips:
echo    - View backend logs: docker-compose logs -f backend
echo    - View database: docker-compose exec postgres psql -U postgres
echo    - Stop services: docker-compose down
echo.
