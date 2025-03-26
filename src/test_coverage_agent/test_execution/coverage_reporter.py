import os
import json
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime


class CoverageReport:
    """Class representing a test coverage report."""
    
    def __init__(
        self,
        repo_path: str,
        overall_coverage: float,
        file_coverage: Dict[str, float],
        uncovered_files: List[str],
        generated_tests: Dict[str, str],
        validation_results: Dict[str, Any]
    ):
        """Initialize a coverage report.
        
        Args:
            repo_path: Path to the repository
            overall_coverage: Overall coverage percentage
            file_coverage: Dictionary mapping files to coverage percentages
            uncovered_files: List of files with no coverage
            generated_tests: Dictionary mapping test files to their content
            validation_results: Dictionary with test validation results
        """
        self.repo_path = repo_path
        self.overall_coverage = overall_coverage
        self.file_coverage = file_coverage
        self.uncovered_files = uncovered_files
        self.generated_tests = generated_tests
        self.validation_results = validation_results
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the report to a dictionary.
        
        Returns:
            Dictionary representation of the report
        """
        return {
            'repo_path': self.repo_path,
            'overall_coverage': self.overall_coverage,
            'file_coverage': self.file_coverage,
            'uncovered_files': self.uncovered_files,
            'generated_tests_count': len(self.generated_tests),
            'validation_success_rate': self._calculate_success_rate(),
            'timestamp': self.timestamp
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate the success rate of test validation.
        
        Returns:
            Success rate as a percentage
        """
        if not self.validation_results:
            return 0.0
            
        success_count = sum(
            1 for result in self.validation_results.values() 
            if result.get('is_valid', False)
        )
        
        return (success_count / len(self.validation_results)) * 100


class CoverageReporter:
    """Reporter for generating coverage reports."""
    
    def __init__(self, repo_path: str):
        """Initialize the coverage reporter.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.reports_dir = os.path.join(repo_path, '.coverage_reports')
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_report(
        self,
        overall_coverage: float,
        file_coverage: Dict[str, float],
        uncovered_files: List[str],
        generated_tests: Dict[str, str],
        validation_results: Dict[str, Any]
    ) -> CoverageReport:
        """Generate a coverage report.
        
        Args:
            overall_coverage: Overall coverage percentage
            file_coverage: Dictionary mapping files to coverage percentages
            uncovered_files: List of files with no coverage
            generated_tests: Dictionary mapping test files to their content
            validation_results: Dictionary with test validation results
            
        Returns:
            CoverageReport object
        """
        return CoverageReport(
            repo_path=self.repo_path,
            overall_coverage=overall_coverage,
            file_coverage=file_coverage,
            uncovered_files=uncovered_files,
            generated_tests=generated_tests,
            validation_results=validation_results
        )
    
    def save_report(self, report: CoverageReport, format: str = 'json') -> str:
        """Save a coverage report to a file.
        
        Args:
            report: CoverageReport to save
            format: Report format ('json' or 'txt')
            
        Returns:
            Path to the saved report
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            # Save as JSON
            report_path = os.path.join(self.reports_dir, f'coverage_report_{timestamp}.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, indent=2)
        else:
            # Save as text
            report_path = os.path.join(self.reports_dir, f'coverage_report_{timestamp}.txt')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Coverage Report - {timestamp}\n")
                f.write(f"Repository: {report.repo_path}\n")
                f.write(f"Overall Coverage: {report.overall_coverage:.2f}%\n\n")
                
                f.write("File Coverage:\n")
                for file_path, coverage in sorted(report.file_coverage.items(), key=lambda x: x[1]):
                    rel_path = os.path.relpath(file_path, report.repo_path)
                    f.write(f"  {rel_path}: {coverage:.2f}%\n")
                
                f.write("\nUncovered Files:\n")
                for file_path in report.uncovered_files:
                    rel_path = os.path.relpath(file_path, report.repo_path)
                    f.write(f"  {rel_path}\n")
                
                f.write(f"\nGenerated Tests: {len(report.generated_tests)}\n")
                success_rate = report._calculate_success_rate()
                f.write(f"Validation Success Rate: {success_rate:.2f}%\n")
        
        return report_path
    
    def load_report(self, report_path: str) -> Optional[CoverageReport]:
        """Load a coverage report from a file.
        
        Args:
            report_path: Path to the report file
            
        Returns:
            CoverageReport object or None if loading fails
        """
        try:
            if report_path.endswith('.json'):
                with open(report_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Basic validation of report data
                required_fields = ['repo_path', 'overall_coverage', 'file_coverage', 'uncovered_files']
                if not all(field in data for field in required_fields):
                    return None
                    
                # Create a report object with empty generated tests and validation results
                # since these are not saved in the JSON
                return CoverageReport(
                    repo_path=data['repo_path'],
                    overall_coverage=data['overall_coverage'],
                    file_coverage=data['file_coverage'],
                    uncovered_files=data['uncovered_files'],
                    generated_tests={},
                    validation_results={}
                )
            
            return None
            
        except Exception as e:
            print(f"Error loading report: {str(e)}")
            return None
    
    def compare_reports(self, old_report: CoverageReport, new_report: CoverageReport) -> Dict[str, Any]:
        """Compare two coverage reports to show changes.
        
        Args:
            old_report: Previous coverage report
            new_report: New coverage report
            
        Returns:
            Dictionary with comparison results
        """
        coverage_change = new_report.overall_coverage - old_report.overall_coverage
        
        # Files with coverage changes
        file_changes = {}
        for file_path, new_coverage in new_report.file_coverage.items():
            if file_path in old_report.file_coverage:
                old_coverage = old_report.file_coverage[file_path]
                change = new_coverage - old_coverage
                if abs(change) > 0.01:  # Only report significant changes
                    file_changes[file_path] = change
        
        # Newly covered files
        newly_covered = [
            file_path for file_path in old_report.uncovered_files
            if file_path not in new_report.uncovered_files
        ]
        
        # Newly uncovered files
        newly_uncovered = [
            file_path for file_path in new_report.uncovered_files
            if file_path not in old_report.uncovered_files
        ]
        
        return {
            'overall_change': coverage_change,
            'file_changes': file_changes,
            'newly_covered': newly_covered,
            'newly_uncovered': newly_uncovered
        }