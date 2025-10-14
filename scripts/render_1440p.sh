#!/bin/bash
# Render all QMsolve/QuTiP enhanced scenes at 1440p60 (premium quality)

echo "============================================"
echo "Rendering Enhanced Scenes at 1440p60"
echo "============================================"
echo ""
echo "⚠️  WARNING: This will take 60-90 minutes!"
echo "   - Scene 01 (3D Bloch): ~25-30 min"
echo "   - Scene 02 (Inner Products): ~20-25 min"
echo "   - Scene 04 (Superposition): ~20-25 min"
echo ""
echo "Starting renders..."
echo ""

# Track start time
START_TIME=$(date +%s)

# Scene 01 - Bloch Sphere (3D - slowest)
echo "============================================"
echo "Scene 01: Bloch Sphere (3D) - ~25-30 min"
echo "============================================"
SCENE1_START=$(date +%s)
manim -qk src/quantum_animation/scenes/enhanced_01_vectors_qutip.py QuantumVectorBlochScene
SCENE1_END=$(date +%s)
SCENE1_TIME=$((SCENE1_END - SCENE1_START))
echo "✓ Scene 01 completed in $((SCENE1_TIME / 60)) min $((SCENE1_TIME % 60)) sec"
echo ""

# Scene 02 - Inner Products
echo "============================================"
echo "Scene 02: Inner Products - ~20-25 min"
echo "============================================"
SCENE2_START=$(date +%s)
manim -qk src/quantum_animation/scenes/enhanced_02_inner_product_qutip.py QuantumInnerProductScene
SCENE2_END=$(date +%s)
SCENE2_TIME=$((SCENE2_END - SCENE2_START))
echo "✓ Scene 02 completed in $((SCENE2_TIME / 60)) min $((SCENE2_TIME % 60)) sec"
echo ""

# Scene 04 - Superposition
echo "============================================"
echo "Scene 04: Superposition - ~20-25 min"
echo "============================================"
SCENE4_START=$(date +%s)
manim -qk src/quantum_animation/scenes/enhanced_04_superposition_qmsolve.py QuantumSuperpositionQMsolveScene
SCENE4_END=$(date +%s)
SCENE4_TIME=$((SCENE4_END - SCENE4_START))
echo "✓ Scene 04 completed in $((SCENE4_TIME / 60)) min $((SCENE4_TIME % 60)) sec"
echo ""

# Calculate total time
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

# Show results
echo "============================================"
echo "✅ All Scenes Rendered at 1440p60!"
echo "============================================"
echo ""
echo "Render times:"
echo "  Scene 01: $((SCENE1_TIME / 60)) min $((SCENE1_TIME % 60)) sec"
echo "  Scene 02: $((SCENE2_TIME / 60)) min $((SCENE2_TIME % 60)) sec"
echo "  Scene 04: $((SCENE4_TIME / 60)) min $((SCENE4_TIME % 60)) sec"
echo "  Total: $((TOTAL_TIME / 60)) min $((TOTAL_TIME % 60)) sec"
echo ""
echo "Output files:"
ls -lh media/videos/enhanced_01_vectors_qutip/2160p60/QuantumVectorBlochScene.mp4 2>/dev/null
ls -lh media/videos/enhanced_02_inner_product_qutip/2160p60/QuantumInnerProductScene.mp4 2>/dev/null
ls -lh media/videos/enhanced_04_superposition_qmsolve/2160p60/QuantumSuperpositionQMsolveScene.mp4 2>/dev/null
echo ""
echo "Total size:"
du -sh media/videos/enhanced_*/2160p60/ 2>/dev/null | awk '{sum+=$1} END {print sum " MB total"}'
echo ""
echo "🎬 Ready for production use!"
