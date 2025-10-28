# 🚀 HOW TO RUN BOTH BACKEND & FRONTEND - COMPLETE GUIDE

## ✅ STATUS: BOTH SERVICES ARE READY!

**Backend (Port 5000):** ✅ Running
**Frontend (Port 8000):** ✅ Running
**Connection:** ✅ Ready to use

---

## 🎯 Option 1: ONE COMMAND START (Easiest)

Run this ONE command and both services start automatically:

```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

This will:
- ✅ Activate the virtual environment
- ✅ Start backend on port 5000
- ✅ Start frontend on port 8000
- ✅ Show you the access URLs

Then go to: **http://localhost:8000/dashboard.html**

---

## 🎯 Option 2: THREE SEPARATE TERMINALS (More Control)

### Terminal 1 - Start Backend

```bash
cd /workspaces/animation_quantum_mech_basics
source .venv/bin/activate
PYTHONPATH=/workspaces/animation_quantum_mech_basics/src python app/backend/app/api/enhanced_api.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server...
 * Restarting with stat
 * Debugger PIN: 123-456-789
127.0.0.1 - - [2025-10-28 06:23:06] "GET / HTTP/1.1" 404
```

### Terminal 2 - Start Frontend

```bash
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/)
```

### Terminal 3 - Open in Browser

```bash
# Option A: Open the Ports panel (recommended)
# 1. Look at bottom of VS Code → "Ports" tab
# 2. Click globe 🌐 next to port 8000
# 3. Your dashboard opens!

# Option B: Open manual URL
http://localhost:8000/dashboard.html
```

---

## 🧪 Test Backend & Frontend Connection

### Test 1: Backend Health Check

```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
    "status": "ok",
    "timestamp": "2025-10-28T06:23:06.491543",
    "connected_clients": 0,
    "webhooks_registered": 0
}
```

✅ If you see this, backend is working!

### Test 2: Run a Simulation via API

```bash
curl -X POST http://localhost:5000/api/full-simulation \
  -H "Content-Type: application/json" \
  -d '{"type":"infinite-well","parameters":{"width":5,"num_states":3}}'
```

**Expected:** Long JSON response with energy levels, wavefunction data, etc.

✅ If you see this, backend is computing!

### Test 3: Frontend Can Reach Backend

1. Open **http://localhost:8000/dashboard.html**
2. Open browser console (F12 or Ctrl+Shift+J)
3. Look for messages like:
   ```
   [API GET] /api/health
   [API POST] /api/full-simulation
   ```

✅ If you see these, frontend is connected!

### Test 4: Run a Simulation from Dashboard

1. Go to **http://localhost:8000/dashboard.html**
2. Select simulation type: "Infinite Square Well"
3. Click "Run Simulation"
4. Watch the plots update!

✅ If plots update, everything is working!

---

## 📊 How They Connect

```
┌─────────────────────────────────────────────────────────┐
│                  YOUR CODESPACE                         │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Backend (Flask API)                              │  │
│  │ - Port 5000                                      │  │
│  │ - Listens: http://0.0.0.0:5000                  │  │
│  │ - Endpoints: /api/health, /api/full-simulation  │  │
│  └──────────────────────────────────────────────────┘  │
│                        ↑↓ (HTTP)                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Frontend (HTTP Server)                           │  │
│  │ - Port 8000                                      │  │
│  │ - Serves: dashboard.html, dashboard.js, etc.    │  │
│  │ - Connects to backend on localhost:5000         │  │
│  └──────────────────────────────────────────────────┘  │
│
└─────────────────────────────────────────────────────────┘
         ↓↓ (PORT FORWARDING)
   
┌─────────────────────────────────────────────────────────┐
│          YOUR LOCAL BROWSER (Via Codespace)             │
│                                                         │
│  https://<codespace>-5000.app.github.dev               │
│  https://<codespace>-8000.app.github.dev               │
│                                                         │
│  → Click link → See Dashboard → Run Simulations!       │
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 PORT FORWARDING FOR CODESPACE

### Automatic (Recommended)
1. When a service starts, you'll see a notification:
   ```
   Your application running on port 5000 is available
   ```
2. Click **"Open in Browser"** button
3. Done! ✅

### Manual Forwarding
1. Press **Ctrl+Shift+P**
2. Type: **"Forward a Port"**
3. Enter: **5000** (then Enter)
4. Enter: **8000** (then Enter)
5. Now both ports are accessible!

### View Forwarded Ports
- Look at bottom of VS Code
- Click **"Ports"** tab
- See all forwarded ports
- Click globe 🌐 to open in browser

---

## 📁 What's Running

### Backend Service
```
Location:  app/backend/app/api/enhanced_api.py
Port:      5000
Type:      Flask API + SocketIO
Features:  6 REST endpoints + WebSocket
Physics:   Schrödinger solver (NumPy/SciPy)
```

**API Endpoints:**
- `GET /api/health` - Server status
- `POST /api/full-simulation` - Run any simulation
- `GET/POST /api/webhooks/*` - Event management
- WebSocket: `/socket.io/` - Real-time updates

### Frontend Service
```
Location:  app/frontend/public/
Port:      8000
Type:      HTTP Server
Features:  Interactive dashboard
Visuals:   Canvas + Three.js rendering
```

**Files Served:**
- `dashboard.html` - Main UI
- `dashboard.js` - Controls & logic (1000+ lines)
- `style.css` - Styling
- `*-visualizer.js` - Plotting libraries

---

## 🎮 Using the Dashboard

Once both services are running and you open the frontend:

1. **Select Simulation** - Dropdown with 4 options
   - Infinite Square Well
   - Finite Square Well
   - Harmonic Oscillator
   - Quantum Tunneling

2. **Adjust Parameters** - Sliders for:
   - Well width
   - Potential height/depth
   - Number of states
   - Other parameters

3. **Run Simulation** - Click button
   - Backend computes in ~100-200ms
   - Results appear instantly
   - Plots update automatically

4. **View Results**
   - Energy Level diagram (left)
   - Probability Density plot (right)
   - Numerical vs analytical comparison
   - Wavefunction visualization

---

## 📋 Troubleshooting

### Issue: "Connection refused" on 5000 or 8000
**Solution:**
```bash
# Check if services are running
ps aux | grep python | grep -E "5000|8000"

# If not running, restart:
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### Issue: "Can't reach" from browser
**Solution:**
1. Make sure ports are forwarded (Ports panel)
2. Try opening one port at a time
3. Try different browser or incognito mode
4. Check Codespace is still running

### Issue: Frontend loads but "Can't connect to backend"
**Solution:**
1. Open browser console (F12)
2. Look for error messages
3. Check backend is responding: `curl http://localhost:5000/api/health`
4. Verify API base URL: In dashboard.js line 9, should be `http://localhost:5000`

### Issue: Backend not responding
**Solution:**
```bash
# View backend logs
tail -f /workspaces/animation_quantum_mech_basics/backend.log

# Restart backend
bash /workspaces/animation_quantum_mech_basics/start_backend.sh

# Or manually:
cd /workspaces/animation_quantum_mech_basics
source .venv/bin/activate
PYTHONPATH=./src python app/backend/app/api/enhanced_api.py
```

### Issue: Frontend won't load
**Solution:**
```bash
# Check frontend is running
curl http://localhost:8000/dashboard.html

# If not, restart:
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000
```

---

## 🚀 QUICK COMMAND REFERENCE

| Task | Command |
|------|---------|
| **Start both services** | `bash /workspaces/animation_quantum_mech_basics/start_all.sh` |
| **Test backend** | `curl http://localhost:5000/api/health` |
| **Test frontend** | `curl http://localhost:8000/dashboard.html` |
| **View backend logs** | `tail -f /workspaces/animation_quantum_mech_basics/backend.log` |
| **View frontend logs** | `tail -f /workspaces/animation_quantum_mech_basics/app/frontend/public/../../../frontend.log` |
| **Kill all services** | `pkill -f "python.*enhanced_api\|python.*http.server"` |

---

## ✅ VERIFICATION CHECKLIST

Before saying "it works":

- [ ] Backend running? `curl http://localhost:5000/api/health`
- [ ] Frontend running? Open http://localhost:8000/dashboard.html
- [ ] Can see dashboard in browser? (Should show controls + canvas)
- [ ] Ports forwarded in Codespace? (Ports panel shows 5000 & 8000)
- [ ] Can run simulation? (Select option, click button, plots appear)
- [ ] Console has no errors? (F12 to check)

---

## 🎉 YOU'RE READY!

### Run This:
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### Then:
1. Open VS Code Ports panel
2. Click port 8000 → "Open in Browser"
3. See your quantum simulator!
4. Pick a simulation and run it!

**Enjoy exploring quantum mechanics! 🔬✨**
