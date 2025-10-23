#!/usr/bin/env python
"""
Main runner for quantum mechanics simulations.

Usage:
    python -m quantum_playground [scenario] [options]

Scenarios:
    - infinite    : Infinite potential well
    - finite      : Finite potential well
    - harmonic    : Quantum harmonic oscillator
    - tunneling   : Quantum tunneling through barrier
    - all         : Run all simulations
"""

import argparse
import sys
from pathlib import Path

# Import simulation classes
from quantum_playground.animations.infinite_well import InfiniteWellSimulation
from quantum_playground.animations.finite_well import FiniteWellSimulation
from quantum_playground.animations.harmonic_oscillator import HarmonicOscillatorSimulation
from quantum_playground.animations.tunneling import TunnelingSimulation


def run_infinite_well(output_dir: Path, skip_animation: bool = False):
    """Run infinite well simulation."""
    print("\n" + "=" * 80)
    print("INFINITE POTENTIAL WELL SIMULATION")
    print("=" * 80)

    sim = InfiniteWellSimulation(well_width=2.0, num_levels=8, num_points=256)

    print("\n[1/2] Generating overview plot...")
    overview_path = output_dir / "infinite_well_overview.png"
    sim.plot_overview(save_path=str(overview_path))

    if not skip_animation:
        print("[2/2] Generating animation...")
        anim_path = output_dir / "infinite_well_animation.mp4"
        sim.animate_eigenstates(num_frames=100, save_path=str(anim_path), fps=30)


def run_finite_well(output_dir: Path, skip_animation: bool = False):
    """Run finite well simulation."""
    print("\n" + "=" * 80)
    print("FINITE POTENTIAL WELL SIMULATION")
    print("=" * 80)

    sim = FiniteWellSimulation(
        well_width=2.0,
        barrier_height=10.0,
        num_levels=6,
        num_points=256,
    )

    print("\n[1/2] Generating comparison plot...")
    comp_path = output_dir / "finite_well_comparison.png"
    sim.plot_comparison(save_path=str(comp_path))

    if not skip_animation:
        print("[2/2] Generating animation...")
        anim_path = output_dir / "finite_well_animation.mp4"
        sim.animate_state_with_penetration(state_index=0, num_frames=100, save_path=str(anim_path), fps=30)


def run_harmonic_oscillator(output_dir: Path, skip_animation: bool = False):
    """Run harmonic oscillator simulation."""
    print("\n" + "=" * 80)
    print("QUANTUM HARMONIC OSCILLATOR SIMULATION")
    print("=" * 80)

    sim = HarmonicOscillatorSimulation(mass=1.0, omega=1.0, num_levels=8, num_points=256)

    print("\n[1/2] Generating overview plot...")
    overview_path = output_dir / "harmonic_oscillator_overview.png"
    sim.plot_overview(save_path=str(overview_path))

    if not skip_animation:
        print("[2/2] Generating animation...")
        anim_path = output_dir / "harmonic_oscillator_animation.mp4"
        import numpy as np

        coeffs = np.array([1.0, 1.0, 0.3])
        sim.animate_superposition(coefficients=coeffs, num_frames=150, save_path=str(anim_path), fps=30)


def run_tunneling(output_dir: Path, skip_animation: bool = False):
    """Run tunneling simulation."""
    print("\n" + "=" * 80)
    print("QUANTUM TUNNELING SIMULATION")
    print("=" * 80)

    sim = TunnelingSimulation(
        barrier_height=5.0,
        barrier_width=0.5,
        particle_energy=3.0,
        num_points=512,
        dt=0.01,
    )

    print("\n[1/3] Running wave packet evolution...")
    trajectory = sim.run_evolution(num_steps=800)

    print("[2/3] Generating analysis figure...")
    analysis_path = output_dir / "tunneling_analysis.png"
    sim.plot_transmission_analysis(trajectory, save_path=str(analysis_path))

    if not skip_animation:
        print("[3/3] Generating animation...")
        anim_path = output_dir / "tunneling_animation.mp4"
        sim.animate_tunneling(trajectory, num_display_frames=150, save_path=str(anim_path), fps=30)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Quantum Mechanics Simulations: Explore 4 quantum systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m quantum_playground infinite
  python -m quantum_playground all --no-animation
  python -m quantum_playground tunneling --output ~/Desktop/quantum_sims
        """,
    )

    parser.add_argument(
        "scenario",
        nargs="?",
        default="all",
        choices=["infinite", "finite", "harmonic", "tunneling", "all"],
        help="Which simulation to run (default: all)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("outputs"),
        help="Output directory for results (default: ./outputs)",
    )

    parser.add_argument(
        "--no-animation",
        action="store_true",
        help="Skip animation generation (only create static plots)",
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "QUANTUM MECHANICS SIMULATION SUITE" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")

    print(f"\nOutput directory: {output_dir.resolve()}")

    try:
        if args.scenario in ["infinite", "all"]:
            run_infinite_well(output_dir, skip_animation=args.no_animation)

        if args.scenario in ["finite", "all"]:
            run_finite_well(output_dir, skip_animation=args.no_animation)

        if args.scenario in ["harmonic", "all"]:
            run_harmonic_oscillator(output_dir, skip_animation=args.no_animation)

        if args.scenario in ["tunneling", "all"]:
            run_tunneling(output_dir, skip_animation=args.no_animation)

        print("\n" + "=" * 80)
        print("✓ All simulations completed successfully!")
        print("=" * 80)
        print(f"\nResults saved to: {output_dir.resolve()}")

    except Exception as e:
        print(f"\n❌ Error during simulation: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
