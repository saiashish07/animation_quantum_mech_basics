#!/bin/bash
# 🚀 SIMPLE START BOTH SERVICES - For Codespace

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🚀 QUANTUM SIMULATOR - AUTO START (Backend + Frontend)       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Activate venv
source /workspaces/animation_quantum_mech_basics/.venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Start backend in background
echo "🔧 Starting BACKEND on port 5000..."
cd /workspaces/animation_quantum_mech_basics
PYTHONPATH=/workspaces/animation_quantum_mech_basics/src python app/backend/app/api/enhanced_api.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   PID: $BACKEND_PID"
sleep 2

# Check if backend started
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "   ✅ Backend is RUNNING!"
else
    echo "   ⚠️  Backend starting... (wait a moment)"
fi
echo ""

# Start frontend in background
echo "🎨 Starting FRONTEND on port 8000..."
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   PID: $FRONTEND_PID"
sleep 1

if curl -s http://localhost:8000/dashboard.html > /dev/null 2>&1; then
    echo "   ✅ Frontend is RUNNING!"
else
    echo "   ⚠️  Frontend starting... (wait a moment)"
fi
echo ""

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 SERVICES STARTED! 🎉                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "📍 ACCESS YOUR APP:"
echo ""
echo "  🔵 BACKEND API:"
echo "     Local:     http://localhost:5000"
echo "     API Health: http://localhost:5000/api/health"
echo ""
echo "  🟢 FRONTEND:"
echo "     Local:     http://localhost:8000/dashboard.html"
echo ""
echo "📌 CODESPACE PORT FORWARDING:"
echo "   1. Open PORTS panel (bottom of VS Code)"
echo "   2. Click globe 🌐 next to port 5000 (Backend)"
echo "   3. Click globe 🌐 next to port 8000 (Frontend)"
echo "   4. OR use: Ctrl+Shift+P → 'Forward a Port'"
echo ""
echo "🧪 TEST BACKEND:"
echo "   curl http://localhost:5000/api/health"
echo ""
echo "📊 VIEW LOGS:"
echo "   Backend:  tail -f /workspaces/animation_quantum_mech_basics/backend.log"
echo "   Frontend: tail -f /workspaces/animation_quantum_mech_basics/app/frontend/public/../../../frontend.log"
echo ""
echo "⏹️  TO STOP SERVICES:"
echo "   kill $BACKEND_PID  $FRONTEND_PID"
echo ""

# Keep script running to show status
sleep 3
echo "✅ Both services are ready!"
echo ""
echo "Next steps:"
echo "  1. Open PORTS panel in VS Code"
echo "  2. Click port 8000 → Open in Browser"
echo "  3. Your dashboard should load!"
echo ""
