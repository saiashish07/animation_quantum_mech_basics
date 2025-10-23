# Quick Start Guide

## Installation & Setup

### 1. Clone and Setup Environment

```bash
# Navigate to project directory
cd animation_quantum_mech_basics

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -e .
```

### 2. Verify Installation

```bash
# Run validation tests
python tests/test_core.py
```

You should see:
```
✓ Testing QuantumGrid... ✓
✓ Testing infinite well eigenvalues... ✓
✓ Testing harmonic oscillator energy spacing... ✓
✓ Testing Gaussian wave packet... ✓
✓ Testing potential classes... ✓
✓ Testing orthonormality... ✓

Results: 6 passed, 0 failed
```

## Running Simulations

### Option 1: Command Line (Easiest for Presentations)

Run all four simulations:
```bash
python -m quantum_playground all
```

Run specific scenario:
```bash
python -m quantum_playground infinite    # Just particle in a box
python -m quantum_playground tunneling   # Just tunneling demo
```

Customize output location:
```bash
python -m quantum_playground all --output ~/Desktop/quantum_animations
```

Skip animations (faster, static plots only):
```bash
python -m quantum_playground all --no-animation
```

### Option 2: Python Scripts (For Customization)

Edit parameters in Python scripts:

```python
# Run tunneling with custom parameters
from quantum_playground.animations import TunnelingSimulation

sim = TunnelingSimulation(
    barrier_height=5.0,      # Make barrier taller
    barrier_width=0.7,       # Make barrier wider
    particle_energy=2.5,     # Lower energy (harder to tunnel)
    num_points=512,          # Higher resolution
    dt=0.005,                # Smaller time step (more accurate)
)

trajectory = sim.run_evolution(num_steps=1000)
sim.plot_transmission_analysis(trajectory, save_path="my_tunneling.png")
sim.animate_tunneling(trajectory, save_path="my_tunneling.mp4")
```

### Option 3: Jupyter Notebooks (Interactive)

```python
# In Jupyter notebook
%matplotlib inline
from quantum_playground.animations import HarmonicOscillatorSimulation
import numpy as np

sim = HarmonicOscillatorSimulation(omega=1.0, num_levels=8)
sim.plot_overview()

# Modify superposition coefficients
c = np.array([1, 0.7, 0.3])  # Different mixing
sim.animate_superposition(coefficients=c)
```

## Output Files

After running simulations, check the `outputs/` directory:

```
outputs/
├── infinite_well_overview.png          # Energy levels + eigenstates
├── infinite_well_animation.mp4         # Animated probability oscillations
├── finite_well_comparison.png          # Finite vs infinite comparison
├── finite_well_animation.mp4           # Evanescent tail visualization
├── harmonic_oscillator_overview.png    # Classical vs quantum
├── harmonic_oscillator_animation.mp4   # Wave packet breathing motion
├── tunneling_analysis.png              # Transmission/reflection breakdown
└── tunneling_animation.mp4             # Wave packet passing through barrier
```

## Using in Presentations

### PowerPoint/Google Slides

1. Insert MP4 videos:
   - Insert → Video → Select from outputs/
   - Most modern versions support H.264

2. Insert PNG plots:
   - Insert → Image → PNG files

3. Create narrative:
   ```
   Slide 1: Infinite Well (Overview)
   Slide 2: Infinite Well (Play animation - 2:30)
   Slide 3: Finite Well (Overview with Comparison)
   Slide 4: Finite Well (Play animation - 2:30)
   Slide 5: Harmonic Oscillator (Overview)
   Slide 6: Harmonic Oscillator (Play animation - 3:00)
   Slide 7: Quantum Tunneling (Analysis plot)
   Slide 8: Quantum Tunneling (Play animation - 3:00)
   ```

### Interactive Demo During Class

Use Python script directly:
```bash
# Keep terminal open, show outputs in real-time
python -m quantum_playground infinite
# Matplotlib shows plots → export with toolbar buttons
```

Or use Jupyter for live editing:
```bash
jupyter lab
# Open notebook, run cells, modify parameters, rerun
```

## Customization Examples

### Example 1: Study Energy Level Density

```python
from quantum_playground.animations import InfiniteWellSimulation

# Increase number of levels to see convergence
sim = InfiniteWellSimulation(well_width=2.0, num_levels=20)
fig = sim.plot_overview()
```

### Example 2: Tunneling Through Different Barriers

```python
from quantum_playground.animations import TunnelingSimulation
import matplotlib.pyplot as plt

# Compare different barrier heights
heights = [3.0, 5.0, 8.0, 15.0]
fig, axes = plt.subplots(1, len(heights))

for ax, h in zip(axes, heights):
    sim = TunnelingSimulation(barrier_height=h, particle_energy=2.5)
    traj = sim.run_evolution(num_steps=500)
    analysis = sim.analyze_transmission(traj)
    
    ax.text(0.5, 0.5, f"V₀={h}\nT={analysis['T_numerical']:.3f}",
           ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_title(f"T ≈ {analysis['T_numerical']:.3f}")

plt.tight_layout()
plt.savefig('barrier_comparison.png', dpi=150)
```

### Example 3: Harmonic Oscillator with Excited States

```python
from quantum_playground.animations import HarmonicOscillatorSimulation
import numpy as np

sim = HarmonicOscillatorSimulation(omega=1.0, num_levels=10)

# Pure n=3 state (no animation needed - it's stationary)
fig, ax = plt.subplots()
psi_3 = sim.eigenvectors[:, 3]
ax.plot(sim.x, np.abs(psi_3)**2, 'b-', linewidth=2)
ax.fill_between(sim.x, 0, np.abs(psi_3)**2, alpha=0.3)
ax.set_title("n=3 State: Third Excited Level")
plt.show()

# Superposition of n=1 and n=2
c = np.array([0, 1, 1])  # Skip n=0, equal mix of n=1 and n=2
sim.animate_superposition(coefficients=c, save_path="excited_packet.mp4")
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'quantum_playground'"

**Solution:**
```bash
# Make sure you're in the project directory
cd animation_quantum_mech_basics

# Reinstall package
pip install -e .
```

### Issue: "ffmpeg not found"

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Solution (macOS):**
```bash
brew install ffmpeg
```

**Solution (Windows):**
Download from ffmpeg.org or:
```bash
pip install imageio imageio-ffmpeg
```

### Issue: Animations are slow or out of memory

**Solutions:**
- Reduce grid resolution: `num_points=256` (smaller = faster)
- Use `--no-animation` for quick testing
- Reduce `num_frames` in animation calls
- Use `dt=0.02` (larger timestep) for tunneling

### Issue: Plot looks wrong or empty

**Solution:**
```python
import matplotlib.pyplot as plt
plt.ion()  # Turn on interactive mode
sim.plot_overview()
plt.show()  # Make sure to show the plot
```

## Performance Benchmarks

On typical laptop (Intel i5, 8GB RAM):

| Scenario | Time | Output Size |
|----------|------|-------------|
| Infinite Well (256 pts, 5 levels) | 0.5s + 12s MP4 | 12MB |
| Finite Well (256 pts, 6 levels) | 0.6s + 12s MP4 | 12MB |
| Harmonic Oscillator (256 pts, 8 levels) | 0.4s + 15s MP4 | 15MB |
| Tunneling (512 pts, 800 steps) | 2s + 20s MP4 | 20MB |

**Total for all**: ~5 minutes

## Next Steps

1. ✅ Run basic simulations
2. 📊 Create presentation slides
3. 🎨 Customize parameters for your class
4. 📝 Add lecture notes alongside plots
5. 🔬 Explore 2D systems (future enhancement)

## Questions?

Check the main README.md for API documentation and physics background.

---

**Happy quantum teaching!** ⚛️
