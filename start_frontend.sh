#!/bin/bash
# 🎨 Start Frontend Server with Port Forwarding for Codespace

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🎨 QUANTUM SIMULATOR - FRONTEND START (Codespace)         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/animation_quantum_mech_basics/app/frontend/public

echo "✅ Changed to: $(pwd)"
echo ""
echo "🌐 Starting HTTP Server on port 8000"
echo ""
echo "📌 PORT FORWARDING FOR CODESPACE:"
echo "   1. Look for notification: 'Your application running on port 8000 is available'"
echo "   2. OR manually forward: Ports panel → Forward port 8000"
echo "   3. Access at: https://<your-codespace>-8000.app.github.dev"
echo ""
echo "⏱️  Starting server..."
echo ""

python -m http.server 8000
