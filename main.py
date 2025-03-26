import os
import sys
import argparse
from typing import Dict, List, Optional, Set, Tuple, Any

# Import necessary components
from repository import RepositoryScanner, TestDetector, CoverageAnalyzer
from test_generation import CodeUnderstandingModule, TestTemplateManager, AIPoweredTestWriter
from test_execution import TestRunner, TestValidator, CoverageReporter
from ui.cli import cli


def main():
    """Main entry point for the Test Coverage Enhancement Agent."""
    parser = argparse.ArgumentParser(
        description="Test Coverage Enhancement Agent - Analyze code repositories and generate tests"
    )
    
    parser.add_argument(
        "repo_path", 
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
        from ui.web import main as web_main
        web_main()
        return
    
    # Use CLI via click
    cli()


if __name__ == "__main__":
    main()