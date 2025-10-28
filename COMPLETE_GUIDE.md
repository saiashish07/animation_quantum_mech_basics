# 🔬 Quantum Mechanics Interactive Simulator - Complete Documentation

## Project Overview

A **full-stack web application** for interactive visualization and exploration of quantum mechanical phenomena using:

- **WebGL/Three.js** for 3D real-time visualizations
- **Flask API** for scientific computations
- **NumPy/SciPy** for quantum solvers
- **C++/WebAssembly** for performance optimization
- **Responsive UI** for intuitive parameter control

### Supported Simulations

| Simulation | Description | Key Features |
|-----------|-------------|--------------|
| **Infinite Square Well** | Particle in a box | Quantized energy levels, orthogonal wavefunctions |
| **Finite Square Well** | Box with finite walls | Bound state analysis, wavefunction penetration |
| **Quantum Tunneling** | Wave packet through barrier | Real-time animation, T & R coefficients |
| **Harmonic Oscillator** | Spring-like potential | Comparison with analytical solutions |

## 🚀 Quick Start

### Fastest Way (Docker)
```bash
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
cd animation_quantum_mech_basics
docker-compose up --build
# Open http://localhost:8080
```

### Standard Way (Manual)
```bash
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
cd animation_quantum_mech_basics
./quickstart.sh
# Follow instructions
```

### Full Documentation
- **Setup**: See [SETUP.md](SETUP.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Web App Guide**: See [README_WEB.md](README_WEB.md)

## 📁 Project Structure

```
animation_quantum_mech_basics/
│
├── 🌐 WEB FRONTEND
│   └── web/
│       ├── public/
│       │   └── index.html                 # Main web app
│       └── src/
│           ├── style.css                  # Responsive styling
│           ├── app.js                     # Main controller (500 lines)
│           ├── api-client.js              # API communication
│           ├── ui-controls.js             # Event handling
│           └── visualizations/
│               ├── core.js                # WebGL/Three.js engine
│               ├── infinite-well.js       # ISW visualizer
│               ├── finite-well.js         # FSW visualizer
│               ├── tunneling.js           # Tunneling visualizer
│               └── harmonic-oscillator.js # HO visualizer
│
├── 🔌 BACKEND API
│   ├── quantum_api.py                     # Flask REST API (400 lines)
│   ├── websocket_support.py               # Real-time streaming
│   └── requirements.txt
│
├── 🧪 QUANTUM PHYSICS CORE
│   └── src/quantum_playground/
│       ├── solvers.py                     # Schrödinger solvers
│       ├── potentials.py                  # Potential definitions
│       └── animations/                    # Animation modules
│
├── ⚡ PERFORMANCE (C++/WASM)
│   └── cpp/
│       └── quantum_wasm.cpp               # High-speed calculations
│
├── 🐳 DEPLOYMENT
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .github/workflows/deploy.yml
│
├── 📚 DOCUMENTATION
│   ├── README_WEB.md                      # Web app guide
│   ├── SETUP.md                           # Setup instructions
│   ├── DEPLOYMENT.md                      # Deployment guide
│   ├── .env.example                       # Configuration template
│   └── COMPLETE_GUIDE.md                  # This file
│
└── 🔧 CONFIGURATION
    ├── package.json
    ├── quickstart.sh
    └── .github/
```

## 🛠️ Technologies & Libraries

### Frontend
| Technology | Purpose | Why Used |
|-----------|---------|----------|
| **Vanilla JS** | Core logic | No build step, maximum compatibility |
| **Three.js** | 3D rendering | Best WebGL library, extensive docs |
| **CSS3** | Styling | Modern responsive design |
| **HTML5** | Markup | Semantic structure |

### Backend
| Technology | Purpose | Why Used |
|-----------|---------|----------|
| **Flask** | Web framework | Lightweight, Pythonic |
| **NumPy** | Arrays & math | Fast numerical computing |
| **SciPy** | Sparse matrices | Efficient eigenvalue solving |
| **Gunicorn** | WSGI server | Production-grade deployment |

### Quantum Physics
| Library | Functionality |
|---------|--------------|
| **NumPy** | Matrix operations |
| **SciPy Sparse** | Efficient Hamiltonian matrices |
| **SciPy ARPACK** | Eigenvalue problem solving |

## 📊 API Reference

### Endpoints

#### 1. **GET `/api/health`**
Health check
```bash
curl http://localhost:5000/api/health
# Response: {"status": "ok", "message": "..."}
```

#### 2. **POST `/api/infinite-well`**
Solve infinite square well
```bash
curl -X POST http://localhost:5000/api/infinite-well \
  -H "Content-Type: application/json" \
  -d '{"width": 5.0, "num_states": 5}'
```

Response includes:
- `x`: spatial grid points
- `potential`: potential array
- `energies`: eigenvalue energies
- `wavefunctions`: eigenvector functions
- `probability_densities`: |ψ|² for each state

#### 3. **POST `/api/finite-well`**
Solve finite square well
```bash
curl -X POST http://localhost:5000/api/finite-well \
  -H "Content-Type: application/json" \
  -d '{"width": 5.0, "height": 50.0, "num_states": 5}'
```

Response: Same as infinite well + bound state count

#### 4. **POST `/api/tunneling`**
Simulate quantum tunneling
```bash
curl -X POST http://localhost:5000/api/tunneling \
  -H "Content-Type: application/json" \
  -d '{
    "barrier_height": 30.0,
    "barrier_width": 2.0,
    "particle_energy": 20.0,
    "packet_sigma": 0.5,
    "duration": 1000
  }'
```

Response includes:
- `transmission_coefficient`: Tunneling probability
- `reflection_coefficient`: 1 - T
- Wavefunction trajectory over time

#### 5. **POST `/api/harmonic-oscillator`**
Solve quantum harmonic oscillator
```bash
curl -X POST http://localhost:5000/api/harmonic-oscillator \
  -H "Content-Type: application/json" \
  -d '{"mass": 1.0, "omega": 1.0, "num_states": 5}'
```

Response: Includes analytical energy comparison

## 🎓 Physical Theory

### Schrödinger Equation
Time-independent form:
```
Ĥψ = Eψ
-ℏ²/(2m) d²ψ/dx² + V(x)ψ = Eψ
```

### Numerical Solution Method
1. **Discretization**: Finite differences on spatial grid
2. **Matrix Formation**: Hamiltonian matrix in position basis
3. **Eigenvalue Problem**: ARPACK algorithm for sparse eigenvalues
4. **Normalization**: ∫|ψ|² dx = 1

### WKB Approximation (Tunneling)
```
T ≈ exp(-2κ)
κ = (1/ℏ) ∫ √[2m(V(x) - E)] dx
```

## 🎨 User Interface Guide

### Main Components

```
┌─────────────────────────────────────────────┐
│  HEADER (Quantum Mechanics Interactive)     │
├──────────┬───────────────────┬──────────────┤
│ SIDEBAR  │  WEBGL CANVAS     │  CONTROL     │
│          │  (3D Render)      │  PANEL       │
│ • Inf    │                   │  - Sliders   │
│ • Fin    │                   │  - Checkboxes│
│ • Tun    │                   │  - Buttons   │
│ • Harm   │                   │              │
├──────────┴───────────────────┴──────────────┤
│ STATISTICS PANEL (Energy, ⟨x⟩, ⟨p⟩, etc)   │
├───────────────────────────────────────────────┤
│ FOOTER                                       │
└───────────────────────────────────────────────┘
```

### Interactive Controls

1. **Simulation Selection**: Click sidebar buttons
2. **Parameter Adjustment**: Drag sliders (real-time updates)
3. **State Selection**: Choose quantum number
4. **Visualization Mode**: Wavefunction, Probability, or Both
5. **Display Options**: Show/hide potential and energy levels
6. **Animation**: Play/pause tunneling simulation

## 🚀 Deployment Strategies

### 1. Local Development
```bash
cd api && python quantum_api.py
cd web/public && python -m http.server 8080
```

### 2. Docker (Recommended)
```bash
docker-compose up --build
```

### 3. Heroku
```bash
git push heroku main
```
(Requires setup of Heroku credentials)

### 4. AWS EC2
```bash
# SSH into instance
git clone <repo>
./quickstart.sh
# Run services in tmux/screen
```

### 5. GitHub Pages (Frontend Only)
```bash
# Push to gh-pages branch
cp -r web/public/* docs/
```

## 🔧 Configuration

### Environment Variables

Create `.env` in `api/`:
```env
FLASK_ENV=production
FLASK_DEBUG=False
GRID_POINTS=2000
CORS_ORIGINS=https://yourdomain.com
```

### API Configuration

In `api/quantum_api.py`:
```python
GRID_POINTS = 1000      # Spatial resolution
X_MIN = -15             # Left boundary
X_MAX = 15              # Right boundary
```

## 📈 Performance Optimization

### Backend
- **Sparse matrices**: O(n) instead of O(n²) memory
- **ARPACK**: Fast eigenvalue algorithm
- **NumPy vectorization**: SIMD operations

### Frontend
- **WebGL**: Hardware-accelerated rendering
- **Three.js**: Optimized geometry/materials
- **Caching**: API response memoization
- **Debouncing**: Rate-limited parameter changes

### WebAssembly
- **C++ compilation**: 10-100x speedup
- **Critical paths**: Derivatives, normalization
- **Memory management**: Direct WASM buffer access

## 🧪 Testing

### Backend Tests
```bash
cd api
python -m pytest tests/ -v
```

### Frontend Testing
Open browser console (F12):
```javascript
// Test API client
await api.solveInfiniteWell(5, 3)

// Test UI
ui.getParameter('well-width')
ui.setParameter('well-width', 7)

// Test visualizer
app.loadSimulation('infinite-well')
```

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Find PID
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Issue: "CORS errors"
Verify `api/quantum_api.py`:
```python
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:8080"]}
})
```

### Issue: "WebGL not working"
- Update GPU drivers
- Try different browser
- Check DevTools → Rendering

### Issue: "Slow computation"
- Reduce GRID_POINTS
- Lower num_states
- Enable WebAssembly compilation

## 📖 References & Resources

### Textbooks
- **Griffiths** - Introduction to Quantum Mechanics
- **Shankar** - Principles of Quantum Mechanics
- **Press et al.** - Numerical Recipes

### Documentation
- [Three.js Docs](https://threejs.org/docs/)
- [Flask Guide](https://flask.palletsprojects.com/)
- [NumPy Reference](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/)
- [Emscripten Guide](https://emscripten.org/docs/)

### Tutorials
- [WebGL Basics](https://learningwebgl.com/)
- [Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Quantum Mechanics](https://www.youtube.com/watch?v=pBSX0Ey1Sk0)

## 🤝 Contributing

Areas for contribution:
1. Additional potential types
2. Improved visualizations
3. Performance optimizations
4. Mobile app wrapper
5. Documentation improvements

## 📄 License & Attribution

Educational project for quantum mechanics visualization.

## 🎉 Getting Started

### 3 Steps to Run:

1. **Clone**
   ```bash
   git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
   ```

2. **Setup**
   ```bash
   cd animation_quantum_mech_basics
   docker-compose up --build
   ```

3. **Open**
   ```
   Browser → http://localhost:8080
   ```

## 📞 Support

- 📖 Read [SETUP.md](SETUP.md) for installation
- 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
- 🌐 Read [README_WEB.md](README_WEB.md) for usage
- 🔍 Check browser console for errors
- 🤝 Open GitHub issues for problems

---

**Happy quantum exploring!** 🔬✨

For detailed information, refer to the specific documentation files.
