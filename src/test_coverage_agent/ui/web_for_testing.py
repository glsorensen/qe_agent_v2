import os
from typing import Dict, List, Optional, Tuple, Any

# Import necessary components from the right paths
from test_coverage_agent.repository.scanner import RepositoryScanner
from test_coverage_agent.repository.test_detector import TestDetector
from test_coverage_agent.repository.coverage_analyzer import CoverageAnalyzer
from test_coverage_agent.test_execution.coverage_reporter import CoverageReporter

class WebUI:
    """Web UI interface for the Test Coverage Enhancement Agent."""
    
    def __init__(self, repo_path: str):
        """Initialize the Web UI.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.scanner = None
        self.detector = None
        self.analyzer = None
        self.reports = []
    
    def scan_repository(self) -> Dict[str, Any]:
        """Scan the repository.
        
        Returns:
            Dictionary with scan results
        """
        self.scanner = RepositoryScanner(self.repo_path)
        files = self.scanner.scan()
        languages = self.scanner.get_common_languages()
        
        return {
            "files": files,
            "languages": languages
        }
    
    def detect_tests(self) -> Dict[str, Any]:
        """Detect tests in the repository.
        
        Returns:
            Dictionary with test detection results
        """
        if not self.scanner:
            self.scan_repository()
        
        source_files, test_files = self.scanner.get_source_and_test_files()
        self.detector = TestDetector(self.repo_path, source_files, test_files)
        
        frameworks = self.detector.detect_test_frameworks()
        analysis = self.detector.analyze_test_structure()
        test_files_by_framework = self.detector.get_test_files_by_framework()
        
        return {
            "frameworks": analysis["frameworks"],
            "test_count": analysis["test_count"],
            "test_to_source_ratio": analysis["test_to_source_ratio"],
            "files_by_framework": analysis["files_by_framework"],
            "test_files_by_framework": test_files_by_framework
        }
    
    def analyze_coverage(self, framework: str = "pytest") -> Dict[str, Any]:
        """Analyze test coverage.
        
        Args:
            framework: Test framework to use
            
        Returns:
            Dictionary with coverage analysis results
        """
        if not self.scanner:
            self.scan_repository()
        
        source_files, test_files = self.scanner.get_source_and_test_files()
        self.analyzer = CoverageAnalyzer(self.repo_path, source_files, test_files)
        
        coverage_data = self.analyzer.run_coverage_analysis(framework)
        gaps = self.analyzer.identify_coverage_gaps()
        
        return {
            "coverage_percentage": coverage_data["coverage_percentage"],
            "covered_files": coverage_data["covered_files"],
            "partially_covered_files": coverage_data["partially_covered_files"],
            "uncovered_files": coverage_data["uncovered_files"],
            "priority_files": gaps["priority_files"],
            "low_coverage_files": gaps["low_coverage_files"]
        }
    
    def generate_report(
        self, 
        overall_coverage: float,
        file_coverage: Dict[str, float],
        uncovered_files: List[str],
        generated_tests: Dict[str, str],
        validation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a coverage report.
        
        Args:
            overall_coverage: Overall coverage percentage
            file_coverage: Dictionary mapping files to coverage percentages
            uncovered_files: List of uncovered files
            generated_tests: Dictionary mapping test files to their content
            validation_results: Dictionary with test validation results
            
        Returns:
            Dictionary with report information
        """
        reporter = CoverageReporter(self.repo_path)
        
        report = reporter.generate_report(
            overall_coverage=overall_coverage,
            file_coverage=file_coverage,
            uncovered_files=uncovered_files,
            generated_tests=generated_tests,
            validation_results=validation_results
        )
        
        # Add report to history
        self.reports.append(report)
        
        # Save report
        report_path = reporter.save_report(report)
        
        return {
            "report": report.to_dict(),
            "saved_path": report_path
        }
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run the full analysis workflow.
        
        Returns:
            Dictionary with all analysis results
        """
        scan_results = self.scan_repository()
        test_results = self.detect_tests()
        coverage_results = self.analyze_coverage()
        
        # Generate a basic report
        report_data = self.generate_report(
            overall_coverage=coverage_results["coverage_percentage"],
            file_coverage={},  # Empty for simplicity
            uncovered_files=coverage_results["uncovered_files"],
            generated_tests={},  # Empty for simplicity
            validation_results={}  # Empty for simplicity
        )
        
        return {
            "scan_results": scan_results,
            "test_results": test_results,
            "coverage_results": coverage_results,
            "report": report_data
        }
    
    def start_server(self, debug: bool = False, port: int = 8501) -> None:
        """Start the web server.
        
        Args:
            debug: Whether to run in debug mode
            port: Port to run the server on
        """
        from flask import Flask, render_template, request, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return jsonify({"status": "Server is running"})
        
        @app.route('/api/scan', methods=['POST'])
        def scan():
            repo_path = request.json.get('repo_path', self.repo_path)
            self.repo_path = repo_path
            return jsonify(self.scan_repository())
        
        @app.route('/api/detect_tests', methods=['POST'])
        def detect_tests():
            return jsonify(self.detect_tests())
        
        @app.route('/api/analyze_coverage', methods=['POST'])
        def analyze_coverage():
            framework = request.json.get('framework', 'pytest')
            return jsonify(self.analyze_coverage(framework))
        
        @app.route('/api/run_analysis', methods=['POST'])
        def run_analysis():
            repo_path = request.json.get('repo_path', self.repo_path)
            self.repo_path = repo_path
            return jsonify(self.run_analysis())
        
        app.run(debug=debug, port=port, host="0.0.0.0")