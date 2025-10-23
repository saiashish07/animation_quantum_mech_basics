# 🎓 Quantum Mechanics Animation Pipeline

> Interactive Simulations | Professional Animations | 4K Videos | GitHub Pages

**Status**: ✅ Production Ready (80% complete)

## 🚀 Quick Start

### Interactive Simulator (5 minutes)
```bash
pip install jupyter numpy scipy matplotlib ipywidgets
jupyter lab Interactive_Quantum_Controls.ipynb
```

### Full Pipeline (10 minutes)
```bash
bash build_quantum_animations.sh
```

### Render Animations (20+ minutes)
```bash
pip install manim
manim -qh src/manim_quantum.py HarmonicOscillatorScene
```

## ✨ Features
- 🎮 **Interactive Simulations**: Real-time quantum mechanics exploration
- 🎬 **Professional Animations**: 4K Manim animations
- 🎥 **Video Processing**: H.265 encoding, optimized GIFs
- 🌐 **Web Ready**: GitHub Pages deployment
- 🎨 **Figma Integration**: Design-to-code UI

## 📚 Documentation

See **[COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)** for complete documentation including:
- Installation & setup
- Running animations
- GitHub Pages deployment
- Figma integration
- Troubleshooting

## 🎯 Project Structure

```
├── Interactive_Quantum_Controls.ipynb  ← Interactive simulator
├── src/
│   ├── manim_quantum.py               ← Animation framework
│   ├── ffmpeg_pipeline.py             ← Video encoder
│   └── quantum_playground/            ← Core solvers
├── scripts/
│   ├── deploy_github_pages.sh         ← Deploy to GitHub Pages
│   └── figma_connector.py             ← Figma integration
├── docs/                              ← GitHub Pages site
└── COMPREHENSIVE_README.md            ← All documentation
```

## 🌐 Live Demo
Visit: [https://your-username.github.io/animation_quantum_mech_basics](https://your-username.github.io/animation_quantum_mech_basics)

## 📊 What's Included

| Component | Status |
|-----------|--------|
| Interactive Notebook | ✅ Complete |
| Manim Framework | ✅ Complete |
| FFmpeg Pipeline | ✅ Complete |
| Build System | ✅ Complete |
| GitHub Pages | ✅ Ready |
| Figma Integration | ⏳ Optional |
| C++ Solver | ⏳ Optional |

## 🔧 System Requirements
- Python 3.12+
- 8 GB RAM
- 5 GB disk space
- Ubuntu 20.04+ or equivalent

## 📝 Quick Commands

```bash
# Open notebook
jupyter lab Interactive_Quantum_Controls.ipynb

# Validate system
bash build_quantum_animations.sh

# Render animation (low quality)
manim -ql src/manim_quantum.py HarmonicOscillatorScene

# Deploy to GitHub Pages
bash scripts/deploy_github_pages.sh
```

## 📖 Learn More

See **COMPREHENSIVE_README.md** for:
- Detailed setup instructions
- Animation rendering guide
- GitHub Pages deployment
- Figma connection
- Troubleshooting
- Technical details

## 🎓 Educational Focus

Learn about:
- Quantum mechanics (Schrödinger equation)
- Numerical methods (FDM, eigenvalue problems)
- Scientific visualization
- Professional animations
- Video encoding
- Web deployment

## 📄 License

Educational project. Feel free to use and modify.

---

**Questions?** Check [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md) or create an issue!
