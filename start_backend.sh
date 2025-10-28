#!/bin/bash
# 🚀 Start Backend API with Port Forwarding for Codespace

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 QUANTUM SIMULATOR - BACKEND START (Codespace)          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
source /workspaces/animation_quantum_mech_basics/.venv/bin/activate

# Change to workspace root
cd /workspaces/animation_quantum_mech_basics

echo "✅ Virtual environment activated"
echo "✅ Working directory: $(pwd)"
echo ""

# Start the backend
echo "🔧 Starting Flask API on http://0.0.0.0:5000"
echo ""
echo "📌 PORT FORWARDING FOR CODESPACE:"
echo "   1. Look for notification: 'Your application running on port 5000 is available'"
echo "   2. OR manually forward: Ports panel → Forward port 5000"
echo "   3. Access at: https://<your-codespace>-5000.app.github.dev"
echo ""
echo "⏱️  Starting server..."
echo ""

PYTHONPATH=/workspaces/animation_quantum_mech_basics/src python app/backend/app/api/enhanced_api.py
