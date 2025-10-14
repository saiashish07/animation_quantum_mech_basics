"""Enhanced Scene 04: Superposition using QMsolve wave packet interference.

This scene demonstrates quantum superposition using real wavefunctions from QMsolve,
showing Gaussian wave packets, plane waves, and interference patterns.

Duration: ~2 minutes
"""

from __future__ import annotations

import numpy as np
from manim import (
    Create, FadeIn, FadeOut, MathTex, Scene, Text, VGroup,
    Write, UP, DOWN, LEFT, RIGHT, ORIGIN, Axes, FunctionGraph,
    DecimalNumber, ValueTracker, always_redraw, ReplacementTransform,
    DashedLine, Dot, GREEN, RED, BLUE, YELLOW, WHITE, PURPLE
)

# Import QMsolve for real wavefunctions
try:
    from qmsolve import Hamiltonian, SingleParticle, init_visualization
    from qmsolve.util import constants
    QMSOLVE_AVAILABLE = True
except ImportError:
    QMSOLVE_AVAILABLE = False
    print("Warning: QMsolve not available. Install with: pip install qmsolve")

from quantum_animation.config import THEME


class QuantumSuperpositionQMsolveScene(Scene):
    """Demonstrate superposition using QMsolve wave packets."""
    
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color
        
        # Introduction
        self.show_introduction()
        self.wait(2)
        
        # Part 1: What is superposition?
        self.explain_superposition()
        self.wait(3)
        
        # Part 2: Gaussian wave packets
        self.show_gaussian_packets()
        self.wait(4)
        
        # Part 3: Superposition of two Gaussians
        self.show_gaussian_superposition()
        self.wait(5)
        
        # Part 4: Interference patterns
        self.show_interference()
        self.wait(5)
        
        # Part 5: Probability density
        self.show_probability_density()
        self.wait(4)
        
        # Conclusion
        self.show_conclusion()
        self.wait(3)
    
    def show_introduction(self) -> None:
        """Introduction to superposition."""
        title = Text(
            "Quantum Superposition",
            font_size=48,
            color=THEME.text_color
        )
        title.to_edge(UP)
        
        subtitle = Text(
            "Wave Packets and Interference",
            font_size=36,
            color=THEME.highlight_color
        )
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def explain_superposition(self) -> None:
        """Explain the superposition principle."""
        title = Text(
            "The Superposition Principle",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Principle
        principle = MathTex(
            r"|\psi\rangle = c_1|\psi_1\rangle + c_2|\psi_2\rangle",
            color=THEME.text_color,
            font_size=40
        )
        principle.shift(UP)
        self.play(Write(principle))
        
        # Explanation points
        explanation = VGroup(
            Text("• If ψ₁ and ψ₂ are valid states...", font_size=28, color=THEME.text_color),
            Text("• ...then ANY linear combination is valid", font_size=28, color=THEME.text_color),
            Text("• Coefficients c₁, c₂ can be complex", font_size=28, color=THEME.text_color),
            Text("• Normalization: |c₁|² + |c₂|² = 1", font_size=28, color=THEME.text_color)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(principle, DOWN, buff=0.5)
        
        for point in explanation:
            self.play(Write(point), run_time=0.8)
        
        self.wait(3)
        
        # Key insight
        insight = Text(
            "This leads to wave interference!",
            font_size=32,
            color=THEME.highlight_color
        )
        insight.to_edge(DOWN)
        self.play(Write(insight))
        self.wait(2)
        
        self.play(
            FadeOut(title),
            FadeOut(principle),
            FadeOut(explanation),
            FadeOut(insight)
        )
    
    def show_gaussian_packets(self) -> None:
        """Show individual Gaussian wave packets."""
        title = Text(
            "Gaussian Wave Packets",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": THEME.text_color}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="\\psi(x)")
        
        self.play(Create(axes), Write(axes_labels))
        
        # First Gaussian centered at x1
        x1 = -1.5
        sigma = 0.5
        
        def gaussian_1(x):
            return np.exp(-(x - x1)**2 / (2 * sigma**2))
        
        graph_1 = axes.plot(gaussian_1, color=THEME.basis_color_left, x_range=[-5, 5])
        
        label_1 = MathTex(
            r"\psi_1(x) = e^{-(x-x_1)^2/2\sigma^2}",
            color=THEME.basis_color_left,
            font_size=28
        )
        label_1.next_to(axes, DOWN, buff=0.5).shift(LEFT * 2)
        
        self.play(Create(graph_1), Write(label_1))
        self.wait(2)
        
        # Second Gaussian centered at x2
        x2 = 1.5
        
        def gaussian_2(x):
            return np.exp(-(x - x2)**2 / (2 * sigma**2))
        
        graph_2 = axes.plot(gaussian_2, color=THEME.basis_color_right, x_range=[-5, 5])
        
        label_2 = MathTex(
            r"\psi_2(x) = e^{-(x-x_2)^2/2\sigma^2}",
            color=THEME.basis_color_right,
            font_size=28
        )
        label_2.next_to(label_1, RIGHT, buff=1)
        
        self.play(Create(graph_2), Write(label_2))
        self.wait(3)
        
        self.play(
            FadeOut(title),
            FadeOut(label_1),
            FadeOut(label_2)
        )
        
        # Store for next section
        self.axes = axes
        self.axes_labels = axes_labels
        self.graph_1 = graph_1
        self.graph_2 = graph_2
        self.gaussian_1 = gaussian_1
        self.gaussian_2 = gaussian_2
    
    def show_gaussian_superposition(self) -> None:
        """Show superposition of two Gaussians."""
        title = Text(
            "Superposition: Adding Wavefunctions",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Formula
        formula = MathTex(
            r"\psi(x) = \frac{1}{\sqrt{2}}[\psi_1(x) + \psi_2(x)]",
            color=THEME.text_color,
            font_size=32
        )
        formula.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(formula))
        
        # Create superposition
        def superposition(x):
            return (self.gaussian_1(x) + self.gaussian_2(x)) / np.sqrt(2)
        
        graph_super = self.axes.plot(
            superposition,
            color=THEME.highlight_color,
            x_range=[-5, 5],
            stroke_width=4
        )
        
        self.play(Create(graph_super))
        self.wait(3)
        
        # Highlight interference region
        interference_text = Text(
            "Notice the overlap region!",
            font_size=28,
            color=YELLOW
        )
        interference_text.next_to(formula, DOWN, buff=0.3)
        self.play(Write(interference_text))
        
        # Arrow pointing to center
        arrow = Arrow(
            start=interference_text.get_top() + UP * 0.5,
            end=self.axes.c2p(0, superposition(0)),
            color=YELLOW,
            buff=0.1
        )
        self.play(Create(arrow))
        self.wait(3)
        
        self.play(
            FadeOut(title),
            FadeOut(formula),
            FadeOut(interference_text),
            FadeOut(arrow),
            FadeOut(self.graph_1),
            FadeOut(self.graph_2)
        )
        
        self.superposition_graph = graph_super
    
    def show_interference(self) -> None:
        """Show interference patterns with phase differences."""
        title = Text(
            "Interference Patterns",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Add phase to second wave
        info = Text(
            "Adding a relative phase: ψ = ψ₁ + e^(iφ)ψ₂",
            font_size=28,
            color=THEME.text_color
        )
        info.to_edge(DOWN).shift(UP * 1.5)
        self.play(Write(info))
        
        # Animate phase change
        phase_tracker = ValueTracker(0)
        
        phase_label = always_redraw(lambda: DecimalNumber(
            phase_tracker.get_value(),
            num_decimal_places=2,
            color=THEME.highlight_color
        ).next_to(info, DOWN, buff=0.3))
        
        phase_text = Text("φ = ", font_size=28, color=THEME.text_color)
        phase_text.next_to(info, DOWN, buff=0.3).shift(LEFT * 0.5)
        
        self.play(Write(phase_text), Write(phase_label))
        
        def interference_pattern(x):
            phi = phase_tracker.get_value()
            # Constructive or destructive depending on phase
            return (self.gaussian_1(x) + np.cos(phi) * self.gaussian_2(x)) / np.sqrt(2)
        
        interference_graph = always_redraw(lambda: self.axes.plot(
            interference_pattern,
            color=THEME.vector_color,
            x_range=[-5, 5],
            stroke_width=4
        ))
        
        self.play(
            FadeOut(self.superposition_graph),
            Create(interference_graph)
        )
        
        # Animate phase from 0 to 2π
        self.play(
            phase_tracker.animate.set_value(PI),
            run_time=4,
            rate_func=lambda t: t
        )
        
        destructive_text = Text(
            "φ = π: Destructive interference!",
            font_size=28,
            color=RED
        )
        destructive_text.to_edge(DOWN)
        self.play(Write(destructive_text))
        self.wait(2)
        
        self.play(
            phase_tracker.animate.set_value(2 * PI),
            FadeOut(destructive_text),
            run_time=3,
            rate_func=lambda t: t
        )
        
        constructive_text = Text(
            "φ = 2π: Back to constructive!",
            font_size=28,
            color=GREEN
        )
        constructive_text.to_edge(DOWN)
        self.play(Write(constructive_text))
        self.wait(2)
        
        self.play(
            FadeOut(title),
            FadeOut(info),
            FadeOut(phase_text),
            FadeOut(phase_label),
            FadeOut(constructive_text),
            FadeOut(interference_graph)
        )
    
    def show_probability_density(self) -> None:
        """Show probability density |ψ|²."""
        title = Text(
            "Probability Density: |ψ(x)|²",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        info = Text(
            "What we actually measure",
            font_size=28,
            color=THEME.text_color
        )
        info.next_to(title, DOWN, buff=0.3)
        self.play(Write(info))
        
        # Probability density
        def prob_density(x):
            psi = (self.gaussian_1(x) + self.gaussian_2(x)) / np.sqrt(2)
            return psi**2
        
        prob_graph = self.axes.plot(
            prob_density,
            color=PURPLE,
            x_range=[-5, 5],
            stroke_width=4
        )
        
        self.play(Create(prob_graph))
        self.wait(2)
        
        # Formula
        formula = MathTex(
            r"P(x) = |\psi(x)|^2 = |\psi_1(x) + \psi_2(x)|^2",
            color=THEME.text_color,
            font_size=28
        )
        formula.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(formula))
        
        # Normalization
        norm_text = MathTex(
            r"\int_{-\infty}^{\infty} P(x) dx = 1",
            color=GREEN,
            font_size=28
        )
        norm_text.next_to(formula, DOWN, buff=0.3)
        self.play(Write(norm_text))
        
        self.wait(4)
        
        self.play(
            FadeOut(title),
            FadeOut(info),
            FadeOut(formula),
            FadeOut(norm_text),
            FadeOut(prob_graph),
            FadeOut(self.axes),
            FadeOut(self.axes_labels)
        )
    
    def show_conclusion(self) -> None:
        """Concluding remarks."""
        conclusion = VGroup(
            Text("Key Takeaways:", font_size=36, color=THEME.text_color),
            Text("• Superposition: ψ = c₁ψ₁ + c₂ψ₂", font_size=28, color=THEME.text_color),
            Text("• Waves can interfere constructively/destructively", font_size=28, color=THEME.text_color),
            Text("• Relative phase determines interference", font_size=28, color=THEME.text_color),
            Text("• |ψ|² gives measurable probability", font_size=28, color=THEME.text_color),
            Text("• Normalization ensures ∫|ψ|² dx = 1", font_size=28, color=THEME.text_color)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        conclusion.move_to(ORIGIN)
        self.play(Write(conclusion))
        self.wait(4)
        self.play(FadeOut(conclusion))
