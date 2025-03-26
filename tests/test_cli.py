import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock

from ui.cli_for_testing import CLI


class TestCLI:
    """Tests for the CLI class."""
    
    @pytest.fixture
    def sample_repo(self):
        """Create a temporary sample repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_init(self, sample_repo):
        """Test initializing the CLI."""
        cli = CLI(sample_repo)
        
        assert cli.repo_path == sample_repo
        assert cli.scanner is None
        assert cli.detector is None
        assert cli.analyzer is None
    
    @patch("builtins.print")
    def test_welcome_message(self, mock_print, sample_repo):
        """Test displaying the welcome message."""
        cli = CLI(sample_repo)
        cli.welcome_message()
        
        # Check that print was called
        mock_print.assert_called()
        # Verify parts of the welcome message
        assert any("Test Coverage Enhancement Agent" in call[0][0] for call in mock_print.call_args_list)
    
    @patch("builtins.print")
    @patch("repository.scanner.RepositoryScanner")
    def test_scan_repository(self, mock_scanner, mock_print, sample_repo):
        """Test scanning the repository."""
        # Mock the scanner
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = {"py": ["file1.py", "file2.py"]}
        mock_scanner_instance.get_common_languages.return_value = {"python": ["file1.py", "file2.py"]}
        mock_scanner.return_value = mock_scanner_instance
        
        cli = CLI(sample_repo)
        cli.scan_repository()
        
        # Check that scanner was initialized and used
        mock_scanner.assert_called_once_with(sample_repo)
        mock_scanner_instance.scan.assert_called_once()
        mock_scanner_instance.get_common_languages.assert_called_once()
        
        # Check that CLI has the scanner instance
        assert cli.scanner is not None
        
        # Check that prints were called
        mock_print.assert_called()
    
    @patch("builtins.print")
    @patch("repository.scanner.RepositoryScanner")
    @patch("repository.test_detector.TestDetector")
    def test_detect_tests(self, mock_detector, mock_scanner, mock_print, sample_repo):
        """Test detecting tests in the repository."""
        # Mock the scanner
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.get_source_and_test_files.return_value = (["src/file1.py"], ["tests/test_file1.py"])
        
        # Mock the detector
        mock_detector_instance = MagicMock()
        mock_detector_instance.detect_test_frameworks.return_value = {"pytest": MagicMock()}
        mock_detector_instance.analyze_test_structure.return_value = {
            "test_count": 1,
            "frameworks": ["pytest"],
            "test_to_source_ratio": 1.0,
            "files_by_framework": {"pytest": 1}
        }
        
        mock_scanner.return_value = mock_scanner_instance
        mock_detector.return_value = mock_detector_instance
        
        cli = CLI(sample_repo)
        cli.scanner = mock_scanner_instance
        cli.detect_tests()
        
        # Check that detector was initialized and used
        mock_detector.assert_called_once()
        mock_detector_instance.detect_test_frameworks.assert_called_once()
        mock_detector_instance.analyze_test_structure.assert_called_once()
        
        # Check that CLI has the detector instance
        assert cli.detector is not None
        
        # Check that prints were called
        mock_print.assert_called()
    
    @patch("builtins.print")
    @patch("repository.scanner.RepositoryScanner")
    @patch("repository.coverage_analyzer.CoverageAnalyzer")
    def test_analyze_coverage(self, mock_analyzer, mock_scanner, mock_print, sample_repo):
        """Test analyzing test coverage."""
        # Mock the scanner
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.get_source_and_test_files.return_value = (["src/file1.py"], ["tests/test_file1.py"])
        
        # Mock the analyzer
        mock_analyzer_instance = MagicMock()
        mock_analyzer_instance.run_coverage_analysis.return_value = {
            "coverage_percentage": 75.0,
            "covered_files": ["src/file1.py"],
            "uncovered_files": [],
            "partially_covered_files": []
        }
        mock_analyzer_instance.identify_coverage_gaps.return_value = {
            "priority_files": [],
            "uncovered_files": [],
            "low_coverage_files": []
        }
        
        mock_scanner.return_value = mock_scanner_instance
        mock_analyzer.return_value = mock_analyzer_instance
        
        cli = CLI(sample_repo)
        cli.scanner = mock_scanner_instance
        cli.analyze_coverage("pytest")
        
        # Check that analyzer was initialized and used
        mock_analyzer.assert_called_once()
        mock_analyzer_instance.run_coverage_analysis.assert_called_once_with("pytest")
        mock_analyzer_instance.identify_coverage_gaps.assert_called_once()
        
        # Check that CLI has the analyzer instance
        assert cli.analyzer is not None
        
        # Check that prints were called
        mock_print.assert_called()
    
    @patch("builtins.print")
    @patch("ui.cli.CLI.scan_repository")
    @patch("ui.cli.CLI.detect_tests")
    @patch("ui.cli.CLI.analyze_coverage")
    def test_run(self, mock_analyze, mock_detect, mock_scan, mock_print, sample_repo):
        """Test running the full CLI workflow."""
        cli = CLI(sample_repo)
        cli.run()
        
        # Check that each step was called
        mock_scan.assert_called_once()
        mock_detect.assert_called_once()
        mock_analyze.assert_called_once()
        
        # Check that prints were called
        mock_print.assert_called()