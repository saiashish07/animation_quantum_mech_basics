#!/usr/bin/env python3
"""
Figma MCP Connector - Integrate Figma designs with Quantum Mechanics website
Converts Figma designs to HTML/CSS/JS components
"""

import os
import json
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict, List

class FigmaConnector:
    """Connect to Figma and generate web components"""
    
    def __init__(self, file_key: str, token: str, output_dir: str = "docs/components"):
        """
        Initialize Figma connector
        
        Args:
            file_key: Figma file key (from URL)
            token: Figma personal access token
            output_dir: Output directory for generated components
        """
        self.file_key = file_key
        self.token = token
        self.output_dir = Path(output_dir)
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-FIGMA-TOKEN": token,
            "Content-Type": "application/json"
        }
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def test_connection(self) -> bool:
        """Test Figma API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/files/{self.file_key}",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_file_info(self) -> Optional[Dict]:
        """Get Figma file information"""
        try:
            response = requests.get(
                f"{self.base_url}/files/{self.file_key}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get file info: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_components(self) -> List[Dict]:
        """Get all components from Figma file"""
        try:
            response = requests.get(
                f"{self.base_url}/files/{self.file_key}/components",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("components", [])
            else:
                print(f"❌ Failed to get components: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def export_image(self, node_id: str, scale: float = 1.0, format: str = "png") -> Optional[str]:
        """Export image from Figma component"""
        try:
            response = requests.get(
                f"{self.base_url}/images/{self.file_key}",
                headers=self.headers,
                params={
                    "ids": node_id,
                    "scale": scale,
                    "format": format
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("images", {}).get(node_id)
            return None
        except Exception as e:
            print(f"❌ Error exporting image: {e}")
            return None
    
    def generate_component_html(self, component: Dict) -> str:
        """Generate HTML for a component"""
        name = component.get("name", "Unknown")
        
        html = f"""<!-- Auto-generated from Figma: {name} -->
<div class="figma-component" data-component="{name}">
    <div class="component-container">
        <!-- Component content -->
    </div>
</div>
"""
        return html
    
    def generate_html_components(self):
        """Generate HTML files for all components"""
        print("▶ Fetching components from Figma...")
        
        components = self.get_components()
        if not components:
            print("❌ No components found")
            return False
        
        print(f"✓ Found {len(components)} components")
        
        for component in components:
            name = component.get("name", "unknown").replace(" ", "_").lower()
            
            # Generate HTML
            html_content = self.generate_component_html(component)
            html_file = self.output_dir / f"{name}.html"
            
            with open(html_file, 'w') as f:
                f.write(html_content)
            
            print(f"  ✓ Generated: {name}.html")
        
        return True
    
    def create_index(self):
        """Create index file listing all components"""
        components = self.get_components()
        
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Components - Quantum Mechanics UI</title>
    <link rel="stylesheet" href="../style.css">
    <style>
        .component-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .component-item { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .component-item h3 { color: #667eea; margin-bottom: 0.5rem; }
    </style>
</head>
<body>
    <h1>Figma Components</h1>
    <p>Auto-generated from Figma design file</p>
    
    <div class="component-list">
"""
        
        for component in components:
            name = component.get("name", "Unknown")
            description = component.get("description", "Component")
            
            index_html += f"""        <div class="component-item">
            <h3>{name}</h3>
            <p>{description}</p>
            <a href="{name.replace(' ', '_').lower()}.html">View Component →</a>
        </div>
"""
        
        index_html += """    </div>
</body>
</html>
"""
        
        with open(self.output_dir / "index.html", 'w') as f:
            f.write(index_html)
        
        print(f"✓ Created: components/index.html")
    
    def generate_all(self):
        """Generate all component files"""
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  FIGMA COMPONENT GENERATION                               ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Test connection
        print("▶ Testing Figma connection...")
        if not self.test_connection():
            print("❌ Cannot connect to Figma. Check token and file key.")
            return False
        print("✓ Connected to Figma")
        
        # Get file info
        print("▶ Fetching file information...")
        file_info = self.get_file_info()
        if file_info:
            print(f"✓ File: {file_info.get('name', 'Unknown')}")
        
        # Generate components
        if not self.generate_html_components():
            return False
        
        # Create index
        self.create_index()
        
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  GENERATION COMPLETE                                       ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        print(f"✓ Components generated in: {self.output_dir}")
        print(f"✓ View components: docs/components/index.html")
        print()
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate web components from Figma designs"
    )
    parser.add_argument(
        "--file-key",
        required=False,
        help="Figma file key (from URL: figma.com/design/[KEY]/...)"
    )
    parser.add_argument(
        "--token",
        required=False,
        help="Figma personal access token"
    )
    parser.add_argument(
        "--output",
        default="docs/components",
        help="Output directory for components"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test connection only"
    )
    
    args = parser.parse_args()
    
    # Get credentials from environment if not provided
    file_key = args.file_key or os.getenv("FIGMA_FILE_KEY")
    token = args.token or os.getenv("FIGMA_TOKEN")
    
    if not file_key or not token:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  FIGMA CONNECTOR - SETUP GUIDE                             ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        print("To use Figma integration:")
        print()
        print("1. Create Figma File:")
        print("   - Go to figma.com → Create new file")
        print("   - Design your UI components")
        print()
        print("2. Get File Key:")
        print("   - In Figma, click Share → Get link")
        print("   - Extract key from URL: figma.com/design/[KEY]/...")
        print()
        print("3. Create Personal Token:")
        print("   - Settings → Developer → Create personal access token")
        print()
        print("4. Use this script:")
        print()
        print("   Option A: Command line arguments")
        print("   python3 scripts/figma_connector.py \\")
        print("     --file-key YOUR_FILE_KEY \\")
        print("     --token YOUR_TOKEN")
        print()
        print("   Option B: Environment variables")
        print("   export FIGMA_FILE_KEY='your_key'")
        print("   export FIGMA_TOKEN='your_token'")
        print("   python3 scripts/figma_connector.py")
        print()
        print("5. Generated components will be in: docs/components/")
        print()
        return 1
    
    # Create connector
    connector = FigmaConnector(
        file_key=file_key,
        token=token,
        output_dir=args.output
    )
    
    # Test connection only
    if args.test:
        print("Testing Figma connection...")
        if connector.test_connection():
            print("✅ Connection successful!")
            file_info = connector.get_file_info()
            if file_info:
                print(f"File: {file_info.get('name', 'Unknown')}")
            return 0
        else:
            print("❌ Connection failed")
            return 1
    
    # Generate components
    success = connector.generate_all()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
