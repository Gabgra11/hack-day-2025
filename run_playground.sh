#!/bin/bash

# Agno Knowledge Base Playground Startup Script

echo "🤖 Starting Agno Knowledge Base Playground..."
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating one with default MongoDB URL..."
    echo "mdb_url=mongodb://localhost:27017" > .env
    echo "✅ Created .env file with default MongoDB URL"
    echo "   Please update it with your actual MongoDB connection string if needed."
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit, agno" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "⚠️  Ollama doesn't seem to be running."
    echo "   Please start Ollama with: ollama serve"
    echo "   Then install a model with: ollama pull llama3.1"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the playground
echo "🚀 Starting Streamlit playground..."
echo "   The playground will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""

streamlit run agno_playground.py 