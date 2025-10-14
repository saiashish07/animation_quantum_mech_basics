"""Manim scene illustrating orthogonality of quantum states."""

from manim import Angle, Create, FadeIn, FadeOut, MathTex, NumberPlane, RIGHT, Scene, UP, Vector

from quantum_animation.config import THEME


class OrthogonalityScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color

        plane = NumberPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), background_line_style={"stroke_opacity": 0.15})
        label = MathTex(r"\langle e_1 | e_2 \rangle = 0", color=THEME.text_color).to_edge(UP)
        label.set_color_by_tex("e_1", THEME.basis_color_right)
        label.set_color_by_tex("e_2", THEME.basis_color_left)

        vec_x = Vector(2.0 * RIGHT, color=THEME.basis_color_right)
        vec_y = Vector(2.0 * UP, color=THEME.basis_color_left)

        self.play(Create(plane), FadeIn(label))
        self.play(Create(vec_x), Create(vec_y))

        right_angle = Angle(vec_x, vec_y, radius=0.6, quadrant=(1, 1), other_angle=False, color=THEME.highlight_color)
        zero_overlap = MathTex(r"\langle e_1 | e_2 \rangle = 0", color=THEME.text_color).next_to(right_angle, UP)

        self.play(Create(right_angle), FadeIn(zero_overlap))
        self.wait(2)

        self.play(FadeOut(plane), FadeOut(vec_x), FadeOut(vec_y), FadeOut(right_angle), FadeOut(zero_overlap), FadeOut(label))


__all__ = ["OrthogonalityScene"]
