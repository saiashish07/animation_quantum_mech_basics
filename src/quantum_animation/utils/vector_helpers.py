"""Helpers for constructing labeled vectors and projections in Manim scenes."""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
from manim import Arrow, MathTex, ORIGIN, RIGHT, UP, VGroup

from quantum_animation.config import THEME


def create_labeled_vector(direction: Iterable[float], label: str, **arrow_kwargs) -> VGroup:
    vector = Arrow(ORIGIN, direction, buff=0.05, color=THEME.vector_color, **arrow_kwargs)
    label_mob = MathTex(label, color=THEME.text_color)
    label_mob.next_to(vector.get_end(), RIGHT + UP, buff=0.1)
    return VGroup(vector, label_mob)


def projection_length(a: Iterable[float], b: Iterable[float]) -> float:
    a_vec = np.array(a, dtype=float)
    b_vec = np.array(b, dtype=float)
    denom = np.dot(b_vec, b_vec)
    if np.isclose(denom, 0.0):
        raise ValueError("Cannot project onto the zero vector.")
    return float(np.dot(a_vec, b_vec) / denom)


def decompose_in_basis(vector: Iterable[float], basis: Tuple[Iterable[float], Iterable[float]]) -> Tuple[float, float]:
    mat = np.column_stack([basis[0], basis[1]])
    coeffs = np.linalg.solve(mat, np.array(vector, dtype=float))
    return float(coeffs[0]), float(coeffs[1])
