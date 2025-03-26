#!/usr/bin/env python3
"""
Run script for the Test Coverage Enhancement Agent.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the parent directory to the Python path if needed
sys.path.insert(0, str(Path(__file__).parent))

# Check if --web flag is used
if "--web" in sys.argv:
    # Launch web interface directly with streamlit
    import subprocess
    from test_coverage_agent.ui import web
    web_script_path = Path(web.__file__).resolve()
    print(f"Starting Streamlit web interface from: {web_script_path}")
    subprocess.run(['streamlit', 'run', str(web_script_path)])
else:
    # Import the main module
    from test_coverage_agent.main import main
    main()

if __name__ == "__main__":
    pass