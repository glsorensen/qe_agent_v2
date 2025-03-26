import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock

from ui.web_for_testing import WebUI


class TestWebUI:
    """Tests for the WebUI class."""
    
    @pytest.fixture
    def sample_repo(self):
        """Create a temporary sample repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_init(self, sample_repo):
        """Test initializing the WebUI."""
        web_ui = WebUI(sample_repo)
        
        assert web_ui.repo_path == sample_repo
        assert web_ui.scanner is None
        assert web_ui.detector is None
        assert web_ui.analyzer is None
        assert web_ui.reports == []
    
    @patch("repository.scanner.RepositoryScanner")
    def test_scan_repository(self, mock_scanner, sample_repo):
        """Test scanning the repository."""
        # Mock the scanner
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = {"py": ["file1.py", "file2.py"]}
        mock_scanner_instance.get_common_languages.return_value = {"python": ["file1.py", "file2.py"]}
        mock_scanner.return_value = mock_scanner_instance
        
        web_ui = WebUI(sample_repo)
        result = web_ui.scan_repository()
        
        # Check that scanner was initialized and used
        mock_scanner.assert_called_once_with(sample_repo)
        mock_scanner_instance.scan.assert_called_once()
        mock_scanner_instance.get_common_languages.assert_called_once()
        
        # Check that WebUI has the scanner instance
        assert web_ui.scanner is not None
        
        # Check the result structure
        assert "files" in result
        assert "languages" in result
        assert result["files"] == {"py": ["file1.py", "file2.py"]}
        assert result["languages"] == {"python": ["file1.py", "file2.py"]}
    
    @patch("repository.scanner.RepositoryScanner")
    @patch("repository.test_detector.TestDetector")
    def test_detect_tests(self, mock_detector, mock_scanner, sample_repo):
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
        mock_detector_instance.get_test_files_by_framework.return_value = {
            "pytest": ["tests/test_file1.py"]
        }
        
        mock_scanner.return_value = mock_scanner_instance
        mock_detector.return_value = mock_detector_instance
        
        web_ui = WebUI(sample_repo)
        web_ui.scanner = mock_scanner_instance
        result = web_ui.detect_tests()
        
        # Check that detector was initialized and used
        mock_detector.assert_called_once()
        mock_detector_instance.detect_test_frameworks.assert_called_once()
        mock_detector_instance.analyze_test_structure.assert_called_once()
        
        # Check that WebUI has the detector instance
        assert web_ui.detector is not None
        
        # Check the result structure
        assert "frameworks" in result
        assert "test_count" in result
        assert "test_to_source_ratio" in result
        assert "files_by_framework" in result
        assert result["frameworks"] == ["pytest"]
        assert result["test_count"] == 1
        assert result["test_to_source_ratio"] == 1.0
        assert result["files_by_framework"] == {"pytest": 1}
    
    @patch("repository.scanner.RepositoryScanner")
    @patch("repository.coverage_analyzer.CoverageAnalyzer")
    def test_analyze_coverage(self, mock_analyzer, mock_scanner, sample_repo):
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
        
        web_ui = WebUI(sample_repo)
        web_ui.scanner = mock_scanner_instance
        result = web_ui.analyze_coverage("pytest")
        
        # Check that analyzer was initialized and used
        mock_analyzer.assert_called_once()
        mock_analyzer_instance.run_coverage_analysis.assert_called_once_with("pytest")
        mock_analyzer_instance.identify_coverage_gaps.assert_called_once()
        
        # Check that WebUI has the analyzer instance
        assert web_ui.analyzer is not None
        
        # Check the result structure
        assert "coverage_percentage" in result
        assert "covered_files" in result
        assert "uncovered_files" in result
        assert "partially_covered_files" in result
        assert "priority_files" in result
        assert result["coverage_percentage"] == 75.0
        assert result["covered_files"] == ["src/file1.py"]
        assert result["uncovered_files"] == []
        assert result["partially_covered_files"] == []
        assert result["priority_files"] == []
    
    @patch("test_execution.coverage_reporter.CoverageReporter")
    def test_generate_report(self, mock_reporter, sample_repo):
        """Test generating a coverage report."""
        # Mock the reporter and report
        mock_report = MagicMock()
        mock_report.to_dict.return_value = {
            "repo_path": sample_repo,
            "overall_coverage": 75.0,
            "timestamp": "2025-01-01T12:00:00"
        }
        
        mock_reporter_instance = MagicMock()
        mock_reporter_instance.generate_report.return_value = mock_report
        mock_reporter_instance.save_report.return_value = os.path.join(sample_repo, "report.json")
        
        mock_reporter.return_value = mock_reporter_instance
        
        web_ui = WebUI(sample_repo)
        result = web_ui.generate_report(
            overall_coverage=75.0,
            file_coverage={},
            uncovered_files=[],
            generated_tests={},
            validation_results={}
        )
        
        # Check that reporter was initialized and used
        mock_reporter.assert_called_once_with(sample_repo)
        mock_reporter_instance.generate_report.assert_called_once()
        mock_reporter_instance.save_report.assert_called_once()
        
        # Check that report was added to WebUI reports
        assert len(web_ui.reports) == 1
        assert web_ui.reports[0] == mock_report
        
        # Check the result structure
        assert "report" in result
        assert "saved_path" in result
        assert result["report"] == {"repo_path": sample_repo, "overall_coverage": 75.0, "timestamp": "2025-01-01T12:00:00"}
        assert result["saved_path"] == os.path.join(sample_repo, "report.json")
    
    @patch("ui.web.WebUI.scan_repository")
    @patch("ui.web.WebUI.detect_tests")
    @patch("ui.web.WebUI.analyze_coverage")
    @patch("ui.web.WebUI.generate_report")
    def test_run_analysis(self, mock_generate, mock_analyze, mock_detect, mock_scan, sample_repo):
        """Test running the full web UI analysis workflow."""
        # Set up mock returns
        mock_scan.return_value = {"files": {}, "languages": {}}
        mock_detect.return_value = {"frameworks": ["pytest"], "test_count": 1}
        mock_analyze.return_value = {"coverage_percentage": 75.0}
        mock_generate.return_value = {"report": {}, "saved_path": "report.json"}
        
        web_ui = WebUI(sample_repo)
        result = web_ui.run_analysis()
        
        # Check that each step was called
        mock_scan.assert_called_once()
        mock_detect.assert_called_once()
        mock_analyze.assert_called_once()
        mock_generate.assert_called_once()
        
        # Check the result structure
        assert "scan_results" in result
        assert "test_results" in result
        assert "coverage_results" in result
        assert "report" in result
        assert result["scan_results"] == {"files": {}, "languages": {}}
        assert result["test_results"] == {"frameworks": ["pytest"], "test_count": 1}
        assert result["coverage_results"] == {"coverage_percentage": 75.0}
        assert result["report"] == {"report": {}, "saved_path": "report.json"}
    
    @patch("ui.web_for_testing.Flask")
    def test_start_server(self, mock_flask, sample_repo):
        """Test starting the web server."""
        # Mock Flask app and methods
        mock_app = MagicMock()
        mock_flask.return_value = mock_app
        
        web_ui = WebUI(sample_repo)
        web_ui.start_server(debug=True, port=5000)
        
        # Check that Flask was initialized and used
        mock_flask.assert_called_once()
        
        # Check that routes were registered (at least one add_url_rule call)
        assert mock_app.add_url_rule.call_count > 0
        
        # Check that the app was run
        mock_app.run.assert_called_once_with(debug=True, port=5000, host="0.0.0.0")