"""
Enhanced Quantum API with WebSocket, Webhooks, and Complete Visualization Data
Connects Python solvers to real-time frontend visualization
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import numpy as np
import sys
from pathlib import Path
from datetime import datetime
import json

# Add src to path
# Path: .../app/backend/app/api/enhanced_api.py -> need to go to .../src
workspace_root = Path(__file__).parent.parent.parent.parent.parent  # Go up to workspace root
sys.path.insert(0, str(workspace_root / 'src'))

from quantum_playground.solvers import (
    QuantumGrid, StationarySolver, TimeDependentSolver,
    GaussianWavePacket, compute_transmission_coefficient
)
from quantum_playground.potentials import (
    InfiniteSquareWell, FiniteSquareWell, RectangularBarrier,
    HarmonicOscillator, PotentialAnalysis
)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
GRID_POINTS = 1000
X_MIN = -15
X_MAX = 15

# Webhook registry
webhooks = {
    'on_simulation_complete': [],
    'on_energy_calculate': [],
    'on_tunneling_start': [],
    'on_error': []
}

# Connected clients
connected_clients = {}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def serialize_array(arr):
    """Convert numpy array to list for JSON serialization"""
    if isinstance(arr, np.ndarray):
        return arr.tolist()
    return arr


def serialize_complex(z):
    """Convert complex number for JSON"""
    if isinstance(z, (complex, np.complexfloating)):
        return {'real': float(z.real), 'imag': float(z.imag)}
    return float(z)


def calculate_statistics(x, psi, dx):
    """Calculate quantum statistics"""
    prob = np.abs(psi) ** 2
    
    # Normalize probability
    prob_norm = prob / (np.sum(prob) * dx + 1e-10)
    
    # Expected values
    exp_x = np.sum(x * prob_norm) * dx
    exp_x2 = np.sum(x**2 * prob_norm) * dx
    
    # Uncertainties
    delta_x = np.sqrt(np.abs(exp_x2 - exp_x**2))
    
    return {
        'expectation_x': float(exp_x),
        'expectation_x2': float(exp_x2),
        'uncertainty_x': float(delta_x),
        'max_probability': float(np.max(prob_norm)),
        'min_probability': float(np.min(prob_norm)),
        'mean_probability': float(np.mean(prob_norm)),
        'integral_probability': float(np.sum(prob_norm) * dx)
    }


def emit_to_webhooks(event_type, data):
    """Trigger webhooks for given event type"""
    if event_type in webhooks:
        for webhook_url in webhooks[event_type]:
            try:
                import requests
                requests.post(webhook_url, json=data, timeout=5)
            except Exception as e:
                print(f"Webhook error: {e}")


# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    client_id = request.sid
    connected_clients[client_id] = {
        'connected_at': datetime.now().isoformat(),
        'simulations': []
    }
    emit('connection_response', {
        'data': 'Connected to quantum simulator',
        'client_id': client_id
    })
    print(f"Client {client_id} connected")


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    client_id = request.sid
    if client_id in connected_clients:
        del connected_clients[client_id]
    print(f"Client {client_id} disconnected")


@socketio.on('subscribe_simulation')
def handle_subscribe(data):
    """Subscribe to specific simulation updates"""
    room = data.get('simulation_type', 'default')
    join_room(room)
    emit('subscribed', {'simulation': room})


@socketio.on('unsubscribe_simulation')
def handle_unsubscribe(data):
    """Unsubscribe from simulation updates"""
    room = data.get('simulation_type', 'default')
    leave_room(room)
    emit('unsubscribed', {'simulation': room})


# ============================================================================
# REST API ENDPOINTS - VISUALIZATION DATA
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check with server info"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'connected_clients': len(connected_clients),
        'webhooks_registered': sum(len(hooks) for hooks in webhooks.values())
    })


@app.route('/api/full-simulation', methods=['POST'])
def full_simulation():
    """Complete simulation with all visualization data"""
    try:
        data = request.get_json()
        sim_type = data.get('type', 'infinite-well')
        
        # Get parameters
        params = data.get('parameters', {})
        
        # Create grid
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        
        if sim_type == 'infinite-well':
            result = solve_infinite_well_full(grid, params)
        elif sim_type == 'finite-well':
            result = solve_finite_well_full(grid, params)
        elif sim_type == 'tunneling':
            result = solve_tunneling_full(grid, params)
        elif sim_type == 'harmonic':
            result = solve_harmonic_full(grid, params)
        else:
            raise ValueError(f"Unknown simulation type: {sim_type}")
        
        # Emit to WebSocket clients
        socketio.emit('simulation_complete', result, room=sim_type)
        emit_to_webhooks('on_simulation_complete', result)
        
        return jsonify(result)
    
    except Exception as e:
        error_data = {'error': str(e), 'timestamp': datetime.now().isoformat()}
        emit_to_webhooks('on_error', error_data)
        return jsonify(error_data), 400


def solve_infinite_well_full(grid, params):
    """Complete infinite well visualization data"""
    width = float(params.get('width', 5.0))
    num_states = int(params.get('num_states', 5))
    
    # Solve
    potential = InfiniteSquareWell(width)
    solver = StationarySolver(grid, mass=1.0)
    energies, wavefunctions = solver.solve_eigenproblem(
        potential(grid.x), num_eigenvalues=num_states
    )
    
    # Build complete response
    response = {
        'simulation_type': 'infinite-well',
        'timestamp': datetime.now().isoformat(),
        'grid': {
            'x': serialize_array(grid.x),
            'x_min': X_MIN,
            'x_max': X_MAX,
            'num_points': GRID_POINTS,
            'dx': float(grid.dx)
        },
        'potential': {
            'values': serialize_array(potential(grid.x)),
            'type': 'infinite_square_well',
            'width': width
        },
        'energy_levels': {
            'values': serialize_array(energies),
            'labels': [f"E_{i+1}" for i in range(num_states)],
            'ground_state': float(energies[0]),
            'spacing': serialize_array(np.diff(energies)) if len(energies) > 1 else []
        },
        'wavefunctions': [
            {
                'state': i + 1,
                'psi': serialize_array(wavefunctions[:, i]),
                'psi_real': serialize_array(np.real(wavefunctions[:, i])),
                'psi_imag': serialize_array(np.imag(wavefunctions[:, i])),
                'energy': float(energies[i])
            }
            for i in range(num_states)
        ],
        'probability_densities': [
            {
                'state': i + 1,
                'values': serialize_array(np.abs(wavefunctions[:, i])**2),
                'max': float(np.max(np.abs(wavefunctions[:, i])**2)),
                'min': float(np.min(np.abs(wavefunctions[:, i])**2))
            }
            for i in range(num_states)
        ],
        'statistics': [
            {
                'state': i + 1,
                **calculate_statistics(grid.x, wavefunctions[:, i], grid.dx)
            }
            for i in range(num_states)
        ],
        'analytical_comparison': [
            {
                'state': i + 1,
                'numerical_energy': float(energies[i]),
                'analytical_energy': float((i+1)**2 * np.pi**2 / (2 * width**2)),
                'error': float(abs(energies[i] - (i+1)**2 * np.pi**2 / (2 * width**2)))
            }
            for i in range(num_states)
        ]
    }
    
    emit_to_webhooks('on_energy_calculate', {'energies': response['energy_levels']})
    return response


def solve_finite_well_full(grid, params):
    """Complete finite well visualization data"""
    width = float(params.get('width', 5.0))
    height = float(params.get('height', 50.0))
    num_states = int(params.get('num_states', 5))
    
    potential = FiniteSquareWell(width, height)
    solver = StationarySolver(grid, mass=1.0)
    energies, wavefunctions = solver.solve_eigenproblem(
        potential(grid.x), num_eigenvalues=num_states
    )
    
    bound_states = int(np.sum(energies < height))
    V_array = potential(grid.x)
    
    response = {
        'simulation_type': 'finite-well',
        'timestamp': datetime.now().isoformat(),
        'grid': {
            'x': serialize_array(grid.x),
            'x_min': X_MIN,
            'x_max': X_MAX,
            'num_points': GRID_POINTS,
            'dx': float(grid.dx)
        },
        'potential': {
            'values': serialize_array(V_array),
            'type': 'finite_square_well',
            'width': width,
            'height': height
        },
        'energy_levels': {
            'values': serialize_array(energies),
            'labels': [f"E_{i+1}" for i in range(num_states)],
            'bound_states': bound_states,
            'ground_state': float(energies[0]),
            'well_depth': height
        },
        'wavefunctions': [
            {
                'state': i + 1,
                'psi': serialize_array(wavefunctions[:, i]),
                'psi_real': serialize_array(np.real(wavefunctions[:, i])),
                'psi_imag': serialize_array(np.imag(wavefunctions[:, i])),
                'energy': float(energies[i]),
                'is_bound': bool(energies[i] < height)
            }
            for i in range(num_states)
        ],
        'probability_densities': [
            {
                'state': i + 1,
                'values': serialize_array(np.abs(wavefunctions[:, i])**2),
                'max': float(np.max(np.abs(wavefunctions[:, i])**2)),
                'penetration': float(np.sum(np.abs(wavefunctions[:, -100:, i])**2 * grid.dx))
            }
            for i in range(num_states)
        ],
        'statistics': [
            {
                'state': i + 1,
                **calculate_statistics(grid.x, wavefunctions[:, i], grid.dx)
            }
            for i in range(num_states)
        ],
        'forbidden_regions': {
            'left': {'start': X_MIN, 'end': -width/2},
            'right': {'start': width/2, 'end': X_MAX}
        }
    }
    
    return response


def solve_tunneling_full(grid, params):
    """Complete tunneling visualization data"""
    barrier_height = float(params.get('barrier_height', 30.0))
    barrier_width = float(params.get('barrier_width', 2.0))
    particle_energy = float(params.get('particle_energy', 20.0))
    packet_sigma = float(params.get('packet_sigma', 0.5))
    duration = int(params.get('duration', 1000))
    
    potential = RectangularBarrier(barrier_height, barrier_width, center=0.0)
    V = potential(grid.x)
    
    # Initial wave packet
    psi0 = GaussianWavePacket.create(
        grid.x, x0=-5.0, sigma=packet_sigma,
        k0=np.sqrt(2.0 * particle_energy), amplitude=1.0
    )
    psi0 = GaussianWavePacket.normalize(psi0, grid.dx)
    
    # Time evolution
    solver = TimeDependentSolver(grid, V, mass=1.0, dt=0.01)
    trajectory = solver.evolve(psi0, duration)
    
    # WKB transmission
    analysis = PotentialAnalysis()
    T_wkb = analysis.tunneling_probability_estimate(particle_energy, V, grid.x)
    R_wkb = 1.0 - T_wkb
    
    response = {
        'simulation_type': 'tunneling',
        'timestamp': datetime.now().isoformat(),
        'grid': {
            'x': serialize_array(grid.x),
            'x_min': X_MIN,
            'x_max': X_MAX,
            'num_points': GRID_POINTS,
            'dx': float(grid.dx)
        },
        'potential': {
            'values': serialize_array(V),
            'type': 'rectangular_barrier',
            'height': barrier_height,
            'width': barrier_width,
            'center': 0.0
        },
        'particle': {
            'energy': particle_energy,
            'classically_forbidden': bool(particle_energy < barrier_height),
            'above_barrier': barrier_height - particle_energy
        },
        'initial_state': {
            'psi': serialize_array(psi0),
            'psi_real': serialize_array(np.real(psi0)),
            'psi_imag': serialize_array(np.imag(psi0)),
            'probability': serialize_array(np.abs(psi0)**2),
            'packet_width': float(packet_sigma)
        },
        'final_state': {
            'psi': serialize_array(trajectory[:, -1]),
            'psi_real': serialize_array(np.real(trajectory[:, -1])),
            'psi_imag': serialize_array(np.imag(trajectory[:, -1])),
            'probability': serialize_array(np.abs(trajectory[:, -1])**2)
        },
        'coefficients': {
            'transmission': float(T_wkb),
            'reflection': float(R_wkb),
            'transmission_percent': float(T_wkb * 100),
            'reflection_percent': float(R_wkb * 100)
        },
        'trajectory': {
            'frames': min(50, duration),
            'data': [
                {
                    'time': int(i),
                    'psi': serialize_array(trajectory[:, i]),
                    'probability': serialize_array(np.abs(trajectory[:, i])**2)
                }
                for i in range(0, duration, max(1, duration // 50))
            ]
        }
    }
    
    emit_to_webhooks('on_tunneling_start', {
        'coefficients': response['coefficients']
    })
    return response


def solve_harmonic_full(grid, params):
    """Complete harmonic oscillator visualization data"""
    mass = float(params.get('mass', 1.0))
    omega = float(params.get('omega', 1.0))
    num_states = int(params.get('num_states', 5))
    
    potential = HarmonicOscillator(mass, omega)
    solver = StationarySolver(grid, mass=mass)
    energies, wavefunctions = solver.solve_eigenproblem(
        potential(grid.x), num_eigenvalues=num_states
    )
    
    analytical_energies = np.array([(n + 0.5) * omega for n in range(num_states)])
    
    response = {
        'simulation_type': 'harmonic-oscillator',
        'timestamp': datetime.now().isoformat(),
        'grid': {
            'x': serialize_array(grid.x),
            'x_min': X_MIN,
            'x_max': X_MAX,
            'num_points': GRID_POINTS,
            'dx': float(grid.dx)
        },
        'potential': {
            'values': serialize_array(potential(grid.x)),
            'type': 'harmonic_oscillator',
            'mass': mass,
            'omega': omega
        },
        'energy_levels': {
            'values': serialize_array(energies),
            'analytical': serialize_array(analytical_energies),
            'labels': [f"E_{i}" for i in range(num_states)],
            'level_spacing': float(omega),
            'ground_state_numerical': float(energies[0]),
            'ground_state_analytical': float(0.5 * omega)
        },
        'wavefunctions': [
            {
                'state': i,
                'psi': serialize_array(wavefunctions[:, i]),
                'psi_real': serialize_array(np.real(wavefunctions[:, i])),
                'psi_imag': serialize_array(np.imag(wavefunctions[:, i])),
                'energy_numerical': float(energies[i]),
                'energy_analytical': float(analytical_energies[i])
            }
            for i in range(num_states)
        ],
        'probability_densities': [
            {
                'state': i,
                'values': serialize_array(np.abs(wavefunctions[:, i])**2),
                'max': float(np.max(np.abs(wavefunctions[:, i])**2))
            }
            for i in range(num_states)
        ],
        'statistics': [
            {
                'state': i,
                **calculate_statistics(grid.x, wavefunctions[:, i], grid.dx)
            }
            for i in range(num_states)
        ],
        'analytical_comparison': [
            {
                'state': i,
                'numerical_energy': float(energies[i]),
                'analytical_energy': float(analytical_energies[i]),
                'percent_error': float(abs(energies[i] - analytical_energies[i]) / analytical_energies[i] * 100)
            }
            for i in range(num_states)
        ]
    }
    
    return response


# ============================================================================
# WEBHOOK MANAGEMENT
# ============================================================================

@app.route('/api/webhooks/register', methods=['POST'])
def register_webhook():
    """Register a webhook endpoint"""
    try:
        data = request.get_json()
        event_type = data.get('event_type')
        webhook_url = data.get('webhook_url')
        
        if event_type not in webhooks:
            return jsonify({'error': 'Invalid event type'}), 400
        
        if webhook_url not in webhooks[event_type]:
            webhooks[event_type].append(webhook_url)
        
        return jsonify({
            'status': 'registered',
            'event_type': event_type,
            'webhook_url': webhook_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/webhooks/unregister', methods=['POST'])
def unregister_webhook():
    """Unregister a webhook endpoint"""
    try:
        data = request.get_json()
        event_type = data.get('event_type')
        webhook_url = data.get('webhook_url')
        
        if event_type in webhooks and webhook_url in webhooks[event_type]:
            webhooks[event_type].remove(webhook_url)
        
        return jsonify({'status': 'unregistered'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/webhooks/list', methods=['GET'])
def list_webhooks():
    """List all registered webhooks"""
    return jsonify(webhooks)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
