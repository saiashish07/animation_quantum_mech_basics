"""Enhanced Scene 01: Vectors & Hilbert Space using QuTiP Bloch Sphere.

This scene demonstrates quantum states as vectors using QuTiP's quantum objects
and visualizes them on the Bloch sphere - a real quantum mechanics tool.

Duration: ~2 minutes
"""

from __future__ import annotations

import numpy as np
from manim import (
    Create, FadeIn, FadeOut, MathTex, Scene, Text, VGroup, 
    Write, UP, DOWN, LEFT, RIGHT, OUT, IN, ORIGIN, ThreeDScene, ThreeDAxes,
    Arrow3D, Sphere, Surface, ParametricFunction, Line, Dot,
    ReplacementTransform, Transform, ValueTracker, always_redraw,
    DecimalNumber, PI, TAU, RED, GREEN, BLUE, YELLOW, WHITE
)

# Import QuTiP for quantum state manipulation
try:
    from qutip import basis, sigmax, sigmay, sigmaz, Bloch
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False
    print("Warning: QuTiP not available. Install with: pip install qutip")

from quantum_animation.config import THEME


class QuantumVectorBlochScene(ThreeDScene):
    """Demonstrate quantum states as vectors on the Bloch sphere using QuTiP."""
    
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color
        
        # Introduction
        self.show_introduction()
        self.wait(2)
        
        # Part 1: Classical vectors to quantum states
        self.classical_to_quantum()
        self.wait(3)
        
        # Part 2: Bloch sphere introduction
        self.introduce_bloch_sphere()
        self.wait(3)
        
        # Part 3: Basis states on Bloch sphere
        self.show_basis_states()
        self.wait(4)
        
        # Part 4: Superposition states
        self.show_superposition_states()
        self.wait(4)
        
        # Part 5: Continuous rotation
        self.animate_state_evolution()
        self.wait(4)
        
        # Conclusion
        self.show_conclusion()
        self.wait(3)
    
    def show_introduction(self) -> None:
        """Show title and motivation."""
        title = Text(
            "Quantum States as Vectors",
            font_size=48,
            color=THEME.text_color
        )
        title.to_edge(UP)
        
        subtitle = Text(
            "Visualized on the Bloch Sphere",
            font_size=32,
            color=THEME.highlight_color
        )
        subtitle.next_to(title, DOWN)
        
        if not QUTIP_AVAILABLE:
            warning = Text(
                "QuTiP not installed - showing conceptual version",
                font_size=24,
                color=RED
            )
            warning.next_to(subtitle, DOWN)
            self.play(Write(title), Write(subtitle), Write(warning))
        else:
            self.play(Write(title), Write(subtitle))
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def classical_to_quantum(self) -> None:
        """Transition from classical to quantum vectors."""
        # 2D classical vector
        explanation = Text(
            "Classical vectors: arrows in space",
            font_size=32,
            color=THEME.text_color
        )
        explanation.to_edge(UP)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        
        # Show 2D plane with vector
        classical_vec = Arrow3D(
            start=ORIGIN,
            end=[2, 1, 0],
            color=THEME.vector_color
        )
        
        label_classical = MathTex(
            r"\vec{v} = (v_x, v_y)",
            color=THEME.text_color
        )
        label_classical.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(label_classical)
        
        self.play(Create(classical_vec), Write(label_classical))
        self.wait(2)
        
        # Transition text
        transition = Text(
            "Quantum states: vectors in Hilbert space",
            font_size=32,
            color=THEME.highlight_color
        )
        transition.to_edge(UP)
        self.add_fixed_in_frame_mobjects(transition)
        
        quantum_label = MathTex(
            r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle",
            color=THEME.text_color
        )
        quantum_label.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(quantum_label)
        
        self.play(
            ReplacementTransform(explanation, transition),
            ReplacementTransform(label_classical, quantum_label),
            FadeOut(classical_vec)
        )
        self.wait(2)
        
        self.play(FadeOut(transition), FadeOut(quantum_label))
    
    def introduce_bloch_sphere(self) -> None:
        """Introduce the Bloch sphere representation."""
        # Set up 3D view
        self.set_camera_orientation(phi=75 * PI / 180, theta=-45 * PI / 180)
        
        title = Text(
            "The Bloch Sphere",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create Bloch sphere
        sphere = Sphere(
            radius=2,
            resolution=(20, 20),
            u_range=[0, PI],
            v_range=[0, TAU]
        )
        sphere.set_opacity(0.2)
        sphere.set_color(THEME.highlight_color)
        
        # Axes
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5],
            y_range=[-2.5, 2.5],
            z_range=[-2.5, 2.5],
            x_length=5,
            y_length=5,
            z_length=5
        )
        
        # Axis labels
        x_label = MathTex("X", color=RED).scale(0.7)
        y_label = MathTex("Y", color=GREEN).scale(0.7)
        z_label = MathTex("Z", color=BLUE).scale(0.7)
        
        x_label.next_to(axes.c2p(2.5, 0, 0), RIGHT)
        y_label.next_to(axes.c2p(0, 2.5, 0), UP)
        z_label.next_to(axes.c2p(0, 0, 2.5), OUT)
        
        self.play(Create(axes), Create(sphere))
        self.play(Write(x_label), Write(y_label), Write(z_label))
        
        info = Text(
            "All possible qubit states live on this sphere",
            font_size=28,
            color=THEME.text_color
        )
        info.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(info)
        self.play(Write(info))
        
        self.wait(2)
        self.play(FadeOut(title), FadeOut(info))
        
        # Store for later use
        self.sphere = sphere
        self.axes = axes
        self.axis_labels = VGroup(x_label, y_label, z_label)
    
    def show_basis_states(self) -> None:
        """Show |0⟩ and |1⟩ states on Bloch sphere."""
        title = Text(
            "Computational Basis States",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # |0⟩ state at north pole (z = +1)
        state_0_vec = Arrow3D(
            start=ORIGIN,
            end=[0, 0, 2],
            color=THEME.basis_color_left
        )
        
        state_0_label = MathTex(r"|0\rangle", color=THEME.basis_color_left)
        state_0_label.next_to(self.axes.c2p(0, 0, 2.5), UP)
        self.add_fixed_in_frame_mobjects(state_0_label)
        
        state_0_dot = Dot(self.axes.c2p(0, 0, 2), color=THEME.basis_color_left)
        
        info_0 = Text(
            "|0⟩: North pole (spin up)",
            font_size=28,
            color=THEME.text_color
        )
        info_0.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(info_0)
        
        self.play(
            Create(state_0_vec),
            Create(state_0_dot),
            Write(state_0_label),
            Write(info_0)
        )
        self.wait(2)
        
        # |1⟩ state at south pole (z = -1)
        state_1_vec = Arrow3D(
            start=ORIGIN,
            end=[0, 0, -2],
            color=THEME.basis_color_right
        )
        
        state_1_label = MathTex(r"|1\rangle", color=THEME.basis_color_right)
        state_1_label.next_to(self.axes.c2p(0, 0, -2.5), DOWN)
        self.add_fixed_in_frame_mobjects(state_1_label)
        
        state_1_dot = Dot(self.axes.c2p(0, 0, -2), color=THEME.basis_color_right)
        
        info_1 = Text(
            "|1⟩: South pole (spin down)",
            font_size=28,
            color=THEME.text_color
        )
        info_1.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(info_1)
        
        self.play(
            ReplacementTransform(info_0, info_1),
            Create(state_1_vec),
            Create(state_1_dot),
            Write(state_1_label)
        )
        self.wait(2)
        
        # Highlight orthogonality
        ortho_info = Text(
            "These states are orthogonal: ⟨0|1⟩ = 0",
            font_size=28,
            color=THEME.highlight_color
        )
        ortho_info.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(ortho_info)
        
        self.play(ReplacementTransform(info_1, ortho_info))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(ortho_info))
        
        # Clean up
        self.play(
            FadeOut(state_0_vec),
            FadeOut(state_1_vec)
        )
        
        self.basis_dots = VGroup(state_0_dot, state_1_dot)
        self.basis_labels = VGroup(state_0_label, state_1_label)
    
    def show_superposition_states(self) -> None:
        """Show superposition states on the equator and elsewhere."""
        title = Text(
            "Superposition States",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # |+⟩ state (x-axis, equator)
        plus_vec = Arrow3D(
            start=ORIGIN,
            end=[2, 0, 0],
            color=THEME.highlight_color
        )
        
        plus_dot = Dot(self.axes.c2p(2, 0, 0), color=THEME.highlight_color)
        
        plus_label = MathTex(
            r"|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)",
            color=THEME.text_color
        )
        plus_label.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(plus_label)
        
        self.play(
            Create(plus_vec),
            Create(plus_dot),
            Write(plus_label)
        )
        self.wait(3)
        
        # |-⟩ state (-x-axis)
        minus_vec = Arrow3D(
            start=ORIGIN,
            end=[-2, 0, 0],
            color=YELLOW
        )
        
        minus_dot = Dot(self.axes.c2p(-2, 0, 0), color=YELLOW)
        
        minus_label = MathTex(
            r"|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)",
            color=THEME.text_color
        )
        minus_label.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(minus_label)
        
        self.play(
            ReplacementTransform(plus_label, minus_label),
            Create(minus_vec),
            Create(minus_dot)
        )
        self.wait(3)
        
        # General superposition
        general_label = MathTex(
            r"|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle",
            color=THEME.text_color,
            font_size=28
        )
        general_label.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(general_label)
        
        self.play(ReplacementTransform(minus_label, general_label))
        self.wait(3)
        
        self.play(
            FadeOut(title),
            FadeOut(general_label),
            FadeOut(plus_vec),
            FadeOut(minus_vec)
        )
        
        self.superposition_dots = VGroup(plus_dot, minus_dot)
    
    def animate_state_evolution(self) -> None:
        """Animate a state evolving on the Bloch sphere."""
        title = Text(
            "State Evolution",
            font_size=36,
            color=THEME.text_color
        )
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        info = Text(
            "Quantum states rotate on the Bloch sphere",
            font_size=28,
            color=THEME.text_color
        )
        info.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(info)
        self.play(Write(info))
        
        # Animate rotating camera
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # Create an evolving state vector
        theta_tracker = ValueTracker(0)
        phi_tracker = ValueTracker(0)
        
        def get_state_vector():
            theta = theta_tracker.get_value()
            phi = phi_tracker.get_value()
            x = 2 * np.sin(theta) * np.cos(phi)
            y = 2 * np.sin(theta) * np.sin(phi)
            z = 2 * np.cos(theta)
            return Arrow3D(
                start=ORIGIN,
                end=[x, y, z],
                color=THEME.vector_color
            )
        
        state_vec = always_redraw(get_state_vector)
        
        def get_state_dot():
            theta = theta_tracker.get_value()
            phi = phi_tracker.get_value()
            x = 2 * np.sin(theta) * np.cos(phi)
            y = 2 * np.sin(theta) * np.sin(phi)
            z = 2 * np.cos(theta)
            return Dot(self.axes.c2p(x, y, z), color=THEME.vector_color)
        
        state_dot = always_redraw(get_state_dot)
        
        self.play(Create(state_vec), Create(state_dot))
        
        # Rotate through various states
        self.play(
            theta_tracker.animate.set_value(PI/2),
            run_time=3,
            rate_func=lambda t: t
        )
        
        self.play(
            phi_tracker.animate.set_value(2*PI),
            run_time=5,
            rate_func=lambda t: t
        )
        
        self.play(
            theta_tracker.animate.set_value(PI),
            run_time=3,
            rate_func=lambda t: t
        )
        
        self.stop_ambient_camera_rotation()
        
        self.play(FadeOut(title), FadeOut(info))
        self.play(FadeOut(state_vec), FadeOut(state_dot))
    
    def show_conclusion(self) -> None:
        """Conclude with key takeaways."""
        conclusion = VGroup(
            Text("Key Takeaways:", font_size=36, color=THEME.text_color),
            Text("• Qubits are vectors on the Bloch sphere", font_size=28, color=THEME.text_color),
            Text("• |0⟩ and |1⟩ are at the poles", font_size=28, color=THEME.text_color),
            Text("• Superpositions fill the entire sphere", font_size=28, color=THEME.text_color),
            Text("• Quantum evolution = rotation on sphere", font_size=28, color=THEME.text_color)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        conclusion.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(conclusion)
        
        self.play(FadeOut(self.sphere), FadeOut(self.axes), FadeOut(self.axis_labels))
        if hasattr(self, 'basis_dots'):
            self.play(FadeOut(self.basis_dots), FadeOut(self.basis_labels))
        if hasattr(self, 'superposition_dots'):
            self.play(FadeOut(self.superposition_dots))
        
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
