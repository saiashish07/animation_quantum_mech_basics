# Quantum Mechanics Simulator - Enhanced Web Application

A professional full-stack quantum mechanics simulator with WebGL visualization, real-time WebSocket updates, and webhook integration.

## 📁 Directory Structure

```
app/
├── frontend/
│   ├── public/
│   │   ├── dashboard.html          # Main dashboard UI
│   │   ├── dashboard.js            # Dashboard controller
│   │   └── style.css               # UI styling
│   └── src/
│       ├── components/             # UI components (expandable)
│       ├── services/
│       │   ├── api-service.js      # REST API client with caching
│       │   ├── websocket-service.js # Real-time communication
│       │   └── state-manager.js    # Centralized state management
│       └── visualizations/
│           ├── energy-levels.js    # Energy level diagram
│           └── probability-density.js # Probability density heatmap
│
└── backend/
    └── app/
        ├── api/
        │   ├── enhanced_api.py     # Flask API with full data endpoints
        │   └── websocket_service.py # WebSocket event handlers
        ├── solvers/                # Quantum solver modules (symlink to src/)
        └── webhooks/
            └── webhook_manager.py  # Webhook registration & dispatch
```

## 🚀 Quick Start

### Backend Setup

```bash
cd app/backend

# Install dependencies
pip install flask flask-cors flask-socketio python-socketio numpy scipy

# Run API server
python app/api/enhanced_api.py
```

Server will start at `http://localhost:5000`

### Frontend

Open `app/frontend/public/dashboard.html` in a modern browser, or serve with:

```bash
cd app/frontend/public
python -m http.server 8000
```

Then navigate to `http://localhost:8000/dashboard.html`

## 📊 API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and connected clients.

### Full Simulation
```
POST /api/full-simulation
Content-Type: application/json

{
  "type": "infinite-well|finite-well|tunneling|harmonic",
  "parameters": {
    "width": 5.0,
    "num_states": 5,
    ...
  }
}
```

Returns complete visualization data:
- Grid coordinates (x)
- Potential function values
- Energy levels (numerical and analytical)
- Wavefunctions (real/imaginary parts)
- Probability densities
- Quantum statistics (⟨x⟩, Δx, etc.)
- Analytical comparison with errors

### Webhook Registration
```
POST /api/webhooks/register
{
  "event_type": "simulation.complete|energy.calculated|tunneling.started|error.occurred",
  "webhook_url": "https://your-server.com/webhook"
}
```

### Webhook List
```
GET /api/webhooks/list
```

## 🔌 WebSocket Events

### Client → Server
- `subscribe` - Subscribe to simulation room
- `unsubscribe` - Leave room
- `request_live_update` - Request real-time streaming

### Server → Client
- `energy_update` - Energy levels changed
- `probability_update` - Probability density updated
- `wavefunction_update` - Wavefunction changed
- `statistics_update` - Statistics calculated
- `simulation_complete` - Simulation finished

## 🎨 Frontend Features

### Services

#### API Service (`api-service.js`)
```javascript
const api = new QuantumAPIService('http://localhost:5000/api');

// Run simulation
const result = await api.infiniteWell(width, numStates);
const result = await api.finiteWell(width, height, numStates);
const result = await api.tunneling(bHeight, bWidth, pEnergy);
const result = await api.harmonicOscillator(mass, omega, numStates);

// Webhooks
await api.registerWebhook('simulation.complete', 'https://...');
await api.listWebhooks();
```

#### WebSocket Service (`websocket-service.js`)
```javascript
const ws = new QuantumWebSocketService('http://localhost:5000');

// Events
ws.on('connect', handler);
ws.on('energy_update', handler);
ws.on('simulation_complete', handler);

// Subscribe/Unsubscribe
ws.subscribe('infinite-well');
ws.requestLiveUpdate('finite-well', parameters);
```

#### State Manager (`state-manager.js`)
```javascript
const state = new QuantumStateManager();

// Parameters
state.updateSimulationParameters('infinite-well', { width: 5.0 });
state.setSimulationData('infinite-well', apiResponse);

// Simulation control
state.setCurrentSimulation('finite-well');
state.setSelectedStates([0, 1, 2]);

// Observers
state.subscribe((action, data, fullState) => {
  console.log(`State changed: ${action}`, data);
});
```

### Visualizations

#### Energy Levels Visualizer
```javascript
const viz = new EnergyLevelsVisualizer(canvas);
viz.setEnergyData(energies, {
  analytical: analyticalEnergies,
  labels: ['E_0', 'E_1', ...],
  errors: errorPercents,
  selectedStates: [0]
});
viz.render();
```

Features:
- Horizontal energy level lines
- Numerical vs analytical comparison
- Error percentage display
- Color highlighting for selected states
- Statistics (ground state, spacing, etc.)

#### Probability Density Visualizer
```javascript
const viz = new ProbabilityDensityVisualizer(canvas);
viz.setProbabilityData(x, densities, {
  labels: ['State 0', 'State 1', ...]
});
viz.render(); // 2D heatmap

// Or single state line plot
viz.renderSingleState(0);
```

Features:
- 2D heatmap of probability density across all states
- Multiple color schemes (hot, cool, viridis)
- Colorbar with scale
- Single-state line plot with area fill
- Position and state axes

## 📈 Supported Simulations

### 1. Infinite Square Well
- Particle in a 1D box
- Analytical solution: E_n = (n²π²ℏ²)/(2mL²)
- Exact comparison with numerical results

### 2. Finite Square Well
- Bounded potential with finite depth
- Bound and scattering states
- Wavefunction penetration into classically forbidden regions
- Bound state count calculation

### 3. Quantum Tunneling
- Rectangular barrier potential
- WKB transmission coefficient calculation
- Time evolution of wave packet
- Transmission/reflection probability

### 4. Harmonic Oscillator
- Quadratic potential
- Analytical eigenvalues: E_n = (n + 1/2)ℏω
- Comparison with numerical solver
- Gaussian wavefunctions

## 🔧 Configuration

### API Configuration (`enhanced_api.py`)
```python
GRID_POINTS = 1000      # Spatial resolution
X_MIN = -15             # Left boundary
X_MAX = 15              # Right boundary
```

### Webhook Configuration
Max retries: 3
Timeout: 5 seconds
Event queue: Asynchronous processing

### WebSocket Configuration
Auto-reconnect: Enabled
Max reconnect attempts: 5
Reconnect delay: 1000ms

## 📊 Data Flow

```
User Input (Controls)
    ↓
State Manager (Parameters Updated)
    ↓
API Service (REST POST)
    ↓
Backend Solver (SciPy)
    ↓
Full Response (All visualization data)
    ↓
State Manager (Data Stored)
    ↓
Visualizers (Energy, Probability, Wavefunction, Stats)
    ↓
Canvas Rendering (Canvas 2D + Three.js WebGL)

[WebSocket Events Stream in Real-time]
[Webhooks Notify External Services]
```

## 🎯 Interactive Controls

### Parameter Adjustment
- **Infinite Well Width**: 1-10 Å
- **Well Depth**: 10-200 meV (finite well)
- **Number of States**: 1-20
- **Barrier Height**: 10-100 meV (tunneling)
- **Particle Energy**: 5-80 meV (tunneling)
- **Frequency**: 0.5-3.0 ω (harmonic)

### Live Updates
- Enable/disable real-time WebSocket streaming
- Select individual states to display
- Toggle graph visibility
- Choose visualization types

### Export & Sharing
- Webhook integration for external processing
- All data available in REST API
- JSON serialization for storage

## 🐛 Troubleshooting

### Server Connection Failed
```
Error: Cannot connect to server
```
- Ensure backend server is running: `python enhanced_api.py`
- Check port 5000 is not blocked
- Verify CORS settings in Flask app

### WebSocket Connection Failed
```
[WebSocket] Socket.IO not loaded
```
- Add Socket.IO script: `<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>`
- Check browser console for errors

### Webhook Not Triggered
- Verify webhook URL is accessible
- Check webhook event type is correct
- Monitor webhook status: `GET /api/webhooks/list`
- Check server logs for delivery errors

## 🚀 Performance Optimization

### Frontend
- Canvas rendering: 60+ FPS
- Smooth animations with requestAnimationFrame
- Event debouncing on parameter sliders
- Lazy loading of visualizations

### Backend
- SciPy sparse eigenvalue solver (ARPACK)
- NumPy vectorized operations
- WebSocket async event processing
- Webhook delivery with thread pool

### Caching
- API response caching (5 minutes)
- State persistence
- WebSocket room-based subscription

## 📚 Technologies

**Frontend**
- Vanilla JavaScript ES6+
- Canvas 2D API
- Three.js WebGL
- Socket.IO client

**Backend**
- Python 3.9+
- Flask web framework
- NumPy/SciPy scientific computing
- Flask-SocketIO real-time

**Physics**
- Schrödinger equation solver
- Finite difference method
- Eigenvalue problems (ARPACK)
- WKB approximation

## 📝 License

Educational use. Based on quantum mechanics principles and computational physics methods.

## 🤝 Contributing

To extend the simulator:

1. **Add new potential**: Edit `src/quantum_playground/potentials.py`
2. **Create visualization**: Add to `app/frontend/src/visualizations/`
3. **New endpoint**: Add to `app/backend/app/api/enhanced_api.py`
4. **UI component**: Create in `app/frontend/src/components/`

## 📞 Support

For questions or issues:
1. Check the browser console for errors
2. Review server logs
3. Verify all dependencies are installed
4. Check API endpoints with curl/Postman
