"""Utility routines for small quantum systems used in animations."""

from __future__ import annotations

import numpy as np

PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
IDENTITY_2 = np.eye(2, dtype=complex)


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if np.isclose(norm, 0.0):
        raise ValueError("Cannot normalize the zero state.")
    return state / norm


def bloch_angles(state: np.ndarray) -> tuple[float, float]:
    state = normalize(state)
    alpha = np.angle(state[0])
    relative = state[1] * np.exp(-1.0j * alpha)
    theta = 2.0 * np.arctan2(np.abs(relative), 1.0)
    phi = np.angle(relative)
    return float(theta), float(phi)


def time_evolution(hamiltonian: np.ndarray, state: np.ndarray, times: np.ndarray) -> np.ndarray:
    evals, evecs = np.linalg.eigh(hamiltonian)
    coeffs = np.dot(np.conj(evecs.T), state)
    phases = np.exp(-1.0j * np.outer(evals, times))
    evolved = np.dot(evecs, coeffs[:, None] * phases)
    return evolved


def qubit_rotation(axis: str, angle: float) -> np.ndarray:
    axis_map = {
        "x": PAULI_X,
        "y": PAULI_Y,
        "z": PAULI_Z,
    }
    if axis.lower() not in axis_map:
        raise ValueError("Axis must be x, y, or z.")
    pauli = axis_map[axis.lower()]
    return np.cos(angle / 2.0) * IDENTITY_2 - 1.0j * np.sin(angle / 2.0) * pauli
