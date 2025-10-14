#!/bin/bash
# Render all enhanced quantum mechanics scenes at 1080p60 (production quality)

echo "============================================"
echo "Starting 1080p60 Rendering"
echo "============================================"
echo ""
echo "Resolution: 1920×1080 @ 60fps"
echo "Quality: High (production ready)"
echo "Estimated time: ~40-50 minutes total"
echo ""

# Array of scene files
SCENES=(
    "src/quantum_animation/scenes/enhanced_01_vectors_qutip.py"
    "src/quantum_animation/scenes/enhanced_02_inner_product_qutip.py"
    "src/quantum_animation/scenes/enhanced_04_superposition_qmsolve.py"
)

# Scene names for display
SCENE_NAMES=(
    "Scene 01: Quantum Vectors & Bloch Sphere (QuTiP)"
    "Scene 02: Inner Products & Fidelity (QuTiP)"
    "Scene 04: Wave Packet Superposition (QMsolve)"
)

TOTAL_START=$(date +%s)

for i in "${!SCENES[@]}"; do
    echo "============================================"
    echo "Rendering ${SCENE_NAMES[$i]}"
    echo "============================================"
    
    START=$(date +%s)
    
    # Render at 1080p60 quality (-qh flag)
    manim -qh "${SCENES[$i]}"
    
    END=$(date +%s)
    DURATION=$((END - START))
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    
    echo ""
    echo "✅ Completed in ${MINUTES}m ${SECONDS}s"
    echo ""
done

TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))
TOTAL_MINUTES=$((TOTAL_DURATION / 60))
TOTAL_SECONDS=$((TOTAL_DURATION % 60))

echo "============================================"
echo "All Renders Complete!"
echo "============================================"
echo "Total time: ${TOTAL_MINUTES}m ${TOTAL_SECONDS}s"
echo ""
echo "Output files:"
find media/videos -name "*.mp4" -type f -exec ls -lh {} \;
echo ""
echo "Total size:"
du -sh media/videos/
