#!/bin/bash
# Deploy Quantum Mechanics Animation Pipeline to GitHub Pages
# This script creates the docs/ folder structure and deploys to GitHub Pages

set -e

PROJECT_ROOT=$(pwd)
DOCS_DIR="$PROJECT_ROOT/docs"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  GITHUB PAGES DEPLOYMENT SETUP                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Create docs directory structure
echo "▶ Creating docs directory structure..."
mkdir -p "$DOCS_DIR"/{assets,components,animations}
echo "✓ Directories created"

# Create index.html
echo "▶ Creating index.html..."
cat > "$DOCS_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Quantum Mechanics Interactive Simulator with Professional Animations">
    <title>Quantum Mechanics Animation Pipeline</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <h1 class="logo">🎓 Quantum Mechanics</h1>
            <ul class="nav-menu">
                <li><a href="#features">Features</a></li>
                <li><a href="#animations">Animations</a></li>
                <li><a href="#simulator">Simulator</a></li>
                <li><a href="#docs">Documentation</a></li>
                <li><a href="https://github.com/saiashish07/animation_quantum_mech_basics" target="_blank">GitHub</a></li>
            </ul>
        </div>
    </nav>

    <header class="hero">
        <div class="hero-content">
            <h1>Quantum Mechanics Animation Pipeline</h1>
            <p>Interactive simulations • Professional animations • 4K videos</p>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="scrollToSection('simulator')">Try Simulator</button>
                <button class="btn btn-secondary" onclick="scrollToSection('animations')">View Animations</button>
            </div>
        </div>
    </header>

    <!-- Features Section -->
    <section id="features" class="features">
        <h2>Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🎮 Interactive Simulator</h3>
                <p>Real-time quantum simulations with adjustable parameters</p>
            </div>
            <div class="feature-card">
                <h3>🎬 Professional Animations</h3>
                <p>4K mathematical animations via Manim framework</p>
            </div>
            <div class="feature-card">
                <h3>🎥 High-Quality Video</h3>
                <p>H.265 codec, 4K@60fps, optimized for web</p>
            </div>
            <div class="feature-card">
                <h3>📊 Quantum Physics</h3>
                <p>Harmonic Oscillator, Infinite Well, Finite Well, Tunneling</p>
            </div>
        </div>
    </section>

    <!-- Animations Section -->
    <section id="animations" class="animations">
        <h2>Animations Gallery</h2>
        <div class="animation-grid">
            <div class="animation-card">
                <h3>Harmonic Oscillator</h3>
                <video width="300" controls>
                    <source src="animations/HarmonicOscillator.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <p>5-level quantum oscillator visualization</p>
            </div>
            <div class="animation-card">
                <h3>Infinite Well</h3>
                <video width="300" controls>
                    <source src="animations/InfiniteWell.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <p>Particle-in-a-box eigenstates</p>
            </div>
            <div class="animation-card">
                <h3>Finite Well</h3>
                <video width="300" controls>
                    <source src="animations/FiniteWell.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <p>Bound states with tunneling</p>
            </div>
            <div class="animation-card">
                <h3>Tunneling</h3>
                <video width="300" controls>
                    <source src="animations/Tunneling.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <p>Wave packet tunneling dynamics</p>
            </div>
        </div>
    </section>

    <!-- Simulator Section -->
    <section id="simulator" class="simulator">
        <h2>Interactive Simulator</h2>
        <p>Download and run the interactive Jupyter notebook locally:</p>
        <div class="simulator-info">
            <h3>Quick Setup</h3>
            <pre><code>pip install jupyter numpy scipy matplotlib ipywidgets
git clone https://github.com/saiashish07/animation_quantum_mech_basics.git
jupyter lab Interactive_Quantum_Controls.ipynb</code></pre>
            <p>Then interact with the sliders to explore quantum mechanics in real-time!</p>
        </div>
    </section>

    <!-- Documentation Section -->
    <section id="docs" class="documentation">
        <h2>Documentation</h2>
        <div class="docs-grid">
            <a href="https://github.com/saiashish07/animation_quantum_mech_basics/blob/main/COMPREHENSIVE_README.md" class="doc-card">
                <h3>Complete Guide</h3>
                <p>All documentation consolidated in one file</p>
            </a>
            <a href="https://github.com/saiashish07/animation_quantum_mech_basics" class="doc-card">
                <h3>Source Code</h3>
                <p>Full implementation on GitHub</p>
            </a>
            <a href="https://github.com/saiashish07/animation_quantum_mech_basics/blob/main/src/manim_quantum.py" class="doc-card">
                <h3>Animation Framework</h3>
                <p>Manim animation implementation</p>
            </a>
            <a href="https://github.com/saiashish07/animation_quantum_mech_basics/blob/main/src/ffmpeg_pipeline.py" class="doc-card">
                <h3>Video Pipeline</h3>
                <p>FFmpeg encoding and processing</p>
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2025 Quantum Mechanics Animation Pipeline | <a href="https://github.com/saiashish07/animation_quantum_mech_basics">GitHub Repository</a></p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
EOF
echo "✓ index.html created"

# Create CSS
echo "▶ Creating style.css..."
cat > "$DOCS_DIR/style.css" << 'EOF'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f5f5f5;
}

/* Navigation */
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}

.nav-menu a:hover {
    opacity: 0.8;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 6rem 2rem;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

/* Buttons */
.btn {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s;
}

.btn-primary {
    background: white;
    color: #667eea;
    font-weight: bold;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
}

.btn-secondary:hover {
    background: white;
    color: #667eea;
}

/* Sections */
section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 4rem 2rem;
}

section h2 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    color: #667eea;
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card h3 {
    color: #667eea;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

/* Animation Grid */
.animation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.animation-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.animation-card video {
    width: 100%;
    height: auto;
    border-radius: 5px;
    margin: 1rem 0;
}

.animation-card h3 {
    color: #667eea;
    margin-bottom: 1rem;
}

/* Simulator Section */
.simulator {
    background: #f9f9f9;
}

.simulator-info {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.simulator-info pre {
    background: #272822;
    color: #f8f8f2;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 0.9rem;
    margin: 1rem 0;
}

/* Documentation Grid */
.docs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.doc-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-decoration: none;
    color: #333;
    transition: all 0.3s;
    border-left: 4px solid #667eea;
}

.doc-card:hover {
    transform: translateX(5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.doc-card h3 {
    color: #667eea;
    margin-bottom: 0.5rem;
}

/* Footer */
.footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem;
}

.footer a {
    color: #667eea;
    text-decoration: none;
}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        gap: 1rem;
        font-size: 0.9rem;
    }

    .hero-content h1 {
        font-size: 2rem;
    }

    .hero-buttons {
        flex-direction: column;
    }

    section h2 {
        font-size: 1.8rem;
    }
}
EOF
echo "✓ style.css created"

# Create JavaScript
echo "▶ Creating script.js..."
cat > "$DOCS_DIR/script.js" << 'EOF'
// Scroll to section smoothly
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Mobile menu toggle (if needed in future)
document.addEventListener('DOMContentLoaded', function() {
    console.log('✓ Website loaded successfully');
});
EOF
echo "✓ script.js created"

# Create _config.yml for Jekyll
echo "▶ Creating _config.yml for Jekyll..."
cat > "$PROJECT_ROOT/_config.yml" << 'EOF'
title: Quantum Mechanics Animation Pipeline
description: Interactive simulations, professional animations, and 4K videos
theme: jekyll-theme-minimal
show_downloads: true
EOF
echo "✓ _config.yml created"

# Create .gitignore
echo "▶ Creating/updating .gitignore..."
cat > "$PROJECT_ROOT/.gitignore" << 'EOF'
# Virtual environments
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Large files (can be regenerated)
outputs/*.mp4
outputs/*.mkv
videos/**/*.mp4
*.egg-info/

# Build artifacts
build/
dist/

# Cache
*.cache
.cache/
EOF
echo "✓ .gitignore created/updated"

# Create simple README for GitHub (different from COMPREHENSIVE_README)
echo "▶ Creating GitHub README.md..."
cat > "$PROJECT_ROOT/README.md" << 'EOF'
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
EOF
echo "✓ README.md created"

# Git setup
echo ""
echo "▶ Initializing Git..."
if [ ! -d .git ]; then
    git init
    echo "✓ Git repository initialized"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  DEPLOYMENT SETUP COMPLETE                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Git (if not done):"
echo "   git config --global user.name 'Your Name'"
echo "   git config --global user.email 'your@email.com'"
echo ""
echo "2. Create repository on GitHub:"
echo "   https://github.com/new"
echo "   - Name: animation_quantum_mech_basics"
echo "   - Public repository"
echo ""
echo "3. Add files and push:"
echo "   git add ."
echo "   git commit -m 'Initial commit: Quantum mechanics pipeline'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/animation_quantum_mech_basics.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Enable GitHub Pages:"
echo "   - Repository Settings → Pages"
echo "   - Source: Deploy from branch"
echo "   - Branch: main → /docs folder"
echo "   - Click Save"
echo ""
echo "5. Website will be live at:"
echo "   https://YOUR_USERNAME.github.io/animation_quantum_mech_basics"
echo ""
echo "✓ Website structure created in: $DOCS_DIR"
echo "✓ Configuration files created"
echo "✓ Ready to push to GitHub!"
echo ""
