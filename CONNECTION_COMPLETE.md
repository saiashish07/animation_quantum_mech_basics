# ✅ BACKEND & FRONTEND - COMPLETE CONNECTION GUIDE

## 🎉 STATUS: FULLY CONNECTED & READY!

**Backend:** ✅ Running on port 5000  
**Frontend:** ✅ Running on port 8000  
**Connection:** ✅ Tested and verified  
**All Tests:** ✅ PASSED

---

## 🚀 HOW TO START BOTH SERVICES

### ⚡ Method 1: ONE COMMAND (Easiest - Recommended)

```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

**That's it!** Both services start automatically.

Then:
1. Look at bottom of VS Code → **Ports** tab
2. Click globe 🌐 next to **Port 8000**
3. Your dashboard opens in browser! ✅

---

### 📋 Method 2: Three Separate Terminals

#### Terminal 1 - Backend
```bash
cd /workspaces/animation_quantum_mech_basics
source .venv/bin/activate
PYTHONPATH=./src python app/backend/app/api/enhanced_api.py
```

Wait for: `* Running on http://0.0.0.0:5000`

#### Terminal 2 - Frontend
```bash
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000
```

Wait for: `Serving HTTP on 0.0.0.0 port 8000`

#### Terminal 3 - Open Browser
```
http://localhost:8000/dashboard.html
```

---

## 🧪 VERIFY EVERYTHING IS WORKING

### Test 1: Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected output:
```json
{
    "status": "ok",
    "timestamp": "2025-10-28T...",
    "connected_clients": 0,
    "webhooks_registered": 0
}
```

✅ If you see this, backend is working!

### Test 2: Backend Computing
```bash
curl -X POST http://localhost:5000/api/full-simulation \
  -H "Content-Type: application/json" \
  -d '{"type":"infinite-well","parameters":{"width":5,"num_states":3}}'
```

Expected: Long JSON response with energy levels  
✅ If you see data, backend is computing!

### Test 3: Frontend Loads
```bash
curl http://localhost:8000/dashboard.html | head -20
```

Should show HTML with title "Quantum Mechanics Simulator"  
✅ If you see HTML, frontend is serving!

### Test 4: Interactive Test
1. Open: `http://localhost:8000/dashboard.html`
2. Open browser console: F12 or Ctrl+Shift+J
3. Look for messages like: `[API GET] /api/health`
4. Select "Infinite Square Well" from dropdown
5. Click "Run Simulation"
6. Watch plots appear! ✨

✅ If plots appear, everything is connected!

---

## 🔄 HOW THEY COMMUNICATE

```
┌────────────────────┐
│  Your Browser      │
│  (Port 8000)       │
└─────────┬──────────┘
          │
          │ HTTP Request:
          │ POST /api/full-simulation
          │
          ▼
┌────────────────────┐
│  Backend Server    │
│  (Port 5000)       │
│                    │
│  • Receives request│
│  • Solves Physics  │
│  • Computes Data   │
│  • Returns JSON    │
└─────────┬──────────┘
          │
          │ HTTP Response:
          │ {energy_levels, wavefunction, ...}
          │
          ▼
┌────────────────────┐
│  Frontend JS       │
│                    │
│  • Receives data   │
│  • Draws plots     │
│  • Updates canvas  │
│  • Shows results   │
└────────────────────┘
```

---

## 📊 WHAT EACH SERVICE DOES

### Backend (Port 5000)
**File:** `app/backend/app/api/enhanced_api.py`

**Responsibilities:**
- Listens for HTTP requests on port 5000
- Receives quantum simulation parameters
- Solves the Schrödinger equation using NumPy/SciPy
- Computes energy levels and eigenfunctions
- Calculates probability density distributions
- Returns complete results as JSON
- Provides WebSocket for real-time updates

**Endpoints:**
- `GET /api/health` - Server status
- `POST /api/full-simulation` - Run any simulation
- `GET/POST /api/webhooks/*` - Event management

### Frontend (Port 8000)
**File:** `app/frontend/public/dashboard.html`

**Responsibilities:**
- Serves interactive dashboard to users
- Provides parameter controls (sliders)
- Sends simulation requests to backend
- Receives computation results
- Renders plots on Canvas
- Updates visualizations in real-time
- Displays energy diagrams
- Shows probability density plots

**Files:**
- `dashboard.html` - UI structure
- `dashboard.js` - Controls and logic (1000+ lines)
- `style.css` - Styling
- `api-service.js` - Backend communication
- `websocket-service.js` - Real-time updates

---

## 🎮 USING THE SIMULATOR

Once both services are running and you open the dashboard:

### 1. Select a Simulation
Click dropdown to choose:
- **Infinite Square Well** - Particle in a box
- **Finite Square Well** - Potential well with finite depth
- **Harmonic Oscillator** - Spring-like potential
- **Quantum Tunneling** - Barrier penetration

### 2. Adjust Parameters
Use sliders to control:
- Well width
- Potential height/depth
- Number of states
- Other simulation-specific parameters

### 3. Run Simulation
Click **"Run Simulation"** button

### 4. View Results
See instantly:
- Energy level diagram (left canvas)
- Probability density plot (right canvas)
- Numerical vs analytical comparison
- Wavefunction visualization

---

## 📁 IMPORTANT FILES

### Backend
```
app/backend/
├── app/
│   ├── api/
│   │   └── enhanced_api.py          ← Main server (6 endpoints)
│   ├── solvers/
│   │   └── quantum_solvers.py       ← Computation logic
│   └── webhooks/
│       └── webhook_manager.py       ← Event system
└── requirements.txt
```

### Frontend
```
app/frontend/
├── public/
│   ├── dashboard.html               ← Main UI
│   ├── dashboard.js                 ← Controller (1000+ lines)
│   ├── style.css                    ← Styling
│   └── *.js                         ← Visualizers
└── src/
    └── services/
        ├── api-service.js           ← Backend communication
        └── websocket-service.js     ← Real-time updates
```

### Physics Core
```
src/quantum_playground/
├── solvers.py                       ← Schrödinger solver
├── potentials.py                    ← 4 potential types
└── animations/                      ← Simulation implementations
```

---

## 🔌 PORT FORWARDING (For Codespace)

When running in GitHub Codespace, you need port forwarding to access from your browser.

### Automatic (Easiest)
1. Start service
2. See notification: "Your application running on port X is available"
3. Click "Open in Browser"
4. Done! ✅

### Manual
1. Press `Ctrl+Shift+P`
2. Type: "Forward a Port"
3. Enter: `5000` (for backend)
4. Enter: `8000` (for frontend)
5. Done! ✅

### View Forwarded Ports
- Click **Ports** tab at bottom of VS Code
- See all forwarded ports
- Click globe 🌐 to open in browser

---

## 🛠️ HELPFUL COMMANDS

### View Logs (Real-time)
```bash
# Backend logs
tail -f /workspaces/animation_quantum_mech_basics/backend.log

# Frontend logs
tail -f /workspaces/animation_quantum_mech_basics/app/frontend/public/../../../frontend.log
```

### Check Running Services
```bash
ps aux | grep python | grep -E "5000|8000"
```

### Kill All Services
```bash
pkill -f "python.*enhanced_api"
pkill -f "python.*http.server"
```

### Kill Specific Service
```bash
lsof -i :5000    # Find what's using port 5000
lsof -i :8000    # Find what's using port 8000
kill -9 <PID>    # Kill the process
```

### Restart Just Backend
```bash
pkill -f "python.*enhanced_api"
cd /workspaces/animation_quantum_mech_basics
source .venv/bin/activate
PYTHONPATH=./src python app/backend/app/api/enhanced_api.py &
```

### Restart Just Frontend
```bash
pkill -f "python.*http.server"
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000 &
```

---

## ❓ TROUBLESHOOTING

### Problem: "Connection refused" on port 5000
**Solution:**
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# If not running, start it
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### Problem: "Connection refused" on port 8000
**Solution:**
```bash
# Check if frontend is running
curl http://localhost:8000/dashboard.html

# If not running, start it
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000
```

### Problem: Frontend loads but "Can't connect to API"
**Solution:**
1. Open browser console (F12)
2. Look for error messages
3. Verify backend: `curl http://localhost:5000/api/health`
4. Check API base URL in `app/frontend/src/services/api-service.js` line 8

### Problem: Port already in use
**Solution:**
```bash
# Find what's using the port
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use different ports (edit code accordingly)
```

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
# Activate venv
source /workspaces/animation_quantum_mech_basics/.venv/bin/activate

# Install missing package
pip install <package-name>

# Or reinstall all
pip install -r app/backend/requirements.txt
```

---

## 📚 DOCUMENTATION FILES

| File | Purpose |
|------|---------|
| **HOW_TO_RUN.md** | Complete step-by-step guide |
| **FRONTEND_BACKEND_CONNECTION.md** | Visual connection diagrams |
| **CODESPACE_SETUP.md** | Codespace-specific guide |
| **QUICK_REFERENCE.sh** | Commands quick reference |
| **README.md** | Project overview |

---

## ✅ VERIFICATION CHECKLIST

Before saying "it works":

- [ ] Backend running? `curl http://localhost:5000/api/health`
- [ ] Frontend serving? `curl http://localhost:8000/dashboard.html`
- [ ] Can see dashboard? (Title, controls, canvases)
- [ ] Ports forwarded? (Ports panel shows 5000 & 8000)
- [ ] Can run simulation? (Select type, click button, plots appear)
- [ ] No console errors? (F12 to check)

---

## 🎉 QUICK START

**Copy-paste this command:**
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

**Then:**
1. Open PORTS panel (bottom of VS Code)
2. Click globe 🌐 next to port 8000
3. Select a simulation
4. Click "Run"
5. Enjoy! 🚀

---

## 📞 NEED HELP?

- **Backend issue?** → Check `backend.log`
- **Frontend issue?** → Check browser console (F12)
- **Connection issue?** → Verify both services running
- **Port conflict?** → Kill process using `lsof -i :<port>`
- **Import error?** → Activate venv: `source .venv/bin/activate`

---

**Your quantum simulator is ready! 🔬✨**
