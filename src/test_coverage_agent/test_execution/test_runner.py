import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Set, Tuple, Any


class TestRunResult:
    """Class representing the result of a test run."""
    
    def __init__(
        self,
        success: bool,
        output: str,
        error_message: Optional[str] = None,
        duration: float = 0.0
    ):
        """Initialize a test run result.
        
        Args:
            success: Whether the test passed
            output: Test output
            error_message: Error message if the test failed
            duration: Test duration in seconds
        """
        self.success = success
        self.output = output
        self.error_message = error_message
        self.duration = duration


class TestRunner:
    """Runner for executing tests in isolation."""
    
    def __init__(self, repo_path: str):
        """Initialize the test runner.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
    
    def run_test_file(self, test_file_path: str) -> TestRunResult:
        """Run a specific test file.
        
        Args:
            test_file_path: Path to the test file
            
        Returns:
            TestRunResult object with the results
        """
        # Determine test framework from file
        if test_file_path.endswith('.py'):
            return self._run_python_test(test_file_path)
        elif test_file_path.endswith('.js') or test_file_path.endswith('.jsx'):
            return self._run_js_test(test_file_path)
        else:
            return TestRunResult(
                success=False,
                output="",
                error_message=f"Unsupported test file type: {test_file_path}"
            )
    
    def run_test_code(self, test_code: str, language: str) -> TestRunResult:
        """Run test code directly (without writing to a file).
        
        Args:
            test_code: Test code to run
            language: Programming language of the test code
            
        Returns:
            TestRunResult object with the results
        """
        # Create a temporary file for the test
        with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_suffix(language)) as temp:
            temp.write(test_code.encode('utf-8'))
            temp_path = temp.name
        
        try:
            # Run the test
            result = self.run_test_file(temp_path)
            return result
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def write_and_run_test(
        self, 
        test_code: str, 
        target_path: str, 
        language: str
    ) -> TestRunResult:
        """Write test code to a file and run it.
        
        Args:
            test_code: Test code to write
            target_path: Path to write the test to
            language: Programming language of the test code
            
        Returns:
            TestRunResult object with the results
        """
        # Create parent directories if needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Write the test file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # Run the test
        return self.run_test_file(target_path)
    
    def _run_python_test(self, test_file_path: str) -> TestRunResult:
        """Run a Python test file.
        
        Args:
            test_file_path: Path to the Python test file
            
        Returns:
            TestRunResult object with the results
        """
        try:
            # Try running with pytest first
            result = subprocess.run(
                ['python', '-m', 'pytest', test_file_path, '-v'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            
            success = result.returncode == 0
            output = result.stdout
            error_message = result.stderr if result.stderr else None
            
            return TestRunResult(
                success=success,
                output=output,
                error_message=error_message
            )
        except Exception as e:
            return TestRunResult(
                success=False,
                output="",
                error_message=str(e)
            )
    
    def _run_js_test(self, test_file_path: str) -> TestRunResult:
        """Run a JavaScript test file.
        
        Args:
            test_file_path: Path to the JavaScript test file
            
        Returns:
            TestRunResult object with the results
        """
        try:
            # Try running with Jest
            result = subprocess.run(
                ['npx', 'jest', test_file_path, '--no-cache'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            
            success = result.returncode == 0
            output = result.stdout
            error_message = result.stderr if result.stderr else None
            
            return TestRunResult(
                success=success,
                output=output,
                error_message=error_message
            )
        except Exception as e:
            return TestRunResult(
                success=False,
                output="",
                error_message=str(e)
            )
    
    def _get_suffix(self, language: str) -> str:
        """Get the file suffix for a given language.
        
        Args:
            language: Programming language
            
        Returns:
            File suffix
        """
        language = language.lower()
        if language == 'python':
            return '.py'
        elif language in ['javascript', 'js']:
            return '.js'
        elif language == 'typescript':
            return '.ts'
        else:
            return '.txt'  # Default