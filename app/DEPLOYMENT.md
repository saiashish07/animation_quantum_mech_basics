# Deployment Guide

Complete guide for deploying the Quantum Simulator to production environments.

## 📋 Prerequisites

- Python 3.9+
- Node.js (optional, for frontend bundling)
- Docker (for containerized deployment)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🏗️ Local Development Setup

### 1. Clone Repository
```bash
git clone <repo>
cd animation_quantum_mech_basics
```

### 2. Backend Setup

```bash
cd app/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
# OR manually:
pip install flask flask-cors flask-socketio python-socketio numpy scipy requests
```

### 3. Frontend Setup
Frontend is vanilla JavaScript, no build step needed. Just serve the files:

```bash
cd ../../frontend/public

# Option 1: Python built-in server
python -m http.server 8000

# Option 2: Node.js http-server
npx http-server

# Option 3: Use your preferred web server (nginx, apache, etc.)
```

### 4. Run Backend
```bash
cd ../../backend/app/api

# Run the Flask server
python enhanced_api.py

# Server starts at http://localhost:5000
```

### 5. Access Frontend
Open browser to `http://localhost:8000/dashboard.html`

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
# Dockerfile - Backend
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY app/backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/backend/app ./

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "api/enhanced_api.py"]
```

### 2. Build Docker Image

```bash
docker build -t quantum-simulator:latest .
```

### 3. Run Container

```bash
docker run -d \
  --name quantum-api \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  quantum-simulator:latest
```

### 4. Docker Compose (Full Stack)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    volumes:
      - ./app/backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8000:80"
    depends_on:
      - backend
    volumes:
      - ./app/frontend/public:/usr/share/nginx/html

volumes:
  quantum-data:
```

Deploy with:
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Deployment (EC2 + Elastic Beanstalk)

1. **Create Elastic Beanstalk environment**:
```bash
eb create quantum-simulator

# Configure:
# - Platform: Python 3.9
# - Instance type: t3.medium
# - Environment variables: FLASK_ENV=production
```

2. **Deploy**:
```bash
eb deploy
```

### Heroku Deployment

1. **Create Procfile**:
```
web: cd app/backend && python -m flask run
```

2. **Create requirements.txt**:
```
flask==2.3.0
flask-cors==4.0.0
flask-socketio==5.3.0
numpy==1.24.0
scipy==1.10.0
requests==2.31.0
```

3. **Deploy**:
```bash
heroku login
heroku create quantum-simulator
git push heroku main
```

### Google Cloud Run

1. **Create Dockerfile**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app/backend/requirements.txt .
RUN pip install -r requirements.txt
COPY app/backend/app ./
CMD exec gunicorn --bind :$PORT --workers 4 --threads 2 api.enhanced_api:app
```

2. **Deploy**:
```bash
gcloud run deploy quantum-simulator \
  --source . \
  --platform managed \
  --region us-central1
```

## 🔐 Security Configuration

### 1. CORS Setup

```python
# enhanced_api.py
from flask_cors import CORS

CORS(app, 
    origins=["https://yourdomain.com"],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"]
)
```

### 2. API Key Authentication

```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_KEY'):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/full-simulation', methods=['POST'])
@require_api_key
def full_simulation():
    # ...
```

### 3. Rate Limiting

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/api/full-simulation', methods=['POST'])
@limiter.limit("10 per minute")
def full_simulation():
    # ...
```

### 4. HTTPS Configuration

```python
# Redirect HTTP to HTTPS
@app.before_request
def enforce_https():
    if not request.is_secure and app.env == 'production':
        return redirect(request.url.replace('http://', 'https://'), code=301)
```

## 📊 Monitoring & Logging

### 1. Application Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/quantum.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Quantum simulator startup')
```

### 2. Performance Metrics

```python
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed = time.time() - request.start_time
    app.logger.info(f'{request.method} {request.path} - {elapsed:.3f}s')
    return response
```

### 3. Health Monitoring

```python
@app.route('/health')
def health():
    return {
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'uptime': process_uptime(),
        'memory': memory_usage(),
        'active_clients': len(connected_clients)
    }
```

## 🚀 Performance Tuning

### 1. Gunicorn Configuration

```bash
# requirements.txt
gunicorn==20.1.0
gevent==21.12.0
gevent-websocket==0.10.1
```

```bash
gunicorn --workers 4 \
         --worker-class gevent \
         --worker-connections 100 \
         --timeout 120 \
         app.api.enhanced_api:app
```

### 2. Caching Optimization

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/health')
@cache.cached(timeout=60)
def health_check():
    # ...
```

### 3. Database Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/quantum',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

## 📦 Backup & Recovery

### 1. Backup Simulation Data

```bash
# Create backup directory
mkdir -p backups

# Backup API logs and cache
tar -czf backups/quantum-$(date +%Y%m%d).tar.gz \
    logs/ \
    cache/ \
    config/
```

### 2. Automated Backup

```bash
# backup.sh
#!/bin/bash
BACKUP_DIR="/backups/quantum"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/quantum_$DATE.tar.gz \
    /app/logs \
    /app/cache

# Keep only last 7 days
find $BACKUP_DIR -name "quantum_*.tar.gz" -mtime +7 -delete
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

## 🧪 Testing

### 1. Unit Tests

```python
# tests/test_api.py
import pytest
from app.api.enhanced_api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert 'status' in response.json

def test_infinite_well(client):
    response = client.post('/api/full-simulation', json={
        'type': 'infinite-well',
        'parameters': {'width': 5.0, 'num_states': 5}
    })
    assert response.status_code == 200
    assert 'energy_levels' in response.json
```

Run tests:
```bash
pytest tests/ -v
```

### 2. Load Testing

```bash
pip install locust
```

```python
# locustfile.py
from locust import HttpUser, task

class SimulatorUser(HttpUser):
    @task
    def run_simulation(self):
        self.client.post('/api/full-simulation', json={
            'type': 'infinite-well',
            'parameters': {'width': 5.0, 'num_states': 5}
        })
```

Run:
```bash
locust -f locustfile.py --host=http://localhost:5000
```

## 📋 Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] CORS settings appropriate
- [ ] Logging configured
- [ ] Database migrations run
- [ ] SSL certificates ready
- [ ] Backup strategy in place

### Post-Deployment
- [ ] Health check endpoint responding
- [ ] WebSocket connections working
- [ ] Webhook delivery tested
- [ ] API rate limiting working
- [ ] Monitoring/logging operational
- [ ] Backup running automatically
- [ ] Performance metrics baseline established

## 🆘 Troubleshooting

### Issue: Out of Memory
```
Solution: Increase GRID_POINTS optimization or reduce max concurrent simulations
```

### Issue: WebSocket Disconnections
```
Solution: Check firewall, increase timeout, use fallback polling
```

### Issue: API Timeouts
```
Solution: Optimize solvers, increase request timeout, scale horizontally
```

## 📞 Support

Refer to main README.md for additional documentation.
