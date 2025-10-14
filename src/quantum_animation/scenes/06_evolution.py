"""Enhanced wavefunction evolution scene with Schrödinger equation visualization."""

from __future__ import annotations

import numpy as np
from manim import (Axes, Create, FadeIn, FadeOut, MathTex, RIGHT, Scene, UP,
                    ValueTracker, always_redraw, Write, Text, VGroup, DOWN, LEFT)

from quantum_animation.config import THEME


class WavefunctionEvolutionScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        # Title
        title = Text("Time Evolution: The Schrödinger Equation", 
                    font_size=40, color=THEME.text_color)
        title.to_edge(UP)
        
        subtitle = Text("How quantum states change with time", 
                       font_size=28, color=THEME.highlight_color)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # Schrödinger equation
        schrodinger = MathTex(
            r"i\hbar \frac{\partial}{\partial t}|\psi(t)\rangle = \hat{H}|\psi(t)\rangle",
            color=THEME.text_color,
            font_size=40
        )
        schrodinger.next_to(title, DOWN)
        
        components = VGroup(
            MathTex(r"i\hbar", r" = \text{quantum constant}", color=THEME.text_color, font_size=26),
            MathTex(r"\hat{H}", r" = \text{Hamiltonian (total energy)}", color=THEME.text_color, font_size=26),
            MathTex(r"|\psi(t)\rangle", r" = \text{quantum state at time } t", color=THEME.text_color, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        components.next_to(schrodinger, DOWN, buff=0.5)

        self.play(Write(schrodinger))
        self.wait(2)
        for comp in components:
            self.play(Write(comp))
            self.wait(1.2)
        
        self.wait(2)
        
        # Transition to visual
        self.play(*[FadeOut(mob) for mob in [schrodinger, components]])

        # Axes setup
        visual_title = Text("1D Wavefunction Evolution", 
                           font_size=32, color=THEME.text_color)
        visual_title.next_to(title, DOWN)
        
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "color": THEME.text_color,
                "include_tip": True,
                "include_numbers": False
            }
        )
        axes.scale(0.8)
        
        x_label = MathTex("x", r"\text{ (position)}", color=THEME.text_color, font_size=30)
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        
        psi_label = MathTex(r"\Re[\psi(x,t)]", r"\text{ (real part)}", color=THEME.text_color, font_size=30)
        psi_label.next_to(axes.y_axis.get_top(), UP)

        self.play(Write(visual_title))
        self.play(Create(axes), Write(x_label), Write(psi_label))
        self.wait(1)

        # Time tracker
        time = ValueTracker(0.0)
        
        time_display = always_redraw(
            lambda: MathTex(
                f"t = {time.get_value():.2f}",
                color=THEME.highlight_color,
                font_size=32
            ).to_edge(DOWN).shift(UP * 0.5)
        )

        # Wavefunction: Gaussian wave packet with time evolution
        def wavefunction(x: float, t: float) -> float:
            """Spreading Gaussian wave packet."""
            width = 1.0 + 0.3 * t  # Spreading over time
            envelope = np.exp(-0.5 * x**2 / width**2)
            oscillation = np.cos(2.0 * x - 3.0 * t)
            return envelope * oscillation

        wave_graph = always_redraw(
            lambda: axes.plot(
                lambda x: wavefunction(x, time.get_value()),
                color=THEME.vector_color,
                stroke_width=4
            )
        )
        
        # Probability density overlay
        prob_graph = always_redraw(
            lambda: axes.plot(
                lambda x: wavefunction(x, time.get_value())**2,
                color=THEME.amplitude_positive,
                stroke_width=3,
                stroke_opacity=0.6
            )
        )

        prob_legend = MathTex(
            r"|\psi|^2", r"\text{ (probability density)}",
            color=THEME.amplitude_positive,
            font_size=24
        )
        prob_legend.to_edge(DOWN).shift(UP * 2 + LEFT * 3)

        self.play(Create(wave_graph), Write(time_display))
        self.wait(1.5)
        
        self.play(Create(prob_graph), Write(prob_legend))
        self.wait(1.5)

        # Animate evolution
        evolution_text = Text("Watching the wavefunction evolve...", 
                             font_size=26, color=THEME.highlight_color)
        evolution_text.next_to(prob_legend, DOWN, buff=0.3)
        
        self.play(FadeIn(evolution_text))
        self.wait(0.5)

        # Slow evolution
        self.play(time.animate.set_value(2.0), run_time=4, rate_func=lambda t: t)
        self.wait(1)
        
        self.play(time.animate.set_value(4.0), run_time=4, rate_func=lambda t: t)
        self.wait(1)
        
        self.play(time.animate.set_value(6.0), run_time=4, rate_func=lambda t: t)
        self.wait(2)

        # Key observations
        self.play(FadeOut(evolution_text))
        
        observations = VGroup(
            Text("Key Observations:", font_size=28, color=THEME.highlight_color),
            Text("• Wave packet spreads over time", font_size=24, color=THEME.text_color),
            Text("• Oscillations continue (de Broglie waves)", font_size=24, color=THEME.text_color),
            Text("• Probability density |ψ|² also evolves", font_size=24, color=THEME.text_color),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        observations.to_edge(DOWN).shift(UP * 0.3)

        for obs in observations:
            self.play(Write(obs))
            self.wait(1.3)
        
        self.wait(3)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)


__all__ = ["WavefunctionEvolutionScene"]
