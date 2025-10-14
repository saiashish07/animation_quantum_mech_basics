#!/bin/bash
# Check rendering progress and output files

echo "============================================"
echo "1440p60 Rendering Status"
echo "============================================"
echo ""

# Check if renders exist
echo "Checking for completed renders..."
echo ""

if [ -f "media/videos/enhanced_01_vectors_qutip/2160p60/QuantumVectorBlochScene.mp4" ]; then
    size=$(ls -lh media/videos/enhanced_01_vectors_qutip/2160p60/QuantumVectorBlochScene.mp4 | awk '{print $5}')
    echo "✓ Scene 01 (Bloch Sphere): $size"
else
    echo "⏳ Scene 01 (Bloch Sphere): Rendering..."
fi

if [ -f "media/videos/enhanced_02_inner_product_qutip/2160p60/QuantumInnerProductScene.mp4" ]; then
    size=$(ls -lh media/videos/enhanced_02_inner_product_qutip/2160p60/QuantumInnerProductScene.mp4 | awk '{print $5}')
    echo "✓ Scene 02 (Inner Products): $size"
else
    echo "⏳ Scene 02 (Inner Products): Not started"
fi

if [ -f "media/videos/enhanced_04_superposition_qmsolve/2160p60/QuantumSuperpositionQMsolveScene.mp4" ]; then
    size=$(ls -lh media/videos/enhanced_04_superposition_qmsolve/2160p60/QuantumSuperpositionQMsolveScene.mp4 | awk '{print $5}')
    echo "✓ Scene 04 (Superposition): $size"
else
    echo "⏳ Scene 04 (Superposition): Not started"
fi

echo ""
echo "Total rendered so far:"
du -sh media/videos/enhanced_*/2160p60/ 2>/dev/null | tail -1

echo ""
echo "To check active renders: ps aux | grep manim"
