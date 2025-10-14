#!/bin/bash
# Live rendering status monitor with progress bar

clear

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎬 MANIM RENDERING STATUS MONITOR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Manim is running
if pgrep -f "manim" > /dev/null; then
    echo "✅ Status: RENDERING ACTIVE"
    echo ""
    
    # Get process info
    PROC_INFO=$(ps aux | grep manim | grep -v grep | head -1)
    PID=$(echo $PROC_INFO | awk '{print $2}')
    CPU=$(echo $PROC_INFO | awk '{print $3}')
    MEM=$(echo $PROC_INFO | awk '{print $6}')
    MEM_MB=$((MEM / 1024))
    TIME=$(echo $PROC_INFO | awk '{print $10}')
    
    echo "📊 Process Information:"
    echo "  PID: $PID"
    echo "  CPU Usage: ${CPU}%"
    echo "  Memory: ${MEM_MB} MB"
    echo "  Running Time: $TIME"
    echo ""
    
    # Get current animation from log
    if [ -f "render_output.log" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📈 Current Progress:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Extract current animation number
        CURRENT_ANIM=$(grep -o "Animation [0-9]*" render_output.log | tail -1 | awk '{print $2}')
        TOTAL_ANIMS=31  # Scene 01 has 31 animations
        
        if [ ! -z "$CURRENT_ANIM" ]; then
            echo "  Scene: enhanced_01_vectors_qutip.py"
            echo "  Animation: $CURRENT_ANIM / $TOTAL_ANIMS"
            echo ""
            
            # Calculate percentage
            PERCENT=$((CURRENT_ANIM * 100 / TOTAL_ANIMS))
            
            # Draw progress bar
            BAR_LENGTH=50
            FILLED=$((PERCENT * BAR_LENGTH / 100))
            EMPTY=$((BAR_LENGTH - FILLED))
            
            printf "  Progress: ["
            printf "%${FILLED}s" | tr ' ' '█'
            printf "%${EMPTY}s" | tr ' ' '░'
            printf "] ${PERCENT}%%\n"
            echo ""
        fi
        
        # Show last few log lines
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📝 Recent Log (last 5 lines):"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        tail -n 5 render_output.log | sed 's/^/  /'
        echo ""
    fi
    
    # Check for completed videos
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📁 Completed Videos:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    VIDEOS=$(find media/videos -name "*.mp4" -path "*/1080p60/*" -type f 2>/dev/null)
    
    if [ -z "$VIDEOS" ]; then
        echo "  ⏳ No videos completed yet..."
    else
        echo "$VIDEOS" | while read video; do
            SIZE=$(ls -lh "$video" | awk '{print $5}')
            echo "  ✅ $(basename $(dirname $(dirname "$video"))): $SIZE"
        done
    fi
    echo ""
    
    # Estimated time remaining
    if [ ! -z "$CURRENT_ANIM" ]; then
        REMAINING=$((TOTAL_ANIMS - CURRENT_ANIM))
        EST_MINUTES=$((REMAINING / 2))  # Rough estimate: ~2 animations per minute
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⏱️  Estimated Time Remaining: ~${EST_MINUTES} minutes"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
    
else
    echo "❌ Status: NO RENDERING ACTIVE"
    echo ""
    echo "Last completed videos:"
    find media/videos -name "*.mp4" -path "*/1080p60/*" -type f -exec ls -lh {} \; 2>/dev/null | tail -3
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Commands:"
echo "  Live updates: watch -n 2 bash scripts/render_status.sh"
echo "  View log: tail -f render_output.log"
echo "  Check process: ps aux | grep manim"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
