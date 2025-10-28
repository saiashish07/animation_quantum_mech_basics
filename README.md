# Quantum Mechanics Simulator

Interactive quantum mechanics simulator with 4 core simulations and real-time WebSocket visualizations.

> 🚀 **Running in GitHub Codespace?** [See the Codespace Setup Guide](CODESPACE_SETUP.md) with port forwarding instructions!

## 🚀 Quick Start

### On GitHub Codespace (Recommended)
1. Open **Ports** panel in VS Code (bottom)
2. Click globe 🌐 next to **Port 8000**
3. See your quantum simulator!
4. [Full Codespace guide](CODESPACE_SETUP.md)

### On Local Machine
```bash
# 1. Setup (first time only)
cd app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run the API
python app/api/enhanced_api.py

# 3. Open frontend (in new terminal)
cd app/frontend/public
python -m http.server 8000

# 4. Visit: http://localhost:8000/dashboard.html
```

## 📊 Simulations

1. **Infinite Potential Well** - Particle in a box
2. **Finite Potential Well** - Bound states with tunneling
3. **Harmonic Oscillator** - Spring-like quantum system
4. **Quantum Tunneling** - Wavefunction penetration

## 🎮 Features

- **Real-time API**: RESTful endpoints for all 4 simulations
- **WebSocket Streaming**: Live wavefunction updates
- **Interactive Controls**: Adjust energy, width, potential parameters
- **Visualizations**: Energy levels, probability density, wavefunction plots
- **Webhooks**: Event-driven integration support

## 📁 Project Structure

```
app/
├── backend/              # Flask API
│   └── app/api/
│       ├── enhanced_api.py       # 6 REST endpoints
│       ├── websocket_service.py  # Real-time streaming
│       └── webhooks/             # Event system
├── frontend/             # Interactive dashboard
│   ├── public/
│   │   ├── dashboard.html        # Main UI
│   │   ├── dashboard.js          # Controls & updates
│   │   └── style.css             # Styling
│   └── src/
│       ├── services/             # API, WebSocket, State
│       └── visualizations/       # Energy & probability plots

src/
├── quantum_playground/   # Physics core
│   ├── solvers.py       # Schrödinger solver
│   ├── potentials.py    # Potential functions
│   └── animations/      # 4 simulations
└── ffmpeg_pipeline.py   # Video generation

tests/
└── test_core.py         # Unit tests
```

## 🔌 API Endpoints

### GET /simulate
Get wavefunction for a simulation type
```bash
curl "http://localhost:5000/simulate?type=infinite_well&width=2&points=100"
```

### GET /energy-levels
Get quantized energy levels
```bash
curl "http://localhost:5000/energy-levels?type=harmonic&n_levels=5"
```

### GET /probability-density
Get probability density function
```bash
curl "http://localhost:5000/probability-density?type=infinite_well&width=2"
```

### POST /webhook
Register webhook for simulation events
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/hook","events":["simulation_complete"]}'
```

### WebSocket: /socket.io
Real-time streaming:
```javascript
const socket = io('http://localhost:5000');
socket.emit('subscribe', {type: 'infinite_well', width: 2});
socket.on('update', (data) => console.log(data.psi));
```

## 🧮 Physics

All simulations solve the Time-Independent Schrödinger Equation:
$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$$

**Implemented Potentials:**
- $V(x) = \infty$ outside well, $0$ inside (Infinite Well)
- Finite step potential with adjustable depth
- $V(x) = \frac{1}{2}m\omega^2 x^2$ (Harmonic Oscillator)
- Custom potential for tunneling barriers

**Methods:**
- Eigenvalue problems via SciPy (eigsh, sparse matrices)
- Finite difference discretization (O(h²) accuracy)
- Normalization to preserve probability

## 🌐 Deployment

### Local Development
```bash
cd app/backend
python app/api/enhanced_api.py
```

### Docker
```bash
docker-compose up
```

### Production
See `app/DEPLOYMENT.md` for cloud deployment options.

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/test_core.py -v

# Run quick demo
python app/quickstart.py
```

## 📚 Documentation

- **Setup**: See above
- **API Guide**: Check API endpoint details above
- **Deployment**: See `app/DEPLOYMENT.md`
- **Physics**: See docstrings in `src/quantum_playground/`

## ⚙️ System Requirements

- Python 3.9+
- NumPy, SciPy (numerical computing)
- Flask, Flask-SocketIO (web framework)
- Modern browser (Chrome, Firefox, Safari)

## 🔧 Troubleshooting

**API won't start?**
```bash
cd app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**WebSocket connection fails?**
- Check CORS settings in `enhanced_api.py`
- Ensure `python-socketio` is installed

**Dashboard doesn't load?**
- Make sure HTTP server is running on port 8000
- Check browser console for errors

## 📦 Dependencies

```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-SocketIO==5.3.4
NumPy==1.24.3
SciPy==1.11.2
python-socketio==5.9.0
Requests==2.31.0
```

## 📄 License

MIT License - See LICENSE file

## 👤 Author

Quantum Mechanics Simulator - Educational Project

---

**Key:** This is a fully functional quantum simulator. Start with **Quick Start** section above!
