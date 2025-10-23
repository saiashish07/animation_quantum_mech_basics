# 🚀 QUICK START: RUNNING SIMULATIONS IN CODESPACE

## ✅ Current Status

**All systems working!** The quantum solver bug has been fixed. You can now run all four quantum mechanics simulations and view the results directly in VS Code.

---

## 📖 HOW TO VIEW THE PLOTS

### Option 1: Visual Explorer (Easiest)
1. Click **Explorer** button on the left sidebar (top icon that looks like two overlapping squares)
2. Navigate to `outputs/` folder
3. Click on any `.png` file
4. The image viewer will open on the right

### Option 2: Open with Preview
1. Right-click on a `.png` file in the explorer
2. Select **Open with...**
3. Choose **Preview**

---

## 🔬 WHAT'S IN EACH PLOT

### 1. **Infinite Potential Well** (`01_infinite_well.png`)
Shows the simplest quantum system - a particle trapped in a box.

**What to look for:**
- Sharp potential walls (infinite height)
- Discrete energy levels (E₁, E₂, E₃...)
- Standing wave patterns (nodes at boundaries)
- Probability increases with energy

**Teaching point:** "Even though the particle is trapped, its probability density looks like waves - this is quantum superposition!"

### 2. **Finite Potential Well** (`02_finite_well.png`)
Shows what happens when the walls aren't infinitely high.

**What to look for:**
- Potential walls are now finite
- Wavefunctions "leak out" beyond the walls (evanescent tails)
- Energy levels are lower than infinite well (particle has more "room")
- Compare side-by-side with infinite well

**Teaching point:** "The particle can now be found outside the well, even though classically it would be trapped. This is quantum tunneling!"

### 3. **Harmonic Oscillator** (`03_harmonic_oscillator.png`)
Shows the quantum version of a mass on a spring.

**What to look for:**
- Parabolic potential V(x) = ½mω²x²
- Energy levels are equally spaced: ΔE = ℏω
- Gaussian-like probability distributions
- Minimum energy is NOT zero (zero-point energy = ½ℏω)

**Teaching point:** "Unlike classical oscillators that can have zero energy, quantum oscillators always have minimum energy. This explains atomic vibrations!"

### 4. **Quantum Tunneling** (`04_tunneling_analysis.png`)
Shows how particles can pass through barriers they shouldn't classically.

**What to look for:**
- Rectangular barrier potential
- Wave packet evolution over time
- Some probability penetrates the barrier
- Transmission coefficient (T ≈ 24%) vs WKB estimate (T ≈ 15%)

**Teaching point:** "Quantum particles can go through walls! This is why radioactive decay happens and why semiconductor devices work."

---

## 💻 RUN MORE SIMULATIONS

### Generate all 4 systems from scratch:
```bash
python -m quantum_playground all
```
Output: New PNGs in `outputs/` (overwrites old ones)

### Generate one system:
```bash
python -m quantum_playground infinite
python -m quantum_playground finite
python -m quantum_playground harmonic
python -m quantum_playground tunneling
```

### Validate everything works:
```bash
python quick_test.py
```

---

## 🎨 CUSTOMIZE YOUR OWN SIMULATIONS

Edit `run_demo.py` to create custom scenarios. For example, change parameters:

```python
# Infinite well with different width
iw = InfiniteWellSimulation(well_width=3.0, num_levels=10)

# Harmonic oscillator with different frequency
ho = HarmonicOscillatorSimulation(mass=1.0, omega=2.0, num_levels=8)

# Tunneling with different particle energy
tunnel = TunnelingSimulation(
    barrier_height=5.0,
    barrier_width=1.0,
    particle_energy=2.0  # Change this!
)
```

Then run:
```bash
python run_demo.py
```

---

## 📊 DATA INSIDE THE CODE

All numerical results are available in Python objects:

```python
from quantum_playground.animations import InfiniteWellSimulation

sim = InfiniteWellSimulation(well_width=2.0, num_levels=6)

# Access computed energy levels
print(sim.eigenvalues)        # Array of E values
print(sim.eigenvectors)        # Column vectors ψ(x)

# Get analytical formula values
print(sim.get_analytical_energies())

# Access the spatial grid
print(sim.x)    # Position points
```

---

## 🐛 TROUBLESHOOTING

### "Module not found" error
```bash
# Reinstall the package
pip install -e .
```

### Plots look wrong
```bash
# Regenerate with higher resolution
# Edit the script to use num_points=512 or num_points=1024
```

### Memory error with large systems
```bash
# Use fewer grid points
# InfiniteWellSimulation(num_points=128)  # Instead of 256
```

---

## 🎓 FOR YOUR CLASS PRESENTATION

### Recommended order:
1. **Start with Infinite Well** - Simplest, most intuitive
2. **Show Finite Well** - Explain penetration/tunneling preview
3. **Harmonic Oscillator** - Most commonly seen in nature (atoms, molecules)
4. **Tunneling** - Wow factor! Show why semiconductors exist

### Discussion talking points:
- "Notice the energy levels aren't evenly spaced in the well - why?"
- "Why can the particle be found outside the barrier in the finite well?"
- "What would happen if we make the barrier wider/taller?"
- "This is the same physics that powers your phone's transistors!"

---

## 📚 REFERENCE DOCUMENTATION

For more details, see:
- `README.md` - Complete technical reference
- `TEACHING_GUIDE.md` - Lecture notes and exam questions
- `SOLVER_FIX_SUMMARY.md` - Technical details of the quantum solver

---

## ✨ NEXT STEPS

1. ✅ View all 4 plots in `outputs/` folder
2. ✅ Understand what each plot shows (see above)
3. ✅ Plan which systems to present first
4. ✅ Create customized versions if needed
5. ✅ Present to your class!

**You're all set! 🚀**
