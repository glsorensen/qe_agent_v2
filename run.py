#!/usr/bin/env python3
"""
Run script for the Test Coverage Enhancement Agent.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
repo_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(repo_root / "src"))

# Import from the src layout
try:
    from test_coverage_agent.main import main
    import subprocess
    from test_coverage_agent.ui import web
    
    # Check if --web flag is used
    if "--web" in sys.argv:
        # Launch web interface directly with streamlit
        web_script_path = Path(web.__file__).resolve()
        print(f"Starting Streamlit web interface from: {web_script_path}")
        subprocess.run(['streamlit', 'run', str(web_script_path)])
    else:
        # Run the main function
        main()
        
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("You may need to install the package in development mode:")
    print("    pip install -e .")
    
if __name__ == "__main__":
    pass