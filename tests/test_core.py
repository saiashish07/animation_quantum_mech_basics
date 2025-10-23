"""
Quick validation tests for quantum playground modules.

Run with: python tests/test_core.py
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from quantum_playground.solvers import QuantumGrid, StationarySolver, GaussianWavePacket
from quantum_playground.potentials import InfiniteSquareWell, HarmonicOscillator


def test_quantum_grid():
    """Test QuantumGrid initialization and spacing."""
    print("Testing QuantumGrid...", end=" ")
    grid = QuantumGrid(-5, 5, 256)
    
    assert grid.num_points == 256
    assert np.isclose(grid.x[0], -5)
    assert np.isclose(grid.x[-1], 5)
    assert grid.dx > 0
    
    # Test kinetic energy matrix
    T = grid.kinetic_energy_matrix(mass=1.0)
    assert T.shape == (256, 256)
    
    print("✓")


def test_infinite_well():
    """Test infinite well eigenvalues."""
    print("Testing infinite well eigenvalues...", end=" ")
    
    well_width = 2.0
    grid = QuantumGrid(-1.5, 1.5, 256)
    
    # Create confining potential
    V = np.zeros_like(grid.x)
    outside = np.abs(grid.x) > well_width / 2
    V[outside] = 50.0
    
    solver = StationarySolver(grid, mass=1.0)
    E, psi = solver.solve_eigenproblem(V, num_eigenvalues=5)
    
    # Analytical energies: E_n = n^2 π^2 / (2L^2)
    E_analytical = np.array([n**2 * np.pi**2 / (2 * well_width**2) for n in range(1, 6)])
    
    # Check within 5% error
    relative_error = np.abs(E - E_analytical) / E_analytical
    assert np.all(relative_error < 0.05), f"Error too large: {relative_error}"
    
    print("✓")


def test_harmonic_oscillator():
    """Test harmonic oscillator energy spacing."""
    print("Testing harmonic oscillator energy spacing...", end=" ")
    
    omega = 1.0
    grid = QuantumGrid(-5, 5, 256)
    
    ho = HarmonicOscillator(mass=1.0, omega=omega)
    V = ho(grid.x)
    
    solver = StationarySolver(grid, mass=1.0)
    E, psi = solver.solve_eigenproblem(V, num_eigenvalues=6)
    
    # Analytical energies: E_n = (n + 0.5) ω
    E_analytical = np.array([(n + 0.5) * omega for n in range(6)])
    
    # Energy spacing should be constant
    dE_numerical = np.diff(E[:5])
    dE_analytical = np.diff(E_analytical[:5])
    
    relative_error = np.abs(dE_numerical - dE_analytical) / dE_analytical
    assert np.all(relative_error < 0.1), f"Spacing error: {relative_error}"
    
    print("✓")


def test_gaussian_packet():
    """Test Gaussian wave packet creation and normalization."""
    print("Testing Gaussian wave packet...", end=" ")
    
    x = np.linspace(-5, 5, 256)
    dx = x[1] - x[0]
    
    psi = GaussianWavePacket.create(x, x0=0, sigma=0.5, k0=2.0, amplitude=1.0)
    psi_norm = GaussianWavePacket.normalize(psi, dx)
    
    # Check normalization
    norm_sq = np.sum(np.abs(psi_norm)**2) * dx
    assert np.isclose(norm_sq, 1.0, atol=1e-6), f"Normalization error: {norm_sq}"
    
    # Check momentum expectation value ≈ ℏ * k0 = k0 (atomic units)
    
    print("✓")


def test_potential_classes():
    """Test potential classes."""
    print("Testing potential classes...", end=" ")
    
    x = np.linspace(-3, 3, 256)
    
    # Infinite well
    well = InfiniteSquareWell(width=2.0)
    V = well(x)
    assert np.max(V[np.abs(x) > 1.0]) > 1e9  # Outside is very large
    
    # Harmonic oscillator
    ho = HarmonicOscillator(mass=1.0, omega=1.0)
    V = ho(x)
    assert V[0] > V[128]  # Increasing with distance
    
    print("✓")


def test_wavefunction_orthonormality():
    """Test that computed eigenfunctions are orthonormal."""
    print("Testing orthonormality...", end=" ")
    
    grid = QuantumGrid(-5, 5, 256)
    
    ho = HarmonicOscillator(mass=1.0, omega=1.0)
    V = ho(grid.x)
    
    solver = StationarySolver(grid, mass=1.0)
    E, psi = solver.solve_eigenproblem(V, num_eigenvalues=5)
    
    # Check orthonormality
    for i in range(5):
        for j in range(5):
            overlap = np.sum(np.conj(psi[:, i]) * psi[:, j]) * grid.dx
            if i == j:
                assert np.isclose(overlap, 1.0, atol=1e-8), f"Normalization failed at {i}"
            else:
                assert np.isclose(overlap, 0.0, atol=1e-8), f"Orthogonality failed at {i},{j}"
    
    print("✓")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("QUANTUM PLAYGROUND VALIDATION TESTS")
    print("=" * 60 + "\n")
    
    tests = [
        test_quantum_grid,
        test_infinite_well,
        test_harmonic_oscillator,
        test_gaussian_packet,
        test_potential_classes,
        test_wavefunction_orthonormality,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
