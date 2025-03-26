#!/usr/bin/env python3
"""
Run script for the Test Coverage Enhancement Agent.
"""

import sys
import os
from pathlib import Path

# Add the repository root to the Python path
repo_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(repo_root))

# Import the main module
from main import main

if __name__ == "__main__":
    main()