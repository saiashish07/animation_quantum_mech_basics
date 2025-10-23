#!/usr/bin/env python
"""
Quick test runner for quantum mechanics simulations in codespace
Run this to verify everything works!
"""

import sys
sys.path.insert(0, '/workspaces/animation_quantum_mech_basics/src')

print("🔬 Quantum Mechanics Simulation - Quick Test")
print("=" * 70)

try:
    print("\n✓ Importing quantum_playground...")
    from quantum_playground.solvers import QuantumGrid, StationarySolver
    from quantum_playground.potentials import InfiniteSquareWell
    import numpy as np
    
    print("✓ All imports successful!")
    
    print("\n✓ Creating grid...")
    grid = QuantumGrid(-1.5, 1.5, 128)
    print(f"  Grid points: {grid.num_points}")
    print(f"  Spacing: dx = {grid.dx:.6f}")
    
    print("\n✓ Creating infinite well potential...")
    well = InfiniteSquareWell(width=2.0)
    V = well(grid.x)
    print(f"  Potential shape: {V.shape}")
    
    print("\n✓ Solving Schrödinger equation...")
    solver = StationarySolver(grid, mass=1.0)
    E, psi = solver.solve_eigenproblem(V, num_eigenvalues=3)
    print(f"  Energy levels: {E[:3]}")
    
    print("\n✓ Computing analytical energies...")
    L = 2.0
    E_analytical = np.array([n**2 * np.pi**2 / (2 * L**2) for n in range(1, 4)])
    print(f"  Analytical:   {E_analytical}")
    
    errors = np.abs(E[:3] - E_analytical) / E_analytical * 100
    errors_str = ", ".join([f"{e:.1f}%" for e in errors])
    print(f"  Errors:       {errors_str}")
    
    if np.all(errors < 5):
        print("\n✅ All tests PASSED!")
        print("=" * 70)
        print("\n🎉 Your system is ready to run full simulations!")
        print("\nNext steps:")
        print("  1. python -m quantum_playground infinite")
        print("  2. python -m quantum_playground finite")
        print("  3. python -m quantum_playground harmonic")
        print("  4. python -m quantum_playground tunneling")
        print("\nOr run all at once:")
        print("  python -m quantum_playground all")
        
    else:
        print("\n⚠️  Some errors are larger than expected")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
