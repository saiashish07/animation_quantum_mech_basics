# Running Quantum Simulations in VS Code Codespace

## 🚀 Quick Start (Right Now!)

### Step 1: Install the Package

```bash
# Navigate to project
cd /workspaces/animation_quantum_mech_basics

# Install in development mode (one-time setup)
pip install -e .
```

### Step 2: Run Validation Tests

```bash
# Verify everything works
python tests/test_core.py
```

Expected output:
```
✓ Testing QuantumGrid... ✓
✓ Testing infinite well eigenvalues... ✓
✓ Testing harmonic oscillator energy spacing... ✓
✓ Testing Gaussian wave packet... ✓
✓ Testing potential classes... ✓
✓ Testing orthonormality... ✓

Results: 6 passed, 0 failed
```

### Step 3: Generate Animated Simulations

```bash
# Generate ALL four simulations
python -m quantum_playground all

# Or run individual scenarios
python -m quantum_playground infinite      # Particle in a box
python -m quantum_playground finite        # Finite barrier
python -m quantum_playground harmonic      # Harmonic oscillator
python -m quantum_playground tunneling     # Tunneling demo
```

This will take 5-10 minutes and generate outputs in `outputs/` folder.

### Step 4: View the Results

```bash
# List generated files
ls -lh outputs/

# You should see:
# - infinite_well_overview.png
# - infinite_well_animation.mp4
# - finite_well_comparison.png
# - finite_well_animation.mp4
# - harmonic_oscillator_overview.png
# - harmonic_oscillator_animation.mp4
# - tunneling_analysis.png
# - tunneling_animation.mp4
```

---

## 📺 Viewing Outputs in VS Code

### Option 1: PNG Images (Easiest)

1. Go to VS Code Explorer (left sidebar)
2. Navigate to `outputs/` folder
3. Click on any `.png` file
4. Image viewer opens automatically

**Files to view:**
- `*_overview.png` - Energy levels and eigenfunctions
- `*_comparison.png` - Numerical vs analytical
- `*_analysis.png` - Detailed measurements

### Option 2: MP4 Animations

**Problem:** VS Code doesn't have great native MP4 support in browser

**Solutions:**

**A) Download and Play Locally**
```bash
# MP4 files are in outputs/ folder
# Download via: VS Code → Right-click file → Download
# Play with: VLC, QuickTime, Windows Media Player
```

**B) Convert to GIF (for quick viewing)**
```bash
# Install ffmpeg (if needed)
# sudo apt-get install ffmpeg

# Convert MP4 to GIF
ffmpeg -i outputs/tunneling_animation.mp4 -vf fps=10 outputs/tunneling.gif
```

**C) View Using Python (in Terminal)**
```bash
# Won't play video, but shows it's created
file outputs/tunneling_animation.mp4
ffprobe outputs/tunneling_animation.mp4  # Shows video info
```

---

## 🎯 Interactive Python Usage (Best for Codespace)

Instead of generating MP4s (which are hard to view here), use interactive Python to see plots immediately:

### Infinite Well Example

```python
# In terminal or Python script
from quantum_playground.animations import InfiniteWellSimulation

# Create simulation
sim = InfiniteWellSimulation(well_width=2.0, num_levels=8)

# Generate and display plot
sim.plot_overview(save_path="well.png")

# View in VS Code: Open outputs/well.png
```

### Tunneling Example

```python
from quantum_playground.animations import TunnelingSimulation

sim = TunnelingSimulation(
    barrier_height=5.0,
    barrier_width=0.5,
    particle_energy=3.0
)

trajectory = sim.run_evolution(num_steps=500)
sim.plot_transmission_analysis(trajectory, save_path="tunneling.png")

# View: Open outputs/tunneling.png in VS Code
```

### Quick Plot Without Saving

```python
import matplotlib.pyplot as plt
from quantum_playground.animations import HarmonicOscillatorSimulation

sim = HarmonicOscillatorSimulation(omega=1.0, num_levels=6)

# This will display inline if in Jupyter
fig = sim.plot_overview()
plt.show()  # For script execution
```

---

## 🐳 Using Jupyter in Codespace

**BEST for interactive work:**

### Step 1: Install Jupyter (if needed)

```bash
pip install jupyter jupyter-lab
```

### Step 2: Start Jupyter

```bash
jupyter lab --ip=0.0.0.0 --no-browser
```

Output will show:
```
To access the server, open this file in a browser:
    file:///home/codespace/.local/share/jupyter/runtime/jpserver-xxxxx.json
Or copy and paste one of these URLs:
    http://127.0.0.1:8888/?token=xxxxx
```

### Step 3: Access from VS Code

1. Click on "Ports" tab at bottom of VS Code
2. Look for port 8888
3. Click the globe icon to open in browser
4. Paste the token

### Step 4: Create Interactive Notebook

Create file `explore_quantum.ipynb`:

```python
# Cell 1: Import and setup
%matplotlib inline
from quantum_playground.animations import InfiniteWellSimulation
import matplotlib.pyplot as plt

# Cell 2: Create simulation
sim = InfiniteWellSimulation(well_width=2.0, num_levels=8)

# Cell 3: Show plot
sim.plot_overview()

# Cell 4: Generate animation (optional, slow)
sim.animate_eigenstates(num_frames=50, save_path="well_small.mp4")
```

Then just run cells one-by-one and see results instantly!

---

## 📊 Complete Workflow in Codespace

### Minimal (5 minutes - just see it works):

```bash
pip install -e .
python tests/test_core.py
```

### Standard (15 minutes - generate plots):

```bash
pip install -e .
python -m quantum_playground all --no-animation
ls outputs/*.png
# Open PNG files in VS Code
```

### Full (10 minutes - with animations):

```bash
pip install -e .
python -m quantum_playground infinite
# Wait for MP4 generation
# Download outputs/ folder to your computer
# Play MP4s on your laptop
```

### Interactive (Best experience):

```bash
pip install jupyter
jupyter lab --ip=0.0.0.0 --no-browser
# Create notebook with simulation code
# Run cells and see plots in real-time
```

---

## 🎨 Custom Simulations (Modify and Run)

### Edit Parameters

Create file `my_simulation.py`:

```python
#!/usr/bin/env python
"""Custom quantum simulation"""

from quantum_playground.animations import TunnelingSimulation
import matplotlib.pyplot as plt

# Customize parameters
print("Running tunneling simulation...")

sim = TunnelingSimulation(
    barrier_height=8.0,      # Make barrier taller
    barrier_width=0.7,       # Make barrier wider
    particle_energy=2.5,     # Lower energy (harder to tunnel!)
    num_points=256,
    dt=0.01
)

print("Evolving wave packet...")
trajectory = sim.run_evolution(num_steps=600)

print("Generating analysis plot...")
sim.plot_transmission_analysis(trajectory, save_path="my_tunneling.png")

print("Done! View: outputs/my_tunneling.png")

# Show analysis
analysis = sim.analyze_transmission(trajectory)
print(f"\nTransmission coefficient: T = {analysis['T_numerical']:.4f}")
print(f"WKB approximation:        T_WKB = {analysis['T_wkb']:.4f}")
print(f"Reflection coefficient:   R = {analysis['R_numerical']:.4f}")
```

Run it:
```bash
python my_simulation.py
```

---

## 🛠️ Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
cd /workspaces/animation_quantum_mech_basics
pip install -e .
```

### Issue: MP4 won't play in browser

**Solution:** Just download and play locally, or convert to GIF, or use PNG plots

### Issue: Simulation is slow

**Solutions:**
- Reduce grid points: `num_points=128` (instead of 256/512)
- Reduce animation frames: `num_frames=50` (instead of 100/150)
- Use `--no-animation` flag for faster run

### Issue: Out of memory

**Solution:**
```bash
python -m quantum_playground all --no-animation
# Just generate PNG plots, skip MP4 generation
```

---

## 📁 File Organization

```
outputs/
├── infinite_well_overview.png          ← View in VS Code
├── infinite_well_animation.mp4         ← Download to computer
├── finite_well_comparison.png          ← View in VS Code
├── finite_well_animation.mp4
├── harmonic_oscillator_overview.png
├── harmonic_oscillator_animation.mp4
├── tunneling_analysis.png
└── tunneling_animation.mp4
```

---

## 🎯 Recommended Approach for Codespace

1. **First time?**
   ```bash
   pip install -e .
   python tests/test_core.py
   ```

2. **Want to see plots?**
   ```bash
   python -m quantum_playground infinite
   # Open outputs/infinite_well_overview.png
   ```

3. **Want animations?**
   ```bash
   python -m quantum_playground all
   # Download outputs/*.mp4 to your computer
   # Play on your laptop
   ```

4. **Interactive exploration?**
   ```bash
   pip install jupyter
   jupyter lab --ip=0.0.0.0 --no-browser
   # Create notebook, run cells interactively
   ```

5. **Custom modifications?**
   - Edit `my_simulation.py`
   - Change parameters
   - `python my_simulation.py`
   - View results in outputs/

---

## ✨ Quick Commands Reference

```bash
# Setup (one-time)
pip install -e .

# Validate
python tests/test_core.py

# Run all simulations
python -m quantum_playground all

# Run specific scenario
python -m quantum_playground tunneling

# Just plot (no animation, faster)
python -m quantum_playground all --no-animation

# Custom output directory
python -m quantum_playground all --output ~/my_outputs

# See generated files
ls -lh outputs/

# View a specific plot
open outputs/tunneling_analysis.png  # macOS
xdg-open outputs/tunneling_analysis.png  # Linux
```

---

**TL;DR:** 
1. `pip install -e .`
2. `python -m quantum_playground infinite`
3. Open `outputs/*.png` in VS Code
4. Download `outputs/*.mp4` to your computer
5. For interactive: use Jupyter Lab!

🚀 Start with: `python tests/test_core.py`
