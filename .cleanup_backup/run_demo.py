#!/usr/bin/env python
"""
Simple demonstration of running quantum simulations in codespace
"""

import sys
sys.path.insert(0, '/workspaces/animation_quantum_mech_basics/src')

print("\n" + "=" * 80)
print("🚀 QUANTUM MECHANICS SIMULATIONS - CODESPACE DEMO")
print("=" * 80)

try:
    # Step 1: Import libraries
    print("\n[1/5] Importing quantum_playground modules...")
    from quantum_playground.animations import (
        InfiniteWellSimulation,
        FiniteWellSimulation,
        HarmonicOscillatorSimulation,
        TunnelingSimulation
    )
    print("      ✅ All modules imported successfully!")
    
    # Step 2: Create output directory
    import os
    print("\n[2/5] Creating outputs directory...")
    os.makedirs('outputs', exist_ok=True)
    print("      ✅ outputs/ directory ready")
    
    # Step 3: Run infinite well
    print("\n[3/5] Creating Infinite Potential Well simulation...")
    print("      Running solver...")
    sim_iw = InfiniteWellSimulation(well_width=2.0, num_levels=6, num_points=200)
    print("      ✅ Solver complete")
    print(f"      📊 Found {len(sim_iw.eigenvalues)} energy levels")
    print(f"      ⚡ Energies: {[f'{E:.2f}' for E in sim_iw.eigenvalues[:3]]} ...")
    
    # Step 4: Run harmonic oscillator
    print("\n[4/5] Creating Harmonic Oscillator simulation...")
    print("      Running solver...")
    sim_ho = HarmonicOscillatorSimulation(mass=1.0, omega=1.0, num_levels=6, num_points=200)
    print("      ✅ Solver complete")
    print(f"      📊 Found {len(sim_ho.eigenvalues)} energy levels")
    analytical_E = [(n + 0.5) for n in range(3)]
    numerical_E = list(sim_ho.eigenvalues[:3])
    print(f"      ⚡ Numerical:  {[f'{E:.2f}' for E in numerical_E]}")
    print(f"      ⚡ Analytical: {[f'{E:.2f}' for E in analytical_E]}")
    
    # Step 5: Run tunneling
    print("\n[5/5] Creating Tunneling simulation...")
    print("      Creating barrier potential...")
    sim_tunnel = TunnelingSimulation(
        barrier_height=5.0,
        barrier_width=0.5,
        particle_energy=3.0,
        num_points=256,
        dt=0.02
    )
    print("      Running wave packet evolution (100 steps)...")
    traj = sim_tunnel.run_evolution(num_steps=100)
    print("      ✅ Evolution complete")
    analysis = sim_tunnel.analyze_transmission(traj)
    print(f"      📊 Transmission: {analysis['T_numerical']:.1%}")
    print(f"      📊 WKB estimate: {analysis['T_wkb']:.1%}")
    print(f"      📊 Reflection:   {analysis['R_numerical']:.1%}")
    
    # Success message
    print("\n" + "=" * 80)
    print("✅ ALL SIMULATIONS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📝 Summary:")
    print("   ✓ Infinite well solver: Working")
    print("   ✓ Harmonic oscillator solver: Working")
    print("   ✓ Tunneling solver: Working")
    print("\n🎯 Next Steps in Codespace:")
    print("   1. Generate PNG plots:")
    print("      python -m quantum_playground infinite")
    print("   2. View outputs:")
    print("      - Open outputs/*.png in VS Code image viewer")
    print("   3. Generate animations (takes 5-10 min):")
    print("      python -m quantum_playground all")
    print("   4. Download outputs/ folder to your computer")
    print("      and play MP4 videos")
    print("\n🌐 Or use Jupyter for interactive exploration:")
    print("   pip install jupyter")
    print("   jupyter lab --ip=0.0.0.0 --no-browser")
    print("\n" + "=" * 80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
