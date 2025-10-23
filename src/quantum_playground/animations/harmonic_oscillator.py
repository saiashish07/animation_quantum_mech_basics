"""
Quantum Harmonic Oscillator Simulation and Visualization.

Demonstrates:
- Parabolic potential V(x) = (1/2)mω²x²
- Evenly spaced energy levels: E_n = (n + 1/2)ħω
- Hermite polynomial eigenfunctions
- Zero-point energy
- Coherent state superpositions (wave packet motion)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from scipy.special import hermite, factorial
import os

from quantum_playground.potentials import HarmonicOscillator
from quantum_playground.solvers import QuantumGrid, StationarySolver, GaussianWavePacket, TimeDependentSolver


class HarmonicOscillatorSimulation:
    """Simulation of quantum harmonic oscillator."""

    def __init__(
        self,
        mass: float = 1.0,
        omega: float = 1.0,
        x_min: float = -5.0,
        x_max: float = 5.0,
        num_points: int = 256,
        num_levels: int = 6,
    ):
        """
        Initialize harmonic oscillator simulation.

        Args:
            mass: Particle mass
            omega: Angular frequency
            x_min, x_max: Spatial domain
            num_points: Grid resolution
            num_levels: Number of levels to compute
        """
        self.mass = mass
        self.omega = omega
        self.num_levels = num_levels

        # Create grid
        self.grid = QuantumGrid(x_min, x_max, num_points)
        self.x = self.grid.x
        self.dx = self.grid.dx

        # Create harmonic oscillator potential
        ho = HarmonicOscillator(mass, omega)
        self.potential = ho(self.x)

        # Solve eigenvalue problem
        self.solver = StationarySolver(self.grid, mass=mass)
        self.eigenvalues, self.eigenvectors = self.solver.solve_eigenproblem(
            self.potential, num_eigenvalues=num_levels + 2
        )
        self.eigenvalues = self.eigenvalues[:num_levels]
        self.eigenvectors = self.eigenvectors[:, :num_levels]

    def get_analytical_eigenvalues(self) -> np.ndarray:
        """
        Get analytical energy levels.

        E_n = (n + 1/2) ħ ω
        In atomic units (ħ=1): E_n = (n + 0.5) ω
        """
        n = np.arange(self.num_levels)
        return (n + 0.5) * self.omega

    def get_analytical_eigenfunctions(self, normalized: bool = True) -> np.ndarray:
        """
        Get analytical harmonic oscillator eigenfunctions.

        ψ_n(x) = (mω/πħ)^(1/4) * H_n(ξ) * exp(-ξ²/2) / √(2^n n!)
        where ξ = √(mω/ħ) x, H_n are Hermite polynomials
        """
        # Characteristic length scale
        x0 = np.sqrt(1.0 / (self.mass * self.omega))  # ħ=1
        xi = self.x / x0

        psi_analytical = np.zeros((len(self.x), self.num_levels), dtype=complex)

        for n in range(self.num_levels):
            # Hermite polynomial
            H_n = hermite(n)
            # Normalization constant
            norm_const = (self.mass * self.omega / np.pi) ** 0.25 / np.sqrt(2 ** n * factorial(n))

            psi_n = norm_const * H_n(xi) * np.exp(-xi ** 2 / 2)
            psi_analytical[:, n] = psi_n

        return psi_analytical

    def plot_overview(self, save_path: str = None) -> None:
        """
        Create comprehensive overview of harmonic oscillator.

        Shows:
        - Potential and eigenstates
        - Energy level diagram (numerical vs analytical)
        - Probability densities
        - Classical vs quantum probability
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)

        # 1. Potential and eigenstates
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(self.x, self.potential, "k-", linewidth=3, label="V(x) = (1/2)mω²x²")

        for i in range(min(4, self.num_levels)):
            E = self.eigenvalues[i]
            psi = self.eigenvectors[:, i]
            prob = np.abs(psi) ** 2

            # Normalize for visualization
            prob_vis = prob / np.max(prob) * 0.3 + E

            ax1.plot(self.x, prob_vis, linewidth=2, label=f"n={i}")
            ax1.axhline(E, color="gray", linestyle=":", alpha=0.3)

        ax1.set_xlabel("Position x", fontsize=11)
        ax1.set_ylabel("Energy / V(x)", fontsize=11)
        ax1.set_title("Harmonic Oscillator: Potential and Eigenstates", fontsize=12, fontweight="bold")
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # 2. Energy level diagram
        ax2 = fig.add_subplot(gs[0, 2])
        analytical_E = self.get_analytical_eigenvalues()
        x_pos = [0.3, 0.7]

        for i in range(min(6, self.num_levels)):
            ax2.hlines(self.eigenvalues[i], x_pos[0] - 0.15, x_pos[0] + 0.15, colors="blue", linewidth=2.5)
            ax2.hlines(analytical_E[i], x_pos[1] - 0.15, x_pos[1] + 0.15, colors="red", linewidth=2.5)
            ax2.text(x_pos[0], self.eigenvalues[i] + 0.15, f"{i}", ha="center", fontsize=9)

        ax2.set_xlim(-0.1, 1.1)
        ax2.set_ylabel("Energy", fontsize=11)
        ax2.set_title("Energy Levels", fontsize=12, fontweight="bold")
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(["Numerical", "Analytical"])
        ax2.grid(True, alpha=0.3, axis="y")

        # 3. Probability densities
        ax3 = fig.add_subplot(gs[1, 0])
        for i in range(min(5, self.num_levels)):
            prob = np.abs(self.eigenvectors[:, i]) ** 2
            ax3.plot(self.x, prob, linewidth=2, label=f"n={i}")

        ax3.set_xlabel("Position x", fontsize=11)
        ax3.set_ylabel("|ψ_n(x)|²", fontsize=11)
        ax3.set_title("Probability Densities", fontsize=12, fontweight="bold")
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)

        # 4. Numerical vs Analytical wavefunctions
        ax4 = fig.add_subplot(gs[1, 1])
        psi_analytical = self.get_analytical_eigenfunctions()

        for i in range(3):
            psi_num = self.eigenvectors[:, i]
            psi_ana = psi_analytical[:, i]

            # Ensure same sign convention
            if np.dot(psi_num, psi_ana) < 0:
                psi_ana = -psi_ana

            ax4.plot(self.x, psi_num, "b-", linewidth=2, label=f"n={i} (numerical)" if i == 0 else "")
            ax4.plot(self.x, psi_ana, "r--", linewidth=1.5, alpha=0.7, label=f"n={i} (analytical)" if i == 0 else "")

        ax4.set_xlabel("Position x", fontsize=11)
        ax4.set_ylabel("ψ(x)", fontsize=11)
        ax4.set_title("Numerical vs Analytical (n=0,1,2)", fontsize=12, fontweight="bold")
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

        # 5. Wavefunction comparison error
        ax5 = fig.add_subplot(gs[1, 2])
        errors = []
        for i in range(self.num_levels):
            psi_num = self.eigenvectors[:, i]
            psi_ana = psi_analytical[:, i]
            if np.dot(psi_num, psi_ana) < 0:
                psi_ana = -psi_ana
            error = np.linalg.norm(psi_num - psi_ana)
            errors.append(error)

        ax5.bar(range(self.num_levels), errors, color="purple", alpha=0.7)
        ax5.set_xlabel("Quantum number n", fontsize=11)
        ax5.set_ylabel("||ψ_numerical - ψ_analytical||", fontsize=11)
        ax5.set_title("Numerical Accuracy", fontsize=12, fontweight="bold")
        ax5.grid(True, alpha=0.3, axis="y")

        # 6. Zero-point energy illustration
        ax6 = fig.add_subplot(gs[2, 0])
        ax6.plot(self.x, self.potential, "k-", linewidth=2)
        ax6.fill_between(self.x, 0, self.potential, alpha=0.1, color="gray")
        ax6.axhline(self.eigenvalues[0], color="red", linewidth=2, label=f"E_0 (ground state)")
        ax6.axhline(0.5 * self.omega, color="red", linestyle="--", alpha=0.5, label="E_0 = (1/2)ħω")

        # Mark classical turning points for ground state
        E0 = self.eigenvalues[0]
        x_classical = np.sqrt(2 * E0 / (self.mass * self.omega ** 2))
        ax6.axvline(-x_classical, color="orange", linestyle=":", alpha=0.7, linewidth=2)
        ax6.axvline(x_classical, color="orange", linestyle=":", alpha=0.7, linewidth=2)

        ax6.set_xlabel("Position x", fontsize=11)
        ax6.set_ylabel("Energy / V(x)", fontsize=11)
        ax6.set_title("Zero-Point Energy", fontsize=12, fontweight="bold")
        ax6.legend(fontsize=9)
        ax6.grid(True, alpha=0.3)

        # 7. Classical probability vs quantum
        ax7 = fig.add_subplot(gs[2, 1:])
        n_display = 0
        E0 = self.eigenvalues[n_display]

        # Classical probability: ρ_cl(x) = 1/π √(2E/mω²) / √(E - V(x))
        x_classical = np.sqrt(2 * E0 / (self.mass * self.omega ** 2))
        V_at_x = 0.5 * self.mass * self.omega ** 2 * self.x ** 2
        rho_classical = np.where(
            V_at_x < E0,
            1.0 / (np.pi * np.sqrt(2 * E0 / (self.mass * self.omega ** 2) - self.x ** 2 / (self.mass * self.omega ** 2))),
            0,
        )
        rho_classical /= np.trapz(rho_classical, self.x)

        # Quantum probability
        prob_quantum = np.abs(self.eigenvectors[:, n_display]) ** 2
        prob_quantum /= np.trapz(prob_quantum, self.x)

        ax7.plot(self.x, prob_quantum, "b-", linewidth=2.5, label="Quantum |ψ₀|²")
        ax7.plot(self.x, rho_classical, "r--", linewidth=2.5, label="Classical ρ(x)")
        ax7.set_xlabel("Position x", fontsize=11)
        ax7.set_ylabel("Probability density", fontsize=11)
        ax7.set_title(f"Ground State: Classical vs Quantum", fontsize=12, fontweight="bold")
        ax7.legend(fontsize=10)
        ax7.grid(True, alpha=0.3)

        plt.suptitle("Quantum Harmonic Oscillator Analysis", fontsize=14, fontweight="bold", y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Saved to {save_path}")

        return fig

    def animate_superposition(
        self,
        coefficients: np.ndarray = None,
        num_frames: int = 150,
        save_path: str = None,
        fps: int = 30,
    ) -> animation.FuncAnimation:
        """
        Animate a coherent superposition of eigenstates (wave packet).

        Args:
            coefficients: Array of amplitudes for superposition [c_0, c_1, ...]
            num_frames: Number of frames
            save_path: Output file
            fps: Frames per second

        Returns:
            Animation object
        """
        if coefficients is None:
            # Default: superposition of first two states
            coefficients = np.array([1.0, 1.0, 0.5]) / np.sqrt(2.25)
            coefficients = coefficients[: self.num_levels]

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # Precompute superposition
        psi_super = np.zeros(len(self.x), dtype=complex)
        for n in range(min(len(coefficients), self.num_levels)):
            psi_super += coefficients[n] * self.eigenvectors[:, n]

        prob_super = np.abs(psi_super) ** 2

        # Plots
        (line_real,) = axes[0].plot([], [], "b-", linewidth=2)
        (line_imag,) = axes[0].plot([], [], "g-", linewidth=2)
        axes[0].set_xlim(self.x[0], self.x[-1])
        axes[0].set_ylim(-np.max(np.abs(psi_super)) * 1.2, np.max(np.abs(psi_super)) * 1.2)
        axes[0].set_xlabel("Position x")
        axes[0].set_ylabel("ψ(x)")
        axes[0].set_title("Wavefunction")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend(["Re[ψ]", "Im[ψ]"], fontsize=9)

        (line_prob,) = axes[1].plot([], [], "r-", linewidth=2.5)
        axes[1].fill_between(self.x, 0, self.potential / 10, alpha=0.1, color="gray")
        axes[1].set_xlim(self.x[0], self.x[-1])
        axes[1].set_ylim(0, np.max(prob_super) * 1.2)
        axes[1].set_xlabel("Position x")
        axes[1].set_ylabel("|ψ(x)|²")
        axes[1].set_title("Probability Density")
        axes[1].grid(True, alpha=0.3)

        # Energy decomposition
        axes[2].set_xlim(-0.5, self.num_levels - 0.5)
        axes[2].set_ylim(0, 1.1)
        axes[2].set_xlabel("Quantum number n")
        axes[2].set_ylabel("Component weight")
        axes[2].set_title("Energy Composition")
        axes[2].grid(True, alpha=0.3, axis="y")

        # Bar plot for components
        bars = axes[2].bar(range(min(len(coefficients), self.num_levels)),
                          np.abs(coefficients[:self.num_levels]) ** 2,
                          color=plt.cm.Spectral(np.linspace(0, 1, min(len(coefficients), self.num_levels))),
                          alpha=0.7)

        frame_text = fig.text(0.5, 0.02, "", ha="center", fontsize=11)

        def animate(frame):
            t = frame / num_frames * 2 * np.pi

            # Time-dependent phase
            psi_t = np.zeros(len(self.x), dtype=complex)
            for n in range(min(len(coefficients), self.num_levels)):
                E_n = self.eigenvalues[n]
                psi_t += coefficients[n] * self.eigenvectors[:, n] * np.exp(-1j * E_n * t)

            prob_t = np.abs(psi_t) ** 2

            line_real.set_data(self.x, np.real(psi_t))
            line_imag.set_data(self.x, np.imag(psi_t))

            line_prob.set_data(self.x, prob_t)

            frame_text.set_text(f"Time: {t/np.pi:.2f}π | Frame: {frame+1}/{num_frames}")

            return [line_real, line_imag, line_prob, frame_text]

        anim = animation.FuncAnimation(
            fig, animate, frames=num_frames, interval=33, blit=False, repeat=True
        )

        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer="ffmpeg", fps=fps, dpi=100)
            print(f"Animation saved to {save_path}")

        plt.suptitle("Harmonic Oscillator: Coherent Superposition (Wave Packet)", fontsize=13, fontweight="bold")
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])

        return anim


def main():
    """Run harmonic oscillator simulation."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("QUANTUM HARMONIC OSCILLATOR SIMULATION")
    print("=" * 70)

    # Create simulation
    sim = HarmonicOscillatorSimulation(mass=1.0, omega=1.0, num_levels=8)

    # Generate overview plot
    print("\nGenerating overview plot...")
    overview_path = os.path.join(output_dir, "harmonic_oscillator_overview.png")
    sim.plot_overview(save_path=overview_path)
    print(f"✓ Saved to {overview_path}")

    # Generate animation
    print("\nGenerating animation...")
    anim_path = os.path.join(output_dir, "harmonic_oscillator_animation.mp4")
    coeffs = np.array([1.0, 1.0, 0.3])  # Superposition of first 3 levels
    sim.animate_superposition(coefficients=coeffs, num_frames=150, save_path=anim_path, fps=30)
    print(f"✓ Saved to {anim_path}")

    print("\n" + "=" * 70)
    print("Simulation complete!")
    print("=" * 70)

    plt.show()


if __name__ == "__main__":
    main()
