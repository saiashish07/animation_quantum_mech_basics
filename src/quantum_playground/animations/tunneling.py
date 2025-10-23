"""
Quantum Tunneling Simulation and Visualization.

Demonstrates:
- Wave packet incident on barrier
- Partial reflection and transmission
- Exponential decay inside barrier (evanescent wave)
- Transmission coefficient calculation
- WKB approximation comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import os

from quantum_playground.potentials import RectangularBarrier
from quantum_playground.solvers import (
    QuantumGrid,
    StationarySolver,
    GaussianWavePacket,
    TimeDependentSolver,
)


class TunnelingSimulation:
    """Simulation of quantum tunneling through a barrier."""

    def __init__(
        self,
        barrier_height: float = 5.0,
        barrier_width: float = 0.5,
        barrier_position: float = 0.0,
        particle_energy: float = 3.0,
        x_min: float = -5.0,
        x_max: float = 5.0,
        num_points: int = 512,
        dt: float = 0.01,
    ):
        """
        Initialize tunneling simulation.

        Args:
            barrier_height: Height of potential barrier (V0)
            barrier_width: Width of barrier
            barrier_position: Center x position of barrier
            particle_energy: Initial kinetic energy of particle
            x_min, x_max: Spatial domain
            num_points: Grid resolution
            dt: Time step for evolution
        """
        self.barrier_height = barrier_height
        self.barrier_width = barrier_width
        self.barrier_position = barrier_position
        self.particle_energy = particle_energy
        self.dt = dt

        # Create grid
        self.grid = QuantumGrid(x_min, x_max, num_points)
        self.x = self.grid.x
        self.dx = self.grid.dx

        # Create barrier potential
        barrier = RectangularBarrier(barrier_height, barrier_width, barrier_position)
        self.potential = barrier(self.x)

        # Parameters for initial wave packet
        self.x_init = x_min + 1.5  # Start from left
        self.packet_width = 0.3
        self.k0 = np.sqrt(2 * particle_energy)  # Wave vector for given energy

        # Create initial Gaussian wave packet
        self.psi_init = GaussianWavePacket.create(
            self.x, x0=self.x_init, sigma=self.packet_width, k0=self.k0, amplitude=1.0
        )
        self.psi_init = GaussianWavePacket.normalize(self.psi_init, self.dx)

        # Create time-dependent solver
        self.td_solver = TimeDependentSolver(self.grid, self.potential, mass=1.0, dt=dt)

    def estimate_wkb_transmission(self) -> float:
        """
        Estimate transmission coefficient using WKB approximation.

        T ≈ exp(-2κ)
        where κ = (1/ħ) ∫ √[2m(V - E)] dx
        """
        E = self.particle_energy
        V = self.potential
        x = self.x
        dx = self.dx

        # Find barrier region
        barrier_mask = V > E
        if not np.any(barrier_mask):
            return 1.0

        # Calculate κ
        integrand = np.sqrt(2.0 * np.maximum(0, V - E))
        kappa = np.sum(integrand[barrier_mask]) * dx

        T = np.exp(-2 * kappa)
        return np.clip(T, 0.0, 1.0)

    def run_evolution(self, num_steps: int = 1000) -> np.ndarray:
        """
        Run time-dependent Schrödinger evolution.

        Args:
            num_steps: Number of time steps

        Returns:
            Trajectory array of shape (num_points, num_steps)
        """
        print(f"Evolving wavefunction for {num_steps} steps...")
        trajectory = self.td_solver.evolve(self.psi_init, num_steps)
        return trajectory

    def analyze_transmission(self, trajectory: np.ndarray) -> dict:
        """
        Analyze transmission and reflection from trajectory.

        Args:
            trajectory: Wavefunction trajectory

        Returns:
            Dictionary with T, R, and other metrics
        """
        # Define regions
        barrier_center_idx = np.argmin(np.abs(self.x - self.barrier_position))
        barrier_half_width_idx = int(self.barrier_width / (2 * self.dx))

        barrier_left = max(0, barrier_center_idx - barrier_half_width_idx)
        barrier_right = min(len(self.x), barrier_center_idx + barrier_half_width_idx)

        # Final wavefunction
        psi_final = trajectory[:, -1]
        prob_final = np.abs(psi_final) ** 2

        # Transmitted: probability to the right of barrier
        prob_transmitted = np.sum(prob_final[barrier_right:]) * self.dx

        # Reflected: probability to the left of barrier
        prob_reflected = np.sum(prob_final[:barrier_left]) * self.dx

        # Inside barrier
        prob_inside = np.sum(prob_final[barrier_left:barrier_right]) * self.dx

        # Initial total probability
        prob_init = np.sum(np.abs(self.psi_init) ** 2) * self.dx

        T = prob_transmitted / (prob_init + 1e-10)
        R = prob_reflected / (prob_init + 1e-10)

        return {
            "T_numerical": T,
            "R_numerical": R,
            "prob_inside": prob_inside,
            "T_wkb": self.estimate_wkb_transmission(),
            "prob_transmitted": prob_transmitted,
            "prob_reflected": prob_reflected,
        }

    def plot_transmission_analysis(self, trajectory: np.ndarray, save_path: str = None) -> None:
        """
        Create detailed analysis figure for tunneling.

        Args:
            trajectory: Wavefunction trajectory
            save_path: Output file path
        """
        analysis = self.analyze_transmission(trajectory)

        fig = plt.figure(figsize=(16, 11))
        gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)

        # 1. Potential barrier
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.fill_between(self.x, 0, self.potential, alpha=0.3, color="red", label="V(x)")
        ax1.plot(self.x, self.potential, "r-", linewidth=2.5)
        ax1.axhline(self.particle_energy, color="green", linestyle="--", linewidth=2, label=f"E = {self.particle_energy}")

        # Mark regions
        barrier_center = self.barrier_position
        half_width = self.barrier_width / 2
        ax1.axvspan(barrier_center - half_width, barrier_center + half_width, alpha=0.1, color="red")

        ax1.set_xlabel("Position x", fontsize=11)
        ax1.set_ylabel("Potential V(x)", fontsize=11)
        ax1.set_title("Tunneling Barrier", fontsize=12, fontweight="bold")
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(self.x[0], self.x[-1])

        # 2. Transmission coefficient comparison
        ax2 = fig.add_subplot(gs[0, 2])
        methods = ["WKB\nApproximation", "Numerical\nSimulation"]
        T_values = [analysis["T_wkb"], analysis["T_numerical"]]
        colors_t = ["#FF7F0E", "#1F77B4"]

        bars = ax2.bar(methods, T_values, color=colors_t, alpha=0.7, edgecolor="black", linewidth=2)
        ax2.set_ylabel("Transmission Coefficient T", fontsize=11)
        ax2.set_title("T Estimation Methods", fontsize=12, fontweight="bold")
        ax2.set_ylim(0, 1)

        for bar, val in zip(bars, T_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.02, f"{val:.3f}",
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax2.grid(True, alpha=0.3, axis="y")

        # 3. Initial wavefunction
        ax3 = fig.add_subplot(gs[1, 0])
        prob_init = np.abs(self.psi_init) ** 2
        ax3.fill_between(self.x, 0, prob_init, alpha=0.3, color="blue")
        ax3.plot(self.x, prob_init, "b-", linewidth=2)
        ax3.set_xlabel("Position x", fontsize=11)
        ax3.set_ylabel("|ψ(x, t=0)|²", fontsize=11)
        ax3.set_title("Initial Wave Packet", fontsize=12, fontweight="bold")
        ax3.grid(True, alpha=0.3)

        # 4. Final wavefunction
        ax4 = fig.add_subplot(gs[1, 1])
        psi_final = trajectory[:, -1]
        prob_final = np.abs(psi_final) ** 2
        ax4.fill_between(self.x, 0, prob_final, alpha=0.3, color="green")
        ax4.plot(self.x, prob_final, "g-", linewidth=2)
        ax4.fill_between(self.x, 0, self.potential / self.barrier_height * np.max(prob_final),
                        alpha=0.1, color="red")
        ax4.set_xlabel("Position x", fontsize=11)
        ax4.set_ylabel("|ψ(x, t_final)|²", fontsize=11)
        ax4.set_title("Final Wavefunction", fontsize=12, fontweight="bold")
        ax4.grid(True, alpha=0.3)

        # 5. Probability flow
        ax5 = fig.add_subplot(gs[1, 2])
        regions = ["Reflected\n(Left)", "Inside\nBarrier", "Transmitted\n(Right)"]
        probs = [
            analysis["prob_reflected"],
            analysis["prob_inside"],
            analysis["prob_transmitted"],
        ]
        colors_flow = ["#FF6B6B", "#FFA500", "#4ECDC4"]

        wedges, texts, autotexts = ax5.pie(probs, labels=regions, colors=colors_flow, autopct="%1.1f%%",
                                           textprops={"fontsize": 10}, startangle=90)
        ax5.set_title("Probability Distribution", fontsize=12, fontweight="bold")

        # 6. Space-time evolution (heatmap)
        ax6 = fig.add_subplot(gs[2, :2])

        # Downsample trajectory for visualization
        time_indices = np.linspace(0, trajectory.shape[1] - 1, 100, dtype=int)
        prob_traj = np.abs(trajectory[:, time_indices]) ** 2

        im = ax6.pcolormesh(self.x, range(len(time_indices)), prob_traj.T, shading="auto", cmap="hot")
        ax6.axvline(self.barrier_position - self.barrier_width / 2, color="cyan", linestyle="--", linewidth=1.5, alpha=0.7)
        ax6.axvline(self.barrier_position + self.barrier_width / 2, color="cyan", linestyle="--", linewidth=1.5, alpha=0.7)

        ax6.set_xlabel("Position x", fontsize=11)
        ax6.set_ylabel("Time step", fontsize=11)
        ax6.set_title("Space-Time Evolution: |ψ(x,t)|²", fontsize=12, fontweight="bold")
        cbar = plt.colorbar(im, ax=ax6)
        cbar.set_label("Probability density", fontsize=10)

        # 7. Exponential decay inside barrier
        ax7 = fig.add_subplot(gs[2, 2])

        # Average probability inside barrier over time
        barrier_center_idx = np.argmin(np.abs(self.x - self.barrier_position))
        barrier_half_width_idx = int(self.barrier_width / (2 * self.dx))
        barrier_left = max(0, barrier_center_idx - barrier_half_width_idx)
        barrier_right = min(len(self.x), barrier_center_idx + barrier_half_width_idx)

        prob_inside_time = [
            np.sum(np.abs(trajectory[barrier_left:barrier_right, t]) ** 2) * self.dx
            for t in range(trajectory.shape[1])
        ]

        time_steps = np.arange(len(prob_inside_time))
        ax7.semilogy(time_steps, np.maximum(prob_inside_time, 1e-10), "r-", linewidth=2)
        ax7.set_xlabel("Time step", fontsize=11)
        ax7.set_ylabel("Prob. inside barrier (log)", fontsize=11)
        ax7.set_title("Decay Inside Barrier", fontsize=12, fontweight="bold")
        ax7.grid(True, alpha=0.3, which="both")

        # 8. Summary statistics box
        ax8 = fig.add_subplot(gs[3, :])
        ax8.axis("off")

        summary_text = f"""
        TUNNELING SIMULATION RESULTS
        ══════════════════════════════════════════════════════════════════════════════════════════

        Barrier Parameters:
            • Height: V₀ = {self.barrier_height:.3f}  |  Width: a = {self.barrier_width:.3f}
            • Position: x₀ = {self.barrier_position:.3f}

        Particle Properties:
            • Energy: E = {self.particle_energy:.3f}  |  E/V₀ = {self.particle_energy/self.barrier_height:.3f}
            • Wave vector: k₀ = {self.k0:.3f}  |  Initial σ = {self.packet_width:.3f}

        Transmission Coefficients:
            • WKB Approximation:  T_WKB = {analysis["T_wkb"]:.4f}
            • Numerical Result:   T_num = {analysis["T_numerical"]:.4f}
            • Reflection:         R = {analysis["R_numerical"]:.4f}
            • Difference:         |T_WKB - T_num| = {abs(analysis["T_wkb"] - analysis["T_numerical"]):.4f}

        Probability Distribution (Final State):
            • Transmitted (right):    {analysis["prob_transmitted"]:.4f} ({analysis["prob_transmitted"]*100:.2f}%)
            • Reflected (left):       {analysis["prob_reflected"]:.4f} ({analysis["prob_reflected"]*100:.2f}%)
            • Inside barrier:         {analysis["prob_inside"]:.4f} ({analysis["prob_inside"]*100:.2f}%)

        Classical Prediction: Particle with E < V₀ cannot classically penetrate. Quantum tunneling allows escape!
        """

        ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes, fontsize=10, verticalalignment="top",
                family="monospace", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

        plt.suptitle("Quantum Tunneling Through Potential Barrier", fontsize=14, fontweight="bold", y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Saved to {save_path}")

        return fig

    def animate_tunneling(
        self,
        trajectory: np.ndarray,
        num_display_frames: int = None,
        save_path: str = None,
        fps: int = 30,
    ) -> animation.FuncAnimation:
        """
        Create animation of wave packet tunneling through barrier.

        Args:
            trajectory: Wavefunction trajectory
            num_display_frames: Number of frames to display (if None, use all)
            save_path: Output file path
            fps: Frames per second

        Returns:
            Animation object
        """
        if num_display_frames is None:
            num_display_frames = trajectory.shape[1]

        # Select frames to display
        frame_indices = np.linspace(0, trajectory.shape[1] - 1, num_display_frames, dtype=int)

        fig, axes = plt.subplots(2, 2, figsize=(14, 9))

        # Top-left: Real and imaginary parts
        ax_cplx = axes[0, 0]
        (line_real,) = ax_cplx.plot([], [], "b-", linewidth=2, label="Re[ψ]")
        (line_imag,) = ax_cplx.plot([], [], "g-", linewidth=2, label="Im[ψ]")
        ax_cplx.axhline(0, color="k", linestyle="-", alpha=0.1, linewidth=0.5)
        ax_cplx.set_xlim(self.x[0], self.x[-1])
        ax_cplx.set_ylim(-0.6, 0.6)
        ax_cplx.set_ylabel("ψ(x)", fontsize=11)
        ax_cplx.set_title("Wavefunction", fontsize=12, fontweight="bold")
        ax_cplx.legend(fontsize=10)
        ax_cplx.grid(True, alpha=0.3)

        # Top-right: Probability density
        ax_prob = axes[0, 1]
        (line_prob,) = ax_prob.plot([], [], "r-", linewidth=2.5)
        fill_prob = ax_prob.fill_between([], [], alpha=0.3, color="red")
        ax_prob.fill_between(self.x, 0, self.potential / self.barrier_height * 0.5, alpha=0.15, color="orange")
        ax_prob.set_xlim(self.x[0], self.x[-1])
        ax_prob.set_ylim(0, np.max(np.abs(trajectory) ** 2) * 1.3)
        ax_prob.set_ylabel("|ψ(x)|²", fontsize=11)
        ax_prob.set_title("Probability Density", fontsize=12, fontweight="bold")
        ax_prob.grid(True, alpha=0.3)

        # Bottom-left: Phase
        ax_phase = axes[1, 0]
        (line_phase,) = ax_phase.plot([], [], "purple", linewidth=2)
        ax_phase.set_xlim(self.x[0], self.x[-1])
        ax_phase.set_ylim(-np.pi, np.pi)
        ax_phase.set_xlabel("Position x", fontsize=11)
        ax_phase.set_ylabel("Phase arg[ψ(x)]", fontsize=11)
        ax_phase.set_title("Wavefunction Phase", fontsize=12, fontweight="bold")
        ax_phase.grid(True, alpha=0.3)

        # Bottom-right: Integrated probabilities
        ax_bars = axes[1, 1]
        ax_bars.set_xlim(-0.5, 2.5)
        ax_bars.set_ylim(0, 1)
        ax_bars.set_ylabel("Probability", fontsize=11)
        ax_bars.set_title("Cumulative Probabilities", fontsize=12, fontweight="bold")
        ax_bars.set_xticks([0, 1, 2])
        ax_bars.set_xticklabels(["Reflected", "Inside", "Transmitted"])
        ax_bars.grid(True, alpha=0.3, axis="y")

        frame_text = fig.text(0.5, 0.02, "", ha="center", fontsize=11)

        def animate(frame_idx):
            t = frame_indices[frame_idx]
            psi = trajectory[:, t]

            # Real and imaginary
            line_real.set_data(self.x, np.real(psi))
            line_imag.set_data(self.x, np.imag(psi))

            # Probability
            prob = np.abs(psi) ** 2
            line_prob.set_data(self.x, prob)

            # Update fill
            ax_prob.clear()
            ax_prob.fill_between(self.x, 0, prob, alpha=0.3, color="red", label="Probability")
            ax_prob.plot(self.x, prob, "r-", linewidth=2.5)
            ax_prob.fill_between(self.x, 0, self.potential / self.barrier_height * 0.5, alpha=0.15, color="orange", label="Barrier")
            ax_prob.set_xlim(self.x[0], self.x[-1])
            ax_prob.set_ylim(0, np.max(np.abs(trajectory) ** 2) * 1.3)
            ax_prob.set_ylabel("|ψ(x)|²", fontsize=11)
            ax_prob.set_title("Probability Density", fontsize=12, fontweight="bold")
            ax_prob.legend(fontsize=9)
            ax_prob.grid(True, alpha=0.3)

            # Phase
            phase = np.angle(psi)
            line_phase.set_data(self.x, phase)

            # Cumulative probabilities
            barrier_center_idx = np.argmin(np.abs(self.x - self.barrier_position))
            barrier_half_width_idx = int(self.barrier_width / (2 * self.dx))
            barrier_left = max(0, barrier_center_idx - barrier_half_width_idx)
            barrier_right = min(len(self.x), barrier_center_idx + barrier_half_width_idx)

            prob_refl = np.sum(prob[:barrier_left]) * self.dx
            prob_inside = np.sum(prob[barrier_left:barrier_right]) * self.dx
            prob_trans = np.sum(prob[barrier_right:]) * self.dx

            ax_bars.clear()
            bars = ax_bars.bar([0, 1, 2], [prob_refl, prob_inside, prob_trans],
                              color=["#FF6B6B", "#FFA500", "#4ECDC4"], alpha=0.7, edgecolor="black", linewidth=1.5)
            ax_bars.set_xlim(-0.5, 2.5)
            ax_bars.set_ylim(0, 1)
            ax_bars.set_ylabel("Probability", fontsize=11)
            ax_bars.set_xticks([0, 1, 2])
            ax_bars.set_xticklabels(["Reflected", "Inside", "Transmitted"])
            ax_bars.grid(True, alpha=0.3, axis="y")

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0.01:
                    ax_bars.text(bar.get_x() + bar.get_width() / 2, height + 0.02, f"{height:.2%}",
                                ha="center", va="bottom", fontsize=9)

            frame_text.set_text(f"Time: {t * self.dt:.2f}  |  Frame: {frame_idx+1}/{num_display_frames}")

            return [line_real, line_imag, line_phase, frame_text]

        anim = animation.FuncAnimation(
            fig, animate, frames=num_display_frames, interval=33, blit=False, repeat=True
        )

        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer="ffmpeg", fps=fps, dpi=100)
            print(f"Animation saved to {save_path}")

        plt.suptitle("Quantum Tunneling: Wave Packet Transmission", fontsize=13, fontweight="bold")
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])

        return anim


def main():
    """Run tunneling simulation."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("QUANTUM TUNNELING SIMULATION")
    print("=" * 70)

    # Create simulation
    sim = TunnelingSimulation(
        barrier_height=5.0,
        barrier_width=0.5,
        particle_energy=3.0,
        num_points=512,
        dt=0.01,
    )

    # Run evolution
    print("\nRunning wave packet evolution...")
    trajectory = sim.run_evolution(num_steps=800)

    # Analysis
    print("\nGenerating analysis figure...")
    analysis_path = os.path.join(output_dir, "tunneling_analysis.png")
    sim.plot_transmission_analysis(trajectory, save_path=analysis_path)
    print(f"✓ Saved to {analysis_path}")

    # Animation
    print("\nGenerating animation...")
    anim_path = os.path.join(output_dir, "tunneling_animation.mp4")
    sim.animate_tunneling(trajectory, num_display_frames=150, save_path=anim_path, fps=30)
    print(f"✓ Saved to {anim_path}")

    print("\n" + "=" * 70)
    print("Simulation complete!")
    print("=" * 70)

    plt.show()


if __name__ == "__main__":
    main()
