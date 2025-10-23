# Teaching Guide & Lecture Notes

## Course Integration

This quantum mechanics simulation suite is designed to support teaching the four fundamental quantum systems. Use these materials alongside traditional textbook chapters.

---

## 1. INFINITE POTENTIAL WELL (Particle in a Box)

### Lecture Objectives
- Understand **quantum confinement** and its effects
- Derive and verify **discrete energy quantization**
- Visualize **standing wave patterns** as eigenfunctions
- Compare with classical particle behavior

### Mathematical Framework

**Setup:**
- Particle confined to $-L/2 \leq x \leq L/2$
- $V(x) = 0$ inside, $V(x) = \infty$ outside
- Boundary conditions: $\psi(\pm L/2) = 0$

**Solutions:**
$$\psi_n(x) = \sqrt{\frac{2}{L}} \sin\left(\frac{n\pi(x + L/2)}{L}\right), \quad n = 1,2,3,...$$

$$E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}$$

**Key Points:**
- No $n=0$ state (ground state is $n=1$, not zero energy)
- Energy spacing: $\Delta E_n = E_{n+1} - E_n = \frac{\pi^2\hbar^2}{2mL^2}(2n+1)$
- Spacing **increases** with $n$ (unlike harmonic oscillator!)
- Average momentum $\langle p \rangle = 0$ (standing wave)

### Running the Simulation

```bash
python -m quantum_playground infinite
```

### Classroom Discussion Points

**From Overview Plot:**
1. *"Why can't we have n=0?"* 
   - Answer: $\psi \equiv 0$ violates normalization and isn't a valid state

2. *"Why are levels not evenly spaced?"*
   - Answer: Show that $\Delta E_n \propto (2n+1)$, gets larger

3. *"What about a particle in 3D?"*
   - Answer: $E_{n_x,n_y,n_z} = \frac{\pi^2\hbar^2}{2m}(n_x^2/a^2 + n_y^2/b^2 + n_z^2/c^2)$
   - Can have **degeneracies** (different $(n_x,n_y,n_z)$ giving same E)

**From Animation:**
- Eigenfunctions oscillate in time: $\Psi_n(x,t) = \psi_n(x) e^{-iE_nt/\hbar}$
- Animation shows $|\psi|^2$ varying periodically with frequency $\omega_n = E_n/\hbar$
- Higher $n$ = faster oscillation = higher energy

### Exam Questions

1. For an electron in a box of width $L = 10 \text{ nm}$:
   - Find $E_1$ and $E_2$
   - Find the minimum energy to excite from $n=1$ to $n=2$

2. Show that $\langle x \rangle = L/2$ (particle is centered)

3. Calculate $\langle p^2 \rangle$ and verify uncertainty principle

---

## 2. FINITE POTENTIAL WELL

### Lecture Objectives
- Understand **bound vs scattering states**
- Visualize **wavefunction penetration** beyond classical region
- Explain **evanescent waves**
- Derive transcendental equation for bound states

### Mathematical Framework

**Setup:**
- $V(x) = 0$ for $|x| < a/2$
- $V(x) = V_0$ for $|x| \geq a/2$
- $V_0 > 0$ (finite barrier)

**Bound States (E < V₀):**

Inside well ($|x| < a/2$): $\psi(x) = A\cos(kx)$ or $B\sin(kx)$ where $k = \sqrt{2mE}/\hbar$

Outside well ($|x| > a/2$): $\psi(x) = Ce^{-\kappa|x|}$ where $\kappa = \sqrt{2m(V_0-E)}/\hbar$

**Transcendental equation (for even parity):**
$$\tan\left(\frac{ka}{2}\right) = \frac{\kappa}{k}$$

### Running the Simulation

```bash
python -m quantum_playground finite
```

### Key Physics

**Number of Bound States:**
- At least one always exists
- More states available if $V_0$ is deeper or well is wider
- Rough rule: $N_{max} \approx \sqrt{\frac{mV_0a^2}{2\pi^2\hbar^2}}$

**Penetration Depth:**
- Characteristic length outside well: $\xi = 1/\kappa$
- Higher energy state → larger $\kappa$ → shorter decay length
- Lower energy state → deeper penetration into classically forbidden region!

**Comparison with Infinite Well:**
- All finite well states have **lower** energy than infinite well counterparts
  - Why? Wavefunction "leaks out" → wider effective region
  - Spreads out wave → lowers kinetic energy
- Energy shift: $\Delta E = E_{infinite} - E_{finite} > 0$

### Classroom Activity

**Interactive Exploration:**
```python
from quantum_playground.animations import FiniteWellSimulation

# Vary barrier height
for V0 in [5, 10, 20, 50]:
    sim = FiniteWellSimulation(barrier_height=V0, num_levels=4)
    print(f"\nV₀ = {V0}:")
    print(f"  Energy levels: {sim.eigenvalues}")
    print(f"  Penetration depths: [see from plot]")
```

### Discussion Questions

1. *"Why does penetration depth decrease with energy?"*
   - Answer: Higher energy → smaller $(V_0 - E)$ → shorter $\xi = 1/\kappa$

2. *"What happens as $V_0 \to \infty$?"*
   - Answer: Penetration → 0, energies → infinite well values, bound states → no limit

3. *"Can a bound state have $E > V_0$?"*
   - Answer: No! By definition, bound states satisfy $E < V_0$
   - If $E > V_0$, particle can escape to infinity → scattering state

---

## 3. QUANTUM HARMONIC OSCILLATOR

### Lecture Objectives
- Master the **foundational SHO model**
- Understand **zero-point energy** (quantum mechanical origin)
- Visualize **Hermite polynomials** and Gaussian envelope
- Compare **quantum vs classical** probability distributions
- Explore **coherent superpositions** (minimum uncertainty packets)

### Mathematical Framework

**Potential:**
$$V(x) = \frac{1}{2}m\omega^2 x^2$$

**Energy Eigenvalues:**
$$E_n = \hbar\omega\left(n + \frac{1}{2}\right), \quad n = 0, 1, 2, ...$$

**Key Feature:** Evenly spaced levels! $\Delta E = \hbar\omega$ (independent of $n$)

**Eigenfunctions:**
$$\psi_n(x) = \left(\frac{m\omega}{\pi\hbar}\right)^{1/4} \frac{1}{\sqrt{2^n n!}} H_n(\xi) e^{-\xi^2/2}$$

where $\xi = \sqrt{m\omega/\hbar} \cdot x$ and $H_n$ are Hermite polynomials.

### Zero-Point Energy

**Classical lowest energy:** $E_{cl} = 0$ (particle at rest at $x=0$)

**Quantum ground state:** $E_0 = \frac{1}{2}\hbar\omega > 0$

**Physical origin (Uncertainty Principle):**
- If $\Delta x \to 0$ (localize in well), then $\Delta p \to \infty$
- Compromise: $\Delta x \approx \sqrt{\hbar/m\omega}$, $\Delta p \approx \sqrt{m\hbar\omega}$
- Kinetic energy: $\langle T \rangle = \langle p^2 \rangle / 2m = \frac{1}{4}\hbar\omega$
- Potential energy: $\langle V \rangle = \frac{1}{2}m\omega^2 \langle x^2 \rangle = \frac{1}{4}\hbar\omega$
- Total: $E_0 = \frac{1}{2}\hbar\omega$ ✓

### Running the Simulation

```bash
python -m quantum_playground harmonic
```

### Coherent States (Wave Packets)

**Definition:** A superposition with $c_n \propto e^{i\phi_n}$ and properly chosen phases minimizes uncertainty.

**Property:** Wave packet oscillates back and forth with period $T = 2\pi/\omega$, maintaining its shape!

**Animation shows:**
1. Real and imaginary parts of superposition
2. Probability density envelope
3. Energy decomposition (which states are contributing)

**Classical Limit:**
- As $n \to \infty$, $\psi_n(x)$ becomes concentrated at classical turning points
- Average $\psi_n$ matches classical probability from $E = \frac{1}{2}m\omega^2 x_{max}^2$

### Exam Problems

1. Calculate $\langle x \rangle$, $\langle x^2 \rangle$, $\Delta x$ for ground state

2. For superposition $\Psi = (|0\rangle + |1\rangle)/\sqrt{2}$:
   - Time dependence: $\Psi(t) = e^{-iE_0t/\hbar}(|0\rangle + e^{-i\omega t}|1\rangle)/\sqrt{2}$
   - Probability oscillates as $|\langle 0|\Psi(t)\rangle|^2 = \frac{1}{2}(1 + \cos(\omega t))$

3. Show that harmonic oscillator satisfies: 
   $$\langle V \rangle = \langle T \rangle = \frac{E}{2}$$ 
   (Virial theorem for $V \propto x^2$)

---

## 4. QUANTUM TUNNELING

### Lecture Objectives
- Understand **barrier penetration** beyond classical prediction
- Apply **WKB approximation** for transmission coefficient
- Visualize **evanescent wave decay** inside barrier
- Explain **classically forbidden regions**
- Real-world applications (radioactive decay, scanning tunneling microscope)

### Mathematical Framework

**Rectangular Barrier:**
$$V(x) = \begin{cases} 0 & x < -a/2 \\ V_0 & -a/2 \leq x \leq a/2 \\ 0 & x > a/2 \end{cases}$$

**Incident Energy:** $E < V_0$ (classically forbidden!)

**Wave Vectors:**
- Outside: $k = \sqrt{2mE}/\hbar$
- Inside: $\kappa = \sqrt{2m(V_0-E)}/\hbar$ (imaginary = evanescent)

**Transmission Coefficient (WKB Approximation):**
$$T \approx e^{-2\gamma}$$

where 

$$\gamma = \frac{1}{\hbar}\int_{-a/2}^{a/2} \sqrt{2m(V_0 - E)} \, dx = \kappa \cdot a$$

(For rectangular barrier: exact formula available)

**Key Result:** $T \approx e^{-2\kappa a}$ → exponential dependence on barrier width!

### Running the Simulation

```bash
python -m quantum_playground tunneling
```

### Physical Interpretation

**Wave Packet Dynamics:**
1. Gaussian packet approaches from left with $\langle k \rangle = \sqrt{2mE}/\hbar$
2. At barrier: partial reflection (travels back left)
3. Inside barrier: wave decays as $e^{-\kappa x}$
4. On right side: packet emerges with reduced amplitude

**Key Observation:** All of this happens in **real time** - watch the animation!

### WKB vs Numerical

The simulation compares:
- **WKB Approximation:** Quick analytical estimate
- **Numerical:** Exact solution by time-dependent Schrödinger evolution

Usually agree within 10-20% for "not-too-thin" barriers.

### Real-World Examples

**1. Alpha Decay (Radioactive Decay)**
- Alpha particle in nucleus experiences Coulomb + nuclear potential
- Can tunnel through Coulomb barrier!
- Decay rates vary exponentially: $\lambda \propto e^{-2\gamma}$

$$^{238}\text{U} \to ^{234}\text{Th} + \alpha \quad \tau_{1/2} = 4.5 \times 10^9 \text{ years}$$

**2. Scanning Tunneling Microscope (STM)**
- Metal tip approaches surface within $\sim 1$ nm
- Electrons tunnel from tip through vacuum barrier (Coulomb potential) to surface
- Tunnel current: $I \propto e^{-2\kappa d}$ where $d$ is separation
- Sensitivity: $d$ changes by 1 Å → current changes by factor of 10!

**3. Fusion Reactions**
- Two nuclei approach each other
- Coulomb repulsion creates barrier
- Only fraction tunneling through can fuse
- Sun's fusion rate is $\sim 10^{50} \times$ lower than if classical physics applied!

### Classroom Demo

**Compare different scenarios:**
```python
from quantum_playground.animations import TunnelingSimulation

scenarios = [
    ("Easy", {"barrier_height": 3.0, "particle_energy": 2.5}),
    ("Moderate", {"barrier_height": 5.0, "particle_energy": 3.0}),
    ("Hard", {"barrier_height": 10.0, "particle_energy": 3.0}),
    ("Very Hard", {"barrier_height": 20.0, "particle_energy": 3.0}),
]

for label, params in scenarios:
    sim = TunnelingSimulation(**params)
    T_wkb = sim.estimate_wkb_transmission()
    print(f"{label:12} T ≈ {T_wkb:.1%}")
```

Expected output:
```
Easy         T ≈ 49.3%
Moderate     T ≈ 12.3%
Hard         T ≈ 0.16%
Very Hard    T ≈ 0.00001%
```

### Quantum vs Classical

| Feature | Classical | Quantum |
|---------|-----------|---------|
| **E < V₀** | Particle bounces back (T=0) | Can tunnel (T>0) |
| **Decay** | Abrupt at barrier edge | Exponential decay |
| **Probability** | At classical turning points | Extends beyond them |
| **Time behavior** | Bounces repeatedly | Slowly tunnels through |

---

## 5. SUGGESTED LESSON SEQUENCES

### One-Week Unit (5 × 90-min lectures)

**Monday:**
- Lecture: Infinite well, mathematical setup, boundary conditions
- Demo: `python -m quantum_playground infinite`
- HW: Derive energy formula, verify numerically

**Tuesday:**
- Lecture: Eigenvalue problems, numerical methods (finite differences)
- Lab: Run simulations with different well widths, compare energies
- Discussion: Why are we using numerical methods?

**Wednesday:**
- Lecture: Finite well, evanescent waves, transcendental equations
- Demo: Compare infinite vs finite
- HW: Estimate number of bound states for given $V_0, a$

**Thursday:**
- Lecture: Harmonic oscillator, zero-point energy, coherent states
- Demo: SHO animation, compare classical probability
- Lab: Verify energy spacing, measure uncertainty products

**Friday:**
- Lecture: Tunneling, WKB approximation, real-world applications
- Demo: Tunneling animation, transmission coefficient comparison
- Project: STM, alpha decay, fusion examples
- Final quiz on all four systems

### Two-Week Intensive (with Jupyter)

Add interactive Jupyter notebooks where students:
1. Modify Hamiltonian (change mass, frequency)
2. Add perturbations
3. Plot eigenvalues vs parameter
4. Animate transitions

### Integration with Textbook

- **Chapter 2** (Schrödinger Equation) → Infinite well demo
- **Chapter 5** (Potentials) → Infinite + finite well
- **Chapter 7** (SHO) → HO demo, coherent states
- **Chapter 13** (Scattering) → Tunneling demo, WKB

---

## 6. ASSESSMENT RUBRIC

### Simulation Projects (100 points)

**Parameter Exploration (30 pts)**
- Vary one parameter systematically
- Plot results (e.g., $E_n$ vs $V_0$)
- Write 1-page analysis

**Numerical Verification (40 pts)**
- Compare simulation with analytical formula
- Calculate percent error
- Discuss sources of discrepancy
- Tune grid resolution for accuracy

**Presentation (30 pts)**
- Create 3-5 slide deck with animations
- Explain key physics insights
- Answer conceptual questions
- Show understanding of underlying math

### Sample Student Questions

1. "My finite well has 7 bound states but theory predicts 5. Why?"
   - Answer: Check barrier height! May be misreading units.

2. "Why does the infinite well animation show changing energy?"
   - Answer: Energy is constant; what oscillates is the phase. The animation shows $|\psi|^2 \propto |e^{-iEt/\hbar}|^2 = const$, so you're seeing numerical noise or a phase-modulated visualization.

3. "How can tunneling be both possible and exponentially suppressed?"
   - Answer: Both! T > 0 (possible) but T ≪ 1 (extremely rare). For macroscopic barriers, T ≈ 0 classically; for atomic-scale barriers, T can be significant.

---

## 7. FURTHER EXPLORATION

### Advanced Topics

1. **2D Systems**
   - Particle in 2D box → rectangular drum
   - Can have degeneracies
   - Interesting nodal patterns

2. **Double Well**
   - Splitting due to tunneling
   - Ammonia inversion (NH₃)
   - Energy splitting goes as $e^{-2\gamma}$

3. **Time-Dependent Perturbation**
   - Apply AC electric field to HO
   - Driven oscillations
   - Resonance condition

4. **Semiclassical WKB**
   - Connection formulas
   - Quantization condition via WKB
   - Bohr-Sommerfeld orbits

### Extensions

- 3D visualization (balls as probability density volumes)
- Interactive Plotly/Dash web app
- GPU acceleration for 2D systems
- Export to Blender for movie production

---

## References

1. **Griffiths, D. J.** (2018). *Introduction to Quantum Mechanics* (3rd ed.). Cambridge University Press.
   - Chapter 2: Schrödinger's Equation
   - Chapter 5: Identical Particles

2. **Shankar, R.** (1994). *Principles of Quantum Mechanics* (2nd ed.). Plenum Press.
   - Chapter 5: Oscillator and Hydrogen Atom
   - Chapter 6: Variational & WKB

3. **Tannor, D. J.** (2007). *Introduction to Quantum Mechanics* (Time-Dependent Perspective). University Science Books.
   - Chapter 2-3: Wave packets and evolution

4. **Feynman, R. P., Leighton, R. B., & Sands, M.** (1963). *Feynman Lectures on Physics*, Vol. III.
   - Intuitive explanations of quantum phenomena

5. **WKB Approximation:** [Comprehensive review](https://en.wikipedia.org/wiki/WKB_approximation)

---

**Created for:** Undergraduate Quantum Mechanics II (3rd year)  
**Duration:** 1-2 weeks, 3-6 contact hours + lab/homework  
**Prerequisites:** Linear algebra, Calculus, Introductory Quantum Mechanics

Good luck with your lectures! 🎓⚛️
