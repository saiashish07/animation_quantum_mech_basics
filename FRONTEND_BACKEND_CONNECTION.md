# 🎯 FRONT-END & BACK-END CONNECTION VISUAL GUIDE

## ✅ EVERYTHING IS WORKING!

Both services are running and connected:
- ✅ **Backend (Port 5000)** - Running
- ✅ **Frontend (Port 8000)** - Running
- ✅ **Connection** - Ready

---

## 🚀 SIMPLEST WAY - ONE COMMAND

Copy and paste this ONE command into terminal:

```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

Then open your browser to:
```
http://localhost:8000/dashboard.html
```

**That's it! Your app is running!** 🎉

---

## 📊 VISUAL CONNECTION FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  YOUR CODESPACE CONTAINER (Ubuntu)                             │
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  BACKEND SERVICE     │         │  FRONTEND SERVICE    │    │
│  │  (Flask API)         │◄──HTTP──►  (HTTP Server)       │    │
│  │  Port 5000           │         │  Port 8000           │    │
│  │                      │         │                      │    │
│  │  • Solves Schrödinger│         │  • Serves HTML files │    │
│  │    equation          │         │  • Runs JavaScript   │    │
│  │  • Returns JSON      │         │  • Renders canvas    │    │
│  │  • WebSocket support │         │  • Controls UI       │    │
│  └──────────────────────┘         └──────────────────────┘    │
│            ▲                                    ▲               │
│            │ Backend logs ←→ Frontend calls → Backend API      │
│            │                                    │               │
│  ┌─────────┴────────────────────────────────────┴──────┐      │
│  │         PORT FORWARDING (GitHub Codespace)         │      │
│  │         Maps ports to your local machine           │      │
│  └──────────────────────────────────────────────────────┘      │
│                            ↓↓↓                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ├─ Port 5000 → Backend URL
                             │  (https://<space>-5000.app.github.dev)
                             │
                             └─ Port 8000 → Frontend URL
                                (https://<space>-8000.app.github.dev)
                                      ↓↓↓
                    ┌─────────────────────────────────┐
                    │   YOUR LOCAL BROWSER            │
                    │   Opens Quantum Dashboard!      │
                    │   • See controls                │
                    │   • Run simulations             │
                    │   • Watch plots update          │
                    └─────────────────────────────────┘
```

---

## 🔄 DATA FLOW - HOW THEY CONNECT

### Step 1: User Opens Dashboard
```
Browser → https://<codespace>-8000.app.github.dev/dashboard.html
          ↓
        Frontend loads (HTML, CSS, JavaScript)
```

### Step 2: Frontend Initializes
```
JavaScript runs (dashboard.js)
          ↓
Creates QuantumAPIService('http://localhost:5000')
          ↓
Connects to backend on port 5000
```

### Step 3: User Selects Simulation
```
Dashboard UI ← User clicks "Infinite Square Well"
          ↓
JavaScript calls: api.fullSimulation('infinite-well', {...})
```

### Step 4: API Request Sent
```
Frontend makes HTTP POST to Backend:
POST http://localhost:5000/api/full-simulation
{
  "type": "infinite-well",
  "parameters": {"width": 5, "num_states": 3}
}
```

### Step 5: Backend Computes
```
Backend receives request
          ↓
Solves Schrödinger equation (NumPy/SciPy)
          ↓
Computes energy levels, eigenstates
          ↓
Generates visualization data (JSON)
```

### Step 6: Response Returns
```
Backend sends JSON response (2-3 KB):
{
  "energy_levels": [0.196, 0.784, 1.765],
  "wavefunctions": [...],
  "grid": {...},
  "probability_density": [...]
}
          ↓
Frontend receives in ~100-200ms
```

### Step 7: Frontend Visualizes
```
JavaScript receives data
          ↓
Extracts: energy levels, probabilities
          ↓
Draws on canvas using Canvas API & Three.js
          ↓
User sees: plots, energy diagram, wavefunction
```

---

## 📍 ACCESS POINTS

### During Development (In Codespace Container)
```
Backend:  http://localhost:5000
Frontend: http://localhost:8000
```

### From Your Local Browser (Via Port Forwarding)
```
Backend:  https://<codespace-name>-5000.app.github.dev
Frontend: https://<codespace-name>-8000.app.github.dev
```

### Example URLs
```
Health check:  https://amazing-zebra-wx57ppx6-5000.app.github.dev/api/health
Dashboard:     https://amazing-zebra-wx57ppx6-8000.app.github.dev/dashboard.html
```

---

## 🚀 STEP-BY-STEP TO GET RUNNING

### Step 1: Start Services (Copy-paste this)
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

You should see:
```
✅ Backend is RUNNING!
✅ Frontend is RUNNING!
🎉 SERVICES STARTED!
```

### Step 2: Open Ports Panel
- Look at **bottom of VS Code**
- Click **"Ports"** tab
- You should see two ports listed

### Step 3: Forward Ports
- Click globe 🌐 next to **Port 8000**
- Browser opens with dashboard!

Or manually:
- Ctrl+Shift+P
- Search: "Forward a Port"
- Enter: 5000
- Enter: 8000

### Step 4: See Your Dashboard
Browser automatically opens to:
```
http://localhost:8000/dashboard.html
```

You should see:
- Title: "Quantum Mechanics Simulator"
- Sidebar with controls
- Two empty canvases (waiting for data)
- "Server: Connecting..." status

### Step 5: Run a Simulation
1. Click dropdown → Select "Infinite Square Well"
2. Click "Run Simulation"
3. Watch plots appear! ✨

---

## 🧪 VERIFY EVERYTHING IS CONNECTED

### Test 1: Backend Responding?
```bash
curl http://localhost:5000/api/health
```
Should show:
```json
{"status": "ok", "timestamp": "...", ...}
```

### Test 2: Frontend Loading?
```bash
curl -I http://localhost:8000/dashboard.html
```
Should show:
```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
```

### Test 3: Backend Computing?
```bash
curl -X POST http://localhost:5000/api/full-simulation \
  -H "Content-Type: application/json" \
  -d '{"type":"infinite-well","parameters":{"width":5,"num_states":3}}'
```
Should show long JSON with energy data

### Test 4: Frontend → Backend Connection?
1. Open dashboard in browser
2. Press F12 (open console)
3. Look for: `[API GET] /api/health`
4. Should see: `Response: {status: "ok", ...}`

✅ All tests pass = Everything is connected!

---

## 🎮 WHAT YOU CAN DO

Once running:

1. **Select any of 4 simulations:**
   - Infinite Square Well
   - Finite Square Well
   - Harmonic Oscillator
   - Quantum Tunneling

2. **Adjust parameters with sliders:**
   - Width: 1-10
   - Depth/Height: 0-20
   - States: 1-5

3. **Click "Run Simulation"**
   - Backend computes instantly
   - Plots update on screen
   - See energy levels & wavefunctions

4. **Explore the results:**
   - Energy level spacing
   - Probability density distribution
   - Ground state vs excited states
   - Tunneling probability

---

## 🛠️ COMMON COMMANDS

### Start Everything
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### View Backend Logs (Real-time)
```bash
tail -f /workspaces/animation_quantum_mech_basics/backend.log
```

### View Frontend Logs (Real-time)
```bash
tail -f /workspaces/animation_quantum_mech_basics/app/frontend/public/../../../frontend.log
```

### Stop Services
```bash
# Kill backend and frontend
pkill -f "python.*enhanced_api"
pkill -f "python.*http.server"
```

### Test Backend Solo
```bash
curl -X POST http://localhost:5000/api/full-simulation \
  -H "Content-Type: application/json" \
  -d '{"type":"infinite-well","parameters":{"width":5,"num_states":3}}' | python -m json.tool
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

## ❓ FAQS

**Q: Backend shows "ModuleNotFoundError"?**
A: Make sure Python path is set correctly. Use: `PYTHONPATH=./src python ...`

**Q: Frontend shows "Can't connect to API"?**
A: Check F12 console. Verify backend is running: `curl http://localhost:5000/api/health`

**Q: Port 5000 or 8000 already in use?**
A: Kill existing process: `lsof -i :5000` then `kill -9 <PID>`

**Q: Need different port?**
A: Edit the files:
- Backend: Change port in `enhanced_api.py` line (socketio.run port)
- Frontend: Change in `dashboard.js` line 8 (new QuantumAPIService URL)

**Q: How to access from outside Codespace?**
A: Use port forwarding URLs from Ports panel (automatic)

---

## ✅ FINAL CHECKLIST

Before you start:
- [ ] You're in /workspaces/animation_quantum_mech_basics
- [ ] .venv folder exists (virtual environment)
- [ ] All packages installed (pip list shows flask, numpy, scipy)

To run:
- [ ] Run: `bash start_all.sh`
- [ ] See: "SERVICES STARTED!"
- [ ] Open: Ports panel
- [ ] Click: Globe on port 8000
- [ ] See: Dashboard loads
- [ ] Try: Run a simulation
- [ ] Enjoy: Quantum mechanics! 🎉

---

## 🎉 YOU'RE READY!

**Just run:**
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

**Then open the Ports panel and click port 8000!**

Welcome to your quantum simulator! 🚀🔬✨
