"""
Infinite Potential Well (Particle in a Box) Simulation and Visualization.

Demonstrates:
- Discrete energy levels
- Standing wave patterns (stationary states)
- Probability density as a function of quantum number
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from typing import Tuple
import os

from quantum_playground.potentials import InfiniteSquareWell
from quantum_playground.solvers import QuantumGrid, StationarySolver


class InfiniteWellSimulation:
    """Simulation of infinite potential well."""

    def __init__(
        self,
        well_width: float = 2.0,
        x_min: float = -1.5,
        x_max: float = 1.5,
        num_points: int = 256,
        num_levels: int = 5,
    ):
        """
        Initialize infinite well simulation.

        Args:
            well_width: Width of the well
            x_min, x_max: Spatial domain boundaries
            num_points: Grid resolution
            num_levels: Number of energy levels to compute
        """
        self.well_width = well_width
        self.num_levels = num_levels

        # Create grid and potential
        self.grid = QuantumGrid(x_min, x_max, num_points)
        self.x = self.grid.x
        self.dx = self.grid.dx

        # For infinite well, enforce boundary conditions in solver
        # Create soft-wall potential (smoothly confines particle)
        well_center = (x_min + x_max) / 2
        half_width = well_width / 2
        self.potential = self._create_soft_well_potential()

        # Solve eigenvalue problem
        self.solver = StationarySolver(self.grid, mass=1.0)
        self.eigenvalues, self.eigenvectors = self.solver.solve_eigenproblem(
            self.potential, num_eigenvalues=num_levels + 2
        )

        # Filter to bound states only
        self.eigenvalues = self.eigenvalues[:num_levels]
        self.eigenvectors = self.eigenvectors[:, :num_levels]

    def _create_soft_well_potential(self) -> np.ndarray:
        """Create smooth confining potential that approximates infinite well."""
        well_center = (self.x[0] + self.x[-1]) / 2
        half_width = self.well_width / 2
        distance_from_center = np.abs(self.x - well_center)

        # Smooth potential that rises steeply outside well
        V = np.zeros_like(self.x)
        outside_well = distance_from_center > half_width
        V[outside_well] = 50.0 * (distance_from_center[outside_well] - half_width) ** 2

        return V

    def get_analytical_energies(self) -> np.ndarray:
        """
        Compute analytical energy levels for infinite well.

        E_n = (n²π²ħ²)/(2mL²)
        In atomic units (ħ=1, m=1): E_n = (n²π²)/(2L²)
        """
        n = np.arange(1, self.num_levels + 1)
        return (n ** 2 * np.pi ** 2) / (2 * self.well_width ** 2)

    def plot_overview(self, save_path: str = None) -> None:
        """
        Create a comprehensive overview figure showing:
        - Potential profile
        - First few eigenstates
        - Energy ladder
        - Probability densities
        """
        fig = plt.figure(figsize=(14, 10))
        gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

        # 1. Potential and eigenstates
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(self.x, self.potential, "k-", linewidth=2, label="Potential V(x)")
        ax1.axhline(0, color="gray", linestyle="--", alpha=0.3)

        # Plot first 3 eigenstates
        for i in range(min(3, self.num_levels)):
            psi = self.eigenvectors[:, i]
            E = self.eigenvalues[i]
            # Shift eigenstates by their energy for visualization
            ax1.plot(self.x, np.abs(psi) + E, label=f"n={i+1}, E={E:.3f}")
            ax1.axhline(E, color="gray", linestyle=":", alpha=0.3)

        ax1.set_xlabel("Position x", fontsize=11)
        ax1.set_ylabel("Energy / |ψ|", fontsize=11)
        ax1.set_title("Infinite Potential Well: Eigenstates Overlaid on Potential", fontsize=12, fontweight="bold")
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # 2. Energy level diagram
        ax2 = fig.add_subplot(gs[1, 0])
        analytical_E = self.get_analytical_energies()
        numerical_E = self.eigenvalues[:len(analytical_E)]

        x_levels = np.array([0.5, 1.5])
        for i, (E_num, E_ana) in enumerate(zip(numerical_E, analytical_E)):
            ax2.hlines(E_num, x_levels[0] - 0.2, x_levels[0] + 0.2, colors="blue", linewidth=2)
            ax2.hlines(E_ana, x_levels[1] - 0.2, x_levels[1] + 0.2, colors="red", linewidth=2)
            ax2.text(x_levels[0], E_num + 0.2, f"n={i+1}", ha="center", fontsize=9)

        ax2.set_xlim(0, 2)
        ax2.set_ylabel("Energy", fontsize=11)
        ax2.set_title("Energy Levels: Numerical vs Analytical", fontsize=12, fontweight="bold")
        ax2.set_xticks([0.5, 1.5])
        ax2.set_xticklabels(["Numerical", "Analytical"])
        ax2.grid(True, alpha=0.3, axis="y")

        # Add legend
        from matplotlib.lines import Line2D

        legend_elements = [Line2D([0], [0], color="blue", lw=2, label="Numerical"),
                          Line2D([0], [0], color="red", lw=2, label="Analytical")]
        ax2.legend(handles=legend_elements, fontsize=9)

        # 3. Probability densities
        ax3 = fig.add_subplot(gs[1, 1])
        for i in range(min(5, self.num_levels)):
            prob_density = self.solver.probability_density(self.eigenvectors[:, i])
            ax3.plot(self.x, prob_density, linewidth=2, label=f"n={i+1}")

        ax3.set_xlabel("Position x", fontsize=11)
        ax3.set_ylabel("|ψ(x)|²", fontsize=11)
        ax3.set_title("Probability Densities", fontsize=12, fontweight="bold")
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)

        # 4. Wavefunction amplitude and phase
        ax4 = fig.add_subplot(gs[2, :])
        i = 2  # Show n=3 state
        psi = self.eigenvectors[:, i]
        phase = np.angle(psi)

        ax4_twin = ax4.twinx()

        line1 = ax4.plot(self.x, np.real(psi), "b-", linewidth=2, label="Re[ψ]")
        line2 = ax4.plot(self.x, np.imag(psi), "g-", linewidth=2, label="Im[ψ]")
        line3 = ax4_twin.plot(self.x, phase, "r--", linewidth=2, alpha=0.7, label="Phase[ψ]")

        ax4.set_xlabel("Position x", fontsize=11)
        ax4.set_ylabel("Wavefunction", fontsize=11, color="black")
        ax4_twin.set_ylabel("Phase (radians)", fontsize=11, color="red")
        ax4.set_title(f"Wavefunction for n=3: Real, Imaginary, and Phase", fontsize=12, fontweight="bold")

        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax4.legend(lines, labels, fontsize=9, loc="upper right")
        ax4.grid(True, alpha=0.3)

        plt.suptitle("Infinite Potential Well Analysis", fontsize=14, fontweight="bold", y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Saved figure to {save_path}")

        return fig

    def animate_eigenstates(
        self,
        num_frames: int = 100,
        save_path: str = None,
        fps: int = 30,
    ) -> animation.FuncAnimation:
        """
        Create animation showing probability density evolution for multiple eigenstates.

        Args:
            num_frames: Number of animation frames
            save_path: Path to save animation (if None, only displays)
            fps: Frames per second for saved animation

        Returns:
            Animation object
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axes = axes.flatten()

        # Prepare data for first 4 eigenstates
        states_to_show = min(4, self.num_levels)
        prob_densities = [
            self.solver.probability_density(self.eigenvectors[:, i])
            for i in range(states_to_show)
        ]
        energies = self.eigenvalues[:states_to_show]

        lines = []
        fills = []
        titles = []

        for idx, ax in enumerate(axes[:states_to_show]):
            (line,) = ax.plot([], [], "b-", linewidth=2)
            fill = ax.fill_between([], [], alpha=0.3)
            lines.append(line)
            fills.append(fill)

            ax.set_xlim(self.x[0], self.x[-1])
            ax.set_ylim(0, np.max(prob_densities) * 1.1)
            ax.set_xlabel("Position x")
            ax.set_ylabel("|ψ(x)|²")
            ax.set_title(f"State n={idx+1}, E={energies[idx]:.3f}")
            ax.grid(True, alpha=0.3)

        frame_text = fig.text(0.5, 0.02, "", ha="center", fontsize=11)

        def animate(frame):
            phase = 2 * np.pi * frame / num_frames
            for i in range(states_to_show):
                # Modulate amplitude with phase (visual effect)
                amplitude = 0.7 + 0.3 * np.cos(phase + energies[i])
                prob_dens = prob_densities[i] * amplitude

                lines[i].set_data(self.x, prob_dens)

                # Update fill
                axes[i].clear()
                axes[i].fill_between(self.x, 0, prob_dens, alpha=0.3, color="blue")
                axes[i].plot(self.x, prob_dens, "b-", linewidth=2)
                axes[i].axhline(0, color="k", linewidth=0.5)
                axes[i].set_xlim(self.x[0], self.x[-1])
                axes[i].set_ylim(0, np.max(prob_densities) * 1.1)
                axes[i].set_xlabel("Position x")
                axes[i].set_ylabel("|ψ(x)|²")
                axes[i].set_title(f"State n={i+1}, E={energies[i]:.3f}")
                axes[i].grid(True, alpha=0.3)

            frame_text.set_text(f"Frame: {frame+1}/{num_frames}")
            return lines + [frame_text]

        anim = animation.FuncAnimation(
            fig, animate, frames=num_frames, interval=33, blit=False, repeat=True
        )

        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer="ffmpeg", fps=fps, dpi=100)
            print(f"Animation saved to {save_path}")

        plt.suptitle("Infinite Potential Well: Stationary State Oscillations", fontsize=13, fontweight="bold")
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])

        return anim


def main():
    """Run infinite well simulation and generate outputs."""
    import sys
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("INFINITE POTENTIAL WELL SIMULATION")
    print("=" * 70)

    # Create simulation
    sim = InfiniteWellSimulation(well_width=2.0, num_levels=8)

    # Generate overview plot
    print("\nGenerating overview plot...")
    overview_path = os.path.join(output_dir, "infinite_well_overview.png")
    sim.plot_overview(save_path=overview_path)
    print(f"✓ Saved to {overview_path}")

    # Generate animation
    print("\nGenerating animation...")
    anim_path = os.path.join(output_dir, "infinite_well_animation.mp4")
    sim.animate_eigenstates(num_frames=100, save_path=anim_path, fps=30)
    print(f"✓ Saved to {anim_path}")

    print("\n" + "=" * 70)
    print("Simulation complete!")
    print("=" * 70)

    plt.show()


if __name__ == "__main__":
    main()
