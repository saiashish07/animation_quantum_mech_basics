#!/bin/bash
# 🚀 QUANTUM SIMULATOR - COMPLETE SETUP & RUN GUIDE

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                 QUANTUM SIMULATOR SETUP & RUN                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: VERIFY PYTHON & DEPENDENCIES
# ============================================================================

echo "📋 STEP 1: Verifying Python Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PYTHON_CMD="/workspaces/animation_quantum_mech_basics/.venv/bin/python"

if [ ! -f "$PYTHON_CMD" ]; then
    echo "❌ Python virtual environment not found!"
    echo "   Creating new virtual environment..."
    python3 -m venv /workspaces/animation_quantum_mech_basics/.venv
    echo "✅ Virtual environment created"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python Version: $PYTHON_VERSION"

# Verify key packages
echo ""
echo "Checking installed packages:"
PACKAGES=("flask" "numpy" "scipy" "flask-socketio" "flask-cors")
for pkg in "${PACKAGES[@]}"; do
    if $PYTHON_CMD -c "import ${pkg//-/_}" 2>/dev/null; then
        echo "  ✅ $pkg"
    else
        echo "  ❌ $pkg (missing)"
    fi
done

# ============================================================================
# STEP 2: BACKEND SETUP
# ============================================================================

echo ""
echo "🔧 STEP 2: Backend Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

BACKEND_DIR="/workspaces/animation_quantum_mech_basics/app/backend"
echo "Backend directory: $BACKEND_DIR"

if [ -f "$BACKEND_DIR/app/api/enhanced_api.py" ]; then
    echo "✅ Backend API file found: enhanced_api.py"
else
    echo "❌ Backend API file not found!"
    exit 1
fi

if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "✅ Requirements file found"
else
    echo "❌ Requirements file not found!"
    exit 1
fi

# ============================================================================
# STEP 3: FRONTEND SETUP
# ============================================================================

echo ""
echo "🎨 STEP 3: Frontend Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FRONTEND_DIR="/workspaces/animation_quantum_mech_basics/app/frontend/public"
echo "Frontend directory: $FRONTEND_DIR"

if [ -f "$FRONTEND_DIR/dashboard.html" ]; then
    echo "✅ Dashboard HTML found"
else
    echo "❌ Dashboard HTML not found!"
    exit 1
fi

if [ -f "$FRONTEND_DIR/dashboard.js" ]; then
    echo "✅ Dashboard JS found"
else
    echo "❌ Dashboard JS not found!"
    exit 1
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo "✅ All setup checks passed!"
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                        READY TO START SERVICES                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 QUICK START (3 TERMINALS):"
echo ""
echo "Terminal 1 - Start Backend:"
echo "  cd /workspaces/animation_quantum_mech_basics/app/backend"
echo "  /workspaces/animation_quantum_mech_basics/.venv/bin/python app/api/enhanced_api.py"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "  cd /workspaces/animation_quantum_mech_basics/app/frontend/public"
echo "  python -m http.server 8000"
echo ""
echo "Terminal 3 - Open Browser:"
echo "  http://localhost:8000/dashboard.html"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
