#!/bin/bash
# Railway Build Script

echo "🚀 Starting ROG Pool Service Build..."

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm ci --production=false
echo "✅ Frontend dependencies installed"

# Build frontend
echo "🏗️ Building frontend..."
npm run build
echo "✅ Frontend built successfully"

# Go back to root
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

echo "🎉 Build completed successfully!"