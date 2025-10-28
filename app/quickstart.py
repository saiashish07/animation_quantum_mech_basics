#!/usr/bin/env python3
"""
Quick Start Script - Run this to test the entire system
"""

import subprocess
import sys
import os
import time
import requests
import json
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status='info'):
    colors = {
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'info': Colors.BLUE
    }
    color = colors.get(status, Colors.BLUE)
    print(f"{color}{'✓' if status == 'success' else '✗' if status == 'error' else '→'} {message}{Colors.ENDC}")

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}")
    print(f"{text.center(50)}")
    print(f"{'='*50}{Colors.ENDC}\n")

def check_python():
    """Check Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} OK", 'success')
        return True
    else:
        print_status(f"Python {version.major}.{version.minor} - Need 3.9+", 'error')
        return False

def check_dependencies():
    """Check required Python packages"""
    print_header("Checking Dependencies")
    
    required = [
        'flask', 'numpy', 'scipy', 'flask_cors', 'flask_socketio', 'requests'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print_status(f"{package}", 'success')
        except ImportError:
            print_status(f"{package} (not installed)", 'error')
            missing.append(package)
    
    if missing:
        print_status(f"\nInstall missing: pip install {' '.join(missing)}", 'warning')
        return False
    
    return True

def test_api_endpoint(url, data=None):
    """Test an API endpoint"""
    try:
        if data:
            response = requests.post(url, json=data, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_server_connection():
    """Test if server is running"""
    print_header("Testing Server Connection")
    
    url = "http://localhost:5000/api/health"
    success, result = test_api_endpoint(url)
    
    if success:
        print_status(f"Server responding", 'success')
        print_status(f"Connected clients: {result.get('connected_clients', 0)}", 'success')
        return True
    else:
        print_status(f"Server not responding: {result}", 'error')
        print_status("Start server with: python app/api/enhanced_api.py", 'warning')
        return False

def test_infinite_well():
    """Test infinite well simulation"""
    print_header("Testing Infinite Well Simulation")
    
    url = "http://localhost:5000/api/full-simulation"
    data = {
        "type": "infinite-well",
        "parameters": {
            "width": 5.0,
            "num_states": 3
        }
    }
    
    success, result = test_api_endpoint(url, data)
    
    if success:
        print_status("Simulation ran successfully", 'success')
        if 'energy_levels' in result:
            energies = result['energy_levels']['values']
            print_status(f"Energy levels: {[f'{e:.3f}' for e in energies[:3]]}", 'success')
        return True
    else:
        print_status(f"Simulation failed: {result}", 'error')
        return False

def test_finite_well():
    """Test finite well simulation"""
    print_header("Testing Finite Well Simulation")
    
    url = "http://localhost:5000/api/full-simulation"
    data = {
        "type": "finite-well",
        "parameters": {
            "width": 4.0,
            "height": 40.0,
            "num_states": 3
        }
    }
    
    success, result = test_api_endpoint(url, data)
    
    if success:
        print_status("Simulation ran successfully", 'success')
        if 'energy_levels' in result:
            bound = result['energy_levels'].get('bound_states', 0)
            print_status(f"Bound states: {bound}", 'success')
        return True
    else:
        print_status(f"Simulation failed: {result}", 'error')
        return False

def test_tunneling():
    """Test tunneling simulation"""
    print_header("Testing Tunneling Simulation")
    
    url = "http://localhost:5000/api/full-simulation"
    data = {
        "type": "tunneling",
        "parameters": {
            "barrier_height": 30.0,
            "barrier_width": 2.0,
            "particle_energy": 20.0,
            "packet_sigma": 0.5,
            "duration": 100
        }
    }
    
    success, result = test_api_endpoint(url, data)
    
    if success:
        print_status("Simulation ran successfully", 'success')
        if 'coefficients' in result:
            T = result['coefficients']['transmission']
            print_status(f"Transmission coefficient: {T:.4f}", 'success')
        return True
    else:
        print_status(f"Simulation failed: {result}", 'error')
        return False

def test_harmonic_oscillator():
    """Test harmonic oscillator"""
    print_header("Testing Harmonic Oscillator")
    
    url = "http://localhost:5000/api/full-simulation"
    data = {
        "type": "harmonic",
        "parameters": {
            "mass": 1.0,
            "omega": 1.0,
            "num_states": 3
        }
    }
    
    success, result = test_api_endpoint(url, data)
    
    if success:
        print_status("Simulation ran successfully", 'success')
        if 'energy_levels' in result:
            levels = result['energy_levels']
            numerical = levels['values']
            analytical = levels['analytical']
            print_status(f"E_0 numerical: {numerical[0]:.4f}, analytical: {analytical[0]:.4f}", 'success')
        return True
    else:
        print_status(f"Simulation failed: {result}", 'error')
        return False

def test_webhooks():
    """Test webhook registration"""
    print_header("Testing Webhook System")
    
    url = "http://localhost:5000/api/webhooks/register"
    data = {
        "event_type": "simulation.complete",
        "webhook_url": "https://example.com/webhook"
    }
    
    success, result = test_api_endpoint(url, data)
    
    if success:
        print_status("Webhook registration successful", 'success')
        return True
    else:
        print_status(f"Webhook registration failed: {result}", 'error')
        return False

def run_all_tests():
    """Run all tests"""
    print_header("Quantum Simulator - Comprehensive Test Suite")
    
    results = {}
    
    # Check environment
    results['python'] = check_python()
    results['dependencies'] = check_dependencies()
    
    if not results['python'] or not results['dependencies']:
        print_status("\nFix issues above before running simulations", 'error')
        return results
    
    # Test server
    if not test_server_connection():
        print_status("\nCannot run simulation tests without server", 'warning')
        return results
    
    # Test simulations
    results['infinite_well'] = test_infinite_well()
    results['finite_well'] = test_finite_well()
    results['tunneling'] = test_tunneling()
    results['harmonic'] = test_harmonic_oscillator()
    results['webhooks'] = test_webhooks()
    
    return results

def print_summary(results):
    """Print test summary"""
    print_header("Test Summary")
    
    for test, passed in results.items():
        status = 'success' if passed else 'error'
        print_status(f"{test.replace('_', ' ').title()}: {'PASS' if passed else 'FAIL'}", status)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print_status(f"\nTotal: {passed}/{total} tests passed", 'success' if passed == total else 'warning')

if __name__ == '__main__':
    try:
        results = run_all_tests()
        print_summary(results)
    except KeyboardInterrupt:
        print_status("\nTests interrupted by user", 'warning')
        sys.exit(1)
    except Exception as e:
        print_status(f"Error during testing: {e}", 'error')
        sys.exit(1)
