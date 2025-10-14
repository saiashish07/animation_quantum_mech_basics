"""Enhanced Scene 02: Inner Products using QuTiP quantum states and fidelity.

This scene demonstrates inner products using real QuTiP quantum states,
showing fidelity, measurement probabilities, and projection operators.

Duration: ~2 minutes
"""

from __future__ import annotations

import numpy as np
from manim import (
    Create, FadeIn, FadeOut, MathTex, Scene, Text, VGroup,
    Write, UP, DOWN, LEFT, RIGHT, ORIGIN, NumberPlane, Vector,
    Arrow, Dot, DashedLine, Angle, Arc, DecimalNumber, ValueTracker,
    always_redraw, ReplacementTransform, BarChart, Axes, GREEN, RED,
    BLUE, YELLOW, WHITE
)

# Import QuTiP for quantum calculations
try:
    from qutip import basis, fidelity, expect, sigmax, sigmay, sigmaz
    import qutip as qt
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False
    print("Warning: QuTiP not available. Install with: pip install qutip")

from quantum_animation.config import THEME


class QuantumInnerProductScene(Scene):
    """Demonstrate inner products using QuTiP quantum states."""
    
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color
        
        # Introduction
        self.show_introduction()
        self.wait(2)
        
        # Part 1: Definition of inner product
        self.define_inner_product()
        self.wait(3)
        
        # Part 2: Calculate real inner products with QuTiP
        self.calculate_qutip_inner_products()
        self.wait(4)
        
        # Part 3: Fidelity between states
        self.show_fidelity()
        self.wait(4)
        
        # Part 4: Measurement probabilities
        self.show_measurement_probabilities()
        self.wait(5)
        
        # Part 5: Projection operators
        self.show_projection_operators()
        self.wait(4)
        
        # Conclusion
        self.show_conclusion()
        self.wait(3)
    
    def show_introduction(self) -> None:
        """Show title and introduction."""
        title = Text(
            "Inner Products in Quantum Mechanics",
            font_size=44,
            color=THEME.text_color
        )
        title.to_edge(UP)
        
        subtitle = Text(
            "Measuring Overlap and Probability",
            font_size=32,
            color=THEME.highlight_color
        )
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def define_inner_product(self) -> None:
        """Define the inner product mathematically."""
        title = Text(
            "The Inner Product",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Definition
        definition = MathTex(
            r"\langle \psi | \phi \rangle = \sum_i \psi_i^* \phi_i",
            color=THEME.text_color,
            font_size=40
        )
        definition.shift(UP)
        
        explanation = VGroup(
            Text("• ψ* = complex conjugate", font_size=28, color=THEME.text_color),
            Text("• Sum over all basis components", font_size=28, color=THEME.text_color),
            Text("• Result: complex number", font_size=28, color=THEME.text_color)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(definition, DOWN, buff=0.5)
        
        self.play(Write(definition))
        self.wait(1)
        self.play(Write(explanation))
        self.wait(3)
        
        # Key property
        property_text = Text(
            "Key: |⟨ψ|φ⟩|² gives probability of measuring φ in state ψ",
            font_size=28,
            color=THEME.highlight_color
        )
        property_text.to_edge(DOWN)
        self.play(Write(property_text))
        self.wait(2)
        
        self.play(
            FadeOut(title),
            FadeOut(definition),
            FadeOut(explanation),
            FadeOut(property_text)
        )
    
    def calculate_qutip_inner_products(self) -> None:
        """Calculate inner products using QuTiP."""
        title = Text(
            "Computing Real Inner Products",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        if not QUTIP_AVAILABLE:
            warning = Text(
                "QuTiP not installed - showing conceptual values",
                font_size=24,
                color=RED
            )
            warning.next_to(title, DOWN)
            self.play(Write(warning))
            inner_products = {
                "⟨0|0⟩": 1.0,
                "⟨0|1⟩": 0.0,
                "⟨+|0⟩": 0.707,
                "⟨+|1⟩": 0.707,
            }
        else:
            # Calculate real inner products using QuTiP
            ket_0 = basis(2, 0)  # |0⟩
            ket_1 = basis(2, 1)  # |1⟩
            ket_plus = (ket_0 + ket_1).unit()  # |+⟩
            ket_minus = (ket_0 - ket_1).unit()  # |-⟩
            
            inner_products = {
                "⟨0|0⟩": abs((ket_0.dag() * ket_0)[0, 0]),
                "⟨0|1⟩": abs((ket_0.dag() * ket_1)[0, 0]),
                "⟨+|0⟩": abs((ket_plus.dag() * ket_0)[0, 0]),
                "⟨+|1⟩": abs((ket_plus.dag() * ket_1)[0, 0]),
            }
        
        # Display results in a table
        results = VGroup()
        for i, (label, value) in enumerate(inner_products.items()):
            row = VGroup(
                MathTex(f"|{label}|", color=THEME.text_color),
                MathTex("=", color=THEME.text_color),
                DecimalNumber(value, num_decimal_places=3, color=THEME.highlight_color)
            ).arrange(RIGHT, buff=0.3)
            results.add(row)
        
        results.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        results.move_to(ORIGIN)
        
        for row in results:
            self.play(Write(row), run_time=0.8)
        
        self.wait(3)
        
        # Highlight orthogonality
        highlight = Text(
            "⟨0|1⟩ = 0: orthogonal states!",
            font_size=32,
            color=THEME.highlight_color
        )
        highlight.to_edge(DOWN)
        self.play(Write(highlight))
        self.wait(2)
        
        self.play(
            FadeOut(title),
            FadeOut(results),
            FadeOut(highlight)
        )
    
    def show_fidelity(self) -> None:
        """Demonstrate fidelity between quantum states."""
        title = Text(
            "Fidelity: How Similar Are Two States?",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Fidelity formula
        formula = MathTex(
            r"F(\psi, \phi) = |\langle \psi | \phi \rangle|^2",
            color=THEME.text_color,
            font_size=36
        )
        formula.shift(UP * 1.5)
        self.play(Write(formula))
        
        info = Text(
            "Fidelity ranges from 0 (orthogonal) to 1 (identical)",
            font_size=28,
            color=THEME.text_color
        )
        info.next_to(formula, DOWN, buff=0.5)
        self.play(Write(info))
        
        # Calculate fidelities
        if QUTIP_AVAILABLE:
            ket_0 = basis(2, 0)
            ket_1 = basis(2, 1)
            ket_plus = (ket_0 + ket_1).unit()
            
            # Create a state at angle θ
            theta = PI / 4
            ket_theta = (np.cos(theta/2) * ket_0 + np.sin(theta/2) * ket_1).unit()
            
            fid_values = {
                "F(|0⟩, |0⟩)": fidelity(ket_0, ket_0),
                "F(|0⟩, |1⟩)": fidelity(ket_0, ket_1),
                "F(|0⟩, |+⟩)": fidelity(ket_0, ket_plus),
                "F(|+⟩, |a⟩)": fidelity(ket_plus, ket_theta),
            }
        else:
            fid_values = {
                "F(|0⟩, |0⟩)": 1.0,
                "F(|0⟩, |1⟩)": 0.0,
                "F(|0⟩, |+⟩)": 0.5,
                "F(|+⟩, |a⟩)": 0.85,
            }
        
        # Create bar chart
        bar_labels = list(fid_values.keys())
        bar_values = list(fid_values.values())
        
        chart = BarChart(
            values=bar_values,
            bar_names=bar_labels,
            y_range=[0, 1, 0.25],
            y_length=4,
            x_length=8,
            bar_colors=[GREEN, RED, YELLOW, BLUE]
        )
        chart.shift(DOWN * 1.5).scale(0.6)
        
        self.play(FadeOut(info))
        self.play(Create(chart))
        self.wait(4)
        
        self.play(
            FadeOut(title),
            FadeOut(formula),
            FadeOut(chart)
        )
    
    def show_measurement_probabilities(self) -> None:
        """Show measurement probabilities using inner products."""
        title = Text(
            "Measurement Probabilities",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # State to measure
        state_formula = MathTex(
            r"|\psi\rangle = \frac{1}{\sqrt{3}}|0\rangle + \sqrt{\frac{2}{3}}|1\rangle",
            color=THEME.text_color,
            font_size=32
        )
        state_formula.shift(UP * 2)
        self.play(Write(state_formula))
        
        # Calculate probabilities
        if QUTIP_AVAILABLE:
            ket_0 = basis(2, 0)
            ket_1 = basis(2, 1)
            psi = (1/np.sqrt(3) * ket_0 + np.sqrt(2/3) * ket_1).unit()
            
            prob_0 = abs((ket_0.dag() * psi)[0, 0])**2
            prob_1 = abs((ket_1.dag() * psi)[0, 0])**2
        else:
            prob_0 = 1/3
            prob_1 = 2/3
        
        # Probability formulas
        prob_formula_0 = MathTex(
            r"P(0) = |\langle 0 | \psi \rangle|^2 = ",
            f"{prob_0:.3f}",
            color=THEME.text_color,
            font_size=32
        )
        prob_formula_0.shift(UP * 0.5)
        
        prob_formula_1 = MathTex(
            r"P(1) = |\langle 1 | \psi \rangle|^2 = ",
            f"{prob_1:.3f}",
            color=THEME.text_color,
            font_size=32
        )
        prob_formula_1.next_to(prob_formula_0, DOWN, buff=0.4)
        
        self.play(Write(prob_formula_0))
        self.play(Write(prob_formula_1))
        
        # Verification
        check = MathTex(
            f"P(0) + P(1) = {prob_0 + prob_1:.3f} = 1 \\checkmark",
            color=GREEN,
            font_size=32
        )
        check.next_to(prob_formula_1, DOWN, buff=0.5)
        self.play(Write(check))
        
        # Visual representation with pie chart
        pie_info = Text(
            "Visual: Probability distribution",
            font_size=28,
            color=THEME.text_color
        )
        pie_info.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(pie_info))
        
        # Create simple bar chart for probabilities
        prob_chart = BarChart(
            values=[prob_0, prob_1],
            bar_names=["|0⟩", "|1⟩"],
            y_range=[0, 1, 0.25],
            y_length=3,
            x_length=4,
            bar_colors=[THEME.basis_color_left, THEME.basis_color_right]
        )
        prob_chart.to_edge(DOWN).shift(DOWN * 0.3).scale(0.7)
        
        self.play(Create(prob_chart))
        self.wait(4)
        
        self.play(
            FadeOut(title),
            FadeOut(state_formula),
            FadeOut(prob_formula_0),
            FadeOut(prob_formula_1),
            FadeOut(check),
            FadeOut(pie_info),
            FadeOut(prob_chart)
        )
    
    def show_projection_operators(self) -> None:
        """Demonstrate projection operators."""
        title = Text(
            "Projection Operators",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Definition
        definition = MathTex(
            r"\hat{P}_\phi = |\phi\rangle\langle\phi|",
            color=THEME.text_color,
            font_size=40
        )
        definition.shift(UP * 1.5)
        self.play(Write(definition))
        
        explanation = Text(
            "Projects any state onto |φ⟩",
            font_size=28,
            color=THEME.text_color
        )
        explanation.next_to(definition, DOWN, buff=0.4)
        self.play(Write(explanation))
        
        # Example
        example_title = Text(
            "Example: Project |+⟩ onto |0⟩",
            font_size=30,
            color=THEME.highlight_color
        )
        example_title.shift(DOWN * 0.5)
        self.play(Write(example_title))
        
        if QUTIP_AVAILABLE:
            ket_0 = basis(2, 0)
            ket_plus = (basis(2, 0) + basis(2, 1)).unit()
            
            # Projection operator
            P_0 = ket_0 * ket_0.dag()
            
            # Project |+⟩ onto |0⟩
            projected = P_0 * ket_plus
            
            # Probability
            prob = expect(P_0, ket_plus)
        else:
            prob = 0.5
        
        calculation = MathTex(
            r"\hat{P}_0|+\rangle = |0\rangle\langle 0|+\rangle = ",
            f"{np.sqrt(prob):.3f}|0\\rangle",
            color=THEME.text_color,
            font_size=32
        )
        calculation.next_to(example_title, DOWN, buff=0.5)
        self.play(Write(calculation))
        
        probability_text = MathTex(
            f"\\text{{Probability}} = {prob:.3f}",
            color=THEME.highlight_color,
            font_size=32
        )
        probability_text.next_to(calculation, DOWN, buff=0.4)
        self.play(Write(probability_text))
        
        self.wait(4)
        
        self.play(
            FadeOut(title),
            FadeOut(definition),
            FadeOut(explanation),
            FadeOut(example_title),
            FadeOut(calculation),
            FadeOut(probability_text)
        )
    
    def show_conclusion(self) -> None:
        """Show concluding remarks."""
        conclusion = VGroup(
            Text("Key Takeaways:", font_size=36, color=THEME.text_color),
            Text("• Inner product ⟨ψ|φ⟩ measures overlap", font_size=28, color=THEME.text_color),
            Text("• |⟨ψ|φ⟩|² gives measurement probability", font_size=28, color=THEME.text_color),
            Text("• Fidelity F(ψ,φ) quantifies similarity", font_size=28, color=THEME.text_color),
            Text("• Projection operators extract components", font_size=28, color=THEME.text_color),
            Text("• All probabilities sum to 1 (normalization)", font_size=28, color=THEME.text_color)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        conclusion.move_to(ORIGIN)
        self.play(Write(conclusion))
        self.wait(4)
        self.play(FadeOut(conclusion))
