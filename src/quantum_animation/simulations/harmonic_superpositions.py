"""Utilities for exploring 1D harmonic oscillator eigenstates with QMsolve."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

try:
    from qmsolve import Hamiltonian, SingleParticle, visualization
except ImportError as exc:  # pragma: no cover - informative guard
    raise ImportError(
        "QMsolve is not installed. Install optional dependencies with 'pip install .[quantum]'"
    ) from exc


def _harmonic_potential(particle) -> Iterable[float]:
    return 0.5 * particle.x**2


@dataclass
class HarmonicSimulationConfig:
    grid_size: int = 256
    extent: float = 12.0
    mass: float = 1.0
    max_states: int = 6


def build_hamiltonian(config: HarmonicSimulationConfig | None = None) -> Hamiltonian:
    config = config or HarmonicSimulationConfig()
    return Hamiltonian(
        particles=SingleParticle(m=config.mass),
        potential=_harmonic_potential,
        N=config.grid_size,
        extent=config.extent,
        spatial_ndim=1,
    )


def solve_eigenstates(config: HarmonicSimulationConfig | None = None):
    config = config or HarmonicSimulationConfig()
    hamiltonian = build_hamiltonian(config)
    eigenstates = hamiltonian.solve(max_states=config.max_states)
    return eigenstates


def visualize_eigenstates(eigenstates=None, *, show_superposition: bool = True,
                           states: int | Sequence[int] = 3):
    eigenstates = eigenstates or solve_eigenstates()
    viz = visualization.init_visualization(eigenstates)
    viz.slider_plot()
    if show_superposition:
        viz.superpositions(states)


__all__ = [
    "HarmonicSimulationConfig",
    "build_hamiltonian",
    "solve_eigenstates",
    "visualize_eigenstates",
]


if __name__ == "__main__":  # pragma: no cover - manual entry point
    visualize_eigenstates()
