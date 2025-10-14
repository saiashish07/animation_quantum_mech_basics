"""Script to concatenate all individual scene videos into one complete video."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = PROJECT_ROOT / "media" / "videos"


def find_videos(quality: str) -> List[Path]:
    """
    Find all rendered scene videos in order.
    
    Args:
        quality: Quality folder name (480p15, 720p30, 1080p60, 1440p60)
    
    Returns:
        List of video file paths in sequence
    """
    scene_order = [
        "01_vectors_hilbert",
        "02_inner_product",
        "03_orthogonality",
        "04_superposition",
        "05_operators",
        "06_evolution",
    ]
    
    class_names = {
        "01_vectors_hilbert": "VectorBasicsScene",
        "02_inner_product": "InnerProductScene",
        "03_orthogonality": "OrthogonalityScene",
        "04_superposition": "SuperpositionScene",
        "05_operators": "OperatorMeasurementScene",
        "06_evolution": "WavefunctionEvolutionScene",
    }
    
    videos = []
    for scene in scene_order:
        video_path = MEDIA_DIR / scene / quality / f"{class_names[scene]}.mp4"
        if video_path.exists():
            videos.append(video_path)
            print(f"✓ Found: {video_path.name}")
        else:
            print(f"✗ Missing: {video_path}")
            print(f"  Expected at: {video_path}")
    
    return videos


def create_concat_file(videos: List[Path], output_file: Path) -> None:
    """Create ffmpeg concat file listing all videos."""
    with open(output_file, 'w') as f:
        for video in videos:
            # ffmpeg concat requires absolute paths or relative to concat file
            f.write(f"file '{video.absolute()}'\n")
    print(f"\n📄 Created concat file: {output_file}")


def concatenate_videos(
    videos: List[Path],
    output_path: Path,
    quality: str
) -> int:
    """
    Concatenate videos using ffmpeg.
    
    Returns:
        Exit code (0 = success)
    """
    if not videos:
        print("❌ No videos to concatenate")
        return 1
    
    print(f"\n🎬 Concatenating {len(videos)} videos...")
    print(f"📹 Output: {output_path}")
    
    # Create temporary concat file
    concat_file = output_path.parent / "filelist.txt"
    create_concat_file(videos, concat_file)
    
    # ffmpeg command
    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",  # Copy streams without re-encoding (fast!)
        "-y",  # Overwrite output file
        str(output_path)
    ]
    
    print(f"\nRunning: {' '.join(command)}\n")
    
    try:
        result = subprocess.run(command, check=False)
        
        if result.returncode == 0:
            print(f"\n✅ Success! Complete video saved to:")
            print(f"   {output_path}")
            print(f"\n📊 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            # Cleanup concat file
            concat_file.unlink()
            
            return 0
        else:
            print(f"\n❌ ffmpeg failed with exit code {result.returncode}")
            return result.returncode
            
    except FileNotFoundError:
        print("\n❌ Error: ffmpeg not found")
        print("   Please install ffmpeg: sudo apt-get install ffmpeg")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Concatenate quantum mechanics scene videos into one complete video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Concatenate high quality videos
  python scripts/concat_videos.py --quality 1080p60
  
  # Concatenate and specify output name
  python scripts/concat_videos.py --quality 720p30 --output my_quantum_video.mp4
  
  # Low quality for testing
  python scripts/concat_videos.py --quality 480p15
        """
    )
    
    parser.add_argument(
        "--quality", "-q",
        default="1080p60",
        choices=["480p15", "720p30", "1080p60", "1440p60"],
        help="Video quality to concatenate (must match rendered quality)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output filename (default: QuantumMechanicsComplete_QUALITY.mp4)"
    )
    
    args = parser.parse_args()
    
    # Find videos
    print(f"🔍 Looking for {args.quality} videos...\n")
    videos = find_videos(args.quality)
    
    if not videos:
        print("\n⚠️  No videos found. Please render them first:")
        print("   python scripts/render_optimized.py --quality h --parallel")
        return 1
    
    if len(videos) < 6:
        print(f"\n⚠️  Warning: Only found {len(videos)}/6 scenes")
        response = input("Continue anyway? [y/N]: ")
        if response.lower() != 'y':
            return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = PROJECT_ROOT / "media" / "complete"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"QuantumMechanicsComplete_{args.quality}.mp4"
    
    # Concatenate
    return concatenate_videos(videos, output_path, args.quality)


if __name__ == "__main__":
    raise SystemExit(main())
