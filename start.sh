#!/bin/bash
echo "🚀 Starting Video Re-creation Agent..."

# Check .env exists
if [ ! -f .env ]; then
    echo "❌ .env not found. Copy .env.example to .env first:"
    echo "   cp .env.example .env"
    exit 1
fi

# Create directories
mkdir -p data/videos data/audio data/outputs

# Start server
echo "📡 Server starting at http://127.0.0.1:8000/"
python3 backend/main.py
