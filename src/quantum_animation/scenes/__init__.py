"""Collection of Manim scenes for the quantum animation project."""

from .vectors_hilbert import VectorBasicsScene
from .inner_product import InnerProductScene
from .orthogonality import OrthogonalityScene
from .basis_superposition import SuperpositionScene
from .operators_eigenvalues import OperatorMeasurementScene
from .wavefunction_evolution import WavefunctionEvolutionScene

__all__ = [
    "VectorBasicsScene",
    "InnerProductScene",
    "OrthogonalityScene",
    "SuperpositionScene",
    "OperatorMeasurementScene",
    "WavefunctionEvolutionScene",
]
