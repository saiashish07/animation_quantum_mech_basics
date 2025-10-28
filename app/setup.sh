#!/bin/bash
# Quick installation and startup script for Quantum Simulator

set -e

echo "======================================"
echo "Quantum Mechanics Simulator Setup"
echo "======================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Setup backend
echo ""
echo "Setting up backend..."
cd app/backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q flask flask-cors flask-socketio python-socketio numpy scipy requests

echo "✓ Backend dependencies installed"

# Test import
echo "Testing imports..."
python3 -c "import flask, numpy, scipy; print('✓ All imports successful')"

# Go back to root
cd ../..

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start the server:"
echo "  1. cd app/backend"
echo "  2. source venv/bin/activate"
echo "  3. python app/api/enhanced_api.py"
echo ""
echo "To serve frontend:"
echo "  cd app/frontend/public"
echo "  python -m http.server 8000"
echo ""
echo "Then open: http://localhost:8000/dashboard.html"
echo ""
