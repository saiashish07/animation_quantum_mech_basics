# Quantum Mechanics Interactive Simulator

## 🚀 Features

### Interactive Simulations
- **Infinite Square Well (Particle in a Box)**: Explore quantized energy levels and wavefunctions
- **Finite Square Well**: Observe wavefunction penetration into classically forbidden regions
- **Quantum Tunneling**: Real-time animation of wave packet tunneling through barriers with transmission coefficients
- **Harmonic Oscillator**: Visualize quantum oscillations with analytical energy comparison

### Advanced Visualizations
- **Real-time WebGL Rendering** using Three.js for smooth, interactive 3D graphics
- **Multiple Visualization Modes**: 
  - Wavefunction (ψ)
  - Probability Density (|ψ|²)
  - Combined View
- **Energy Level Diagrams**: Visual representation of energy eigenstates
- **Potential Profiles**: Clear visualization of potential energy landscapes

### Interactive Controls
- **Parameter Adjustment**: Real-time sliders for well width, height, barrier properties, etc.
- **State Selection**: Choose which eigenstate to visualize
- **Animation Controls**: Play/pause quantum tunneling animations
- **Display Options**: Toggle potential, energy levels, and visualization modes

### Physical Insights
- **Transmission Coefficients**: Calculate quantum tunneling probabilities using WKB approximation
- **Statistical Calculations**: ⟨x⟩, ⟨p⟩, Δx, Δp
- **Analytical Comparison**: Verify numerical solutions against exact solutions
- **Bound State Analysis**: Determine number of bound states in finite wells

## 🛠️ Technology Stack

### Frontend
- **WebGL/Three.js**: 3D visualization and rendering
- **Vanilla JavaScript**: No frameworks for maximum compatibility
- **Responsive CSS**: Works on desktop, tablet, and mobile

### Backend
- **Flask**: Python web framework for API
- **NumPy/SciPy**: Scientific computing and numerical methods
- **Sparse Matrices**: Efficient eigenvalue problem solving

### Performance
- **C++/WebAssembly**: Optional WASM modules for critical calculations
- **Caching**: API response caching for repeated queries
- **Vectorization**: NumPy vectorized operations throughout

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
cd animation_quantum_mech_basics
```

### 2. Run Quick Start Script
```bash
chmod +x quickstart.sh
./quickstart.sh
```

### 3. Start the Services

**Terminal 1 - Backend API:**
```bash
cd api
source venv/bin/activate
python quantum_api.py
```

**Terminal 2 - Frontend Server:**
```bash
cd web/public
python -m http.server 8080
```

### 4. Open in Browser
Navigate to: **http://localhost:8080/index.html**

## 🐳 Docker Quick Start

```bash
# Build and run with Docker Compose
docker-compose up --build

# Then open http://localhost:8080
```

## 📚 API Documentation

### Base URL
`http://localhost:5000/api`

### Endpoints

#### Health Check
```bash
curl http://localhost:5000/api/health
```

#### Solve Infinite Well
```bash
curl -X POST http://localhost:5000/api/infinite-well \
  -H "Content-Type: application/json" \
  -d '{"width": 5.0, "num_states": 5}'
```

#### Solve Finite Well
```bash
curl -X POST http://localhost:5000/api/finite-well \
  -H "Content-Type: application/json" \
  -d '{"width": 5.0, "height": 50.0, "num_states": 5}'
```

#### Simulate Tunneling
```bash
curl -X POST http://localhost:5000/api/tunneling \
  -H "Content-Type: application/json" \
  -d '{"barrier_height": 30, "barrier_width": 2, "particle_energy": 20, "packet_sigma": 0.5}'
```

#### Solve Harmonic Oscillator
```bash
curl -X POST http://localhost:5000/api/harmonic-oscillator \
  -H "Content-Type: application/json" \
  -d '{"mass": 1.0, "omega": 1.0, "num_states": 5}'
```

## 📖 Usage Guide

### Infinite Square Well
1. Select "Infinite Square Well" from the sidebar
2. Adjust the well width using the slider
3. Change the number of states to compute
4. Select different quantum states (n = 1, 2, 3, ...)
5. Observe how energy increases with n: E_n = (n²π²ℏ²)/(2mL²)

### Finite Square Well
1. Adjust well width and depth (V₀)
2. Notice the bound state count decreases as depth decreases
3. Observe wavefunction penetration into classically forbidden regions
4. Compare bound state energies with the well depth

### Quantum Tunneling
1. Set barrier height (V) and particle energy (E)
2. Adjust barrier width
3. Click "Start Animation" to see wave packet propagation
4. Watch the transmission and reflection coefficients update
5. Lower E relative to V shows lower transmission (exponential tunneling)

### Harmonic Oscillator
1. Adjust mass (m) and angular frequency (ω)
2. Notice energy levels: E_n = (n + ½)ℏω
3. Compare numerical vs analytical energies
4. Observe that uncertainty product Δx·Δp ≈ ℏ/2

## 🔬 Physical Theory

### Schrödinger Equation
The time-independent Schrödinger equation:
```
-ℏ²/(2m) d²ψ/dx² + V(x)ψ = Eψ
```

### Numerical Solution
- **Finite Difference Method**: Discretize spatial derivatives
- **Eigenvalue Problem**: Solve Hψ = Eψ using sparse matrix algorithms
- **Crank-Nicolson Scheme**: Time evolution for tunneling simulations

### WKB Approximation for Tunneling
Transmission coefficient:
```
T ≈ exp(-2κ)
κ = (1/ℏ) ∫ √[2m(V(x) - E)] dx
```

## 🎨 Customization

### Adding New Potentials
1. Create a new potential class in `src/quantum_playground/potentials.py`
2. Add Flask endpoint in `api/quantum_api.py`
3. Create visualizer in `web/src/visualizations/`
4. Add UI controls to `web/public/index.html`

### Changing Visual Style
Edit `web/src/style.css` to customize:
- Color scheme
- Layout and spacing
- Typography
- Dark/light mode

### Adjusting Grid Resolution
In `api/quantum_api.py`:
```python
GRID_POINTS = 1000  # Increase for finer resolution
```

## 🚀 Deployment

### Heroku
```bash
git push heroku main
```

### AWS/DigitalOcean
```bash
docker build -t quantum-simulator .
docker push your-registry/quantum-simulator
```

### GitHub Pages (frontend only)
Copy `web/public` to `gh-pages` branch

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Performance Tips

- Increase grid points for accuracy (slower computation)
- Use fewer states for faster calculations
- Enable WebAssembly compilation for critical paths
- Browser hardware acceleration improves rendering

## 🐛 Troubleshooting

### API not responding
- Check backend is running: `http://localhost:5000/api/health`
- Verify ports aren't in use: `lsof -i :5000`
- Check CORS settings in `quantum_api.py`

### Visualization not showing
- Open browser console (F12) for JavaScript errors
- Check Three.js is loaded: `typeof THREE`
- Verify WebGL support: `WebGL` tab in DevTools

### Slow performance
- Reduce grid points in API
- Disable advanced rendering in browser
- Use production build with minified code

## 📝 References

- Griffiths - Introduction to Quantum Mechanics
- Press et al. - Numerical Recipes in C
- Three.js Documentation: https://threejs.org/
- Emscripten Guide: https://emscripten.org/

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional simulation types
- Improved visualization modes
- Performance optimizations
- Mobile app adaptation

## 📄 License

Educational use - See LICENSE file for details

## 🎓 Educational Use

This simulator is designed for:
- Undergraduate quantum mechanics courses
- Physics visualization and exploration
- Interactive learning of quantum phenomena
- Research visualization of quantum systems

Perfect for students and educators who want to explore quantum mechanics interactively!

---

**Questions?** Check the [API Documentation](DEPLOYMENT.md) or open an issue.
