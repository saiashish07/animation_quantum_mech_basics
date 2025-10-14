"""Master scene that combines all quantum mechanics topics into one video."""

from manim import Scene, Wait, FadeOut, Text, Write

from quantum_animation.config import THEME


class QuantumMechanicsComplete(Scene):
    """
    Complete quantum mechanics animation combining all topics.
    This creates a single unified video covering:
    1. Vectors and Hilbert Space
    2. Inner Products and Normalization
    3. Orthogonality
    4. Basis and Superposition
    5. Operators and Eigenvalues
    6. Wavefunction Evolution
    
    Note: Due to Manim's architecture, we can't directly call other scene's construct().
    Instead, we'll import and recreate the content in sequence.
    """
    
    def construct(self) -> None:
        self.camera.background_color = THEME.background_color
        
        # Opening title
        opening = Text(
            "Quantum Mechanics Through Linear Algebra",
            font_size=48,
            color=THEME.text_color
        )
        subtitle = Text(
            "A Visual Introduction",
            font_size=32,
            color=THEME.highlight_color
        )
        subtitle.next_to(opening, DOWN)
        
        self.play(Write(opening))
        self.play(Write(subtitle))
        self.wait(3)
        self.play(FadeOut(opening), FadeOut(subtitle))
        self.wait(1)
        
        # Import and run each scene's logic
        from quantum_animation.scenes.01_vectors_hilbert import VectorBasicsScene
        vectors_scene = VectorBasicsScene()
        vectors_scene.camera = self.camera
        vectors_scene.construct()
        self.wait(1)
        
        from quantum_animation.scenes.02_inner_product import InnerProductScene
        inner_scene = InnerProductScene()
        inner_scene.camera = self.camera
        inner_scene.construct()
        self.wait(1)
        
        from quantum_animation.scenes.03_orthogonality import OrthogonalityScene
        ortho_scene = OrthogonalityScene()
        ortho_scene.camera = self.camera
        ortho_scene.construct()
        self.wait(1)
        
        from quantum_animation.scenes.04_superposition import SuperpositionScene
        super_scene = SuperpositionScene()
        super_scene.camera = self.camera
        super_scene.construct()
        self.wait(1)
        
        from quantum_animation.scenes.05_operators import OperatorMeasurementScene
        op_scene = OperatorMeasurementScene()
        op_scene.camera = self.camera
        op_scene.construct()
        self.wait(1)
        
        from quantum_animation.scenes.06_evolution import WavefunctionEvolutionScene
        evo_scene = WavefunctionEvolutionScene()
        evo_scene.camera = self.camera
        evo_scene.construct()
        
        # Closing
        closing = Text(
            "Thank you for watching!",
            font_size=44,
            color=THEME.highlight_color
        )
        self.play(Write(closing))
        self.wait(3)
        self.play(FadeOut(closing))


__all__ = ["QuantumMechanicsComplete"]
