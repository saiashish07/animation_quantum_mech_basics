"""
Potential Energy Functions for Quantum Systems

Provides factory functions and classes for defining potential energy profiles
used in various quantum mechanical systems.
"""

import numpy as np
from typing import Tuple, Callable


class Potential:
    """Base class for potential energy functions."""
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Evaluate potential at positions x."""
        raise NotImplementedError
    
    def name(self) -> str:
        """Return a descriptive name for the potential."""
        raise NotImplementedError


class InfiniteSquareWell(Potential):
    """
    Infinite Potential Well (Particle in a Box)
    
    Potential is 0 inside the well [-L/2, L/2] and infinite outside.
    Boundary conditions: ψ(-L/2) = ψ(L/2) = 0
    Analytical solution: E_n = (n²π²ħ²)/(2mL²), n = 1,2,3,...
    """
    
    def __init__(self, width: float):
        """
        Args:
            width: Width of the well (L)
        """
        self.width = width
        self.left = -width / 2
        self.right = width / 2
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Return 0 inside the well, large value outside."""
        V = np.zeros_like(x, dtype=float)
        V[(x < self.left) | (x > self.right)] = 1e10  # Effectively infinite
        return V
    
    def name(self) -> str:
        return f"Infinite Square Well (L={self.width})"


class FiniteSquareWell(Potential):
    """
    Finite Potential Well
    
    Potential is 0 inside [-L/2, L/2] and V0 outside.
    Allows bound states with wavefunction penetration (evanescent tails).
    Bound states satisfy transcendental equations.
    """
    
    def __init__(self, width: float, height: float):
        """
        Args:
            width: Width of the well (L)
            height: Potential height outside the well (V0)
        """
        self.width = width
        self.height = height
        self.left = -width / 2
        self.right = width / 2
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Return 0 inside the well, V0 outside."""
        V = np.full_like(x, self.height, dtype=float)
        mask = (x >= self.left) & (x <= self.right)
        V[mask] = 0
        return V
    
    def name(self) -> str:
        return f"Finite Square Well (L={self.width}, V0={self.height})"


class RectangularBarrier(Potential):
    """
    Rectangular Potential Barrier
    
    Potential is 0 everywhere except in region [x_center - width/2, x_center + width/2]
    where it is V0. Used for studying quantum tunneling.
    """
    
    def __init__(self, height: float, width: float, center: float = 0.0):
        """
        Args:
            height: Barrier height (V0)
            width: Barrier width
            center: Center position of the barrier
        """
        self.height = height
        self.width = width
        self.center = center
        self.left = center - width / 2
        self.right = center + width / 2
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Return V0 inside the barrier, 0 outside."""
        V = np.zeros_like(x, dtype=float)
        mask = (x >= self.left) & (x <= self.right)
        V[mask] = self.height
        return V
    
    def name(self) -> str:
        return f"Rectangular Barrier (V0={self.height}, width={self.width})"


class HarmonicOscillator(Potential):
    """
    Quantum Harmonic Oscillator
    
    Parabolic potential: V(x) = (1/2) m ω² x²
    Analytical solutions: E_n = (n + 1/2) ħ ω, ψ_n(x) = H_n(ξ) exp(-ξ²/2)
    where H_n are Hermite polynomials and ξ = sqrt(mω/ħ) x
    """
    
    def __init__(self, mass: float, omega: float):
        """
        Args:
            mass: Particle mass (m)
            omega: Angular frequency (ω)
        """
        self.mass = mass
        self.omega = omega
        # Reduced constants for convenience
        self.spring_constant = mass * omega ** 2  # k = mω²
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Return V(x) = (1/2) m ω² x²"""
        return 0.5 * self.mass * self.omega ** 2 * x ** 2
    
    def name(self) -> str:
        return f"Harmonic Oscillator (m={self.mass}, ω={self.omega})"
    
    @property
    def level_spacing(self) -> float:
        """Energy spacing between levels: ΔE = ħ ω"""
        # Returning ω as a proxy (ħ = 1 in our atomic units)
        return self.omega


class PiecewisePotential(Potential):
    """
    General piecewise potential combining multiple regions.
    """
    
    def __init__(self, regions: list):
        """
        Args:
            regions: List of (left_edge, right_edge, value) tuples
        """
        self.regions = sorted(regions, key=lambda r: r[0])
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Evaluate piecewise potential."""
        V = np.zeros_like(x, dtype=float)
        for left, right, value in self.regions:
            mask = (x >= left) & (x <= right)
            V[mask] = value
        return V
    
    def name(self) -> str:
        return "Piecewise Potential"


class PotentialAnalysis:
    """Utilities for analyzing potentials."""

    @staticmethod
    def estimate_classically_forbidden_region(E: float, V: np.ndarray, x: np.ndarray) -> Tuple:
        """
        Find classically forbidden region where E < V(x).

        Args:
            E: Energy level
            V: Potential array
            x: Spatial grid

        Returns:
            Tuple (x_min, x_max) of forbidden region, or (None, None) if none exists
        """
        forbidden = V > E
        if not np.any(forbidden):
            return None, None

        indices = np.where(forbidden)[0]
        return x[indices[0]], x[indices[-1]]

    @staticmethod
    def tunneling_probability_estimate(E: float, V: np.ndarray, x: np.ndarray) -> float:
        """
        Rough estimate of tunneling probability using WKB approximation.

        T ≈ exp(-2 κ)
        where κ = (1/ħ) ∫ √[2m(V(x) - E)] dx over forbidden region

        Args:
            E: Particle energy
            V: Potential array
            x: Spatial grid

        Returns:
            Estimated transmission coefficient (0 to 1)
        """
        dx = x[1] - x[0]
        forbidden_mask = (V > E) & (V - E > 0)

        if not np.any(forbidden_mask):
            return 1.0  # No barrier to tunnel through

        # κ = ∫ √[2m(V - E)] dx (in atomic units, m=1)
        integrand = np.sqrt(2.0 * np.maximum(0, V - E))
        kappa = np.sum(integrand[forbidden_mask]) * dx

        # WKB: T = exp(-2κ)
        T = np.exp(-2 * kappa)
        return np.clip(T, 0.0, 1.0)
