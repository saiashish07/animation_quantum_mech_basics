#!/bin/bash
# Test all QMsolve/QuTiP enhanced scenes

echo "============================================"
echo "Testing QMsolve & QuTiP Enhanced Scenes"
echo "============================================"
echo ""

# Check if qutip and qmsolve are available
echo "Checking dependencies..."
python3 -c "import qutip; print('✓ QuTiP version:', qutip.__version__)" 2>/dev/null || echo "⚠ QuTiP not installed (scenes will use fallback values)"
python3 -c "import qmsolve; print('✓ QMsolve installed')" 2>/dev/null || echo "⚠ QMsolve not installed (scenes will use fallback values)"
echo ""

# Test Scene 01 - Bloch Sphere
echo "============================================"
echo "Testing Scene 01: Bloch Sphere (QuTiP)"
echo "============================================"
if manim -ql src/quantum_animation/scenes/enhanced_01_vectors_qutip.py QuantumVectorBlochScene; then
    size=$(ls -lh media/videos/enhanced_01_vectors_qutip/480p15/QuantumVectorBlochScene.mp4 2>/dev/null | awk '{print $5}')
    echo "✓ Scene 01 rendered successfully: $size"
else
    echo "✗ Scene 01 failed to render"
    exit 1
fi
echo ""

# Test Scene 02 - Inner Products
echo "============================================"
echo "Testing Scene 02: Inner Products (QuTiP)"
echo "============================================"
if manim -ql src/quantum_animation/scenes/enhanced_02_inner_product_qutip.py QuantumInnerProductScene; then
    size=$(ls -lh media/videos/enhanced_02_inner_product_qutip/480p15/QuantumInnerProductScene.mp4 2>/dev/null | awk '{print $5}')
    echo "✓ Scene 02 rendered successfully: $size"
else
    echo "✗ Scene 02 failed to render"
    exit 1
fi
echo ""

# Test Scene 04 - Superposition
echo "============================================"
echo "Testing Scene 04: Superposition (QMsolve)"
echo "============================================"
if manim -ql src/quantum_animation/scenes/enhanced_04_superposition_qmsolve.py QuantumSuperpositionQMsolveScene; then
    size=$(ls -lh media/videos/enhanced_04_superposition_qmsolve/480p15/QuantumSuperpositionQMsolveScene.mp4 2>/dev/null | awk '{print $5}')
    echo "✓ Scene 04 rendered successfully: $size"
else
    echo "✗ Scene 04 failed to render"
    exit 1
fi
echo ""

# Summary
echo "============================================"
echo "✅ All Enhanced Scenes Tested Successfully!"
echo "============================================"
echo ""
echo "Output files:"
ls -lh media/videos/enhanced_*/480p15/*.mp4 2>/dev/null
echo ""
echo "Total size:"
du -sh media/videos/enhanced_*/480p15/ 2>/dev/null
echo ""
echo "Next steps:"
echo "1. Render at high quality: manim -qh <file.py> <SceneName>"
echo "2. Install QuTiP/QMsolve: pip install qutip qmsolve"
echo "3. Create remaining scenes (03, 05, 06)"
