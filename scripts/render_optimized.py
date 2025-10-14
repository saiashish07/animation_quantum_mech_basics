"""Optimized parallel rendering script with caching and threading."""

from __future__ import annotations

import argparse
import multiprocessing as mp
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple


# Enhanced scene definitions with new numbered files
SCENES = {
    "complete": ("quantum_animation.scenes.00_complete", "QuantumMechanicsComplete"),
    "vectors": ("quantum_animation.scenes.01_vectors_hilbert", "VectorBasicsScene"),
    "inner_product": ("quantum_animation.scenes.02_inner_product", "InnerProductScene"),
    "orthogonality": ("quantum_animation.scenes.03_orthogonality", "OrthogonalityScene"),
    "superposition": ("quantum_animation.scenes.04_superposition", "SuperpositionScene"),
    "operators": ("quantum_animation.scenes.05_operators", "OperatorMeasurementScene"),
    "evolution": ("quantum_animation.scenes.06_evolution", "WavefunctionEvolutionScene"),
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def render_scene(
    scene_key: str, 
    quality: str, 
    preview: bool,
    use_cache: bool = True
) -> Tuple[str, int, float]:
    """
    Render a single scene and return timing information.
    
    Returns:
        Tuple of (scene_key, exit_code, elapsed_time)
    """
    start_time = time.time()
    
    module, class_name = SCENES[scene_key]
    module_path = PROJECT_ROOT / "src" / Path(module.replace(".", "/") + ".py")
    
    command = [
        sys.executable,
        "-m",
        "manim",
    ]
    
    # Add quality flags
    if quality == "l":
        command.extend(["-ql"])  # Low quality, fast render
    elif quality == "m":
        command.extend(["-qm"])  # Medium quality
    elif quality == "h":
        command.extend(["-qh"])  # High quality
    elif quality == "p":
        command.extend(["-qp"])  # Production quality
    
    # Preview flag
    if preview:
        command.append("-p")
    
    # Disable caching for fresh renders if requested
    if not use_cache:
        command.append("--flush_cache")
    
    # Add write to movie flag for better performance
    command.append("--write_to_movie")
    
    # Scene specification
    command.extend([str(module_path), class_name])
    
    print(f"\n{'='*60}")
    print(f"🎬 Rendering: {scene_key}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=False,  # Show output in real-time
            text=True,
            check=False
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {scene_key} completed in {elapsed:.2f}s")
        else:
            print(f"❌ {scene_key} failed with code {result.returncode}")
        
        return (scene_key, result.returncode, elapsed)
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ {scene_key} raised exception: {e}")
        return (scene_key, 1, elapsed)


def render_parallel(
    scene_keys: List[str],
    quality: str,
    preview: bool,
    max_workers: int | None = None,
    use_cache: bool = True
) -> Dict[str, Tuple[int, float]]:
    """
    Render multiple scenes in parallel using ThreadPoolExecutor.
    
    Args:
        scene_keys: List of scene keys to render
        quality: Quality level (l, m, h, p)
        preview: Whether to preview after rendering
        max_workers: Maximum number of parallel workers (default: CPU count)
        use_cache: Whether to use Manim's caching system
    
    Returns:
        Dictionary mapping scene_key to (exit_code, elapsed_time)
    """
    if max_workers is None:
        # Use number of CPU cores, but cap at 4 to avoid overwhelming system
        max_workers = min(mp.cpu_count(), 4)
    
    print(f"\n🚀 Starting parallel render with {max_workers} workers")
    print(f"📊 Rendering {len(scene_keys)} scene(s)")
    print(f"⚙️  Quality: {quality}, Cache: {use_cache}, Preview: {preview}\n")
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all render jobs
        future_to_scene = {
            executor.submit(render_scene, key, quality, preview, use_cache): key
            for key in scene_keys
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_scene):
            scene_key, exit_code, elapsed = future.result()
            results[scene_key] = (exit_code, elapsed)
    
    return results


def print_summary(results: Dict[str, Tuple[int, float]]) -> int:
    """Print render summary and return overall exit code."""
    print(f"\n{'='*60}")
    print("📈 RENDER SUMMARY")
    print(f"{'='*60}\n")
    
    total_time = sum(elapsed for _, elapsed in results.values())
    successful = sum(1 for code, _ in results.values() if code == 0)
    failed = len(results) - successful
    
    for scene_key, (exit_code, elapsed) in sorted(results.items()):
        status = "✅" if exit_code == 0 else "❌"
        print(f"{status} {scene_key:20s} - {elapsed:6.2f}s - Exit code: {exit_code}")
    
    print(f"\n{'='*60}")
    print(f"Total scenes: {len(results)}")
    print(f"Successful:   {successful}")
    print(f"Failed:       {failed}")
    print(f"Total time:   {total_time:.2f}s")
    print(f"{'='*60}\n")
    
    return 0 if failed == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Optimized parallel renderer for quantum mechanics scenes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Render all scenes in parallel at high quality
  python scripts/render_optimized.py --quality h --parallel
  
  # Render complete video (single file)
  python scripts/render_optimized.py complete --quality h
  
  # Render specific scenes sequentially
  python scripts/render_optimized.py vectors inner_product --quality m
  
  # Fast preview with cache disabled
  python scripts/render_optimized.py --quality l --no-cache --preview
        """
    )
    
    parser.add_argument(
        "scenes",
        nargs="*",
        default=["all"],
        help="Scene keys to render (default: all). Use 'complete' for single combined video."
    )
    
    parser.add_argument(
        "--quality", "-q",
        default="m",
        choices=["l", "m", "h", "p"],
        help="Render quality: l=low(480p), m=medium(720p), h=high(1080p), p=production(1440p)"
    )
    
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="Open rendered video(s) after completion"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Render scenes in parallel (faster, uses more resources)"
    )
    
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=None,
        help="Number of parallel workers (default: min(CPU_count, 4))"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable Manim caching for fresh renders"
    )
    
    args = parser.parse_args()
    
    # Determine which scenes to render
    if "all" in args.scenes:
        # Render all individual scenes (not the complete one)
        scene_keys = [k for k in SCENES.keys() if k != "complete"]
    else:
        scene_keys = []
        for s in args.scenes:
            if s in SCENES:
                scene_keys.append(s)
            else:
                print(f"⚠️  Unknown scene: {s}")
                print(f"Available scenes: {', '.join(SCENES.keys())}")
                return 1
    
    if not scene_keys:
        print("❌ No valid scenes to render")
        return 1
    
    # Render
    use_cache = not args.no_cache
    
    if args.parallel and len(scene_keys) > 1:
        # Parallel rendering
        results = render_parallel(
            scene_keys,
            args.quality,
            args.preview,
            args.workers,
            use_cache
        )
        return print_summary(results)
    else:
        # Sequential rendering
        print(f"\n🎬 Sequential rendering mode\n")
        results = {}
        for key in scene_keys:
            _, exit_code, elapsed = render_scene(key, args.quality, args.preview, use_cache)
            results[key] = (exit_code, elapsed)
            if exit_code != 0:
                print(f"\n⚠️  Scene {key} failed, stopping")
                break
        
        return print_summary(results)


if __name__ == "__main__":
    raise SystemExit(main())
