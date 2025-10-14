"""Manim scene demonstrating inner products and normalization."""

from __future__ import annotations

import numpy as np
from manim import (Create, DashedLine, FadeIn, FadeOut, MathTex, NumberPlane, RIGHT,
                    Scene, UP, DOWN, Vector)

from quantum_animation.config import THEME
from quantum_animation.utils.vector_helpers import projection_length


class InnerProductScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        plane = NumberPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), background_line_style={"stroke_opacity": 0.15})
        title = MathTex(r"\langle a | b \rangle", color=THEME.text_color).to_edge(UP)

        vec_a_end = 2.2 * RIGHT + 0.6 * UP
        vec_b_end = 1.0 * RIGHT + 1.7 * UP
        vec_a = Vector(vec_a_end, color=THEME.vector_color)
        vec_b = Vector(vec_b_end, color=THEME.highlight_color)

        self.play(Create(plane), FadeIn(title))
        self.play(Create(vec_a), Create(vec_b))

        scalar = projection_length(vec_b_end, vec_a_end)
        proj_end = scalar * vec_a_end
        projection = Vector(proj_end, color=THEME.highlight_color)
        projection.set_opacity(0.6)
        drop = DashedLine(vec_b_end, proj_end, color=THEME.text_color, dash_length=0.12)

        self.play(Create(projection), Create(drop))
        self.wait(1.5)

        norm_formula = MathTex(r"\|a\| = 1", color=THEME.text_color).next_to(title, DOWN)
        normalized_vec = Vector(vec_a_end / np.linalg.norm(vec_a_end), color=THEME.vector_color)
        self.play(FadeIn(norm_formula))
        self.play(FadeOut(vec_a), Create(normalized_vec))
        self.wait(1.5)

        elements = [plane, title, vec_b, projection, drop, norm_formula, normalized_vec]
        self.play(*[FadeOut(mob) for mob in elements])


__all__ = ["InnerProductScene"]
