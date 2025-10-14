"""Simplified master scene - renders all individual scenes then concatenates."""

# This file serves as documentation for combining scenes.
# To create a single unified video, use the render_optimized.py script
# with the "complete" option:
#
# python scripts/render_optimized.py complete --quality h
#
# Or render all scenes and concatenate manually:
#
# python scripts/render_optimized.py --quality h --parallel
# 
# Then use ffmpeg to concatenate:
# ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
#
# Where filelist.txt contains:
# file 'media/videos/01_vectors_hilbert/1080p60/VectorBasicsScene.mp4'
# file 'media/videos/02_inner_product/1080p60/InnerProductScene.mp4'
# file 'media/videos/03_orthogonality/1080p60/OrthogonalityScene.mp4'
# file 'media/videos/04_superposition/1080p60/SuperpositionScene.mp4'
# file 'media/videos/05_operators/1080p60/OperatorMeasurementScene.mp4'
# file 'media/videos/06_evolution/1080p60/WavefunctionEvolutionScene.mp4'

# For a true single-render complete scene, all logic would need to be duplicated here.
# The individual numbered scenes are designed to be rendered separately and combined.
