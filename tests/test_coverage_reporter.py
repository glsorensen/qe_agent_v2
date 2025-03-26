import os
import json
import pytest
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

from test_coverage_agent.test_execution.coverage_reporter import CoverageReporter, CoverageReport


class TestCoverageReporter:
    """Tests for the CoverageReporter class."""
    
    @pytest.fixture
    def sample_repo(self):
        """Create a temporary sample repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def sample_report_data(self):
        """Create sample report data."""
        return {
            "repo_path": "/repo",
            "overall_coverage": 75.5,
            "file_coverage": {
                "/repo/file1.py": 100.0,
                "/repo/file2.py": 50.0
            },
            "uncovered_files": ["/repo/file3.py"],
            "generated_tests": {"test1.py": "test content"},
            "validation_results": {
                "test1.py": {"is_valid": True}
            }
        }
    
    def test_init(self, sample_repo):
        """Test initializing the CoverageReporter."""
        reporter = CoverageReporter(sample_repo)
        
        assert reporter.repo_path == sample_repo
        assert reporter.reports_dir == os.path.join(sample_repo, '.coverage_reports')
        assert os.path.exists(reporter.reports_dir)
    
    def test_generate_report(self, sample_repo, sample_report_data):
        """Test generating a coverage report."""
        reporter = CoverageReporter(sample_repo)
        
        report = reporter.generate_report(
            overall_coverage=sample_report_data["overall_coverage"],
            file_coverage=sample_report_data["file_coverage"],
            uncovered_files=sample_report_data["uncovered_files"],
            generated_tests=sample_report_data["generated_tests"],
            validation_results=sample_report_data["validation_results"]
        )
        
        assert isinstance(report, CoverageReport)
        assert report.repo_path == sample_repo
        assert report.overall_coverage == 75.5
        assert len(report.file_coverage) == 2
        assert len(report.uncovered_files) == 1
        assert len(report.generated_tests) == 1
        assert len(report.validation_results) == 1
    
    def test_coverage_report_to_dict(self, sample_repo, sample_report_data):
        """Test converting a CoverageReport to a dictionary."""
        reporter = CoverageReporter(sample_repo)
        
        report = reporter.generate_report(
            overall_coverage=sample_report_data["overall_coverage"],
            file_coverage=sample_report_data["file_coverage"],
            uncovered_files=sample_report_data["uncovered_files"],
            generated_tests=sample_report_data["generated_tests"],
            validation_results=sample_report_data["validation_results"]
        )
        
        report_dict = report.to_dict()
        
        assert report_dict["repo_path"] == sample_repo
        assert report_dict["overall_coverage"] == 75.5
        assert report_dict["file_coverage"] == sample_report_data["file_coverage"]
        assert report_dict["uncovered_files"] == sample_report_data["uncovered_files"]
        assert report_dict["generated_tests_count"] == 1
        assert report_dict["validation_success_rate"] == 100.0
        assert "timestamp" in report_dict
    
    def test_calculate_success_rate(self, sample_repo):
        """Test calculating validation success rate."""
        # Create a report with mixed validation results
        report = CoverageReport(
            repo_path=sample_repo,
            overall_coverage=75.0,
            file_coverage={},
            uncovered_files=[],
            generated_tests={},
            validation_results={
                "test1.py": {"is_valid": True},
                "test2.py": {"is_valid": True},
                "test3.py": {"is_valid": False}
            }
        )
        
        success_rate = report._calculate_success_rate()
        
        assert success_rate == 2/3 * 100  # 2 out of 3 tests passed
    
    def test_calculate_success_rate_empty(self, sample_repo):
        """Test calculating validation success rate with no results."""
        report = CoverageReport(
            repo_path=sample_repo,
            overall_coverage=75.0,
            file_coverage={},
            uncovered_files=[],
            generated_tests={},
            validation_results={}
        )
        
        success_rate = report._calculate_success_rate()
        
        assert success_rate == 0.0
    
    def test_save_report_json(self, sample_repo, sample_report_data):
        """Test saving a report in JSON format."""
        reporter = CoverageReporter(sample_repo)
        
        report = reporter.generate_report(
            overall_coverage=sample_report_data["overall_coverage"],
            file_coverage=sample_report_data["file_coverage"],
            uncovered_files=sample_report_data["uncovered_files"],
            generated_tests=sample_report_data["generated_tests"],
            validation_results=sample_report_data["validation_results"]
        )
        
        # Mock datetime to get consistent filenames
        with patch('test_coverage_agent.test_execution.coverage_reporter.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
            mock_datetime.strftime.return_value = '20250101_120000'
            
            report_path = reporter.save_report(report, format='json')
        
        # Check that the file was created
        assert os.path.exists(report_path)
        assert report_path.endswith('.json')
        
        # Check content
        with open(report_path, 'r') as f:
            saved_data = json.load(f)
            
        assert saved_data["overall_coverage"] == 75.5
        assert saved_data["repo_path"] == sample_repo
        assert len(saved_data["file_coverage"]) == 2
    
    def test_save_report_txt(self, sample_repo, sample_report_data):
        """Test saving a report in text format."""
        reporter = CoverageReporter(sample_repo)
        
        report = reporter.generate_report(
            overall_coverage=sample_report_data["overall_coverage"],
            file_coverage=sample_report_data["file_coverage"],
            uncovered_files=sample_report_data["uncovered_files"],
            generated_tests=sample_report_data["generated_tests"],
            validation_results=sample_report_data["validation_results"]
        )
        
        # Mock datetime to get consistent filenames
        with patch('test_coverage_agent.test_execution.coverage_reporter.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
            mock_datetime.strftime.return_value = '20250101_120000'
            
            report_path = reporter.save_report(report, format='txt')
        
        # Check that the file was created
        assert os.path.exists(report_path)
        assert report_path.endswith('.txt')
        
        # Check content
        with open(report_path, 'r') as f:
            content = f.read()
            
        assert "Overall Coverage: 75.50%" in content
        assert "Repository: " + sample_repo in content
        assert "Uncovered Files:" in content
        assert "Generated Tests: 1" in content
    
    def test_load_report(self, sample_repo, sample_report_data):
        """Test loading a report from a file."""
        reporter = CoverageReporter(sample_repo)
        
        # Create a sample report JSON file
        report_file = os.path.join(reporter.reports_dir, "test_report.json")
        report_data = {
            "repo_path": sample_repo,
            "overall_coverage": 75.5,
            "file_coverage": {
                "/repo/file1.py": 100.0,
                "/repo/file2.py": 50.0
            },
            "uncovered_files": ["/repo/file3.py"],
            "timestamp": "2025-01-01T12:00:00"
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f)
        
        # Load the report
        loaded_report = reporter.load_report(report_file)
        
        assert loaded_report is not None
        assert loaded_report.repo_path == sample_repo
        assert loaded_report.overall_coverage == 75.5
        assert len(loaded_report.file_coverage) == 2
        assert len(loaded_report.uncovered_files) == 1
        assert loaded_report.generated_tests == {}  # Not saved in JSON
        assert loaded_report.validation_results == {}  # Not saved in JSON
    
    def test_load_report_invalid(self, sample_repo):
        """Test loading an invalid report."""
        reporter = CoverageReporter(sample_repo)
        
        # Create an invalid report JSON file
        report_file = os.path.join(reporter.reports_dir, "invalid_report.json")
        with open(report_file, 'w') as f:
            f.write("Not a valid JSON file")
        
        # Try to load the report
        loaded_report = reporter.load_report(report_file)
        
        assert loaded_report is None
    
    def test_compare_reports(self, sample_repo):
        """Test comparing two coverage reports."""
        reporter = CoverageReporter(sample_repo)
        
        # Create two reports with different coverage data
        old_report = CoverageReport(
            repo_path=sample_repo,
            overall_coverage=70.0,
            file_coverage={
                "/repo/file1.py": 90.0,
                "/repo/file2.py": 50.0
            },
            uncovered_files=["/repo/file3.py", "/repo/file4.py"],
            generated_tests={},
            validation_results={}
        )
        
        new_report = CoverageReport(
            repo_path=sample_repo,
            overall_coverage=75.0,
            file_coverage={
                "/repo/file1.py": 100.0,
                "/repo/file2.py": 50.0,
                "/repo/file3.py": 50.0
            },
            uncovered_files=["/repo/file4.py", "/repo/file5.py"],
            generated_tests={},
            validation_results={}
        )
        
        # Compare the reports
        comparison = reporter.compare_reports(old_report, new_report)
        
        assert comparison["overall_change"] == 5.0
        assert len(comparison["file_changes"]) == 1
        assert comparison["file_changes"]["/repo/file1.py"] == 10.0
        assert len(comparison["newly_covered"]) == 1
        assert "/repo/file3.py" in comparison["newly_covered"]
        assert len(comparison["newly_uncovered"]) == 1
        assert "/repo/file5.py" in comparison["newly_uncovered"]