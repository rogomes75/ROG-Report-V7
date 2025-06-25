#!/bin/bash
# Minimal start script for Railway

echo "🚀 Starting ROG Pool Service (Minimal)..."

# Navigate to backend directory
cd backend

echo "📁 Current directory: $(pwd)"
echo "📋 Files in backend:"
ls -la

# Get port from environment or default to 8000
PORT=${PORT:-8000}
echo "🌐 Starting minimal server on port $PORT"

# Start the minimal application
exec python -m uvicorn server_minimal:app --host 0.0.0.0 --port $PORT