"""Manim scene demonstrating basis states and superposition."""

from __future__ import annotations

import numpy as np
from manim import (Create, FadeIn, FadeOut, MathTex, NumberPlane, RIGHT, Scene, UP, DOWN,
                    ValueTracker, Vector, always_redraw)

from quantum_animation.config import THEME


class SuperpositionScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        plane = NumberPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), background_line_style={"stroke_opacity": 0.15})
        basis_label = MathTex(r"\{|0\rangle, |1\rangle\}", color=THEME.text_color).to_edge(UP)

        basis_zero = Vector(2.0 * RIGHT, color=THEME.basis_color_right)
        basis_one = Vector(2.0 * UP, color=THEME.basis_color_left)

        theta = ValueTracker(0.0)

        super_vec = always_redraw(
            lambda: Vector(
                np.cos(theta.get_value()) * RIGHT * 2.0 + np.sin(theta.get_value()) * UP * 2.0,
                color=THEME.vector_color,
            )
        )

        state_label = always_redraw(
            lambda: MathTex(
                r"|\psi\rangle = {\cos(\theta)}|0\rangle + {\sin(\theta)}|1\rangle",
                color=THEME.text_color,
            ).next_to(plane, DOWN)
        )

        self.play(Create(plane), FadeIn(basis_label))
        self.play(Create(basis_zero), Create(basis_one))
        self.play(FadeIn(super_vec), FadeIn(state_label))

        self.play(theta.animate.set_value(np.pi / 3), run_time=2)
        self.play(theta.animate.set_value(5 * np.pi / 6), run_time=2)
        self.play(theta.animate.set_value(np.pi / 4), run_time=2)

        self.play(*[FadeOut(mob) for mob in [plane, basis_label, basis_zero, basis_one, super_vec, state_label]])


__all__ = ["SuperpositionScene"]
