#!/bin/bash

# Quick Start Script for Quantum Simulation Web Application

echo "🚀 Quantum Mechanics Interactive Simulator - Quick Start"
echo "=========================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Setup backend
echo ""
echo -e "${YELLOW}Setting up backend API...${NC}"
cd api/

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install backend dependencies${NC}"
    exit 1
fi

cd ..

# Setup frontend
echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"

# Check if Python is available for server
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Frontend can be served with Python's built-in server${NC}"
fi

# Display instructions
echo ""
echo -e "${GREEN}========== Setup Complete ==========${NC}"
echo ""
echo "📝 To start the application:"
echo ""
echo "Terminal 1 - Start Backend API:"
echo "  cd api"
echo "  source venv/bin/activate"
echo "  python quantum_api.py"
echo ""
echo "Terminal 2 - Start Frontend Server:"
echo "  cd web/public"
echo "  python -m http.server 8080"
echo ""
echo "Then open your browser to: http://localhost:8080/index.html"
echo ""
echo "🌐 API will be available at: http://localhost:5000/api"
echo ""
echo "📖 For more information, see DEPLOYMENT.md"
echo ""
