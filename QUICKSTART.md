# Quantum Mechanics Animation Project - Quick Start Guide

## ✅ Project Status

All rendering issues have been **FIXED**! All 6 scenes render successfully.

## 🚀 Rendering All Animations

### Batch Render All Topics
```bash
python scripts/render_all.py --quality h
```

### Render Individual Topics
```bash
python scripts/render_all.py vectors --quality m
python scripts/render_all.py inner_product --quality m
python scripts/render_all.py orthogonality --quality m
python scripts/render_all.py superposition --quality m
python scripts/render_all.py operators --quality m
python scripts/render_all.py evolution --quality m
```

**Quality options:**
- `l` = low (480p15) - fast preview
- `m` = medium (720p30) - good quality
- `h` = high (1080p60) - presentation quality
- `p` = production (1440p60) - final export

**Add `--preview` to auto-open videos after rendering.**

## 📹 Output Locations

Videos are saved to:
```
media/videos/
├── vectors_hilbert/
├── inner_product/
├── orthogonality/
├── basis_superposition/
├── operators_eigenvalues/
└── wavefunction_evolution/
```

## 🎯 Topics Covered

| Scene | Duration | Description |
|-------|----------|-------------|
| **VectorBasicsScene** | ~10s | Vectors as quantum states, Hilbert space introduction |
| **InnerProductScene** | ~10s | Inner products, projections, normalization |
| **OrthogonalityScene** | ~8s | Orthogonal states, zero overlap visualization |
| **SuperpositionScene** | ~8s | Basis states and dynamic superposition |
| **OperatorMeasurementScene** | ~8s | Matrix operators and eigenvalue extraction |
| **WavefunctionEvolutionScene** | ~9s | Time evolution via Schrödinger equation |

**Total runtime: ~53 seconds** (add narration/pauses for 10-15 minute presentation)

## 🔬 QMsolve Interactive Visualizations

### Install quantum extras (if not already):
```bash
pip install .[quantum]
```

### Launch harmonic oscillator demo:
```bash
python -m quantum_animation.simulations.harmonic_superpositions
```

This opens an interactive Matplotlib window with:
- Slider to browse eigenstates
- Circular widgets to control superposition coefficients
- Real-time wavefunction animation

### From Python/Jupyter:
```python
from quantum_animation import solve_eigenstates, visualize_eigenstates

# Compute first 5 eigenstates
eigenstates = solve_eigenstates()

# Launch interactive viewer
visualize_eigenstates(eigenstates, states=5)
```

## 🛠️ What Was Fixed

1. **Dataclass mutable defaults** → Converted Manim color objects to hex strings
2. **LaTeX undefined control sequences** → Replaced `\ket{}` with `|ket\rangle`
3. **Indentation errors** → Corrected spacing in vector scene
4. **Import errors** → Added missing constants (RIGHT, UP, DOWN, ORIGIN)
5. **System dependencies** → Ensured libcairo2, libpango installed for manimpango

## 📝 Next Steps

1. **Add narration:**
   - Write voiceover scripts for each scene
   - Use tools like manim-voiceover or record separately

2. **Extend animations:**
   - Increase wait times for key concepts
   - Add text annotations/equations
   - Create transitions between scenes

3. **Integrate QMsolve data:**
   - Export eigenstates from QMsolve
   - Feed into Manim for physics-accurate wavefunctions
   - Animate double-slit, fermions, hydrogen atom examples

4. **Final assembly:**
   - Concatenate videos with ffmpeg
   - Add background music
   - Export to YouTube/presentation format

## 🎨 Customization

Edit `src/quantum_animation/config.py` to change colors:
```python
@dataclass(frozen=True)
class ThemeConfig:
    background_color: str = "#0f172a"      # Dark blue
    vector_color: str = TEAL_E.to_hex()    # Teal arrows
    highlight_color: str = ORANGE.to_hex() # Orange emphasis
    # ...
```

## 📚 Resources

- **Manim docs:** https://docs.manim.community/
- **QMsolve examples:** https://github.com/quantum-visualizations/qmsolve
- **3Blue1Brown source:** https://github.com/3b1b/manim

---

**All systems operational! Ready to render your quantum mechanics animations.** 🎬✨
