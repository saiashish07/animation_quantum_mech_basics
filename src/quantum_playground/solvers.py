"""
Core quantum mechanics solvers using finite difference method.

Implements:
- Spatial discretization
- Hamiltonian matrix construction
- Eigenvalue problems
- Time-dependent evolution (Crank-Nicolson scheme)
"""

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as sp_linalg
from typing import Tuple, Dict, Optional
import warnings


class QuantumGrid:
    """Manages spatial discretization and kinetic energy operator."""

    def __init__(self, x_min: float, x_max: float, num_points: int):
        """
        Initialize spatial grid.

        Args:
            x_min: Left boundary
            x_max: Right boundary
            num_points: Number of grid points
        """
        self.x_min = x_min
        self.x_max = x_max
        self.num_points = num_points
        self.x = np.linspace(x_min, x_max, num_points)
        self.dx = self.x[1] - self.x[0]

    def kinetic_energy_matrix(self, mass: float = 1.0) -> sparse.csr_matrix:
        """
        Construct kinetic energy operator: -ℏ²/(2m) d²/dx².

        Using finite difference: d²ψ/dx² ≈ [ψ(i+1) - 2ψ(i) + ψ(i-1)] / dx²
        The operator -d²/dx² is positive definite, with positive eigenvalues.

        Args:
            mass: Particle mass (default 1.0 in atomic units)

        Returns:
            Sparse tridiagonal matrix of kinetic energy operator
        """
        # hbar² / (2m) = 1/2 in atomic units
        hbar_sq_over_2m = 1.0 / (2.0 * mass)
        # Coefficient for -d²/dx² (negative sign to get the - operator)
        coeff = -hbar_sq_over_2m / (self.dx ** 2)

        # Tridiagonal structure: [1, -2, 1] / dx² with negative coefficient
        # gives us: -hbar²/(2m) * (d²/dx²) = +hbar²/(2m) * (-d²/dx²)
        diagonals = [
            np.ones(self.num_points - 1) * coeff,  # superdiagonal
            np.ones(self.num_points) * (-2.0 * coeff),  # main diagonal
            np.ones(self.num_points - 1) * coeff,  # subdiagonal
        ]
        T = sparse.diags(diagonals, offsets=[1, 0, -1], shape=(self.num_points, self.num_points))
        return T.tocsr()


class StationarySolver:
    """Solves time-independent Schrödinger equation."""

    def __init__(self, grid: QuantumGrid, mass: float = 1.0):
        """
        Initialize stationary solver.

        Args:
            grid: QuantumGrid instance
            mass: Particle mass
        """
        self.grid = grid
        self.mass = mass
        self.T = grid.kinetic_energy_matrix(mass)

    def solve_eigenproblem(
        self, potential: np.ndarray, num_eigenvalues: int = 10, which: str = "SM"
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve -ℏ²/(2m) d²ψ/dx² + V(x)ψ = E ψ.

        Args:
            potential: Potential values on grid (length = num_points)
            num_eigenvalues: Number of lowest eigenvalues to compute
            which: 'SM' for smallest magnitude, 'SA' for smallest algebraic

        Returns:
            eigenvalues: Array of energy eigenvalues
            eigenvectors: Columns are normalized eigenvectors
        """
        # Construct potential matrix (diagonal)
        V = sparse.diags(potential, offsets=0, shape=(self.grid.num_points, self.grid.num_points))

        # Full Hamiltonian: H = T + V
        H = self.T + V

        # Solve eigenvalue problem
        try:
            eigenvalues, eigenvectors = sp_linalg.eigsh(
                H, k=num_eigenvalues, which=which, return_eigenvectors=True
            )
        except sp_linalg.ArpackNoConvergence as e:
            warnings.warn(f"ARPACK did not converge: {e}")
            eigenvalues = e.eigenvalues
            eigenvectors = e.eigenvectors

        # Sort by energy
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Normalize eigenvectors
        for i in range(eigenvectors.shape[1]):
            norm = np.sqrt(np.sum(np.abs(eigenvectors[:, i]) ** 2) * self.grid.dx)
            eigenvectors[:, i] /= norm

        return eigenvalues, eigenvectors

    def probability_density(self, wavefunction: np.ndarray) -> np.ndarray:
        """Compute |ψ|² from wavefunction."""
        return np.abs(wavefunction) ** 2

    def normalize_wavefunction(self, wavefunction: np.ndarray) -> np.ndarray:
        """Normalize wavefunction to unit probability."""
        norm = np.sqrt(np.sum(np.abs(wavefunction) ** 2) * self.grid.dx)
        return wavefunction / norm


class TimeDependentSolver:
    """
    Solves time-dependent Schrödinger equation using Crank-Nicolson scheme.

    i ℏ ∂ψ/∂t = Ĥ ψ
    """

    def __init__(self, grid: QuantumGrid, potential: np.ndarray, mass: float = 1.0, dt: float = 0.01):
        """
        Initialize time-dependent solver.

        Args:
            grid: QuantumGrid instance
            potential: Static potential on grid
            mass: Particle mass
            dt: Time step
        """
        self.grid = grid
        self.potential = potential
        self.mass = mass
        self.dt = dt

        # Build kinetic energy matrix
        self.T = grid.kinetic_energy_matrix(mass)

        # Build potential matrix
        self.V = sparse.diags(potential, offsets=0, shape=(grid.num_points, grid.num_points))

        # Hamiltonian
        self.H = self.T + self.V

        # For Crank-Nicolson: (I + i*H*dt/2) ψ(t+dt) = (I - i*H*dt/2) ψ(t)
        # Rearrange: [I + i*H*dt/2] ψ(t+dt) = [I - i*H*dt/2] ψ(t)
        # In atomic units with ℏ=1:
        self._build_crank_nicolson_matrices()

    def _build_crank_nicolson_matrices(self):
        """Build matrices for Crank-Nicolson scheme."""
        I = sparse.eye(self.grid.num_points, format="csr")
        coeff = 1j * self.dt / 2.0  # ℏ=1 in atomic units

        self.A = I + coeff * self.H  # LHS
        self.B = I - coeff * self.H  # RHS

        # Factorize A for efficient solving
        self.A_lu = sp_linalg.splu(self.A.tocsc())

    def step(self, psi: np.ndarray) -> np.ndarray:
        """
        Advance wavefunction by one time step using Crank-Nicolson.

        Args:
            psi: Current wavefunction (complex array)

        Returns:
            psi_new: Wavefunction at next time step
        """
        rhs = self.B @ psi
        psi_new = self.A_lu.solve(rhs)
        return psi_new

    def evolve(self, psi_init: np.ndarray, num_steps: int) -> np.ndarray:
        """
        Evolve wavefunction for multiple time steps.

        Args:
            psi_init: Initial wavefunction (complex array)
            num_steps: Number of time steps

        Returns:
            psi_trajectory: Array of shape (num_points, num_steps)
        """
        psi = psi_init.copy()
        trajectory = np.zeros((self.grid.num_points, num_steps), dtype=complex)
        trajectory[:, 0] = psi

        for t in range(1, num_steps):
            psi = self.step(psi)
            trajectory[:, t] = psi

        return trajectory


class GaussianWavePacket:
    """Utility to create Gaussian wave packets for tunneling scenarios."""

    @staticmethod
    def create(
        x: np.ndarray,
        x0: float,
        sigma: float,
        k0: float = 0.0,
        amplitude: float = 1.0,
    ) -> np.ndarray:
        """
        Create a Gaussian wave packet.

        ψ(x) = A * exp[-(x - x₀)²/(2σ²)] * exp(i k₀ x)

        Args:
            x: Spatial grid
            x0: Center position
            sigma: Width (standard deviation)
            k0: Wavenumber (momentum = ℏ k₀)
            amplitude: Overall amplitude

        Returns:
            Complex wavefunction
        """
        psi = amplitude * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2)) * np.exp(1j * k0 * x)
        return psi

    @staticmethod
    def normalize(psi: np.ndarray, dx: float) -> np.ndarray:
        """Normalize wavefunction to unit probability."""
        norm = np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
        return psi / norm


def compute_transmission_coefficient(
    psi_transmitted: np.ndarray,
    psi_incident: np.ndarray,
    barrier_region: Tuple[int, int],
    dx: float,
) -> float:
    """
    Estimate transmission coefficient from wave packet dynamics.

    T = |∫ |ψ_transmitted|² dx| / |∫ |ψ_incident|² dx|

    Args:
        psi_transmitted: Transmitted part of wavefunction
        psi_incident: Incident (initial) wavefunction
        barrier_region: Tuple (i_start, i_end) of barrier indices
        dx: Grid spacing

    Returns:
        Transmission probability (0 to 1)
    """
    i_start, i_end = barrier_region
    prob_transmitted = np.sum(np.abs(psi_transmitted[i_end:]) ** 2) * dx
    prob_incident = np.sum(np.abs(psi_incident) ** 2) * dx

    T = prob_transmitted / (prob_incident + 1e-10)
    return np.clip(T, 0.0, 1.0)


def compute_reflection_coefficient(psi: np.ndarray, barrier_region: Tuple[int, int], dx: float) -> float:
    """
    Estimate reflection coefficient.

    R = 1 - T
    """
    return 1.0 - compute_transmission_coefficient(psi, psi, barrier_region, dx)
