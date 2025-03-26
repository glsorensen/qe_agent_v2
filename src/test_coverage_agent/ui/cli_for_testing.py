import os
from typing import Dict, List, Optional, Set, Tuple, Any
import json

# Import necessary components from the right paths
from test_coverage_agent.repository.scanner import RepositoryScanner
from test_coverage_agent.repository.test_detector import TestDetector
from test_coverage_agent.repository.coverage_analyzer import CoverageAnalyzer
from test_coverage_agent.test_execution.coverage_reporter import CoverageReporter

class CLI:
    """CLI interface for the Test Coverage Enhancement Agent."""
    
    def __init__(self, repo_path: str):
        """Initialize the CLI.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.scanner = None
        self.detector = None
        self.analyzer = None
    
    def welcome_message(self) -> None:
        """Display a welcome message."""
        print("=" * 60)
        print("Test Coverage Enhancement Agent")
        print("=" * 60)
        print(f"Repository: {self.repo_path}")
        print("-" * 60)
    
    def scan_repository(self) -> None:
        """Scan the repository."""
        print("Scanning repository...")
        self.scanner = RepositoryScanner(self.repo_path)
        files = self.scanner.scan()
        languages = self.scanner.get_common_languages()
        
        print(f"Found {sum(len(files_list) for files_list in files.values())} files")
        for lang, files_list in languages.items():
            print(f"  {lang.capitalize()}: {len(files_list)} files")
    
    def detect_tests(self) -> None:
        """Detect tests in the repository."""
        if not self.scanner:
            self.scan_repository()
        
        print("Detecting tests...")
        source_files, test_files = self.scanner.get_source_and_test_files()
        self.detector = TestDetector(self.repo_path, source_files, test_files)
        
        frameworks = self.detector.detect_test_frameworks()
        analysis = self.detector.analyze_test_structure()
        
        print(f"Found {len(test_files)} test files")
        
        if frameworks:
            print("Detected test frameworks:")
            for framework_name in frameworks:
                print(f"  {framework_name}")
        else:
            print("No test frameworks detected")
        
        print(f"Test to source ratio: {analysis['test_to_source_ratio']:.2f}")
    
    def analyze_coverage(self, framework: str = "pytest") -> None:
        """Analyze test coverage.
        
        Args:
            framework: Test framework to use
        """
        if not self.scanner:
            self.scan_repository()
        
        print(f"Analyzing coverage using {framework}...")
        source_files, test_files = self.scanner.get_source_and_test_files()
        self.analyzer = CoverageAnalyzer(self.repo_path, source_files, test_files)
        
        coverage_data = self.analyzer.run_coverage_analysis(framework)
        gaps = self.analyzer.identify_coverage_gaps()
        
        print(f"Overall coverage: {coverage_data['coverage_percentage']:.2f}%")
        print(f"Covered files: {len(coverage_data['covered_files'])}")
        print(f"Partially covered files: {len(coverage_data['partially_covered_files'])}")
        print(f"Uncovered files: {len(coverage_data['uncovered_files'])}")
        
        if gaps["priority_files"]:
            print("\nPriority files to test:")
            for i, file in enumerate(gaps["priority_files"][:5], 1):
                print(f"  {i}. {os.path.basename(file)}")
            
            if len(gaps["priority_files"]) > 5:
                print(f"  ... and {len(gaps['priority_files']) - 5} more files")
    
    def run(self) -> None:
        """Run the full CLI workflow."""
        self.welcome_message()
        self.scan_repository()
        self.detect_tests()
        self.analyze_coverage()