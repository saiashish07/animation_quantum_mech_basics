# 🚀 GitHub Codespace Setup Guide - Quantum Simulator

## ✅ Status: EVERYTHING IS RUNNING!

Both backend and frontend services are already started and ready to use!

---

## 🌐 Access Your Application

### Option 1: VS Code Ports Panel (Easiest)
1. In VS Code, open the **"Ports"** panel (bottom panel, click "Ports" tab)
2. You should see two entries:
   - **Port 5000** (Backend API)
   - **Port 8000** (Frontend)
3. **Click the globe icon 🌐** next to each port to open in browser

### Option 2: Manual Port Forwarding
1. Go to **Command Palette** (Ctrl+Shift+P)
2. Search for: **"Forward a Port"**
3. Enter: `5000` (for backend)
4. Enter: `8000` (for frontend)

### Option 3: GitHub Codespace URLs
You'll see notifications when ports are forwarded. The URLs will look like:
- **Backend**: `https://<codespace-name>-5000.app.github.dev`
- **Frontend**: `https://<codespace-name>-8000.app.github.dev`

---

## 🎯 Access Points

| Service | Local URL | Codespace URL | Port |
|---------|-----------|---------------|------|
| **Backend API** | http://localhost:5000/api/health | https://<codespace>-5000.app.github.dev/api/health | 5000 |
| **Frontend Dashboard** | http://localhost:8000/dashboard.html | https://<codespace>-8000.app.github.dev/dashboard.html | 8000 |

---

## 🧪 Test Your Setup

### 1. Test Backend Health (in new terminal)
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{
  "status": "ok",
  "timestamp": "2025-10-28T...",
  "connected_clients": 0,
  "webhooks_registered": 0
}
```

### 2. Open Frontend Dashboard
Open your browser and go to:
```
http://localhost:8000/dashboard.html
```

You should see:
- ✅ Quantum simulation dashboard
- ✅ Dropdown with 4 simulation types
- ✅ Parameter sliders
- ✅ "Run Simulation" button
- ✅ Energy level visualization
- ✅ Probability density plots

### 3. Run a Test Simulation
- Select "Infinite Square Well" from dropdown
- Click "Run Simulation"
- Watch the plots update!

---

## 📝 Terminal Commands Reference

### Start Backend (if it stops)
```bash
bash /workspaces/animation_quantum_mech_basics/start_backend.sh
```

### Start Frontend (if it stops)
```bash
bash /workspaces/animation_quantum_mech_basics/start_frontend.sh
```

### Check Backend Logs
```bash
# Show last 20 lines of backend output
curl -s http://localhost:5000/api/health | jq
```

### Restart Everything
```bash
# Terminal 1 - Backend
bash /workspaces/animation_quantum_mech_basics/start_backend.sh

# Terminal 2 - Frontend
bash /workspaces/animation_quantum_mech_basics/start_frontend.sh
```

---

## 🛠️ Troubleshooting

### Issue: "Connection refused" or "Can't reach"
**Solution:**
1. Check Ports panel - are both ports forwarded?
2. Look for notifications at top of VS Code
3. Try forwarding manually: Ctrl+Shift+P → "Forward a Port"

### Issue: Backend shows "Module not found"
**Solution:**
```bash
# Install missing module
source /workspaces/animation_quantum_mech_basics/.venv/bin/activate
pip install <module-name>

# Then restart backend
bash /workspaces/animation_quantum_mech_basics/start_backend.sh
```

### Issue: Frontend loads but can't connect to API
**Solution:**
1. Open browser console (F12)
2. Look for errors about API calls
3. Verify backend is responding: `curl http://localhost:5000/api/health`
4. Check that base URL in dashboard is correct

### Issue: Port already in use
**Solution:**
```bash
# Check what's using the port
lsof -i :5000  # for backend
lsof -i :8000  # for frontend

# Kill process if needed
kill -9 <PID>

# Or use different ports
python -m http.server 8001  # for frontend on different port
```

---

## 📊 4 Available Simulations

1. **Infinite Square Well** 🔲
   - Particle in a 1D box
   - Shows discrete energy levels

2. **Finite Square Well** 📦
   - Shallow potential well
   - Shows bound and quasi-bound states

3. **Harmonic Oscillator** 〰️
   - Spring-like potential
   - Shows quantum spring behavior

4. **Quantum Tunneling** 🚪
   - Particle through barrier
   - Shows transmission probability

---

## 🎨 Features

✅ **Real-time Visualization**
- Energy level diagrams
- Probability density plots
- Live parameter updates

✅ **Interactive Controls**
- Adjust well width/depth
- Change barrier height
- Modify particle mass
- Set number of states

✅ **WebSocket Support**
- Bi-directional communication
- Real-time streaming
- Live wavefunction updates

✅ **Webhook Integration**
- Event notifications
- Simulation callbacks
- Custom event handlers

---

## 📚 Documentation

- **`QUICK_START.md`** - Quick start guide
- **`BACKEND_FRONTEND_FIXES.md`** - Technical details
- **`QUICK_FIX_REFERENCE.md`** - Common fixes
- **`FIX_STATUS.txt`** - Complete status report

---

## 🔐 Important Notes

### Why Port Forwarding?
In Codespaces, ports inside the container are not directly accessible from your local browser. **Port forwarding** creates a tunnel through GitHub's servers to make them accessible.

### Automatic Port Detection
When you access a port from inside VS Code, Codespace usually detects it and asks:
```
Your application running on port 5000 is available.
→ Make Public  Open in Browser  →
```

Click **"Open in Browser"** to auto-forward!

### Public vs Private Ports
- **Private** (default): Only you can access
- **Public**: Anyone with the link can access
  - Change in Ports panel → right-click port → "Port Visibility" → "Public"

---

## ✅ Next Steps

1. **Open Ports panel** (bottom of VS Code)
2. **Click globe icon** for port 8000 (frontend)
3. **See your dashboard**
4. **Run a simulation**
5. **Explore the UI!**

---

**Your quantum simulator is ready to go! 🎉**

Need help? Check the troubleshooting section or see the full documentation!
