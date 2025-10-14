"""Manim scene introducing vectors and Hilbert space intuition."""

from manim import Create, FadeIn, FadeOut, NumberPlane, RIGHT, Scene, Tex, ThreeDAxes, UP, DOWN

from quantum_animation.config import THEME
from quantum_animation.utils.vector_helpers import create_labeled_vector


class VectorBasicsScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        plane = NumberPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), background_line_style={"stroke_opacity": 0.2})
        title = Tex("Vectors as Quantum States", color=THEME.text_color).to_edge(UP)

        basis_x = create_labeled_vector(2.2 * RIGHT, r"|e_1\rangle")
        basis_y = create_labeled_vector(1.8 * UP, r"|e_2\rangle")
        state = create_labeled_vector(1.5 * RIGHT + 1.2 * UP, r"|\psi\rangle")

        self.play(Create(plane), FadeIn(title))
        self.play(FadeIn(basis_x), FadeIn(basis_y))
        self.wait(1)
        self.play(FadeIn(state))
        self.wait(2)

        hilbert_axes = ThreeDAxes(x_range=(-2, 2, 1), y_range=(-2, 2, 1), z_range=(-2, 2, 1))
        hilbert_axes.scale(0.8).to_edge(DOWN)
        hilbert_label = Tex("Hilbert Space", color=THEME.text_color).next_to(hilbert_axes, UP)

        self.play(FadeOut(plane), FadeOut(basis_x), FadeOut(basis_y))
        self.play(Create(hilbert_axes), FadeIn(hilbert_label))
        self.wait(2)
        self.play(FadeOut(hilbert_axes), FadeOut(hilbert_label), FadeOut(state), FadeOut(title))


__all__ = ["VectorBasicsScene"]
