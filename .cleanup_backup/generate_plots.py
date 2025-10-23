#!/usr/bin/env python
"""
Simple plot generator for quantum simulations.
Generates only static PNG plots (no videos) for quick testing.
"""

import sys
sys.path.insert(0, '/workspaces/animation_quantum_mech_basics/src')

import os
import argparse
from pathlib import Path

def generate_plots(output_dir='outputs', systems='all'):
    """Generate all quantum system plots."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    from quantum_playground.animations import (
        InfiniteWellSimulation,
        FiniteWellSimulation,
        HarmonicOscillatorSimulation,
        TunnelingSimulation
    )
    import matplotlib
    matplotlib.use('Agg')
    
    print("\n" + "=" * 80)
    print("QUANTUM MECHANICS VISUALIZATION SUITE")
    print("=" * 80)
    
    try:
        # Infinite Well
        if systems in ['all', 'infinite']:
            print("\n[1/4] Generating Infinite Potential Well plot...")
            sim = InfiniteWellSimulation(well_width=2.0, num_levels=6, num_points=256)
            path = os.path.join(output_dir, '01_infinite_well.png')
            sim.plot_overview(save_path=path)
            print(f"      ✓ Saved: {path}")
        
        # Finite Well
        if systems in ['all', 'finite']:
            print("\n[2/4] Generating Finite Potential Well plot...")
            sim = FiniteWellSimulation(well_width=2.0, barrier_height=10.0, num_levels=6, num_points=256)
            path = os.path.join(output_dir, '02_finite_well.png')
            sim.plot_comparison(save_path=path)
            print(f"      ✓ Saved: {path}")
        
        # Harmonic Oscillator
        if systems in ['all', 'harmonic']:
            print("\n[3/4] Generating Harmonic Oscillator plot...")
            sim = HarmonicOscillatorSimulation(mass=1.0, omega=1.0, num_levels=6, num_points=256)
            path = os.path.join(output_dir, '03_harmonic_oscillator.png')
            sim.plot_overview(save_path=path)
            print(f"      ✓ Saved: {path}")
        
        # Tunneling
        if systems in ['all', 'tunneling']:
            print("\n[4/4] Generating Tunneling Analysis plot...")
            sim = TunnelingSimulation(barrier_height=5.0, barrier_width=0.5, particle_energy=3.0, num_points=512, dt=0.02)
            traj = sim.run_evolution(num_steps=200)
            path = os.path.join(output_dir, '04_tunneling_analysis.png')
            sim.plot_transmission_analysis(traj, save_path=path)
            print(f"      ✓ Saved: {path}")
        
        print("\n" + "=" * 80)
        print("✓ All plots generated successfully!")
        print("=" * 80)
        print(f"\nResults saved to: {os.path.abspath(output_dir)}")
        print("\n📖 To view plots in VS Code:")
        print("   1. Open the Explorer sidebar (Ctrl+Shift+E)")
        print("   2. Navigate to the outputs/ folder")
        print("   3. Click on any PNG file to view it")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate quantum mechanics visualization plots",
        epilog="""
Examples:
  python generate_plots.py                  # All plots
  python generate_plots.py infinite         # Just infinite well
  python generate_plots.py all --output ~/Desktop
        """
    )
    
    parser.add_argument(
        'systems',
        nargs='?',
        default='all',
        choices=['all', 'infinite', 'finite', 'harmonic', 'tunneling'],
        help='Which systems to visualize (default: all)'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        default='outputs',
        help='Output directory (default: outputs/)'
    )
    
    args = parser.parse_args()
    
    success = generate_plots(args.output, args.systems)
    sys.exit(0 if success else 1)
