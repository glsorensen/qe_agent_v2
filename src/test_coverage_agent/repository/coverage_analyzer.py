import os
import subprocess
import json
from typing import Dict, List, Optional, Set, Tuple, Any


class CoverageAnalyzer:
    """Analyzer for test coverage in a repository."""
    
    def __init__(self, repo_path: str, source_files: List[str], test_files: List[str]):
        """Initialize the coverage analyzer.
        
        Args:
            repo_path: Path to the repository
            source_files: List of source code file paths
            test_files: List of test file paths
        """
        self.repo_path = repo_path
        self.source_files = source_files
        self.test_files = test_files
        self.coverage_data: Dict[str, Any] = {}
    
    def run_coverage_analysis(self, framework: str = 'pytest') -> Dict[str, Any]:
        """Run coverage analysis using the specified test framework.
        
        Args:
            framework: Test framework to use (default: pytest)
            
        Returns:
            Dictionary with coverage analysis results
        """
        # Create a temporary directory for coverage reports
        os.makedirs(os.path.join(self.repo_path, '.coverage_reports'), exist_ok=True)
        
        try:
            # Default to pytest with coverage
            if framework == 'pytest':
                # Use pytest-cov to generate coverage data
                result = subprocess.run(
                    [
                        'python', '-m', 'pytest', 
                        '--cov=.', 
                        '--cov-report=json:.coverage_reports/coverage.json',
                        '--cov-report=xml:.coverage_reports/coverage.xml'
                    ],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                # Parse the JSON report
                coverage_file = os.path.join(self.repo_path, '.coverage_reports', 'coverage.json')
                if os.path.exists(coverage_file):
                    with open(coverage_file, 'r') as f:
                        self.coverage_data = json.load(f)
            
            # Other frameworks can be added here
            elif framework == 'jest':
                # Run Jest with coverage
                result = subprocess.run(
                    ['npx', 'jest', '--coverage'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                # Parse the JSON report if available
                coverage_file = os.path.join(self.repo_path, 'coverage', 'coverage-final.json')
                if os.path.exists(coverage_file):
                    with open(coverage_file, 'r') as f:
                        self.coverage_data = json.load(f)
            
            return self.parse_coverage_data()
            
        except Exception as e:
            return {
                'error': str(e),
                'coverage_percentage': 0.0,
                'covered_files': [],
                'uncovered_files': self.source_files,
                'partially_covered_files': []
            }
    
    def parse_coverage_data(self) -> Dict[str, Any]:
        """Parse the collected coverage data.
        
        Returns:
            Dictionary with parsed coverage information
        """
        if not self.coverage_data:
            return {
                'coverage_percentage': 0.0,
                'covered_files': [],
                'uncovered_files': self.source_files,
                'partially_covered_files': []
            }
        
        # Process coverage data from pytest-cov (JSON format)
        covered_files: List[str] = []
        uncovered_files: List[str] = []
        partially_covered_files: List[Dict[str, Any]] = []
        
        total_statements = 0
        covered_statements = 0
        
        # Extract file coverage information
        for file_path, file_data in self.coverage_data.get('files', {}).items():
            # Skip test files
            abs_path = os.path.join(self.repo_path, file_path)
            if abs_path in self.test_files:
                continue
                
            # Get statement and line coverage
            statements = file_data.get('summary', {}).get('num_statements', 0)
            missing = file_data.get('summary', {}).get('missing_lines', 0)
            covered = statements - missing
            
            total_statements += statements
            covered_statements += covered
            
            # Categorize files based on coverage
            if statements == 0:
                # Skip empty files
                continue
            elif missing == 0:
                covered_files.append(abs_path)
            elif covered == 0:
                uncovered_files.append(abs_path)
            else:
                # Partially covered
                partially_covered_files.append({
                    'file': abs_path,
                    'total_lines': statements,
                    'covered_lines': covered,
                    'coverage_percentage': round((covered / statements) * 100, 2),
                    'uncovered_line_numbers': file_data.get('missing_lines', [])
                })
        
        # Calculate overall coverage percentage
        coverage_percentage = 0.0
        if total_statements > 0:
            coverage_percentage = round((covered_statements / total_statements) * 100, 2)
        
        # Find files that are not in the coverage report
        covered_paths = set(covered_files + uncovered_files + [p['file'] for p in partially_covered_files])
        missing_files = [f for f in self.source_files if f not in covered_paths]
        
        return {
            'coverage_percentage': coverage_percentage,
            'covered_files': covered_files,
            'uncovered_files': uncovered_files + missing_files,
            'partially_covered_files': partially_covered_files,
            'total_statements': total_statements,
            'covered_statements': covered_statements
        }
    
    def identify_coverage_gaps(self) -> Dict[str, Any]:
        """Identify and prioritize coverage gaps in the codebase.
        
        Returns:
            Dictionary with information about coverage gaps including:
            - priority_files: Files that should be tested first
            - uncovered_files: Files with no coverage
            - low_coverage_files: Files with low coverage
        """
        if not self.coverage_data:
            self.run_coverage_analysis()
            
        # Get basic coverage data
        coverage_info = self.parse_coverage_data()
        
        # Priority calculation factors:
        # 1. Files with no coverage
        # 2. Files with low coverage percentage
        # 3. Files with many uncovered lines
        
        # Sort partially covered files by coverage percentage (ascending)
        low_coverage_threshold = 50.0  # Files below 50% coverage
        low_coverage_files = sorted(
            [p for p in coverage_info['partially_covered_files'] if p['coverage_percentage'] < low_coverage_threshold],
            key=lambda x: x['coverage_percentage']
        )
        
        # Uncovered files are already prioritized
        uncovered_files = coverage_info['uncovered_files']
        
        # Combine for overall priority list
        # First uncovered files, then low coverage files
        priority_files = uncovered_files + [p['file'] for p in low_coverage_files]
        
        return {
            'priority_files': priority_files,
            'uncovered_files': uncovered_files,
            'low_coverage_files': low_coverage_files
        }