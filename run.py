#!/usr/bin/env python3
"""
Run script for the Test Coverage Enhancement Agent.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the repository root to the Python path
repo_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(repo_root))

# Check if --web flag is used
if "--web" in sys.argv:
    # Launch web interface directly with streamlit
    import subprocess
    web_script_path = os.path.join(repo_root, 'ui', 'web.py')
    print(f"Starting Streamlit web interface from: {web_script_path}")
    subprocess.run(['streamlit', 'run', web_script_path])
else:
    # Import the main module
    from main import main
    main()

if __name__ == "__main__":
    pass