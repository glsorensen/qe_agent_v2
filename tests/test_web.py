import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
import pandas as pd
import tempfile

# Mock streamlit for testing
sys.modules['streamlit'] = MagicMock()
sys.modules['streamlit'].session_state = {}

# Import web module after mocking
from test_coverage_agent.ui.web_for_testing import WebUI


class TestWebUI:
    """Tests for the web interface."""
    
    @pytest.fixture
    def web_ui(self):
        """Create a WebUI instance."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ui = WebUI(temp_dir)
            yield ui
    
    @pytest.fixture
    def mock_repository_scanner(self):
        """Mock the RepositoryScanner class."""
        with patch('test_coverage_agent.ui.web_for_testing.RepositoryScanner') as mock_cls:
            mock_instance = MagicMock()
            mock_cls.return_value = mock_instance
            
            # Set up scanner methods
            mock_instance.scan.return_value = {'py': ['file1.py', 'file2.py']}
            mock_instance.get_source_and_test_files.return_value = (
                ['src/file1.py', 'src/file2.py'],
                ['tests/test_file1.py']
            )
            mock_instance.get_common_languages.return_value = {
                'python': ['file1.py', 'file2.py']
            }
            
            yield mock_cls, mock_instance
    
    @pytest.fixture
    def mock_test_detector(self):
        """Mock the TestDetector class."""
        with patch('test_coverage_agent.ui.web_for_testing.TestDetector') as mock_cls:
            mock_instance = MagicMock()
            mock_cls.return_value = mock_instance
            
            # Set up detector methods
            mock_instance.detect_test_frameworks.return_value = {'pytest': MagicMock()}
            mock_instance.analyze_test_structure.return_value = {
                'test_count': 1,
                'frameworks': ['pytest'],
                'test_to_source_ratio': 1.0,
                'files_by_framework': {'pytest': 1}
            }
            
            yield mock_cls, mock_instance
    
    @pytest.fixture
    def mock_coverage_analyzer(self):
        """Mock the CoverageAnalyzer class."""
        with patch('test_coverage_agent.ui.web_for_testing.CoverageAnalyzer') as mock_cls:
            mock_instance = MagicMock()
            mock_cls.return_value = mock_instance
            
            # Set up analyzer methods
            mock_instance.run_coverage_analysis.return_value = {
                'coverage_percentage': 75.0,
                'covered_files': ['src/file1.py'],
                'partially_covered_files': [],
                'uncovered_files': ['src/file2.py']
            }
            mock_instance.identify_coverage_gaps.return_value = {
                'priority_files': ['src/file2.py'],
                'uncovered_files': ['src/file2.py'],
                'low_coverage_files': []
            }
            
            yield mock_cls, mock_instance

    def test_init(self):
        """Test initializing the web interface."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ui = WebUI(temp_dir)
            
            assert ui.repo_path == temp_dir
            assert ui.scanner is None
            assert ui.detector is None
            assert ui.analyzer is None
            assert hasattr(ui, 'reports')
    
    def test_scan_repository(self, web_ui, mock_repository_scanner):
        """Test scanning a repository."""
        # Get mocks
        mock_cls, mock_instance = mock_repository_scanner
        
        # Run the method
        web_ui.scan_repository()
        
        # Check mocks were called correctly
        mock_cls.assert_called_once_with(web_ui.repo_path)
        mock_instance.scan.assert_called_once()
        mock_instance.get_source_and_test_files.assert_called_once()
        
        # Check that UI has scanner instance
        assert web_ui.scanner is not None
        assert web_ui.scanner == mock_instance
    
    def test_detect_tests(self, web_ui, mock_repository_scanner, mock_test_detector):
        """Test detecting tests in the repository."""
        # Set up scanner mock
        mock_scanner_cls, mock_scanner = mock_repository_scanner
        web_ui.scanner = mock_scanner
        
        # Get test detector mock
        mock_detector_cls, mock_detector = mock_test_detector
        
        # Run the method
        web_ui.detect_tests()
        
        # Check mocks were called correctly
        mock_detector_cls.assert_called_once()
        mock_detector.detect_test_frameworks.assert_called_once()
        mock_detector.analyze_test_structure.assert_called_once()
        
        # Check that UI has detector instance
        assert web_ui.detector is not None
        assert web_ui.detector == mock_detector
    
    def test_analyze_coverage(self, web_ui, mock_repository_scanner, mock_coverage_analyzer):
        """Test analyzing test coverage."""
        # Set up scanner mock
        mock_scanner_cls, mock_scanner = mock_repository_scanner
        web_ui.scanner = mock_scanner
        
        # Get analyzer mock
        mock_analyzer_cls, mock_analyzer = mock_coverage_analyzer
        
        # Run the method
        web_ui.analyze_coverage("pytest")
        
        # Check mocks were called correctly
        mock_analyzer_cls.assert_called_once()
        mock_analyzer.run_coverage_analysis.assert_called_once_with("pytest")
        mock_analyzer.identify_coverage_gaps.assert_called_once()
        
        # Check that UI has analyzer instance
        assert web_ui.analyzer is not None
        assert web_ui.analyzer == mock_analyzer
    
    @patch('test_coverage_agent.ui.web_for_testing.CodeUnderstandingModule')
    @patch('test_coverage_agent.ui.web_for_testing.TestTemplateManager')
    @patch('test_coverage_agent.ui.web_for_testing.AIPoweredTestWriter')
    def test_initialize_test_generation(self, mock_writer_cls, mock_template_cls, 
                                      mock_understanding_cls, web_ui):
        """Test initializing test generation components."""
        # Set up mocks
        mock_understanding = MagicMock()
        mock_understanding_cls.return_value = mock_understanding
        
        mock_template = MagicMock()
        mock_template_cls.return_value = mock_template
        
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer
        
        # Set up UI
        web_ui.api_key = "test-key"
        web_ui.llm_provider = "claude"
        
        # Run the method
        web_ui.initialize_test_generation()
        
        # Check mocks were called correctly
        mock_understanding_cls.assert_called_once_with(web_ui.repo_path, [])
        mock_template_cls.assert_called_once()
        mock_writer_cls.assert_called_once_with(
            "test-key", mock_understanding, mock_template, "claude"
        )
        
        # Check that UI has instances
        assert web_ui.code_understanding is not None
        assert web_ui.template_manager is not None
        assert web_ui.test_writer is not None
        
        assert web_ui.code_understanding == mock_understanding
        assert web_ui.template_manager == mock_template
        assert web_ui.test_writer == mock_writer
    
    @patch('test_coverage_agent.ui.web_for_testing.TestValidator')
    def test_initialize_test_validator(self, mock_validator_cls, web_ui):
        """Test initializing the test validator."""
        # Set up mock
        mock_validator = MagicMock()
        mock_validator_cls.return_value = mock_validator
        
        # Set up UI
        web_ui.api_key = "test-key"
        web_ui.llm_provider = "claude"
        
        # Run the method
        web_ui.initialize_test_validator()
        
        # Check mock was called correctly
        mock_validator_cls.assert_called_once_with(
            web_ui.repo_path, "test-key", "claude"
        )
        
        # Check that UI has instance
        assert web_ui.test_validator is not None
        assert web_ui.test_validator == mock_validator