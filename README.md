# Quantum Mechanics Animation Project

Python project scaffolding for beginner-friendly quantum mechanics animations inspired by 3Blue1Brown. The codebase is organized around modular Manim scenes that illustrate linear algebra concepts used in introductory quantum mechanics.

## Project Goals
- Visualize the bridge from classical vectors to Hilbert spaces and wavefunctions.
- Demonstrate inner products, normalization, and orthogonality geometrically.
- Animate basis states, superposition, and measurement via operators and eigenvalues.
- Show simple wavefunction evolution driven by the time-dependent Schrödinger equation.

## Repository Layout
```
src/quantum_animation/
├── scenes/                 # Manim scenes grouped by concept
├── simulations/            # QMsolve-powered explorations (harmonic oscillator, etc.)
├── utils/                  # Shared helpers for geometry and quantum data
├── __init__.py
├── config.py
scripts/                    # Utility scripts (rendering, data prep)
pyproject.toml              # Project and dependency metadata
README.md                   # Project overview and developer notes
```

## Getting Started
1. **Create a virtual environment** (Python 3.10+ recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -U pip
   pip install .
   ```
   Optional extras:
   ```bash
   pip install .[visualization]
   pip install .[quantum]
   ```
      The `visualization` group installs Matplotlib/VPython helpers, while the
      `quantum` group brings in QuTiP and QMsolve for physics-driven simulations.
3. **Render a scene with Manim**:
   ```bash
   manim -pqh src/quantum_animation/scenes/vectors_hilbert.py VectorBasicsScene
   ```

## Suggested Workflow
- Tweak numerical parameters in `config.py` to keep a consistent visual style.
- Reuse helpers from `quantum_animation.utils` to keep scenes concise.
- Test each scene individually before batching renders with `scripts/render_all.py`.
- Use the `quantum` optional dependency group when experimenting with QuTiP or QMsolve driven animations.

## QMsolve Quick Start
- Run the harmonic-oscillator helper to explore eigenstates and superpositions:
   ```bash
   python -m quantum_animation.simulations.harmonic_superpositions
   ```
- A Matplotlib UI appears with sliders for mixing the lowest eigenstates via
   `visualization.superpositions`, matching the QMsolve examples.
- Adjust `HarmonicSimulationConfig` (grid size, extent, max_states) to mirror the
   official `examples/1D_harmonic_oscillator*.py` scripts or to prep data for Manim scenes.

## Next Steps
- Draft narration or on-screen text tied to each scene.
- Expand interactive notebooks (e.g., Jupyter) for audience experiments.
- Integrate exported videos into a final voiceover or slideshow.
