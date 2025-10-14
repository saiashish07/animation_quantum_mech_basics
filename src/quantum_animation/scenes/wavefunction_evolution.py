"""Manim scene showing a simple wavefunction evolving in time."""

from __future__ import annotations

import numpy as np
from manim import (Axes, Create, FadeIn, FadeOut, MathTex, RIGHT, Scene, UP,
                    ValueTracker, always_redraw)

from quantum_animation.config import THEME


class WavefunctionEvolutionScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        axes = Axes(x_range=(-4, 4, 1), y_range=(-1.2, 1.2, 0.4), axis_config={"color": THEME.text_color})
        axes_labels = MathTex(r"x", r"\Re[\psi(x, t)]", color=THEME.text_color)
        axes_labels[0].next_to(axes.x_axis.get_end(), RIGHT)
        axes_labels[1].next_to(axes.y_axis.get_top(), UP)

        schrodinger = MathTex(r"i\hbar \frac{\partial}{\partial t}|\psi(t)\rangle = \hat{H}|\psi(t)\rangle", color=THEME.text_color).to_edge(UP)

        time = ValueTracker(0.0)

        def wavefunction(x: float, t: float) -> float:
            return np.exp(-0.5 * x**2) * np.cos(2.0 * x - t)

        wave_graph = always_redraw(lambda: axes.plot(lambda x: wavefunction(x, time.get_value()), color=THEME.vector_color))

        self.play(Create(axes), FadeIn(axes_labels), FadeIn(schrodinger))
        self.play(Create(wave_graph))

        self.play(time.animate.set_value(2.5), run_time=3)
        self.play(time.animate.set_value(5.0), run_time=3)

        self.play(FadeOut(axes), FadeOut(axes_labels), FadeOut(schrodinger), FadeOut(wave_graph))


__all__ = ["WavefunctionEvolutionScene"]
