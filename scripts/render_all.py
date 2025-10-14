"""Helper script to batch-render the quantum animation scenes with Manim."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCENES = {
    "vectors": ("quantum_animation.scenes.vectors_hilbert", "VectorBasicsScene"),
    "inner_product": ("quantum_animation.scenes.inner_product", "InnerProductScene"),
    "orthogonality": ("quantum_animation.scenes.orthogonality", "OrthogonalityScene"),
    "superposition": ("quantum_animation.scenes.basis_superposition", "SuperpositionScene"),
    "operators": ("quantum_animation.scenes.operators_eigenvalues", "OperatorMeasurementScene"),
    "evolution": ("quantum_animation.scenes.wavefunction_evolution", "WavefunctionEvolutionScene"),
}



PROJECT_ROOT = Path(__file__).resolve().parents[1]


def render(scene_key: str, quality: str, preview: bool) -> int:
    module, class_name = SCENES[scene_key]
    module_path = PROJECT_ROOT / "src" / Path(module.replace(".", "/") + ".py")
    command = [
        sys.executable,
        "-m",
        "manim",
        "-q",
        quality,
    ]
    if preview:
        command.append("-p")
    command.extend([str(module_path), class_name])

    print("Running:", " ".join(command))
    return subprocess.call(command)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render predefined quantum mechanics scenes.")
    parser.add_argument(
        "scene",
        choices=list(SCENES.keys()) + ["all"],
        nargs="?",
        default="all",
        help="Scene key to render or 'all'.",
    )
    parser.add_argument("--quality", default="m", choices=["l", "m", "h", "p"], help="Manim quality flag (l=low, m=medium, h=high, p=production).")
    parser.add_argument("--preview", action="store_true", help="Open the rendered video after completion.")
    args = parser.parse_args()

    if args.scene == "all":
        for name in SCENES:
            if render(name, args.quality, args.preview):
                return 1
        return 0

    return render(args.scene, args.quality, args.preview)


if __name__ == "__main__":
    raise SystemExit(main())
