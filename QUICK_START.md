# 🚀 Quick Start Guide - Quantum Simulator

## ✅ Status: READY TO RUN!

All Python imports are fixed and all dependencies are installed.

---

## 🏃 Running the Application (30 seconds)

### Terminal 1: Start Backend Server
```bash
source /workspaces/animation_quantum_mech_basics/.venv/bin/activate
cd /workspaces/animation_quantum_mech_basics/app/backend
python app/api/enhanced_api.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server...
```

### Terminal 2: Start Frontend Server
```bash
cd /workspaces/animation_quantum_mech_basics/app/frontend/public
python -m http.server 8000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000
```

### Terminal 3 (or Browser): Open Dashboard
```
http://localhost:8000/dashboard.html
```

---

## ✨ What You'll See

1. **Dashboard UI** loads with:
   - Simulation type selector (4 options)
   - Parameter sliders
   - "Run Simulation" button

2. **Run a simulation:**
   - Select a simulation type
   - Click "Run Simulation"
   - Watch energy levels and probability plots update!

---

## 🧪 Quick Test

Verify backend is running:
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{
  "status": "ok",
  "timestamp": "...",
  "connected_clients": 0,
  "webhooks_registered": 0
}
```

---

## 📚 Simulations Available

1. **Infinite Square Well** - Particle in a box
2. **Finite Square Well** - Shallow potential well
3. **Harmonic Oscillator** - Spring-like potential
4. **Quantum Tunneling** - Barrier penetration

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" on :5000 | Make sure backend is running (Terminal 1) |
| "Connection refused" on :8000 | Make sure frontend is running (Terminal 2) |
| Dashboard not connecting to API | Check browser console (F12) for errors |
| Module import errors | Run: `source .venv/bin/activate` first |

---

## 📖 Complete Documentation

- **BACKEND_FRONTEND_FIXES.md** - Technical details of all fixes
- **QUICK_FIX_REFERENCE.md** - Quick reference for common issues
- **FIX_STATUS.txt** - Comprehensive status report
- **setup_guide.py** - Run with `python setup_guide.py`

---

## ✅ All Issues Resolved

✅ Python import modules - FIXED (all 9 packages installed)
✅ Backend API base URL - FIXED (changed to http://localhost:5000)
✅ Frontend API initialization - FIXED (correct base URL in dashboard.js)
✅ CSS compatibility - FIXED (added standard appearance property)
✅ Project structure - CLEAN (removed old/duplicate code)
✅ Disk space - OPTIMIZED (97% reduction)

---

**Ready to explore quantum mechanics! 🎓**
