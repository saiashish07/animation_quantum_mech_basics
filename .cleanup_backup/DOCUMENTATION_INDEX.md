# Documentation Index

Quick navigation guide for all documentation and source files in the quantum mechanics simulation suite.

## 📖 Main Documentation

### For First-Time Users
1. **START HERE**: [QUICKSTART.md](QUICKSTART.md)
   - Installation (5 minutes)
   - Running simulations (3 commands)
   - Troubleshooting common issues
   - Output file guide

### For Instructors
2. **TEACHING_GUIDE.md** (Comprehensive)
   - Mathematical background for each system
   - Classroom discussion points
   - Exam questions with solutions
   - Real-world application examples
   - Suggested lesson sequences
   - Assessment rubrics

### For Full Understanding
3. **README.md** (Complete Reference)
   - Feature overview
   - Mathematical frameworks (with LaTeX)
   - Installation with all options
   - Full API documentation
   - Physics references
   - Extension ideas

### Project Information
4. **PROJECT_SUMMARY.md** (Overview)
   - What was built
   - File structure
   - Technologies used
   - Performance characteristics
   - Quality assurance
   - Comparison with alternatives

---

## 🎯 Quick Reference

### Run Commands

```bash
# All simulations
python -m quantum_playground all

# Individual scenarios
python -m quantum_playground infinite      # Particle in a box
python -m quantum_playground finite        # Finite barrier
python -m quantum_playground harmonic      # Harmonic oscillator
python -m quantum_playground tunneling     # Tunneling demo

# Options
python -m quantum_playground all --no-animation    # Plots only
python -m quantum_playground all --output ~/Desktop/output
```

### Python API Quick Start

```python
# Infinite Well
from quantum_playground.animations import InfiniteWellSimulation
sim = InfiniteWellSimulation(well_width=2.0, num_levels=8)
sim.plot_overview(save_path="well.png")
sim.animate_eigenstates(save_path="well.mp4")

# Finite Well
from quantum_playground.animations import FiniteWellSimulation
sim = FiniteWellSimulation(well_width=2.0, barrier_height=10.0)
sim.plot_comparison(save_path="comparison.png")
sim.animate_state_with_penetration(save_path="animation.mp4")

# Harmonic Oscillator
from quantum_playground.animations import HarmonicOscillatorSimulation
sim = HarmonicOscillatorSimulation(mass=1.0, omega=1.0)
sim.plot_overview(save_path="sho.png")
sim.animate_superposition(save_path="packet.mp4")

# Quantum Tunneling
from quantum_playground.animations import TunnelingSimulation
sim = TunnelingSimulation(barrier_height=5.0, barrier_width=0.5)
trajectory = sim.run_evolution(num_steps=800)
sim.plot_transmission_analysis(trajectory, save_path="tunneling.png")
sim.animate_tunneling(trajectory, save_path="tunneling.mp4")
```

---

## 📁 Source Code Guide

### Core Modules

**`src/quantum_playground/solvers.py`** (450 lines)
- `QuantumGrid`: Spatial discretization management
- `StationarySolver`: Time-independent Schrödinger
- `TimeDependentSolver`: Crank-Nicolson evolution
- `GaussianWavePacket`: Wave packet utilities
- Helper functions for transmission coefficients

[Read about solvers](README.md#core-modules)

**`src/quantum_playground/potentials.py`** (250 lines)
- `InfiniteSquareWell`: Particle in a box
- `FiniteSquareWell`: Finite barrier
- `HarmonicOscillator`: SHO potential
- `RectangularBarrier`: Tunneling barrier
- `PotentialAnalysis`: WKB and tunneling utilities

[Read about potentials](README.md#core-modules)

### Animation Scripts

**`src/quantum_playground/animations/infinite_well.py`** (300 lines)
- `InfiniteWellSimulation` class
- Energy level diagram generation
- Eigenstate visualization
- Analytic verification

[Usage example in TEACHING_GUIDE.md](#1-infinite-potential-well-particle-in-a-box)

**`src/quantum_playground/animations/finite_well.py`** (350 lines)
- `FiniteWellSimulation` class
- Finite vs infinite comparison
- Evanescent tail analysis
- Penetration depth visualization

[Usage example in TEACHING_GUIDE.md](#2-finite-potential-well)

**`src/quantum_playground/animations/harmonic_oscillator.py`** (400 lines)
- `HarmonicOscillatorSimulation` class
- Hermite polynomial eigenfunctions
- Classical vs quantum probability
- Coherent superposition animation

[Usage example in TEACHING_GUIDE.md](#3-quantum-harmonic-oscillator)

**`src/quantum_playground/animations/tunneling.py`** (500 lines)
- `TunnelingSimulation` class
- Wave packet dynamics
- WKB approximation comparison
- Space-time visualization
- Transmission coefficient analysis

[Usage example in TEACHING_GUIDE.md](#4-quantum-tunneling)

### Support Files

**`src/quantum_playground/__main__.py`** (200 lines)
- CLI interface
- Argument parsing
- Simulation runners
- Output management

**`src/quantum_playground/__init__.py`** (40 lines)
- Package exports
- Version info
- Quick API reference

**`tests/test_core.py`** (200 lines)
- Unit tests
- Eigenvalue verification
- Normalization checks
- Orthogonality tests

Run tests: `python tests/test_core.py`

---

## 🔧 Configuration Files

**`pyproject.toml`**
- Modern Python packaging (PEP 517/518)
- Dependency specifications
- Build system configuration
- Tool configurations (Black, Ruff)

**`requirements.txt`**
- Simple pip installation
- Core dependencies
- Optional performance packages
- Development tools

**`.gitignore`** (if using git)
- Exclude venv/
- Exclude outputs/ (generated files)
- Exclude __pycache__
- IDE files (.vscode, .idea)

---

## 📊 Output Files

After running simulations, outputs are organized in `outputs/`:

### Overview Plots (PNG, 150 DPI)
- `infinite_well_overview.png`
  - Energy levels
  - Eigenstates overlaid
  - Analytical comparison
  - Phase information

- `finite_well_comparison.png`
  - Finite vs infinite comparison
  - Evanescent tails (log scale)
  - Penetration depths
  - Energy shift analysis

- `harmonic_oscillator_overview.png`
  - Potential and eigenstates
  - Energy spacing
  - Classical vs quantum probability
  - Uncertainty product verification

- `tunneling_analysis.png`
  - Barrier potential
  - WKB vs numerical T
  - Initial and final wavefunctions
  - Space-time evolution heatmap
  - Transmission probability breakdown

### Animations (MP4, H.264)
- `infinite_well_animation.mp4` (2:30)
  - Eigenstate probability oscillations
  - Multiple states simultaneously

- `finite_well_animation.mp4` (2:30)
  - Evanescent tail visualization
  - Linear and log scale views

- `harmonic_oscillator_animation.mp4` (3:00)
  - Wavefunction, probability, phase
  - Energy decomposition
  - Wave packet breathing

- `tunneling_animation.mp4` (3:00)
  - Wave packet approaching barrier
  - Real and imaginary parts
  - Probability tracking
  - Cumulative transmission

---

## 🎓 Learning Path

### Path 1: Visual Learner (Start with Animations)
1. Run `python -m quantum_playground all`
2. Watch MP4 files in outputs/
3. Read TEACHING_GUIDE.md explanations
4. Study corresponding sections in README.md

### Path 2: Theory-First (Start with Math)
1. Read TEACHING_GUIDE.md for each system
2. Study equations in README.md
3. Run corresponding simulation
4. Compare numerical results with analytical

### Path 3: Hands-On Coder (Start with Python)
1. Read QUICKSTART.md
2. Install and run simulations
3. Modify Python scripts (change parameters)
4. Read code comments and docstrings
5. Implement your own modifications

### Path 4: Instructor Prep (Start with Teaching)
1. Read TEACHING_GUIDE.md completely
2. Review suggested lesson sequences
3. Generate outputs for your parameters
4. Check exam questions
5. Prepare classroom discussion points
6. Embed animations in slides

---

## 🔍 Finding What You Need

### "How do I run this?"
→ [QUICKSTART.md](QUICKSTART.md)

### "What does tunneling mean?"
→ [TEACHING_GUIDE.md - Quantum Tunneling section](TEACHING_GUIDE.md#4-quantum-tunneling)

### "What are the equations?"
→ [README.md - Mathematical Framework](README.md#mathematical-framework)

### "How do I modify parameters?"
→ [QUICKSTART.md - Customization Examples](QUICKSTART.md#customization-examples)

### "How does the solver work?"
→ [README.md - Core Modules](README.md#core-modules)

### "What's the technical status?"
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### "Can I use this in my presentation?"
→ [QUICKSTART.md - Using in Presentations](QUICKSTART.md#using-in-presentations)

### "What should I teach my class?"
→ [TEACHING_GUIDE.md - Suggested Lesson Sequences](TEACHING_GUIDE.md#5-suggested-lesson-sequences)

### "Are the results correct?"
→ [README.md - Verification](README.md#testing--validation)

### "What if something breaks?"
→ [QUICKSTART.md - Troubleshooting](QUICKSTART.md#troubleshooting)

### "How do I extend this?"
→ [README.md - Extension Ideas](README.md#extension-ideas)

---

## 📚 Additional Resources

### Recommended Textbooks
- Griffiths, D.J. - "Introduction to Quantum Mechanics" (3rd ed.)
- Shankar, R. - "Principles of Quantum Mechanics"
- Tannor, D.J. - "Introduction to Quantum Mechanics: A Time-Dependent Perspective"

See full references in [README.md](README.md#references)

### Online Resources
- WKB Approximation: [Wikipedia](https://en.wikipedia.org/wiki/WKB_approximation)
- Tunneling Physics: [Physics Stack Exchange](https://physics.stackexchange.com)
- Quantum Mechanics: [Stanford Encyclopedia](https://plato.stanford.edu)

### Related Projects
- QuantumBehavior (2D visualization)
- qutip (general quantum computing)
- Pyquil (quantum programming)

---

## 🚀 Getting Started (TL;DR)

```bash
# 1. Clone and setup
git clone <repo>
cd animation_quantum_mech_basics
python -m venv venv
source venv/bin/activate
pip install -e .

# 2. Run simulations
python -m quantum_playground all

# 3. Find outputs
ls outputs/  # See PNG and MP4 files

# 4. Read documentation
# For teaching: TEACHING_GUIDE.md
# For technical: README.md
# For setup help: QUICKSTART.md
```

**Estimated time: 10 minutes from clone to first animation**

---

## 📞 Support

- **Setup issues**: See [QUICKSTART.md - Troubleshooting](QUICKSTART.md#troubleshooting)
- **Teaching questions**: See [TEACHING_GUIDE.md](TEACHING_GUIDE.md)
- **Technical details**: See [README.md](README.md)
- **API usage**: See docstrings in source code or README API section
- **Custom modifications**: All code is well-commented and extensible

---

## 📝 File Organization Summary

```
ROOT/
├── Documentation/
│   ├── README.md                 ← Full technical reference
│   ├── QUICKSTART.md            ← Setup & basic usage
│   ├── TEACHING_GUIDE.md        ← Lecture notes & exam Qs
│   └── PROJECT_SUMMARY.md       ← Project overview
│
├── Source Code/
│   └── src/quantum_playground/
│       ├── solvers.py           ← Core algorithms
│       ├── potentials.py        ← Potential classes
│       ├── __main__.py          ← CLI interface
│       └── animations/
│           ├── infinite_well.py
│           ├── finite_well.py
│           ├── harmonic_oscillator.py
│           └── tunneling.py
│
├── Configuration/
│   ├── pyproject.toml
│   └── requirements.txt
│
├── Testing/
│   └── tests/test_core.py
│
└── Outputs/ (generated)
    ├── *.png                    ← Plots
    └── *.mp4                    ← Animations
```

---

**Last Updated**: October 2025  
**Status**: ✅ Complete and Ready for Use  
**Version**: 0.1.0

🎓 Happy Learning! ⚛️
