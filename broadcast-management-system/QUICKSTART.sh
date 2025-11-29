#!/bin/bash

# Broadcast Management System - Quick Start Script

set -e

echo "🚀 Broadcast Management System - Quick Start"
echo "=============================================="
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js."
    exit 1
fi

echo "✓ All prerequisites found!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your settings"
fi

echo ""
echo "🔨 Building services..."
cd backend
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:5000/api/auth/me > /dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start"
        exit 1
    fi
    sleep 1
done

cd ..

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

echo ""
echo "✓ All services started successfully!"
echo ""
echo "📍 Access points:"
echo "   - Backend API:    http://localhost:5000"
echo "   - Frontend (React): http://localhost:3000"
echo ""
echo "🎯 Next steps:"
echo "   1. Start frontend: cd frontend && npm start"
echo "   2. Open http://localhost:3000 in your browser"
echo "   3. Create an account or login"
echo ""
echo "📚 Documentation:"
echo "   - Main README:     ./README.md"
echo "   - Firebase Setup:  ./FIREBASE_SETUP.md"
echo "   - Deployment:      ./DEPLOYMENT.md"
echo "   - Testing:         ./TESTING.md"
echo ""
echo "💡 Tips:"
echo "   - View backend logs: docker-compose logs -f backend"
echo "   - View database: docker-compose exec postgres psql -U postgres"
echo "   - Stop services: docker-compose down"
echo ""
