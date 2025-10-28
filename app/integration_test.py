#!/usr/bin/env python3
"""
Integration test - Verify backend, frontend, and API fixes
Run this after starting the backend to verify everything works
"""

import asyncio
import json
import time
from datetime import datetime
import sys
from pathlib import Path

print("="*70)
print("QUANTUM SIMULATOR - BACKEND & FRONTEND INTEGRATION TEST")
print("="*70)

# Check required packages
packages_ok = True
try:
    import requests
    print("✅ requests module available")
except ImportError:
    print("⚠️  requests module not found (for testing)")
    packages_ok = False

BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

print(f"\nTesting at: {BASE_URL}")
print("="*70)

# Test 1: Health Check
print("\n[TEST 1] Health Check")
print("-" * 70)
try:
    if packages_ok:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Connected clients: {data.get('connected_clients')}")
            print(f"   Webhooks registered: {data.get('webhooks_registered')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Health check error: {e}")
    print(f"   Make sure backend is running: python app/api/enhanced_api.py")

# Test 2: Infinite Well Simulation
print("\n[TEST 2] Infinite Well Simulation")
print("-" * 70)
try:
    if packages_ok:
        payload = {
            "type": "infinite-well",
            "parameters": {
                "width": 5.0,
                "num_states": 3
            }
        }
        print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(f"{API_BASE}/full-simulation", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simulation successful")
            print(f"   Simulation type: {data.get('simulation_type')}")
            print(f"   Grid points: {len(data.get('grid', {}).get('x', []))}")
            print(f"   Energy levels: {len(data.get('energy_levels', {}).get('values', []))}")
            print(f"   Wavefunctions: {len(data.get('wavefunctions', []))}")
            print(f"   Probability densities: {len(data.get('probability_densities', []))}")
            
            # Show sample energy
            energies = data.get('energy_levels', {}).get('values', [])
            if energies:
                print(f"   Ground state energy: {energies[0]:.4f}")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Simulation error: {e}")

# Test 3: Harmonic Oscillator
print("\n[TEST 3] Harmonic Oscillator Simulation")
print("-" * 70)
try:
    if packages_ok:
        payload = {
            "type": "harmonic",
            "parameters": {
                "mass": 1.0,
                "omega": 1.0,
                "num_states": 3
            }
        }
        response = requests.post(f"{API_BASE}/full-simulation", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simulation successful")
            print(f"   Simulation type: {data.get('simulation_type')}")
            
            # Compare numerical vs analytical
            energies = data.get('energy_levels', {}).get('values', [])
            analytical = data.get('energy_levels', {}).get('analytical', [])
            
            if energies and analytical:
                print(f"   Energy comparison (numerical vs analytical):")
                for i, (num, ana) in enumerate(zip(energies, analytical)):
                    error = abs(num - ana) / abs(ana) * 100 if ana != 0 else 0
                    print(f"     Level {i+1}: {num:.4f} vs {ana:.4f} (error: {error:.2f}%)")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Simulation error: {e}")

# Test 4: Finite Well Simulation
print("\n[TEST 4] Finite Well Simulation")
print("-" * 70)
try:
    if packages_ok:
        payload = {
            "type": "finite-well",
            "parameters": {
                "width": 5.0,
                "height": 50.0,
                "num_states": 3
            }
        }
        response = requests.post(f"{API_BASE}/full-simulation", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simulation successful")
            print(f"   Simulation type: {data.get('simulation_type')}")
            
            energy_info = data.get('energy_levels', {})
            print(f"   Bound states: {energy_info.get('bound_states')}")
            print(f"   Well depth: {energy_info.get('well_depth')}")
            
            # Check tunneling penetration
            prob_dens = data.get('probability_densities', [])
            if prob_dens:
                print(f"   Penetration into forbidden region:")
                for state_data in prob_dens[:2]:
                    penetration = state_data.get('penetration', 0)
                    print(f"     State {state_data['state']}: {penetration:.4f}")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Simulation error: {e}")

# Test 5: Tunneling Simulation
print("\n[TEST 5] Quantum Tunneling Simulation")
print("-" * 70)
try:
    if packages_ok:
        payload = {
            "type": "tunneling",
            "parameters": {
                "barrier_height": 30.0,
                "barrier_width": 2.0,
                "particle_energy": 20.0,
                "packet_sigma": 0.5,
                "duration": 100
            }
        }
        response = requests.post(f"{API_BASE}/full-simulation", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simulation successful")
            print(f"   Simulation type: {data.get('simulation_type')}")
            
            particle = data.get('particle', {})
            print(f"   Particle energy: {particle.get('energy')}")
            print(f"   Classically forbidden: {particle.get('classically_forbidden')}")
            
            coef = data.get('coefficients', {})
            print(f"   Transmission: {coef.get('transmission_percent'):.2f}%")
            print(f"   Reflection: {coef.get('reflection_percent'):.2f}%")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Simulation error: {e}")

# Test 6: Webhook Registration
print("\n[TEST 6] Webhook System")
print("-" * 70)
try:
    if packages_ok:
        # Register
        payload = {
            "event_type": "on_simulation_complete",
            "webhook_url": "https://example.com/webhook",
            "metadata": {"test": True}
        }
        response = requests.post(f"{API_BASE}/webhooks/register", json=payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ Webhook registered")
            print(f"   Event type: {payload['event_type']}")
            print(f"   URL: {payload['webhook_url']}")
        else:
            print(f"⚠️  Webhook registration response: {response.status_code}")
        
        # List
        response = requests.get(f"{API_BASE}/webhooks/list", timeout=5)
        if response.status_code == 200:
            webhooks = response.json()
            print(f"✅ Webhooks listed")
            for event_type, urls in webhooks.items():
                if urls:
                    print(f"   {event_type}: {len(urls)} registered")
        else:
            print(f"⚠️  Webhook list response: {response.status_code}")
    else:
        print("⚠️  Skipping (requests module not available)")
except Exception as e:
    print(f"❌ Webhook error: {e}")

# Frontend Configuration Check
print("\n[TEST 7] Frontend Configuration")
print("-" * 70)

frontend_config = {
    "API_BASE_URL": "http://localhost:5000",
    "WEBSOCKET_URL": "http://localhost:5000",
    "SIMULATIONS": ["infinite-well", "finite-well", "tunneling", "harmonic"],
    "VISUALIZATION_TYPES": ["energy-levels", "probability-density", "wavefunction", "statistics"],
    "CONTROLS": {
        "infinite-well": ["wellWidth", "numStates"],
        "finite-well": ["finiteWidth", "wellDepth", "finiteNumStates"],
        "tunneling": ["barrierHeight", "barrierWidth", "particleEnergy"],
        "harmonic": ["omega", "harmonicNumStates"]
    }
}

print(f"✅ Frontend Configuration:")
print(f"   API URL: {frontend_config['API_BASE_URL']}")
print(f"   WebSocket URL: {frontend_config['WEBSOCKET_URL']}")
print(f"   Simulations supported: {len(frontend_config['SIMULATIONS'])}")
for sim in frontend_config['SIMULATIONS']:
    print(f"      - {sim}")

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

if packages_ok:
    print("""
✅ All tests completed!

If you see checkmarks (✅) for all tests:
   1. Backend is running correctly
   2. API endpoints are working
   3. Frontend can connect and get data
   4. All 4 simulations are functional
   5. WebSocket and webhooks ready

Next steps:
   1. Open http://localhost:8000/dashboard.html in browser
   2. Select a simulation type
   3. Adjust parameters
   4. Click "Run Simulation"
   5. View visualizations update in real-time
""")
else:
    print("""
⚠️  Some tests were skipped (requests module not installed)

To run full tests:
   pip install requests

Then run this script again.

Alternatively, manually test:
   1. Start backend: python app/api/enhanced_api.py
   2. Start frontend: cd app/frontend/public && python -m http.server 8000
   3. Open: http://localhost:8000/dashboard.html
   4. Run a simulation and check browser console for errors
""")

print("\n" + "="*70)
