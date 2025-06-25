#!/bin/bash
# Start script for Railway

echo "🚀 Starting ROG Pool Service..."

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found"
    exit 1
fi

# Navigate to backend directory
cd backend

echo "📁 Current directory: $(pwd)"
echo "📋 Files in backend:"
ls -la

# Check if server_simple.py exists
if [ ! -f "server_simple.py" ]; then
    echo "❌ server_simple.py not found"
    exit 1
fi

# Get port from environment or default to 8000
PORT=${PORT:-8000}
echo "🌐 Starting server on port $PORT"

# Start the application
exec python -m uvicorn server_simple:app --host 0.0.0.0 --port $PORT