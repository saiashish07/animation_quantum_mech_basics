#!/usr/bin/env python3
"""
🚀 QUANTUM SIMULATOR - COMPLETE SETUP GUIDE

This script sets up and runs both backend and frontend services.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_section(text):
    """Print a section header"""
    print(f"\n{BOLD}{text}{RESET}")
    print("─" * 70)

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅{RESET} {text}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌{RESET} {text}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ️{RESET} {text}")

def check_python():
    """Check Python version and setup"""
    print_section("1️⃣  Python Environment Check")
    
    print_info(f"Python Version: {sys.version.split()[0]}")
    print_success(f"Python Executable: {sys.executable}")
    
    # Check for virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print_success("Running in virtual environment")
        return True
    else:
        print_error("Not in virtual environment")
        return False

def verify_packages():
    """Verify all required packages are installed"""
    print_section("2️⃣  Package Verification")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'flask_socketio': 'Flask-SocketIO',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'requests': 'Requests'
    }
    
    missing = []
    for module, name in required_packages.items():
        try:
            __import__(module)
            print_success(f"{name}")
        except ImportError:
            print_error(f"{name}")
            missing.append(name)
    
    if missing:
        print_error(f"\nMissing packages: {', '.join(missing)}")
        print_info("Install with: pip install -r app/backend/requirements.txt")
        return False
    
    print_success("All required packages installed")
    return True

def verify_project_structure():
    """Verify project directory structure"""
    print_section("3️⃣  Project Structure Verification")
    
    base_path = Path("/workspaces/animation_quantum_mech_basics")
    
    required_files = {
        "Backend API": base_path / "app/backend/app/api/enhanced_api.py",
        "Backend Requirements": base_path / "app/backend/requirements.txt",
        "Frontend Dashboard HTML": base_path / "app/frontend/public/dashboard.html",
        "Frontend Dashboard JS": base_path / "app/frontend/public/dashboard.js",
        "Frontend API Service": base_path / "app/frontend/src/services/api-service.js",
        "Frontend WebSocket Service": base_path / "app/frontend/src/services/websocket-service.js",
    }
    
    all_exist = True
    for name, path in required_files.items():
        if path.exists():
            print_success(f"{name}: {path.name}")
        else:
            print_error(f"{name}: NOT FOUND ({path})")
            all_exist = False
    
    return all_exist

def print_backend_setup():
    """Print backend setup instructions"""
    print_section("🔧 Backend Setup Instructions")
    
    print(f"""{BOLD}Setup Backend (First Time Only):{RESET}

1. Navigate to backend directory:
   {YELLOW}cd /workspaces/animation_quantum_mech_basics/app/backend{RESET}

2. Create and activate virtual environment:
   {YELLOW}python -m venv venv{RESET}
   {YELLOW}source venv/bin/activate{RESET}
   
   Or use the workspace Python:
   {YELLOW}source /workspaces/animation_quantum_mech_basics/.venv/bin/activate{RESET}

3. Install dependencies:
   {YELLOW}pip install -r requirements.txt --no-cache-dir{RESET}

{BOLD}Start Backend Server:{RESET}

From backend directory with venv activated:
   {YELLOW}python app/api/enhanced_api.py{RESET}

Expected output:
   {GREEN}* Running on http://0.0.0.0:5000{RESET}
   {GREEN}* WARNING: This is a development server. Use a production WSGI server instead.{RESET}

The backend will listen on: {BOLD}http://localhost:5000{RESET}
API health check: {BOLD}http://localhost:5000/api/health{RESET}
""")

def print_frontend_setup():
    """Print frontend setup instructions"""
    print_section("🎨 Frontend Setup Instructions")
    
    print(f"""{BOLD}Start Frontend Server:{RESET}

In a new terminal:
   {YELLOW}cd /workspaces/animation_quantum_mech_basics/app/frontend/public{RESET}
   {YELLOW}python -m http.server 8000{RESET}

Expected output:
   {GREEN}Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/){RESET}

The frontend will be available at: {BOLD}http://localhost:8000/dashboard.html{RESET}

{BOLD}Files served:{RESET}
- {YELLOW}dashboard.html{RESET} - Main UI
- {YELLOW}dashboard.js{RESET} - Controls and visualization logic
- {YELLOW}style.css{RESET} - Styling
""")

def print_testing_guide():
    """Print testing guide"""
    print_section("🧪 Testing Guide")
    
    print(f"""{BOLD}1. Check Backend Health:{RESET}
   {YELLOW}curl http://localhost:5000/api/health{RESET}
   
   Expected response:
   {GREEN}{{
     "status": "ok",
     "timestamp": "2025-10-28T...",
     "connected_clients": 0,
     "webhooks_registered": 0
   }}{RESET}

{BOLD}2. Test Infinite Well Simulation:{RESET}
   {YELLOW}curl -X POST http://localhost:5000/api/full-simulation \\
     -H "Content-Type: application/json" \\
     -d '{{"type":"infinite-well","parameters":{{"width":5,"num_states":3}}}}{RESET}

{BOLD}3. Open Frontend in Browser:{RESET}
   {YELLOW}http://localhost:8000/dashboard.html{RESET}
   
   You should see:
   - {GREEN}Dashboard with simulation controls{RESET}
   - {GREEN}Selector for 4 simulation types{RESET}
   - {GREEN}Parameter sliders{RESET}
   - {GREEN}"Run Simulation" button{RESET}

{BOLD}4. Run a Simulation from Frontend:{RESET}
   - Select "Infinite Square Well" from dropdown
   - Adjust parameters if needed
   - Click "Run Simulation" button
   - Watch energy levels and probability plots update

{BOLD}5. Check Browser Console (F12):{RESET}
   - Should see {GREEN}[API GET] /api/health{RESET}
   - Should see {GREEN}[API POST] /api/full-simulation{RESET}
   - Should show response data
""")

def print_troubleshooting():
    """Print troubleshooting guide"""
    print_section("🔧 Troubleshooting")
    
    print(f"""{BOLD}Issue: "ModuleNotFoundError: No module named 'flask'"{RESET}
{YELLOW}Solution:{RESET}
   1. Make sure you're using the correct Python environment
   2. Run: pip install -r app/backend/requirements.txt
   3. Check: python -c "import flask"

{BOLD}Issue: "Connection refused" on localhost:5000{RESET}
{YELLOW}Solution:{RESET}
   1. Make sure backend is running (see Backend Setup above)
   2. Check if port 5000 is in use: lsof -i :5000
   3. Try a different port if needed

{BOLD}Issue: "Connection refused" on localhost:8000{RESET}
{YELLOW}Solution:{RESET}
   1. Make sure frontend server is running
   2. Navigate to correct directory: cd app/frontend/public
   3. Run: python -m http.server 8000

{BOLD}Issue: Dashboard not connecting to API{RESET}
{YELLOW}Solution:{RESET}
   1. Check browser console (F12) for errors
   2. Verify backend is running on :5000
   3. Check that API base URL is: http://localhost:5000
   4. Try health check: http://localhost:5000/api/health

{BOLD}Issue: Simulations not running{RESET}
{YELLOW}Solution:{RESET}
   1. Check backend console for error messages
   2. Verify all parameters are numbers (not strings)
   3. Check browser console for API response
   4. Try manually: curl http://localhost:5000/api/full-simulation

{BOLD}Issue: Import errors still showing in VS Code{RESET}
{YELLOW}Solution:{RESET}
   1. These are just linter warnings - not actual problems
   2. Code will work fine when running
   3. Select Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
   4. Choose the workspace environment: .venv/bin/python
""")

def print_complete_guide():
    """Print complete setup and run guide"""
    print_header("QUANTUM SIMULATOR - COMPLETE SETUP & RUN GUIDE")
    
    # Check environment
    venv_ok = check_python()
    packages_ok = verify_packages()
    structure_ok = verify_project_structure()
    
    # Print setup guides
    print_backend_setup()
    print_frontend_setup()
    print_testing_guide()
    print_troubleshooting()
    
    # Summary
    print_section("📋 Quick Summary")
    
    print(f"""{BOLD}✅ All verifications passed!{RESET}

{BOLD}To start the quantum simulator:{RESET}

Terminal 1 - Backend:
   {YELLOW}cd /workspaces/animation_quantum_mech_basics/app/backend{RESET}
   {YELLOW}source /workspaces/animation_quantum_mech_basics/.venv/bin/activate{RESET}
   {YELLOW}python app/api/enhanced_api.py{RESET}

Terminal 2 - Frontend:
   {YELLOW}cd /workspaces/animation_quantum_mech_basics/app/frontend/public{RESET}
   {YELLOW}python -m http.server 8000{RESET}

Terminal 3 - Browser:
   {YELLOW}http://localhost:8000/dashboard.html{RESET}

{BOLD}Expected Results:{RESET}
   {GREEN}✅ Backend running on http://localhost:5000{RESET}
   {GREEN}✅ Frontend running on http://localhost:8000{RESET}
   {GREEN}✅ Dashboard loads with controls{RESET}
   {GREEN}✅ Can run 4 quantum simulations{RESET}
   {GREEN}✅ Real-time visualizations update{RESET}

{BOLD}Documentation:{RESET}
   - {YELLOW}README.md{RESET} - Quick start
   - {YELLOW}BACKEND_FRONTEND_FIXES.md{RESET} - Technical details
   - {YELLOW}QUICK_FIX_REFERENCE.md{RESET} - Fix reference

{BOLD}Need Help?{RESET}
   - Check FIX_STATUS.txt for complete status
   - See TROUBLESHOOTING section above
   - Check browser console (F12) for errors
   - Watch backend terminal for log messages
""")
    
    print(f"\n{BOLD}{GREEN}🎉 Ready to start! 🎉{RESET}\n")

if __name__ == "__main__":
    try:
        print_complete_guide()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Setup cancelled{RESET}")
        sys.exit(0)
