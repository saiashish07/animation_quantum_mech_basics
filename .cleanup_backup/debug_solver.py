#!/usr/bin/env python
"""
Debug script to test quantum solver step-by-step.
"""

import sys
sys.path.insert(0, '/workspaces/animation_quantum_mech_basics/src')

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as sp_linalg

print("=" * 80)
print("DEBUGGING QUANTUM SOLVER")
print("=" * 80)

# Test 1: Simple particle in a box with soft wall potential
print("\n[TEST 1] Soft Wall Potential (Smooth Confinement)")
print("-" * 80)

x_min, x_max = -1.0, 1.0
N = 128
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

print(f"Grid: x ∈ [{x_min}, {x_max}], N={N}, dx={dx:.6f}")

# Kinetic energy matrix: T = -ℏ²/(2m) d²/dx²
# In atomic units: T = -1/2 d²/dx²
# Finite difference: d²ψ/dx² ≈ [ψ(i+1) - 2ψ(i) + ψ(i-1)] / dx²
hbar_sq_over_2m = 0.5
coeff = hbar_sq_over_2m / (dx ** 2)

diagonals = [
    np.ones(N - 1) * coeff,      # superdiagonal
    np.ones(N) * (-2.0 * coeff),  # main diagonal
    np.ones(N - 1) * coeff,      # subdiagonal
]
T = sparse.diags(diagonals, offsets=[1, 0, -1], shape=(N, N))
T = T.tocsr()

print(f"Kinetic energy coefficient: {coeff:.6f}")
print(f"Kinetic energy matrix: shape={T.shape}, nnz={T.nnz}")

# Soft wall potential: V(x) = λ(|x| - x0)² for |x| > x0
well_width = 2.0  # Total width
half_width = well_width / 2
lambda_param = 50.0

V_array = np.zeros(N)
for i, xi in enumerate(x):
    if abs(xi) > half_width:
        V_array[i] = lambda_param * (abs(xi) - half_width) ** 2

V = sparse.diags(V_array, offsets=0, shape=(N, N))
V = V.tocsr()

print(f"Potential: V_min={V_array.min():.6f}, V_max={V_array.max():.6f}")
print(f"Potential at boundaries: V(±1.0)={V_array[0]:.6f}")

# Full Hamiltonian
H = T + V
print(f"Hamiltonian: shape={H.shape}, nnz={H.nnz}")

# Solve eigenvalue problem
print("\nSolving eigenvalue problem (3 lowest states)...")
try:
    E, psi = sp_linalg.eigsh(H, k=3, which='SM', return_eigenvectors=True)
    print(f"✓ Eigenvalue solve successful!")
    print(f"  Eigenvalues (numerical): {E}")
    
    # Analytical solution for infinite square well (approximate)
    # E_n ≈ (n²π²)/(2L²) for large well-depth
    # But we're using soft wall, so it won't match exactly
    # Just check that energies are positive and in reasonable range
    
    if np.all(E > 0):
        print("  ✓ All eigenvalues are positive!")
    else:
        print(f"  ✗ ERROR: Negative eigenvalues! {E}")
        
    if np.all(np.diff(E) > 0):
        print("  ✓ Eigenvalues are properly ordered")
    else:
        print(f"  ✗ ERROR: Eigenvalues not ordered! dE={np.diff(E)}")
        
except Exception as e:
    print(f"✗ Error solving eigenvalues: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Check eigenvector properties
print("\n[TEST 2] Eigenvector Properties")
print("-" * 80)

print(f"Eigenvector shape: {psi.shape}")
print(f"Eigenvector dtype: {psi.dtype}")

# Check orthonormality
print("\nOrthonormality check (∫ψ_i* ψ_j dx = δ_ij):")
for i in range(min(3, psi.shape[1])):
    for j in range(min(3, psi.shape[1])):
        overlap = np.sum(psi[:, i] * psi[:, j]) * dx
        if i == j:
            print(f"  ⟨{i}|{j}⟩ = {overlap:.6f} (should be ≈ 1.0)")
        else:
            print(f"  ⟨{i}|{j}⟩ = {overlap:.2e} (should be ≈ 0.0)")

# Test 3: Virial theorem check
print("\n[TEST 3] Expectation Values")
print("-" * 80)

for i in range(min(3, psi.shape[1])):
    psi_i = psi[:, i]
    
    # ⟨E⟩ = ⟨ψ|H|ψ⟩
    Hpsi = H @ psi_i
    E_expect = np.sum(psi_i * Hpsi) * dx
    
    # ⟨T⟩ = ⟨ψ|T|ψ⟩
    Tpsi = T @ psi_i
    T_expect = np.sum(psi_i * Tpsi) * dx
    
    # ⟨V⟩ = ⟨ψ|V|ψ⟩
    V_expect = np.sum(psi_i * (V @ psi_i)) * dx
    
    print(f"State n={i+1}:")
    print(f"  E_eigenvalue = {E[i]:.6f}")
    print(f"  ⟨E⟩ = {E_expect:.6f}")
    print(f"  ⟨T⟩ = {T_expect:.6f}")
    print(f"  ⟨V⟩ = {V_expect:.6f}")
    print(f"  ⟨T⟩ + ⟨V⟩ = {T_expect + V_expect:.6f}")

print("\n" + "=" * 80)
print("DEBUG COMPLETE")
print("=" * 80 + "\n")
