#!/usr/bin/env python3
"""
Backend startup script with correct Python path
This script ensures the quantum_playground module is importable
"""

import sys
from pathlib import Path

# Add src directory to Python path
workspace_root = Path(__file__).parent
src_path = workspace_root / 'src'
sys.path.insert(0, str(src_path))

# Now run the Flask app
if __name__ == '__main__':
    # Import and run the app
    from app.backend.app.api.enhanced_api import app, socketio
    
    print(f"📍 Python path includes: {src_path}")
    print(f"🚀 Starting Backend API...")
    print(f"📌 Running on http://0.0.0.0:5000")
    print(f"💡 Make sure to forward port 5000 in GitHub Codespace settings")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
