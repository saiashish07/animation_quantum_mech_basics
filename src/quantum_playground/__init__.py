"""
Quantum Playground: Interactive Simulations for Quantum Mechanics

Comprehensive Python suite for visualizing 4 fundamental quantum systems:
  1. Infinite Potential Well (Particle in a Box)
  2. Finite Potential Well
  3. Quantum Harmonic Oscillator
  4. Quantum Tunneling

Modules:
  - solvers: Core Schrödinger equation solver and Hamiltonian construction
  - potentials: Potential energy functions (well, barrier, harmonic oscillator)
  - animations: Visualization and animation utilities

Quick Start:
  python -m quantum_playground all              # Run all simulations
  python -m quantum_playground tunneling        # Just tunneling
  python -m quantum_playground all --no-animation  # Static plots only

API Example:
  from quantum_playground.animations import TunnelingSimulation
  
  sim = TunnelingSimulation(barrier_height=5.0)
  trajectory = sim.run_evolution(num_steps=800)
  sim.plot_transmission_analysis(trajectory, save_path='tunneling.png')
  sim.animate_tunneling(trajectory, save_path='tunneling.mp4')
"""

__version__ = "0.1.0"
__author__ = "Quantum Mechanics Simulation Team"

# Export main simulation classes
from quantum_playground.animations import (
    InfiniteWellSimulation,
    FiniteWellSimulation,
    HarmonicOscillatorSimulation,
    TunnelingSimulation,
)

__all__ = [
    "InfiniteWellSimulation",
    "FiniteWellSimulation",
    "HarmonicOscillatorSimulation",
    "TunnelingSimulation",
]
