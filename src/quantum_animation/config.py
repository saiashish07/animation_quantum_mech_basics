"""Global configuration for consistent styling across scenes."""

from dataclasses import dataclass
from manim import BLUE_D, GREEN_E, MAROON_E, ORANGE, PURPLE, TEAL_E, WHITE


@dataclass(frozen=True)
class ThemeConfig:
    background_color: str = "#0f172a"
    vector_color: str = TEAL_E.to_hex()
    basis_color_left: str = MAROON_E.to_hex()
    basis_color_right: str = BLUE_D.to_hex()
    highlight_color: str = ORANGE.to_hex()
    amplitude_positive: str = GREEN_E.to_hex()
    amplitude_negative: str = PURPLE.to_hex()
    text_color: str = WHITE.to_hex()


THEME = ThemeConfig()
