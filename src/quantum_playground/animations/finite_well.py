"""
Finite Potential Well Simulation and Visualization.

Demonstrates:
- Bound states with wavefunction penetration
- Evanescent tails outside the well
- Comparison with infinite well (same width)
- Energy shift due to finite barrier
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LogNorm
import os

from quantum_playground.potentials import FiniteSquareWell, InfiniteSquareWell
from quantum_playground.solvers import QuantumGrid, StationarySolver


class FiniteWellSimulation:
    """Simulation of finite potential well."""

    def __init__(
        self,
        well_width: float = 2.0,
        barrier_height: float = 10.0,
        x_min: float = -3.0,
        x_max: float = 3.0,
        num_points: int = 256,
        num_levels: int = 5,
    ):
        """
        Initialize finite well simulation.

        Args:
            well_width: Width of the well
            barrier_height: Height of potential barrier outside well
            x_min, x_max: Spatial domain
            num_points: Grid resolution
            num_levels: Number of energy levels
        """
        self.well_width = well_width
        self.barrier_height = barrier_height
        self.num_levels = num_levels

        # Create grid
        self.grid = QuantumGrid(x_min, x_max, num_points)
        self.x = self.grid.x
        self.dx = self.grid.dx

        # Create finite well potential
        finite_well = FiniteSquareWell(well_width, barrier_height)
        self.potential = finite_well(self.x)

        # Create infinite well potential for comparison
        infinite_well = InfiniteSquareWell(well_width)
        self.potential_inf = infinite_well(self.x)

        # Solve finite well
        self.solver = StationarySolver(self.grid, mass=1.0)
        self.eigenvalues, self.eigenvectors = self.solver.solve_eigenproblem(
            self.potential, num_eigenvalues=num_levels + 2
        )

        # Filter to get only the first num_levels bound states
        bound_mask = self.eigenvalues < barrier_height
        if np.sum(bound_mask) >= num_levels:
            bound_indices = np.where(bound_mask)[0][:num_levels]
            self.eigenvalues = self.eigenvalues[bound_indices]
            self.eigenvectors = self.eigenvectors[:, bound_indices]
        else:
            self.eigenvalues = self.eigenvalues[:num_levels]
            self.eigenvectors = self.eigenvectors[:, :num_levels]

        # Solve infinite well for comparison
        # Use higher potential to approximate infinite
        self.solver_inf = StationarySolver(self.grid, mass=1.0)
        V_infinite = np.full_like(self.x, 1e10)
        center = (self.x[0] + self.x[-1]) / 2
        half_width = well_width / 2
        inside_mask = np.abs(self.x - center) < half_width
        V_infinite[inside_mask] = 0
        self.eigenvalues_inf, self.eigenvectors_inf = self.solver_inf.solve_eigenproblem(
            V_infinite, num_eigenvalues=num_levels + 2
        )
        self.eigenvalues_inf = self.eigenvalues_inf[:num_levels]
        self.eigenvectors_inf = self.eigenvectors_inf[:, :num_levels]

    def plot_comparison(self, save_path: str = None) -> None:
        """
        Create comparison figure: finite well vs infinite well.

        Shows:
        - Potentials overlaid
        - Eigenstates for both
        - Energy level diagram
        - Probability penetration depth
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)

        # 1. Potential comparison
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.fill_between(self.x, 0, self.potential, alpha=0.2, color="blue", label="Finite Well V(x)")
        ax1.plot(self.x, self.potential, "b-", linewidth=2)

        # Mark well boundaries
        center = (self.x[0] + self.x[-1]) / 2
        half_width = self.well_width / 2
        ax1.axvline(center - half_width, color="gray", linestyle="--", alpha=0.5)
        ax1.axvline(center + half_width, color="gray", linestyle="--", alpha=0.5)

        ax1.set_xlabel("Position x", fontsize=11)
        ax1.set_ylabel("Potential V(x)", fontsize=11)
        ax1.set_title("Finite Potential Well", fontsize=12, fontweight="bold")
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 2. Energy level comparison
        ax2 = fig.add_subplot(gs[0, 2])
        x_pos = [0.2, 0.8]
        colors_finite = plt.cm.Blues(np.linspace(0.4, 0.9, self.num_levels))
        colors_infinite = plt.cm.Reds(np.linspace(0.4, 0.9, self.num_levels))

        for i in range(self.num_levels):
            ax2.hlines(self.eigenvalues[i], x_pos[0] - 0.15, x_pos[0] + 0.15,
                       colors=colors_finite[i], linewidth=3, label=f"Finite n={i+1}" if i < 2 else "")
            ax2.hlines(self.eigenvalues_inf[i], x_pos[1] - 0.15, x_pos[1] + 0.15,
                       colors=colors_infinite[i], linewidth=3, label=f"Infinite n={i+1}" if i < 2 else "")

        ax2.axhline(self.barrier_height, color="k", linestyle=":", linewidth=2, alpha=0.5, label="Barrier height")
        ax2.set_xlim(-0.1, 1.1)
        ax2.set_ylabel("Energy", fontsize=11)
        ax2.set_title("Energy Levels", fontsize=12, fontweight="bold")
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(["Finite", "Infinite"])
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3, axis="y")

        # 3. Eigenstates for finite well
        ax3 = fig.add_subplot(gs[1, 0])
        for i in range(min(3, self.num_levels)):
            psi = self.eigenvectors[:, i]
            prob = np.abs(psi) ** 2
            ax3.plot(self.x, prob, linewidth=2, label=f"n={i+1}")

        ax3.fill_between(self.x, 0, self.potential / self.barrier_height * np.max(np.abs(self.eigenvectors)**2),
                        alpha=0.1, color="gray")
        ax3.set_xlabel("Position x", fontsize=11)
        ax3.set_ylabel("|ψ(x)|²", fontsize=11)
        ax3.set_title("Finite Well: Probability Density", fontsize=12, fontweight="bold")
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)

        # 4. Eigenstates for infinite well (for comparison)
        ax4 = fig.add_subplot(gs[1, 1])
        for i in range(min(3, self.num_levels)):
            psi = self.eigenvectors_inf[:, i]
            prob = np.abs(psi) ** 2
            ax4.plot(self.x, prob, linewidth=2, label=f"n={i+1}")

        center = (self.x[0] + self.x[-1]) / 2
        half_width = self.well_width / 2
        ax4.axvspan(center - half_width, center + half_width, alpha=0.1, color="gray")
        ax4.set_xlabel("Position x", fontsize=11)
        ax4.set_ylabel("|ψ(x)|²", fontsize=11)
        ax4.set_title("Infinite Well: Probability Density", fontsize=12, fontweight="bold")
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

        # 5. Penetration depth visualization
        ax5 = fig.add_subplot(gs[1, 2])
        for i in range(min(4, self.num_levels)):
            psi = self.eigenvectors[:, i]
            prob = np.abs(psi) ** 2

            # Find penetration depth (where probability drops to 1/e)
            right_edge = center + half_width
            right_part = prob[self.x > right_edge]
            if len(right_part) > 0 and np.max(right_part) > 0:
                threshold = np.max(right_part) / np.e
                penetration_indices = np.where(right_part > threshold)[0]
                if len(penetration_indices) > 0:
                    penetration_depth = self.x[np.where(self.x > right_edge)[0][penetration_indices[-1]]] - right_edge
                else:
                    penetration_depth = 0
            else:
                penetration_depth = 0

            ax5.bar(i, penetration_depth, color=f"C{i}", alpha=0.7)

        ax5.set_xlabel("Quantum number n", fontsize=11)
        ax5.set_ylabel("Penetration depth", fontsize=11)
        ax5.set_title("Evanescent Tail Depth", fontsize=12, fontweight="bold")
        ax5.grid(True, alpha=0.3, axis="y")

        # 6. Log-scale probability (shows tails)
        ax6 = fig.add_subplot(gs[2, :2])
        for i in range(min(2, self.num_levels)):
            psi = self.eigenvectors[:, i]
            prob = np.abs(psi) ** 2
            prob_safe = np.maximum(prob, 1e-8)
            ax6.semilogy(self.x, prob_safe, linewidth=2, label=f"n={i+1}")

        ax6.fill_between(self.x, 1e-10, self.potential / self.barrier_height * 1e-4,
                        alpha=0.1, color="gray", label="Potential (scaled)")
        ax6.set_xlabel("Position x", fontsize=11)
        ax6.set_ylabel("|ψ(x)|² (log scale)", fontsize=11)
        ax6.set_title("Exponential Decay Outside Well", fontsize=12, fontweight="bold")
        ax6.legend(fontsize=9)
        ax6.grid(True, alpha=0.3, which="both")

        # 7. Energy shift analysis
        ax7 = fig.add_subplot(gs[2, 2])
        energy_shifts = self.eigenvalues_inf - self.eigenvalues
        ax7.bar(range(self.num_levels), energy_shifts, color="purple", alpha=0.7)
        ax7.set_xlabel("Quantum number n", fontsize=11)
        ax7.set_ylabel("ΔE = E_inf - E_finite", fontsize=11)
        ax7.set_title("Energy Shifts Due to Finite Barrier", fontsize=12, fontweight="bold")
        ax7.grid(True, alpha=0.3, axis="y")

        plt.suptitle("Finite Potential Well Analysis", fontsize=14, fontweight="bold", y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Saved to {save_path}")

        return fig

    def animate_state_with_penetration(
        self,
        state_index: int = 0,
        num_frames: int = 100,
        save_path: str = None,
        fps: int = 30,
    ) -> animation.FuncAnimation:
        """
        Animate a single eigenstate with emphasis on evanescent tail penetration.

        Args:
            state_index: Which eigenstate to animate (0-based)
            num_frames: Number of frames
            save_path: Output file
            fps: Frames per second

        Returns:
            Animation object
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        psi = self.eigenvectors[:, state_index]
        prob = np.abs(psi) ** 2
        E = self.eigenvalues[state_index]

        # Left plot: linear scale
        ax_lin = axes[0]
        ax_lin.fill_between(self.x, 0, self.potential / self.barrier_height, alpha=0.1, color="gray")
        (line_lin,) = ax_lin.plot([], [], "b-", linewidth=2.5)
        ax_lin.set_xlim(self.x[0], self.x[-1])
        ax_lin.set_ylim(0, np.max(prob) * 1.2)
        ax_lin.set_xlabel("Position x", fontsize=11)
        ax_lin.set_ylabel("|ψ(x)|²", fontsize=11)
        ax_lin.set_title(f"State n={state_index+1} (Linear Scale), E={E:.3f}", fontsize=11, fontweight="bold")
        ax_lin.grid(True, alpha=0.3)

        # Right plot: log scale to see tails
        ax_log = axes[1]
        (line_log,) = ax_log.semilogy([], [], "r-", linewidth=2.5)
        ax_log.set_xlim(self.x[0], self.x[-1])
        ax_log.set_ylim(1e-8, np.max(prob) * 2)
        ax_log.set_xlabel("Position x", fontsize=11)
        ax_log.set_ylabel("|ψ(x)|² (log scale)", fontsize=11)
        ax_log.set_title(f"State n={state_index+1} (Log Scale)", fontsize=11, fontweight="bold")
        ax_log.grid(True, alpha=0.3, which="both")

        frame_text = fig.text(0.5, 0.02, "", ha="center", fontsize=11)

        def animate(frame):
            phase = 2 * np.pi * frame / num_frames
            amplitude = 0.7 + 0.3 * np.sin(phase)

            prob_animated = prob * amplitude

            line_lin.set_data(self.x, prob_animated)
            prob_safe = np.maximum(prob_animated, 1e-8)
            line_log.set_data(self.x, prob_safe)

            frame_text.set_text(f"Frame: {frame+1}/{num_frames} | Amplitude: {amplitude:.2f}")

            return [line_lin, line_log, frame_text]

        anim = animation.FuncAnimation(
            fig, animate, frames=num_frames, interval=33, blit=False, repeat=True
        )

        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer="ffmpeg", fps=fps, dpi=100)
            print(f"Animation saved to {save_path}")

        plt.suptitle("Finite Potential Well: Evanescent Tail Penetration", fontsize=13, fontweight="bold")
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])

        return anim


def main():
    """Run finite well simulation."""
    import sys
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("FINITE POTENTIAL WELL SIMULATION")
    print("=" * 70)

    # Create simulation
    sim = FiniteWellSimulation(well_width=2.0, barrier_height=10.0, num_levels=6)

    # Generate comparison plot
    print("\nGenerating comparison plot...")
    comp_path = os.path.join(output_dir, "finite_well_comparison.png")
    sim.plot_comparison(save_path=comp_path)
    print(f"✓ Saved to {comp_path}")

    # Generate animation
    print("\nGenerating animation...")
    anim_path = os.path.join(output_dir, "finite_well_animation.mp4")
    sim.animate_state_with_penetration(state_index=0, num_frames=100, save_path=anim_path, fps=30)
    print(f"✓ Saved to {anim_path}")

    print("\n" + "=" * 70)
    print("Simulation complete!")
    print("=" * 70)

    plt.show()


if __name__ == "__main__":
    main()
