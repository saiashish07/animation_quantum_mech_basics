# Complete Setup and Run Guide

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 14+** (optional, for npm tools)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **Git**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🔧 System Setup

### Linux/Mac

```bash
# Install Python and pip
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Install Node.js (optional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Windows

Download and install:
1. Python: https://www.python.org/downloads/
2. Node.js: https://nodejs.org/ (optional)
3. Docker Desktop: https://www.docker.com/products/docker-desktop

## 🚀 Quick Start (Recommended)

### Method 1: Using Bash Script

```bash
# Clone repository
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
cd animation_quantum_mech_basics

# Make script executable
chmod +x quickstart.sh

# Run setup
./quickstart.sh

# Follow the instructions from the output
```

### Method 2: Docker Compose (Easiest)

```bash
# Clone repository
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
cd animation_quantum_mech_basics

# Build and run
docker-compose up --build

# Access at http://localhost:8080
```

### Method 3: Manual Setup

#### Step 1: Setup Backend

```bash
# Navigate to API directory
cd api/

# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start API server
python quantum_api.py
```

**Output:**
```
 * Serving Flask app 'quantum_api'
 * Running on http://127.0.0.1:5000
```

#### Step 2: Setup Frontend (New Terminal)

```bash
# Navigate to frontend directory
cd web/public/

# Start web server (Python 3)
python -m http.server 8080

# Output:
# Serving HTTP on 0.0.0.0 port 8080
```

#### Step 3: Open in Browser

Navigate to: **http://localhost:8080/index.html**

## 📚 Project Structure

```
animation_quantum_mech_basics/
├── api/                              # Backend API
│   ├── quantum_api.py               # Flask application
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment
├── web/                             # Frontend
│   ├── public/
│   │   └── index.html              # Main HTML
│   └── src/
│       ├── style.css               # Styling
│       ├── app.js                  # Main app controller
│       ├── api-client.js           # API communication
│       ├── ui-controls.js          # UI handlers
│       └── visualizations/         # Three.js visualizers
├── src/                            # Quantum physics core
│   └── quantum_playground/
│       ├── solvers.py              # Schrödinger solver
│       ├── potentials.py           # Potential definitions
│       └── animations/             # Animation modules
├── cpp/                            # C++ WebAssembly
│   └── quantum_wasm.cpp           # Performance modules
├── tests/                          # Unit tests
├── docker-compose.yml             # Docker setup
├── Dockerfile                     # Container definition
└── README_WEB.md                  # Web app documentation
```

## 🎮 Using the Application

### Navigation
1. **Sidebar**: Select simulation type
2. **Control Panel**: Adjust parameters with sliders
3. **Main Canvas**: Interactive 3D visualization
4. **Stats Panel**: View physical quantities

### Infinite Square Well
```
1. Select "Infinite Square Well"
2. Adjust "Well Width" (L)
3. Set "Number of States"
4. Choose "Selected State" (n)
5. View energy: E_n = (n²π²ℏ²)/(2mL²)
```

### Finite Square Well
```
1. Select "Finite Square Well"
2. Set "Well Width" and "Well Depth"
3. Observe penetration into forbidden region
4. Check number of bound states
```

### Quantum Tunneling
```
1. Select "Quantum Tunneling"
2. Set barrier properties and particle energy
3. Click "Start Animation"
4. Watch wave packet tunnel with T coefficient
```

### Harmonic Oscillator
```
1. Select "Harmonic Oscillator"
2. Adjust mass (m) and frequency (ω)
3. Change quantum number (n)
4. Compare numerical vs analytical energies
```

## 🔌 API Usage Examples

### Get Health Status
```bash
curl http://localhost:5000/api/health
```

### Solve Infinite Well
```bash
curl -X POST http://localhost:5000/api/infinite-well \
  -H "Content-Type: application/json" \
  -d '{
    "width": 5.0,
    "num_states": 5
  }'
```

### Simulate Tunneling
```bash
curl -X POST http://localhost:5000/api/tunneling \
  -H "Content-Type: application/json" \
  -d '{
    "barrier_height": 30.0,
    "barrier_width": 2.0,
    "particle_energy": 20.0,
    "packet_sigma": 0.5
  }'
```

## 🏗️ Building WebAssembly (Optional)

For performance optimization:

```bash
# Install Emscripten
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh

# Build WASM
cd ../cpp/
emcc quantum_wasm.cpp -o quantum.js -s WASM=1 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -O3

# Copy to web directory
cp quantum.* ../web/src/
```

## 🚢 Deployment Options

### Local Network (LAN)

```bash
# Get your machine IP
hostname -I  # Linux/Mac
ipconfig     # Windows

# Run API with external access
python quantum_api.py --host 0.0.0.0

# Run frontend with external access
python -m http.server 8080 --bind 0.0.0.0
```

Then access from another machine: `http://<your-ip>:8080`

### Heroku Deployment

```bash
# Create Heroku app
heroku login
heroku create your-app-name

# Push code
git push heroku main

# View logs
heroku logs --tail
```

### Docker Hub

```bash
# Build image
docker build -t yourusername/quantum-simulator .

# Push to Docker Hub
docker login
docker push yourusername/quantum-simulator

# Run from Docker Hub
docker run -p 5000:5000 -p 8080:8080 yourusername/quantum-simulator
```

### AWS EC2

```bash
# Launch EC2 instance
# SSH into instance
ssh -i key.pem ec2-user@your-instance

# Clone and setup
git clone <repo>
cd animation_quantum_mech_basics
./quickstart.sh

# Start services in background
nohup bash -c 'cd api && source venv/bin/activate && python quantum_api.py' > api.log &
nohup bash -c 'cd web/public && python -m http.server 8080' > web.log &
```

### Render.com (Simple)

```yaml
# render.yaml
services:
  - type: web
    name: quantum-api
    env: python
    buildCommand: pip install -r api/requirements.txt
    startCommand: cd api && python quantum_api.py
    
  - type: web
    name: quantum-web
    env: static
    staticPublishPath: web/public
```

## 🧪 Testing

### Backend Tests
```bash
cd api/
source venv/bin/activate
pytest tests/ -v

# Coverage
pytest --cov=quantum_api tests/
```

### Frontend Tests
```bash
# Manual browser testing
# Open browser console (F12)
# Run commands like:
api.solveInfiniteWell(5, 3)
ui.getParameter('well-width')
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port
python quantum_api.py --port 5001
python -m http.server 8081
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf api/venv
python3 -m venv api/venv
source api/venv/bin/activate
pip install -r api/requirements.txt
```

### CORS Errors
Check `quantum_api.py`:
```python
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:8080"]}
})
```

### WebGL Not Working
- Update graphics drivers
- Try Chrome instead of Firefox
- Check DevTools → Rendering → GPU acceleration

## 📊 Performance Monitoring

### Check API Response Time
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/api/health
```

### Monitor Memory Usage
```bash
# Linux
watch -n 1 'ps aux | grep python'

# Mac
while true; do ps aux | grep python; sleep 1; done
```

### Profile API
```bash
pip install flask-profiler
# Add profiler to quantum_api.py
```

## 🔐 Security Considerations

### Production Checklist
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set CORS origins correctly
- [ ] Use strong API keys if needed
- [ ] Regular dependency updates
- [ ] SQL injection prevention
- [ ] Rate limiting enabled

## 📝 Environment Variables

Create `.env` file in `api/`:
```env
FLASK_ENV=production
FLASK_DEBUG=False
GRID_POINTS=2000
CORS_ORIGINS=https://yourdomain.com
```

## 📖 Additional Resources

- **Quantum Physics**:
  - Griffiths - Introduction to Quantum Mechanics
  - Shankar - Principles of Quantum Mechanics

- **Web Development**:
  - Three.js Documentation: https://threejs.org/docs/
  - Flask Guide: https://flask.palletsprojects.com/
  - WebAssembly: https://emscripten.org/

- **Deployment**:
  - Docker: https://docs.docker.com/
  - Heroku: https://devcenter.heroku.com/
  - AWS: https://aws.amazon.com/

## 🆘 Getting Help

1. Check browser console (F12) for JavaScript errors
2. Check terminal output for Python errors
3. Review API logs: `http://localhost:5000/api/health`
4. See DEPLOYMENT.md for detailed guides
5. Open an issue on GitHub

## 🎉 Success!

Once everything is running:
- Frontend: http://localhost:8080
- API: http://localhost:5000/api
- WebGL: Interactive 3D visualizations
- Real-time: Parameter updates instantly

Enjoy exploring quantum mechanics!
