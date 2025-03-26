import os
import sys
import argparse
from typing import Dict, List, Optional, Set, Tuple, Any

# Import necessary components
from test_coverage_agent.repository import RepositoryScanner, TestDetector, CoverageAnalyzer
from test_coverage_agent.test_generation import CodeUnderstandingModule, TestTemplateManager, AIPoweredTestWriter
from test_coverage_agent.test_execution import TestRunner, TestValidator, CoverageReporter
from test_coverage_agent.ui.cli import cli


def main():
    """Main entry point for the Test Coverage Enhancement Agent."""
    parser = argparse.ArgumentParser(
        description="Test Coverage Enhancement Agent - Analyze code repositories and generate tests"
    )
    
    parser.add_argument(
        "repo_path", 
        nargs='?',  # Make repo_path optional
        help="Path to the repository to analyze"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        help="Anthropic API key for AI test generation"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output directory for generated tests"
    )
    
    parser.add_argument(
        "--analyze-only", "-a",
        action="store_true",
        help="Only analyze the repository, don't generate tests"
    )
    
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Start the web interface"
    )
    
    args = parser.parse_args()
    
    # Check if web interface is requested
    if args.web:
        import subprocess
        import os
        import importlib.util
        from pathlib import Path
        
        # Get the path to the web.py module
        from test_coverage_agent.ui import web
        web_script_path = Path(web.__file__).resolve()
        print(f"Starting Streamlit web interface from: {web_script_path}")
        subprocess.run(['streamlit', 'run', str(web_script_path)])
        return
    
    # Check if a repository path was provided
    if args.repo_path:
        # Use CLI via click
        from test_coverage_agent.ui.cli import cli
        cli(['analyze', args.repo_path])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()