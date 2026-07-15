#!/bin/bash

# AI Sports Analytics Dashboard - Quick Start Script

echo "🏆 AI Sports Analytics Dashboard"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if we're in the frontend directory
if [ ! -f "app.py" ]; then
    echo "⚠️  Please run this script from the dashboard/ directory"
    echo "   cd dashboard"
    echo "   ./start.sh"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is installed in venv
if ! python -c "import streamlit" &> /dev/null 2>&1; then
    echo "📦 Installing required packages in virtual environment..."
    pip install -r ../requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install packages. Please check your internet connection."
        deactivate
        exit 1
    fi
    echo "✅ Packages installed successfully"
else
    echo "✅ Packages are already installed"
fi

echo ""
echo "🚀 Starting the dashboard..."
echo "   The dashboard will open in your browser at http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run app.py

# Deactivate venv when done
deactivate
