import os
import pytest
import tempfile
import subprocess
from unittest.mock import patch, MagicMock

from test_execution.test_runner import TestRunner, TestRunResult


class TestTestRunner:
    """Tests for the TestRunner class."""
    
    @pytest.fixture
    def sample_repo(self):
        """Create a temporary sample repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a sample Python test file
            with open(os.path.join(temp_dir, "test_sample.py"), "w") as f:
                f.write("""
import pytest

def test_passing():
    assert True

def test_failing():
    assert False
                """)
            
            yield temp_dir
    
    def test_init(self, sample_repo):
        """Test initializing the TestRunner."""
        runner = TestRunner(sample_repo)
        assert runner.repo_path == sample_repo
    
    def test_get_suffix(self, sample_repo):
        """Test getting file suffix for different languages."""
        runner = TestRunner(sample_repo)
        
        assert runner._get_suffix("python") == ".py"
        assert runner._get_suffix("javascript") == ".js"
        assert runner._get_suffix("typescript") == ".ts"
        assert runner._get_suffix("unknown_language") == ".txt"
    
    @patch("subprocess.run")
    def test_run_python_test(self, mock_run, sample_repo):
        """Test running a Python test."""
        # Mock a successful test run
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Test passed!"
        mock_process.stderr = ""
        
        mock_run.return_value = mock_process
        
        runner = TestRunner(sample_repo)
        test_file = os.path.join(sample_repo, "test_sample.py")
        
        result = runner._run_python_test(test_file)
        
        assert result.success is True
        assert result.output == "Test passed!"
        assert result.error_message is None
        
        # Verify subprocess.run was called correctly
        mock_run.assert_called_once_with(
            ['python', '-m', 'pytest', test_file, '-v'],
            cwd=sample_repo,
            capture_output=True,
            text=True,
            check=False
        )
    
    @patch("subprocess.run")
    def test_run_python_test_failure(self, mock_run, sample_repo):
        """Test running a Python test that fails."""
        # Mock a failing test run
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Test failed!"
        mock_process.stderr = "Error message"
        
        mock_run.return_value = mock_process
        
        runner = TestRunner(sample_repo)
        test_file = os.path.join(sample_repo, "test_sample.py")
        
        result = runner._run_python_test(test_file)
        
        assert result.success is False
        assert result.output == "Test failed!"
        assert result.error_message == "Error message"
    
    @patch("subprocess.run", side_effect=Exception("Command failed"))
    def test_run_python_test_exception(self, mock_run, sample_repo):
        """Test handling exceptions while running Python tests."""
        runner = TestRunner(sample_repo)
        test_file = os.path.join(sample_repo, "test_sample.py")
        
        result = runner._run_python_test(test_file)
        
        assert result.success is False
        assert result.output == ""
        assert result.error_message == "Command failed"
    
    @patch("subprocess.run")
    def test_run_js_test(self, mock_run, sample_repo):
        """Test running a JavaScript test."""
        # Mock a successful test run
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Test passed!"
        mock_process.stderr = ""
        
        mock_run.return_value = mock_process
        
        runner = TestRunner(sample_repo)
        test_file = os.path.join(sample_repo, "test_sample.js")
        
        result = runner._run_js_test(test_file)
        
        assert result.success is True
        assert result.output == "Test passed!"
        assert result.error_message is None
        
        # Verify subprocess.run was called correctly
        mock_run.assert_called_once_with(
            ['npx', 'jest', test_file, '--no-cache'],
            cwd=sample_repo,
            capture_output=True,
            text=True,
            check=False
        )
    
    def test_run_test_file_unsupported(self, sample_repo):
        """Test running an unsupported test file type."""
        runner = TestRunner(sample_repo)
        test_file = os.path.join(sample_repo, "test_sample.unknown")
        
        result = runner.run_test_file(test_file)
        
        assert result.success is False
        assert "Unsupported test file type" in result.error_message
    
    @patch("test_execution.test_runner.tempfile.NamedTemporaryFile")
    @patch("test_execution.test_runner.os.unlink")
    def test_run_test_code(self, mock_unlink, mock_temp_file, sample_repo):
        """Test running test code directly."""
        # Set up mocks
        mock_file = MagicMock()
        mock_file.name = os.path.join(sample_repo, "temp_test.py")
        mock_temp_file.return_value.__enter__.return_value = mock_file
        
        # Create a runner with a mocked run_test_file method
        runner = TestRunner(sample_repo)
        runner.run_test_file = MagicMock(return_value=TestRunResult(True, "Test passed!"))
        
        result = runner.run_test_code("def test_example():\n    assert True", "python")
        
        assert result.success is True
        assert result.output == "Test passed!"
        
        # Verify temp file was written to
        mock_file.write.assert_called_once_with(b"def test_example():\n    assert True")
        
        # Verify run_test_file was called
        runner.run_test_file.assert_called_once_with(mock_file.name)
    
    def test_write_and_run_test(self, sample_repo):
        """Test writing and running a test."""
        # Create a runner with a mocked run_test_file method
        runner = TestRunner(sample_repo)
        runner.run_test_file = MagicMock(return_value=TestRunResult(True, "Test passed!"))
        
        # Create test directory
        test_dir = os.path.join(sample_repo, "new_tests")
        test_file = os.path.join(test_dir, "test_new.py")
        test_code = "def test_example():\n    assert True"
        
        result = runner.write_and_run_test(test_code, test_file, "python")
        
        assert result.success is True
        assert result.output == "Test passed!"
        
        # Verify file was written
        assert os.path.exists(test_file)
        with open(test_file, "r") as f:
            assert f.read() == test_code
        
        # Verify run_test_file was called
        runner.run_test_file.assert_called_once_with(test_file)