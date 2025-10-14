"""Manim scene connecting linear operators to eigenvalues and measurements."""

from __future__ import annotations

from manim import (ApplyMatrix, Create, FadeIn, FadeOut, MathTex, Matrix, NumberPlane,
                    RIGHT, Scene, UP, Vector)

from quantum_animation.config import THEME


class OperatorMeasurementScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        operator_display = Matrix([[2, 0], [0, 1]], element_to_mobject_config={"color": THEME.text_color})
        operator_title = MathTex(r"\hat{A}", color=THEME.text_color).next_to(operator_display, UP)

        plane = NumberPlane(background_line_style={"stroke_opacity": 0.1})
        eigenvector = Vector(RIGHT + UP, color=THEME.vector_color)
        eigen_label = MathTex(r"|v\rangle", color=THEME.text_color).next_to(eigenvector.get_end(), UP)

        self.play(FadeIn(operator_title), FadeIn(operator_display))
        self.play(Create(plane))
        self.play(Create(eigenvector), FadeIn(eigen_label))

        scaling_matrix = [[2.0, 0.0], [0.0, 1.0]]
        result_label = MathTex(r"\hat{A}|v\rangle = 2|v\rangle", color=THEME.text_color).to_edge(UP)

        self.play(FadeIn(result_label))
        self.play(ApplyMatrix(scaling_matrix, plane), ApplyMatrix(scaling_matrix, eigenvector))
        self.wait(1.5)

        self.play(FadeOut(plane), FadeOut(eigenvector), FadeOut(eigen_label), FadeOut(operator_title), FadeOut(operator_display), FadeOut(result_label))


__all__ = ["OperatorMeasurementScene"]
