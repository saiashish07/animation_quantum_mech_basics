"""
Flask API Backend for Quantum Simulation
Provides REST endpoints for quantum mechanical calculations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from quantum_playground.solvers import (
    QuantumGrid,
    StationarySolver,
    TimeDependentSolver,
    GaussianWavePacket,
    compute_transmission_coefficient
)
from quantum_playground.potentials import (
    InfiniteSquareWell,
    FiniteSquareWell,
    RectangularBarrier,
    HarmonicOscillator,
    PotentialAnalysis
)

app = Flask(__name__)
CORS(app)

# Configuration
GRID_POINTS = 1000
X_MIN = -15
X_MAX = 15


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


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Quantum API is running'})


@app.route('/api/infinite-well', methods=['POST'])
def solve_infinite_well():
    """Solve infinite square well problem"""
    try:
        data = request.get_json()
        width = float(data.get('width', 5.0))
        num_states = int(data.get('num_states', 5))

        # Create grid and potential
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = InfiniteSquareWell(width)

        # Solve
        solver = StationarySolver(grid, mass=1.0)
        energies, wavefunctions = solver.solve_eigenproblem(
            potential(grid.x), 
            num_eigenvalues=num_states
        )

        # Prepare response
        response = {
            'x': serialize_array(grid.x),
            'potential': serialize_array(potential(grid.x)),
            'energies': serialize_array(energies),
            'wavefunctions': [serialize_array(wavefunctions[:, i]) for i in range(num_states)],
            'probability_densities': [
                serialize_array(np.abs(wavefunctions[:, i])**2) 
                for i in range(num_states)
            ],
            'grid_info': {
                'x_min': X_MIN,
                'x_max': X_MAX,
                'num_points': GRID_POINTS,
                'dx': grid.dx
            }
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/finite-well', methods=['POST'])
def solve_finite_well():
    """Solve finite square well problem"""
    try:
        data = request.get_json()
        width = float(data.get('width', 5.0))
        height = float(data.get('height', 50.0))
        num_states = int(data.get('num_states', 5))

        # Create grid and potential
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = FiniteSquareWell(width, height)

        # Solve
        solver = StationarySolver(grid, mass=1.0)
        energies, wavefunctions = solver.solve_eigenproblem(
            potential(grid.x),
            num_eigenvalues=num_states
        )

        # Prepare response
        response = {
            'x': serialize_array(grid.x),
            'potential': serialize_array(potential(grid.x)),
            'energies': serialize_array(energies),
            'wavefunctions': [serialize_array(wavefunctions[:, i]) for i in range(num_states)],
            'probability_densities': [
                serialize_array(np.abs(wavefunctions[:, i])**2)
                for i in range(num_states)
            ],
            'grid_info': {
                'x_min': X_MIN,
                'x_max': X_MAX,
                'num_points': GRID_POINTS,
                'dx': grid.dx
            },
            'bound_states': int(np.sum(energies < height))
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/tunneling', methods=['POST'])
def simulate_tunneling():
    """Simulate quantum tunneling"""
    try:
        data = request.get_json()
        barrier_height = float(data.get('barrier_height', 30.0))
        barrier_width = float(data.get('barrier_width', 2.0))
        particle_energy = float(data.get('particle_energy', 20.0))
        packet_sigma = float(data.get('packet_sigma', 0.5))
        duration = int(data.get('duration', 1000))

        # Create grid and potential
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = RectangularBarrier(barrier_height, barrier_width, center=0.0)
        V = potential(grid.x)

        # Initial wave packet (incident from left)
        psi0 = GaussianWavePacket.create(
            grid.x,
            x0=-5.0,
            sigma=packet_sigma,
            k0=np.sqrt(2.0 * particle_energy),  # momentum
            amplitude=1.0
        )
        psi0 = GaussianWavePacket.normalize(psi0, grid.dx)

        # Time evolution
        solver = TimeDependentSolver(grid, V, mass=1.0, dt=0.01)
        trajectory = solver.evolve(psi0, duration)

        # Calculate transmission coefficient (rough estimate from final state)
        psi_final = trajectory[:, -1]
        barrier_indices = (np.abs(grid.x) < barrier_width / 2 + 1)
        barrier_end_idx = len(grid.x) // 2 + int(barrier_width / 2 * GRID_POINTS / (X_MAX - X_MIN))

        T = compute_transmission_coefficient(
            psi_final,
            psi0,
            (GRID_POINTS // 2 - 50, barrier_end_idx + 50),
            grid.dx
        )
        R = 1.0 - T

        # Use WKB approximation for transmission coefficient
        analysis = PotentialAnalysis()
        T_wkb = analysis.tunneling_probability_estimate(particle_energy, V, grid.x)
        R_wkb = 1.0 - T_wkb

        # Prepare response
        response = {
            'x': serialize_array(grid.x),
            'potential': serialize_array(V),
            'initial_wavefunction': serialize_array(psi0),
            'initial_probability': serialize_array(np.abs(psi0)**2),
            'final_wavefunction': serialize_array(psi_final),
            'final_probability': serialize_array(np.abs(psi_final)**2),
            'trajectory_samples': [
                {
                    'time': i,
                    'wavefunction': serialize_array(trajectory[:, i::max(1, duration//50)][:, 0]),
                    'probability': serialize_array(np.abs(trajectory[:, i::max(1, duration//50)][:, 0])**2)
                }
                for i in range(0, duration, max(1, duration//50))
            ],
            'transmission_coefficient': float(T_wkb),
            'reflection_coefficient': float(R_wkb),
            'barrier_parameters': {
                'height': barrier_height,
                'width': barrier_width,
                'particle_energy': particle_energy
            },
            'grid_info': {
                'x_min': X_MIN,
                'x_max': X_MAX,
                'num_points': GRID_POINTS,
                'dx': grid.dx
            }
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/harmonic-oscillator', methods=['POST'])
def solve_harmonic_oscillator():
    """Solve harmonic oscillator problem"""
    try:
        data = request.get_json()
        mass = float(data.get('mass', 1.0))
        omega = float(data.get('omega', 1.0))
        num_states = int(data.get('num_states', 5))

        # Create grid and potential
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = HarmonicOscillator(mass, omega)

        # Solve
        solver = StationarySolver(grid, mass=mass)
        energies, wavefunctions = solver.solve_eigenproblem(
            potential(grid.x),
            num_eigenvalues=num_states
        )

        # Prepare response
        response = {
            'x': serialize_array(grid.x),
            'potential': serialize_array(potential(grid.x)),
            'energies': serialize_array(energies),
            'analytical_energies': [
                (n + 0.5) * omega for n in range(num_states)
            ],
            'wavefunctions': [serialize_array(wavefunctions[:, i]) for i in range(num_states)],
            'probability_densities': [
                serialize_array(np.abs(wavefunctions[:, i])**2)
                for i in range(num_states)
            ],
            'grid_info': {
                'x_min': X_MIN,
                'x_max': X_MAX,
                'num_points': GRID_POINTS,
                'dx': grid.dx
            },
            'parameters': {
                'mass': mass,
                'omega': omega,
                'level_spacing': omega
            }
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/transmission-coefficient', methods=['POST'])
def get_transmission_coefficient():
    """Calculate transmission coefficient using WKB approximation"""
    try:
        data = request.get_json()
        barrier_height = float(data.get('barrier_height', 30.0))
        barrier_width = float(data.get('barrier_width', 2.0))
        particle_energy = float(data.get('particle_energy', 20.0))

        # Create grid and potential
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = RectangularBarrier(barrier_height, barrier_width, center=0.0)
        V = potential(grid.x)

        # Calculate transmission coefficient
        analysis = PotentialAnalysis()
        T = analysis.tunneling_probability_estimate(particle_energy, V, grid.x)
        R = 1.0 - T

        response = {
            'transmission': float(T),
            'reflection': float(R),
            'barrier_height': barrier_height,
            'barrier_width': barrier_width,
            'particle_energy': particle_energy,
            'energy_diff': barrier_height - particle_energy
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
