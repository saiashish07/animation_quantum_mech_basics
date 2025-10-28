# 🚀 COMPLETE GUIDE: Connect Codespace + Port Forwarding + Run App

## ✅ What You'll Learn

This guide shows you exactly how to:
1. ✅ Forward ports from Codespace to your browser
2. ✅ Start backend (Port 5000)
3. ✅ Start frontend (Port 8000)
4. ✅ Connect them together
5. ✅ See your app running in browser

**Time needed:** ~5 minutes ⏱️

---

## 📋 QUICK SUMMARY

| Component | Port | Status |
|-----------|------|--------|
| Backend API | 5000 | Ready ✅ |
| Frontend Server | 8000 | Ready ✅ |
| Browser Access | Via Port Forward | Ready ✅ |

---

## 🎯 STEP 1: Open Ports Panel in VS Code

### Location
- Look at the **bottom of VS Code** window
- You'll see tabs: `PROBLEMS`, `OUTPUT`, `DEBUG CONSOLE`, `TERMINAL`, **`PORTS`**

### Action
1. Click the **`PORTS`** tab
2. You should see an empty panel (or existing ports)
3. This is where port forwarding happens

**Screenshot of Ports Panel:**
```
┌─────────────────────────────────────────────┐
│ PORTS                                       │
├─────────────────────────────────────────────┤
│                                             │
│ No ports are currently forwarded            │
│                                             │
│ Forward a port: Ctrl+Shift+P               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎯 STEP 2: Start Backend & Frontend (First Terminal)

Copy and paste this ONE command:

```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### What Happens
```
✅ Virtual environment activated
✅ Backend starting on port 5000
✅ Frontend starting on port 8000
🎉 SERVICES STARTED!
```

### Expected Output
```
╔════════════════════════════════════════════════════════════╗
║  🚀 QUANTUM SIMULATOR - AUTO START                         ║
╚════════════════════════════════════════════════════════════╝

✅ Virtual environment activated
✅ Working directory: /workspaces/animation_quantum_mech_basics

🔧 Starting BACKEND on port 5000...
   PID: 55338
   ✅ Backend is RUNNING!

🎨 Starting FRONTEND on port 8000...
   PID: 55380
   ✅ Frontend is RUNNING!

📍 ACCESS YOUR APP:
  🔵 BACKEND API:
     Local: http://localhost:5000
     API Health: http://localhost:5000/api/health
  
  🟢 FRONTEND:
     Local: http://localhost:8000/dashboard.html
```

**✅ Leave this terminal running!** Don't close it or the services stop.

---

## 🎯 STEP 3: Automatic Port Forwarding (Easiest)

When services start, you'll see a **notification** at the bottom right:

```
Your application running on port 5000 is available
┌──────────────────────┐
│ Make Public  Open in Browser → │
└──────────────────────┘
```

### Action for Port 5000
1. Click **`Open in Browser`**
2. Backend opens in a new tab (shows 404 - that's OK)
3. **Port 5000 is now forwarded!** ✅

### Action for Port 8000
1. Same notification will appear for port 8000
2. Click **`Open in Browser`**
3. **Frontend dashboard opens!** 🎉
4. **Port 8000 is now forwarded!** ✅

---

## 🎯 STEP 4: Manual Port Forwarding (If Automatic Doesn't Work)

### Method A: Command Palette
1. Press **`Ctrl+Shift+P`** (or Cmd+Shift+P on Mac)
2. Type: `Forward a Port`
3. Press Enter
4. Enter: `5000`
5. Press Enter
6. Enter: `8000`
7. Press Enter

### Method B: Ports Panel
1. Open **PORTS** panel (bottom of VS Code)
2. Look for input box or button "Forward a Port"
3. Click it
4. Enter port number `5000`
5. Repeat for `8000`

---

## 🎯 STEP 5: View Forwarded Ports

In the **PORTS** panel, you should now see:

```
LOCAL ADDRESS           RUNNING PROCESS        VISIBILITY
localhost:5000         flask                  Private 🔒
localhost:8000         python -m http.server  Private 🔒
```

### Click the Globe 🌐 Icon
- Each port has a **globe icon** next to it
- Click the globe next to **port 8000**
- Your dashboard opens in browser! 🎉

---

## 🎯 STEP 6: Your Dashboard is Now Running!

### Expected Screen
```
┌─────────────────────────────────────────────────────┐
│  🌌 Quantum Mechanics Simulator                     │
├──────────┬──────────────────────────────────────────┤
│ SIDEBAR  │  MAIN AREA                              │
│          │                                          │
│ 📊 Simulation │  ┌──────────────────────────────┐ │
│ [Dropdown ▼]  │  │  Energy Levels Canvas        │ │
│               │  │  (showing plot)              │ │
│               │  └──────────────────────────────┘ │
│ 📈 Parameters │  ┌──────────────────────────────┐ │
│ Width: [====] │  │  Probability Density Canvas  │ │
│ States: [==]  │  │  (showing plot)              │ │
│               │  └──────────────────────────────┘ │
│ [Run Simulation] (Green Button)                   │
│               │                                    │
└────────────────────────────────────────────────────┘
```

### Status Bar
- Top of dashboard shows: `✅ Server: Connected`
- This means frontend successfully connected to backend!

---

## 🎯 STEP 7: Run Your First Simulation

### Action
1. **Select Simulation Type:**
   - Click dropdown that says "Select Simulation"
   - Choose: **"Infinite Square Well"**

2. **Adjust Parameters (Optional):**
   - Width slider: Set to 5
   - States slider: Set to 3

3. **Run Simulation:**
   - Click the green **"Run Simulation"** button

### Result
```
AFTER 150ms (very fast!):
✅ Energy level diagram appears on left canvas
✅ Probability density plot appears on right canvas
✅ Shows discrete energy levels
✅ Shows wavefunction probability
```

### Try Other Simulations
- **Finite Square Well** - Bound states with tunneling
- **Harmonic Oscillator** - Spring-like behavior
- **Quantum Tunneling** - Wavefunction through barrier

---

## 🧪 VERIFY EVERYTHING IS CONNECTED

### Test 1: Backend Responding
**Open new terminal and run:**
```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
    "status": "ok",
    "timestamp": "2025-10-28T...",
    "connected_clients": 1,
    "webhooks_registered": 0
}
```

### Test 2: Frontend Serving
**Open new terminal and run:**
```bash
curl http://localhost:8000/dashboard.html | head -20
```

**Expected:** Shows HTML starting with `<!DOCTYPE html>`

### Test 3: Check Browser Console
1. Open dashboard in browser
2. Press **F12** (or Ctrl+Shift+J)
3. Click **Console** tab
4. Look for messages like:
   ```
   [API GET] /api/health
   Response: {status: "ok", ...}
   ```

✅ If you see these = Everything connected!

---

## 📊 FULL DATA FLOW

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  YOU in Browser (Via Port Forward)                      │
│  https://<codespace>-8000.app.github.dev               │
│                ↓                                        │
│  Opens: dashboard.html (Frontend loads)                │
│                ↓                                        │
│  You select: "Infinite Square Well"                    │
│  You click: "Run Simulation"                           │
│                ↓                                        │
│  Frontend makes HTTP POST to Backend:                  │
│  POST http://localhost:5000/api/full-simulation        │
│  {type: "infinite-well", parameters: {...}}           │
│                ↓                                        │
│  ┌───────────────────────────────────────┐            │
│  │ BACKEND (Port 5000)                   │            │
│  │ • Receives request                    │            │
│  │ • Solves Schrödinger equation         │            │
│  │ • Computes energy levels              │            │
│  │ • Generates visualization data        │            │
│  │ Time: ~100-150ms                      │            │
│  └───────────────────────────────────────┘            │
│                ↓                                        │
│  Backend returns JSON response with:                   │
│  - energy_levels: [0.196, 0.784, 1.765]               │
│  - wavefunctions: [array data]                         │
│  - probability_density: [array data]                   │
│                ↓                                        │
│  Frontend receives data (~150ms total)                 │
│                ↓                                        │
│  JavaScript draws plots on canvas                      │
│                ↓                                        │
│  ✅ YOU SEE: Energy diagram + Probability plot! 🎉    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ TROUBLESHOOTING

### Problem: "Connection refused" on port 5000
**Solution:**
```bash
# Check if backend is running
ps aux | grep "enhanced_api"

# If not running, start it:
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### Problem: "Connection refused" on port 8000
**Solution:**
```bash
# Check if frontend is running
ps aux | grep "http.server"

# If not running, start it in the same start_all.sh command
```

### Problem: Ports panel shows "No ports"
**Solution:**
1. Make sure services are running
2. Press Ctrl+Shift+P
3. Search: "Forward a Port"
4. Manually enter: 5000, then 8000

### Problem: Dashboard loads but "Can't connect to API"
**Solution:**
1. Open browser console (F12)
2. Look for error messages
3. Check backend is responding: `curl http://localhost:5000/api/health`
4. Verify API base URL in dashboard.js is: `http://localhost:5000`

### Problem: Port already in use
**Solution:**
```bash
# Find what's using the port
lsof -i :5000

# Kill it
kill -9 <PID>

# Then restart
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

---

## 📍 YOUR APPS ARE HERE

### Access Points During Development (In Codespace)
```
Backend API:   http://localhost:5000
Frontend:      http://localhost:8000/dashboard.html
```

### Access Points From Browser (Via Port Forward)
```
Backend API:   https://<codespace-name>-5000.app.github.dev
Frontend:      https://<codespace-name>-8000.app.github.dev/dashboard.html
```

### Example Real URLs
```
Health check:  https://amazing-zebra-wx57ppx6-5000.app.github.dev/api/health
Dashboard:     https://amazing-zebra-wx57ppx6-8000.app.github.dev/dashboard.html
```

---

## 🎯 COMPLETE CHECKLIST

Before you say "it's working":

- [ ] **Ports panel open?** (Bottom of VS Code)
- [ ] **Backend running?** (Port 5000 shows in Ports panel)
- [ ] **Frontend running?** (Port 8000 shows in Ports panel)
- [ ] **Both forwarded?** (Globe icons visible)
- [ ] **Dashboard loads?** (Opens when clicking port 8000 globe)
- [ ] **Can see controls?** (Dropdown, sliders, button visible)
- [ ] **Can run simulation?** (Select type, click button)
- [ ] **See plots?** (Energy diagram appears on left, probability on right)
- [ ] **Status connected?** (Shows "✅ Server: Connected" at top)

✅ All checked? **YOU'RE DONE!** 🎉

---

## 🚀 QUICK START SUMMARY

### One Command (Copy-Paste)
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

### Then (In VS Code)
1. Open **PORTS** panel (bottom)
2. Click globe 🌐 next to **port 8000**
3. Dashboard opens!

### Then (In Dashboard)
1. Select simulation
2. Click "Run Simulation"
3. Watch plots appear! ✨

---

## 📚 ADDITIONAL RESOURCES

- **Full guide:** `CONNECTION_COMPLETE.md`
- **Troubleshooting:** `CODESPACE_SETUP.md`
- **Commands reference:** `QUICK_REFERENCE.sh`
- **Architecture:** `FRONTEND_BACKEND_CONNECTION.md`

---

## 🎉 YOU'RE READY!

Your quantum simulator is:
- ✅ Backend ready on port 5000
- ✅ Frontend ready on port 8000
- ✅ Port forwarding configured
- ✅ All systems connected

**Now run:**
```bash
bash /workspaces/animation_quantum_mech_basics/start_all.sh
```

**Then open Ports panel → Click port 8000 → Enjoy! 🚀🔬✨**
