# Quantum Mechanics Interactive Simulator - Deployment Guide

## Overview

This is a full-stack web application for interactive quantum mechanics simulations featuring:

- **WebGL Visualizations** (Three.js) - Real-time 3D rendering of wavefunctions
- **Flask Backend API** - Scientific computations using NumPy/SciPy
- **C++ Acceleration** - WebAssembly modules for performance-critical calculations
- **Interactive Controls** - Real-time parameter adjustment
- **Multiple Scenarios**:
  - Infinite Square Well (Particle in a Box)
  - Finite Square Well
  - Quantum Tunneling
  - Harmonic Oscillator

## Project Structure

```
.
├── web/                          # Frontend Web Application
│   ├── public/
│   │   └── index.html           # Main HTML file
│   └── src/
│       ├── style.css            # Global styling
│       ├── api-client.js        # API communication
│       ├── app.js               # Main application controller
│       ├── ui-controls.js       # UI event handling
│       └── visualizations/
│           ├── core.js          # WebGL/Three.js core
│           ├── infinite-well.js # Infinite well visualizer
│           ├── finite-well.js   # Finite well visualizer
│           ├── tunneling.js     # Tunneling visualizer
│           └── harmonic-oscillator.js  # Harmonic oscillator
│
├── api/                          # Backend Flask API
│   ├── quantum_api.py           # Main API server
│   └── requirements.txt          # Python dependencies
│
├── cpp/                          # C++ WebAssembly Modules
│   └── quantum_wasm.cpp         # Performance-critical calculations
│
└── src/                          # Quantum Physics Core (existing)
    └── quantum_playground/      # Quantum solver implementations
        ├── solvers.py           # Schrödinger equation solvers
        ├── potentials.py        # Potential definitions
        └── animations/          # Animation modules
```

## Installation

### 1. Backend Setup

```bash
# Navigate to API directory
cd api/

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
# The frontend is pure HTML/JavaScript - no build step required!
# Just ensure you have a web server running.

# Option A: Use Python's built-in server
cd web/public/
python -m http.server 8080

# Option B: Use Node.js http-server
npx http-server web/public -p 8080

# Option C: Use any other web server (Apache, Nginx, etc.)
```

### 3. C++ WebAssembly Build (Optional - for performance)

```bash
# Install Emscripten SDK (one-time setup)
# Follow: https://emscripten.org/docs/getting_started/downloads.html

cd cpp/

# Compile to WebAssembly
emcripten++ quantum_wasm.cpp -o quantum.js -s WASM=1 \
    -s ALLOW_MEMORY_GROWTH=1 \
    -s EXPORTED_FUNCTIONS='["_create_gaussian_packet","_compute_probability_density",...]'

# Output files: quantum.js and quantum.wasm
```

## Running the Application

### Development Mode

**Terminal 1 - Start Backend API:**
```bash
cd api/
source venv/bin/activate
python quantum_api.py
```

The API will be available at `http://localhost:5000`

**Terminal 2 - Start Frontend Web Server:**
```bash
cd web/public/
python -m http.server 8080
```

The frontend will be available at `http://localhost:8080`

Then open your browser to: **http://localhost:8080/index.html**

### Production Deployment

#### Option 1: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy backend
COPY api/ /app/api/
COPY src/ /app/src/

# Install Python dependencies
RUN pip install -r /app/api/requirements.txt

# Copy frontend
COPY web/public/ /app/web/

# Expose ports
EXPOSE 5000 8080

# Run both services
CMD ["sh", "-c", "cd /app/api && python quantum_api.py & cd /app/web && python -m http.server 8080"]
```

Build and run:
```bash
docker build -t quantum-simulator .
docker run -p 5000:5000 -p 8080:8080 quantum-simulator
```

#### Option 2: GitHub Pages Deployment

The frontend can be deployed to GitHub Pages:

```bash
# Copy web/public contents to docs/ or gh-pages branch
# Update API_URL in api-client.js to point to your backend

# For static hosting with CORS-enabled backend at a different domain
# Ensure your backend API has CORS enabled (already configured in quantum_api.py)
```

#### Option 3: Heroku Deployment

`Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT api.quantum_api:app
```

Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

Update frontend `api-client.js`:
```javascript
const api = new QuantumSimulationAPI('https://your-app-name.herokuapp.com/api');
```

#### Option 4: AWS/DigitalOcean/Render Deployment

Deploy the backend as a containerized service and the frontend as static files.

### Environment Configuration

Create `.env` file in `api/` directory:
```
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=http://localhost:8080,https://yourdomain.com
API_PORT=5000
```

Update `quantum_api.py` to use environment variables:
```python
from dotenv import load_dotenv
import os

load_dotenv()

CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True', port=port)
```

## API Endpoints

All endpoints return JSON and accept POST requests with JSON bodies.

### 1. Health Check
```
GET /api/health
Response: {"status": "ok", "message": "..."}
```

### 2. Infinite Square Well
```
POST /api/infinite-well
Body: {"width": 5.0, "num_states": 5}
Response: {
    "x": [...],
    "potential": [...],
    "energies": [...],
    "wavefunctions": [...],
    "probability_densities": [...]
}
```

### 3. Finite Square Well
```
POST /api/finite-well
Body: {"width": 5.0, "height": 50.0, "num_states": 5}
Response: {...same as infinite well + "bound_states": 3}
```

### 4. Quantum Tunneling
```
POST /api/tunneling
Body: {
    "barrier_height": 30.0,
    "barrier_width": 2.0,
    "particle_energy": 20.0,
    "packet_sigma": 0.5,
    "duration": 1000
}
Response: {
    "x": [...],
    "potential": [...],
    "initial_wavefunction": [...],
    "final_wavefunction": [...],
    "transmission_coefficient": 0.15,
    "reflection_coefficient": 0.85
}
```

### 5. Harmonic Oscillator
```
POST /api/harmonic-oscillator
Body: {"mass": 1.0, "omega": 1.0, "num_states": 5}
Response: {
    ...same as other simulations...
    "analytical_energies": [0.5, 1.5, 2.5, ...]
}
```

### 6. Transmission Coefficient
```
POST /api/transmission-coefficient
Body: {
    "barrier_height": 30.0,
    "barrier_width": 2.0,
    "particle_energy": 20.0
}
Response: {
    "transmission": 0.15,
    "reflection": 0.85
}
```

## Webhook Integration

For automated deployments, set up webhooks:

### GitHub Webhook to Heroku
1. Go to your GitHub repo → Settings → Webhooks
2. Add webhook pointing to Heroku deployment URL
3. On push to `main` branch, Heroku automatically redeploys

### Continuous Integration Setup (GitHub Actions)

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.13
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```

## Performance Optimization

### Backend Optimization
- Results are cached by the Flask API client
- Sparse matrix operations for large systems
- NumPy vectorization throughout

### Frontend Optimization
- WebGL rendering for smooth visualization
- Request debouncing for rapid parameter changes
- Browser caching for static assets

### C++ WebAssembly
- Compile critical functions to WebAssembly for 10-100x speedup
- Use for real-time calculations and derivatives

```javascript
// Example: Using WebAssembly in frontend
const wasmModule = await WebAssembly.instantiateStreaming(
    fetch('quantum.wasm')
);
const { compute_probability_density } = wasmModule.instance.exports;
```

## Troubleshooting

### API Connection Issues
- Ensure backend is running on port 5000
- Check CORS settings in `quantum_api.py`
- Verify API_URL in `web/src/api-client.js`

### Performance Issues
- Use WebAssembly compilation for C++
- Reduce number of grid points if needed
- Enable browser hardware acceleration (DevTools → Rendering)

### WebGL Not Working
- Update graphics drivers
- Check browser console for errors
- Fallback to 2D Canvas rendering if needed

## Development Notes

### Adding New Simulations
1. Create potential class in `src/quantum_playground/potentials.py`
2. Create Flask endpoint in `api/quantum_api.py`
3. Create visualizer in `web/src/visualizations/`
4. Add UI controls in `web/public/index.html`

### Extending the API
```python
@app.route('/api/new-simulation', methods=['POST'])
def new_simulation():
    data = request.get_json()
    # ... computation logic ...
    return jsonify(response)
```

### Custom Visualizations
```javascript
class CustomVisualizer {
    constructor(core) {
        this.core = core;
        this.data = null;
    }
    
    async load(params) {
        this.data = await api.customEndpoint(params);
    }
    
    visualize(index) {
        // Use this.core.plotWavefunction() or create custom Three.js objects
    }
}
```

## References

- **Quantum Mechanics**: Griffiths - Introduction to Quantum Mechanics
- **Numerical Methods**: Press et al. - Numerical Recipes
- **Three.js**: https://threejs.org/docs/
- **Flask**: https://flask.palletsprojects.com/
- **WebAssembly**: https://emscripten.org/

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, refer to:
- Browser console (F12) for JavaScript errors
- Flask logs for backend errors
- Check `requirements.txt` for dependency issues
