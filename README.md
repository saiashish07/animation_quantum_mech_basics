# Quantum Mechanics Animations with Manim

Beautiful, educational quantum mechanics animations inspired by 3Blue1Brown, created with [Manim](https://www.manim.community/) and [QMsolve](https://github.com/quantum-visualizations/qmsolve).

## 🎬 Quick Start

```bash
# Install dependencies
pip install -e .

# Render all enhanced scenes in parallel (high quality)
python scripts/render_optimized.py --quality h --parallel

# Combine into single video
python scripts/concat_videos.py --quality 1080p60
```

**Output:** `media/complete/QuantumMechanicsComplete_1080p60.mp4` (~2 min 45 sec)

## 📚 Enhanced Topics

| # | Topic | Duration | Key Features |
|---|-------|----------|--------------|
| 1 | **Vectors & Hilbert Space** | ~30s | 3D visualization, basis vectors, quantum states |
| 2 | **Inner Products** | ~25s | Geometric overlap, projections, normalization |
| 3 | **Orthogonality** | ~20s | Independent states, spin examples |
| 4 | **Superposition** | ~25s | Animated coefficients, probability conservation |
| 5 | **Operators & Eigenvalues** | ~30s | Visual transformations, measurement outcomes |
| 6 | **Time Evolution** | ~35s | Spreading wave packets, Schrödinger equation |

**Total: ~2 min 45 sec** of comprehensive quantum mechanics education

## 🚀 Features

- ✅ **3Blue1Brown-inspired** animations with professional pacing
- ✅ **Step-by-step explanations** with title cards and physical interpretations
- ✅ **Parallel rendering** (3-4x faster with multi-core CPUs)
- ✅ **Automatic concatenation** into single output video
- ✅ **Quality presets** from 480p15 to 1440p60

## Project Goals
- Visualize the bridge from classical vectors to Hilbert spaces and wavefunctions
- Demonstrate inner products, normalization, and orthogonality geometrically
- Animate basis states, superposition, and measurement via operators and eigenvalues
- Show simple wavefunction evolution driven by the time-dependent Schrödinger equation

## 📁 Repository Layout
```
src/quantum_animation/
├── scenes/
│   ├── 01_vectors_hilbert.py      # Enhanced: Vector basics & Hilbert space
│   ├── 02_inner_product.py        # Enhanced: Inner products & overlap
│   ├── 03_orthogonality.py        # Enhanced: Orthogonal states
│   ├── 04_superposition.py        # Enhanced: Superposition principle
│   ├── 05_operators.py            # Enhanced: Operators & eigenvalues
│   ├── 06_evolution.py            # Enhanced: Time evolution
│   ├── vectors_hilbert.py         # Original: Basic vector demo
│   ├── inner_product.py           # Original: Basic inner product
│   └── ...                        # Other original scenes
├── simulations/                   # QMsolve-powered explorations
├── utils/                         # Shared helpers (vectors, quantum)
├── config.py                      # Theme configuration
scripts/
├── render_optimized.py            # Parallel batch renderer
├── concat_videos.py               # Video concatenation tool
└── render_all.py                  # Original sequential renderer
media/                             # Output directory (auto-generated)
├── complete/                      # Combined videos
└── videos/                        # Individual scene renders
pyproject.toml                     # Package configuration
README.md                          # This file
```

## 🛠️ Getting Started

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config ffmpeg
```

**macOS:**
```bash
brew install cairo pango ffmpeg
```

### 2. Install Python Package

```bash
# Install in editable mode
pip install -e .

# Optional: Install visualization and quantum simulation tools
pip install -e ".[visualization,quantum]"
```

The `visualization` group installs Matplotlib/VPython helpers, while the `quantum` group brings in QuTiP and QMsolve for physics-driven simulations.

### 3. Test Single Scene

```bash
# Quick preview at low quality
manim -pql src/quantum_animation/scenes/01_vectors_hilbert.py VectorBasicsScene

# High quality render
manim -pqh src/quantum_animation/scenes/01_vectors_hilbert.py VectorBasicsScene
```

### 4. Render All Enhanced Scenes

```bash
# Parallel rendering at high quality (recommended)
python scripts/render_optimized.py --quality h --parallel

# Sequential rendering (more stable on some systems)
python scripts/render_optimized.py --quality h --all
```

### 5. Combine into Single Video

```bash
python scripts/concat_videos.py --quality 1080p60
```

**Output:** `media/complete/QuantumMechanicsComplete_1080p60.mp4`

## 🎨 Quality Presets

| Flag | Resolution | FPS | Render Time* | Use Case |
|------|------------|-----|--------------|----------|
| `l` | 480p | 15 | ~2 min | Quick preview |
| `m` | 720p | 30 | ~5 min | Testing |
| `h` | 1080p | 60 | ~15 min | **Production** |
| `p` | 1440p | 60 | ~30 min | High-end |

*Approximate time for all 6 scenes with parallel rendering

## 📖 Documentation

- **[COMPLETE_WORKFLOW.md](COMPLETE_WORKFLOW.md)** - Detailed step-by-step guide, troubleshooting
- **[ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)** - Before/after comparison, metrics
- **[QUICKSTART.md](QUICKSTART.md)** - Original quick reference (basic scenes)
- **[FIXES_SUMMARY.md](FIXES_SUMMARY.md)** - Error resolution history

## 🎯 Usage Examples

### Render Specific Scene
```bash
# Original basic scenes
manim -pqh src/quantum_animation/scenes/vectors_hilbert.py VectorBasicsScene

# Enhanced scenes with explanations
manim -pqh src/quantum_animation/scenes/01_vectors_hilbert.py VectorBasicsScene
```

### Batch Rendering Options
```bash
# All scenes, parallel, high quality
python scripts/render_optimized.py --quality h --parallel

# Medium quality for faster preview
python scripts/render_optimized.py --quality m --parallel

# Disable cache (force fresh render)
python scripts/render_optimized.py --quality h --parallel --no-cache
```

### Video Concatenation
```bash
# Standard concatenation
python scripts/concat_videos.py --quality 1080p60

# Custom output filename
python scripts/concat_videos.py --quality 1080p60 --output MyQuantumVideo.mp4
```

## 🎓 Educational Use

These animations are designed for:
- **University courses** (quantum mechanics intro)
- **YouTube educational content** (3Blue1Brown style)
- **Conference presentations** (clear visualizations)
- **Self-study materials** (comprehensive explanations)

## Suggested Workflow
- Tweak visual parameters in `config.py` for consistent styling
- Reuse helpers from `quantum_animation.utils` to keep scenes concise
- Test individual scenes before batch rendering
- Use parallel rendering for production-quality output

## 🔬 QMsolve Quick Start
Run the harmonic-oscillator helper to explore eigenstates and superpositions:
```bash
python -m quantum_animation.simulations.harmonic_superpositions
```
A Matplotlib UI appears with sliders for mixing the lowest eigenstates via `visualization.superpositions`, matching the QMsolve examples. Adjust `HarmonicSimulationConfig` (grid size, extent, max_states) to mirror the official `examples/1D_harmonic_oscillator*.py` scripts or to prep data for Manim scenes.

## 🐛 Troubleshooting

### "No module named 'quantum_animation'"
```bash
pip install -e .
```

### "ffmpeg not found"
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg          # macOS
```

### LaTeX compilation errors
The enhanced scenes use standard LaTeX notation. If you still encounter errors:
```bash
sudo apt-get install texlive-full  # Large download
```

### Slow rendering
- Use lower quality: `--quality l`
- Enable parallel rendering: `--parallel`
- Ensure caching is enabled (default)

See [COMPLETE_WORKFLOW.md](COMPLETE_WORKFLOW.md#troubleshooting) for detailed solutions.

## 🤝 Contributing

Contributions welcome! Ideas:
- Add more quantum topics (entanglement, measurement, decoherence)
- Improve animations (smoother transitions, better visuals)
- Create interactive Jupyter notebooks
- Enhance documentation

## 🙏 Acknowledgments

- **[Manim Community](https://www.manim.community/)** - Animation framework
- **[QMsolve](https://github.com/quantum-visualizations/qmsolve)** - Quantum simulations
- **[3Blue1Brown](https://www.3blue1brown.com/)** - Educational style inspiration

## 📚 Resources

- **Manim Docs:** https://docs.manim.community/
- **Quantum Textbooks:**
  - Griffiths, *Introduction to Quantum Mechanics*
  - Sakurai, *Modern Quantum Mechanics*
  - Nielsen & Chuang, *Quantum Computation and Quantum Information*

---

**Start creating beautiful quantum animations! 🎬✨**

```bash
# Full workflow: render and combine
python scripts/render_optimized.py --quality h --parallel && \
python scripts/concat_videos.py --quality 1080p60
```
