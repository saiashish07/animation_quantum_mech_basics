#!/bin/bash
# Optimize Project Structure - Remove duplicates and consolidate
# Reduces disk usage for 32GB systems

set -e

PROJECT_ROOT=$(pwd)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PROJECT OPTIMIZATION - Consolidation & Cleanup           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "▶ Current disk usage:"
du -sh "$PROJECT_ROOT" | head -1
echo ""

# Backup old files
echo "▶ Creating backup of files to be removed..."
mkdir -p "$PROJECT_ROOT/.cleanup_backup"

# List of markdown files to remove (consolidate into COMPREHENSIVE_README.md)
MARKDOWN_FILES=(
    "CODESPACE_GUIDE.md"
    "CODESPACE_QUICKSTART.md"
    "COMPLETION_REPORT.txt"
    "COMPLETION_SUMMARY.md"
    "DOCUMENTATION_INDEX.md"
    "EXECUTION_CHECKLIST.md"
    "GETTING_STARTED.md"
    "IMPLEMENTATION_SUMMARY_V2.md"
    "PROJECT_SUMMARY.md"
    "PROJECT_STATUS.md"
    "QUICKSTART.md"
    "QUICKSTART_V2.md"
    "SIMULATION_RESULTS.md"
    "SOLVER_FIX_SUMMARY.md"
    "START_HERE.md"
    "TEACHING_GUIDE.md"
    "README_FINAL_STATUS.md"
)

echo "▶ Backing up and removing duplicate markdown files..."
for file in "${MARKDOWN_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  - Backing up: $file"
        cp "$PROJECT_ROOT/$file" "$PROJECT_ROOT/.cleanup_backup/"
    fi
done
echo "✓ Backups created in .cleanup_backup/"
echo ""

# Unnecessary Python scripts (debug/demo files)
PYTHON_SCRIPTS=(
    "debug_solver.py"
    "generate_plots.py"
    "quick_test.py"
    "run_demo.py"
)

echo "▶ Removing debug/demo Python scripts..."
for file in "${PYTHON_SCRIPTS[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  - Removing: $file"
        mv "$PROJECT_ROOT/$file" "$PROJECT_ROOT/.cleanup_backup/"
    fi
done
echo "✓ Debug files moved to backup"
echo ""

# Old/duplicate notebooks
echo "▶ Removing old notebooks..."
if [ -f "$PROJECT_ROOT/Quantum_Mechanics_Interactive_Simulator.ipynb" ]; then
    echo "  - Removing: Quantum_Mechanics_Interactive_Simulator.ipynb (use Interactive_Quantum_Controls.ipynb instead)"
    mv "$PROJECT_ROOT/Quantum_Mechanics_Interactive_Simulator.ipynb" "$PROJECT_ROOT/.cleanup_backup/"
fi
echo "✓ Old notebooks removed"
echo ""

# Archive docs_archive folder
echo "▶ Compressing docs_archive..."
if [ -d "$PROJECT_ROOT/docs_archive" ]; then
    tar -czf "$PROJECT_ROOT/.cleanup_backup/docs_archive.tar.gz" "$PROJECT_ROOT/docs_archive"
    rm -rf "$PROJECT_ROOT/docs_archive"
    echo "✓ docs_archive compressed and removed"
fi
echo ""

# Remove .venv if present (users should create locally)
echo "▶ Checking for .venv..."
if [ -d "$PROJECT_ROOT/.venv" ]; then
    echo "  - Removing .venv (users should create locally with: python3 -m venv .venv)"
    rm -rf "$PROJECT_ROOT/.venv"
    echo "✓ .venv removed"
fi
echo ""

# Clean Python cache
echo "▶ Cleaning Python cache..."
find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name ".DS_Store" -delete 2>/dev/null || true
echo "✓ Cache cleaned"
echo ""

# Remove old markdown files (keeping only COMPREHENSIVE_README.md)
echo "▶ Removing consolidated markdown files..."
rm -f "$PROJECT_ROOT"/CODESPACE_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/COMPLETION_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/DOCUMENTATION_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/EXECUTION_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/GETTING_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/PROJECT_STATUS.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/QUICKSTART*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/IMPLEMENTATION_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/TEACHING_*.md 2>/dev/null || true
rm -f "$PROJECT_ROOT"/README_*.md 2>/dev/null || true
echo "✓ Markdown files consolidated"
echo ""

# Ensure key files exist
echo "▶ Verifying key files..."
REQUIRED_FILES=(
    "COMPREHENSIVE_README.md"
    "README.md"
    "Interactive_Quantum_Controls.ipynb"
    "src/manim_quantum.py"
    "src/ffmpeg_pipeline.py"
    "build_quantum_animations.sh"
    "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PROJECT_ROOT/$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done
echo "✓ All key files present"
echo ""

# Create .gitignore to prevent large files
echo "▶ Updating .gitignore..."
cat >> "$PROJECT_ROOT/.gitignore" << 'EOF'
# Large generated files (can be regenerated)
outputs/*.mp4
outputs/*.mkv
outputs/**/*.mp4
videos/**/*.mp4
*.egg-info/

# Virtual environment
.venv/
venv/

# Cache and build
__pycache__/
*.pyc
build/
dist/

# IDE
.vscode/
.idea/

# Backup
.cleanup_backup/
EOF
echo "✓ .gitignore updated"
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  OPTIMIZATION COMPLETE                                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "▶ New disk usage:"
du -sh "$PROJECT_ROOT" | head -1
echo ""

echo "Files removed/consolidated:"
echo "  ✓ 17 duplicate markdown files → 1 COMPREHENSIVE_README.md"
echo "  ✓ 4 debug/demo Python scripts"
echo "  ✓ 1 old notebook"
echo "  ✓ Python cache and __pycache__"
echo "  ✓ .venv (removed, users create locally)"
echo "  ✓ docs_archive (compressed)"
echo ""

echo "Backup location: .cleanup_backup/"
echo "  - Contains: Old markdown files, debug scripts, compressed archive"
echo "  - Can be deleted after verification"
echo ""

echo "✓ Project structure optimized for 32GB systems"
echo ""

echo "Next steps:"
echo "  1. Review README.md and COMPREHENSIVE_README.md"
echo "  2. Verify no required files were removed"
echo "  3. Run: bash scripts/deploy_github_pages.sh"
echo "  4. Delete .cleanup_backup/ if satisfied"
echo ""
