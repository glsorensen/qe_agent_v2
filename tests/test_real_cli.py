import os
import sys
import pytest
import tempfile
import json
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from test_coverage_agent.ui.cli import cli, analyze, generate


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_repository_scanner():
    """Mock the RepositoryScanner class."""
    with patch('test_coverage_agent.ui.cli.RepositoryScanner') as mock_scanner_cls:
        mock_instance = MagicMock()
        mock_scanner_cls.return_value = mock_instance
        
        # Set up scanner methods
        mock_instance.scan.return_value = {'py': ['file1.py', 'file2.py']}
        mock_instance.get_source_and_test_files.return_value = (
            ['src/file1.py', 'src/file2.py'],
            ['tests/test_file1.py']
        )
        
        yield mock_scanner_cls, mock_instance


@pytest.fixture
def mock_test_detector():
    """Mock the TestDetector class."""
    with patch('test_coverage_agent.ui.cli.TestDetector') as mock_detector_cls:
        mock_instance = MagicMock()
        mock_detector_cls.return_value = mock_instance
        
        # Set up detector methods
        mock_instance.detect_test_frameworks.return_value = {'pytest': MagicMock()}
        mock_instance.analyze_test_structure.return_value = {
            'test_count': 1,
            'frameworks': ['pytest'],
            'test_to_source_ratio': 1.0,
            'files_by_framework': {'pytest': 1}
        }
        
        yield mock_detector_cls, mock_instance


@pytest.fixture
def mock_coverage_analyzer():
    """Mock the CoverageAnalyzer class."""
    with patch('test_coverage_agent.ui.cli.CoverageAnalyzer') as mock_analyzer_cls:
        mock_instance = MagicMock()
        mock_analyzer_cls.return_value = mock_instance
        
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
        
        yield mock_analyzer_cls, mock_instance


class TestCLICommands:
    """Tests for the CLI commands."""
    
    def test_cli_help(self, cli_runner):
        """Test the CLI help command."""
        result = cli_runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Test Coverage Enhancement Agent' in result.output
        assert 'analyze' in result.output
        assert 'generate' in result.output
    
    def test_analyze_command(self, cli_runner, mock_repository_scanner, 
                            mock_test_detector, mock_coverage_analyzer):
        """Test the analyze command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary output file
            output_file = os.path.join(temp_dir, 'analysis.json')
            
            # Run the command
            result = cli_runner.invoke(cli, ['analyze', temp_dir, '--output', output_file])
            
            # Check result
            assert result.exit_code == 0
            assert 'Analyzing repository' in result.output
            assert 'Detecting test frameworks' in result.output
            assert 'Analyzing test coverage' in result.output
            assert 'Analysis report saved to' in result.output
            
            # Verify mocks were called correctly
            mock_scanner_cls, mock_scanner = mock_repository_scanner
            mock_detector_cls, mock_detector = mock_test_detector
            mock_analyzer_cls, mock_analyzer = mock_coverage_analyzer
            
            mock_scanner_cls.assert_called_once_with(temp_dir)
            mock_scanner.scan.assert_called_once()
            mock_scanner.get_source_and_test_files.assert_called_once()
            
            mock_detector_cls.assert_called_once()
            mock_detector.detect_test_frameworks.assert_called_once()
            mock_detector.analyze_test_structure.assert_called_once()
            
            mock_analyzer_cls.assert_called_once()
            mock_analyzer.run_coverage_analysis.assert_called_once()
            
            # Check that output file was created with expected content
            assert os.path.exists(output_file)
            with open(output_file, 'r') as f:
                report = json.load(f)
                assert 'repo_path' in report
                assert 'coverage_percentage' in report
                assert report['coverage_percentage'] == 75.0
                
    def test_analyze_without_output(self, cli_runner, mock_repository_scanner,
                                  mock_test_detector, mock_coverage_analyzer):
        """Test the analyze command without output file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run the command
            result = cli_runner.invoke(cli, ['analyze', temp_dir])
            
            # Check result
            assert result.exit_code == 0
            assert 'Analyzing repository' in result.output
            assert 'Analysis report saved to' not in result.output
            
            # Verify mocks were called correctly
            mock_scanner_cls, mock_scanner = mock_repository_scanner
            mock_detector_cls, mock_detector = mock_test_detector
            mock_analyzer_cls, mock_analyzer = mock_coverage_analyzer
            
            mock_scanner_cls.assert_called_once_with(temp_dir)
            mock_scanner.scan.assert_called_once()

    @patch('test_coverage_agent.ui.cli.CodeUnderstandingModule')
    @patch('test_coverage_agent.ui.cli.TestTemplateManager')
    @patch('test_coverage_agent.ui.cli.AIPoweredTestWriter')
    @patch('test_coverage_agent.ui.cli.TestValidator')
    @patch('test_coverage_agent.ui.cli.CoverageReporter')
    def test_generate_command(self, mock_reporter_cls, mock_validator_cls, 
                            mock_writer_cls, mock_template_cls, mock_understanding_cls,
                            cli_runner, mock_repository_scanner, mock_test_detector, 
                            mock_coverage_analyzer):
        """Test the generate command."""
        # Mock the code understanding module
        mock_understanding = MagicMock()
        mock_understanding_cls.return_value = mock_understanding
        mock_understanding.get_all_functions.return_value = []
        mock_understanding.get_all_classes.return_value = []
        
        # Mock the template manager
        mock_template = MagicMock()
        mock_template_cls.return_value = mock_template
        
        # Mock the test writer
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer
        
        # Mock the test validator
        mock_validator = MagicMock()
        mock_validator_cls.return_value = mock_validator
        
        # Mock the coverage reporter
        mock_reporter = MagicMock()
        mock_reporter_cls.return_value = mock_reporter
        mock_reporter.generate_report.return_value = {}
        mock_reporter.save_report.return_value = "report.json"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run the command
            result = cli_runner.invoke(cli, [
                'generate', 
                temp_dir, 
                '--api-key', 'test-key',
                '--llm-provider', 'claude',
                '--output-dir', os.path.join(temp_dir, 'generated')
            ])
            
            # Check result
            assert result.exit_code == 0
            assert 'Generating tests for repository' in result.output
            assert 'Initializing AI-powered test writer' in result.output
            assert 'Generating coverage report' in result.output
            
            # Verify mocks were called correctly
            mock_scanner_cls, mock_scanner = mock_repository_scanner
            mock_detector_cls, mock_detector = mock_test_detector
            mock_analyzer_cls, mock_analyzer = mock_coverage_analyzer
            
            mock_scanner_cls.assert_called_once_with(temp_dir)
            mock_scanner.scan.assert_called_once()
            
            mock_detector_cls.assert_called_once()
            mock_detector.detect_test_frameworks.assert_called_once()
            
            mock_analyzer_cls.assert_called_once()
            mock_analyzer.run_coverage_analysis.assert_called_once()
            mock_analyzer.identify_coverage_gaps.assert_called_once()
            
            mock_understanding_cls.assert_called_once()
            mock_understanding.analyze_all_files.assert_called_once()
            
            mock_template_cls.assert_called_once()
            
            mock_writer_cls.assert_called_once_with(
                'test-key', mock_understanding, mock_template, 'claude'
            )
            
            mock_validator_cls.assert_called_once_with(temp_dir, 'test-key', 'claude')
            
            mock_reporter_cls.assert_called_once_with(temp_dir)
            mock_reporter.generate_report.assert_called_once()
            mock_reporter.save_report.assert_called_once()
            
    def test_generate_with_limit(self, cli_runner, mock_repository_scanner, 
                               mock_test_detector, mock_coverage_analyzer):
        """Test the generate command with a limit."""
        with patch('test_coverage_agent.ui.cli.CodeUnderstandingModule') as mock_understanding_cls, \
             patch('test_coverage_agent.ui.cli.TestTemplateManager') as mock_template_cls, \
             patch('test_coverage_agent.ui.cli.AIPoweredTestWriter') as mock_writer_cls, \
             patch('test_coverage_agent.ui.cli.TestValidator') as mock_validator_cls, \
             patch('test_coverage_agent.ui.cli.CoverageReporter') as mock_reporter_cls:
            
            # Mock the code understanding module
            mock_understanding = MagicMock()
            mock_understanding_cls.return_value = mock_understanding
            mock_understanding.get_all_functions.return_value = []
            mock_understanding.get_all_classes.return_value = []
            
            # Mock the template manager
            mock_template = MagicMock()
            mock_template_cls.return_value = mock_template
            
            # Mock the test writer
            mock_writer = MagicMock()
            mock_writer_cls.return_value = mock_writer
            
            # Mock the test validator
            mock_validator = MagicMock()
            mock_validator_cls.return_value = mock_validator
            
            # Mock the coverage reporter
            mock_reporter = MagicMock()
            mock_reporter_cls.return_value = mock_reporter
            mock_reporter.generate_report.return_value = {}
            mock_reporter.save_report.return_value = "report.json"
            
            # Set up analyzer to return multiple priority files
            _, mock_analyzer = mock_coverage_analyzer
            mock_analyzer.identify_coverage_gaps.return_value = {
                'priority_files': ['file1.py', 'file2.py', 'file3.py'],
                'uncovered_files': ['file1.py', 'file2.py', 'file3.py'],
                'low_coverage_files': []
            }
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Run the command with limit=2
                result = cli_runner.invoke(cli, [
                    'generate', 
                    temp_dir, 
                    '--api-key', 'test-key',
                    '--limit', '2'
                ])
                
                # Check result
                assert result.exit_code == 0
                assert 'Found 2 files with coverage gaps' in result.output