# Test Execution Module API

The Test Execution module provides components for running tests, validating test quality, and generating coverage reports.

## TestRunner

```python
from test_execution.test_runner import TestRunner, TestRunResult
```

The `TestRunner` class executes tests and collects results, including coverage data.

### Constructor

```python
def __init__(self, repository_path: str):
    """Initialize a TestRunner.

    Args:
        repository_path: Path to the repository
    """
```

### Methods

#### run_tests

```python
def run_tests(self, test_paths: Optional[List[str]] = None) -> TestRunResult:
    """Run tests and collect results.

    Args:
        test_paths: Optional list of specific test paths to run. If None, run all tests.

    Returns:
        TestRunResult containing test results and coverage data
    """
```

Runs tests and returns a `TestRunResult` containing results and coverage data.

#### run_specific_test

```python
def run_specific_test(self, test_path: str, test_name: Optional[str] = None) -> TestRunResult:
    """Run a specific test file or test function.

    Args:
        test_path: Path to the test file
        test_name: Optional name of specific test to run

    Returns:
        TestRunResult for the specific test
    """
```

Runs a specific test file or test function and returns the result.

#### collect_coverage_data

```python
def collect_coverage_data(self, test_run_result: TestRunResult) -> Dict[str, Any]:
    """Extract and process coverage data from a test run.

    Args:
        test_run_result: TestRunResult from a test run

    Returns:
        Dict containing processed coverage data
    """
```

Extracts and processes coverage data from a test run.

### TestRunResult Class

```python
class TestRunResult:
    """Class representing the result of a test run."""
    
    def __init__(self, success: bool, test_count: int, failures: List[Dict[str, Any]], 
                 coverage_data: Optional[Dict[str, Any]] = None):
        """Initialize a TestRunResult.

        Args:
            success: Whether all tests passed
            test_count: Number of tests run
            failures: List of test failures with details
            coverage_data: Optional coverage data collected during the run
        """
        self.success = success
        self.test_count = test_count
        self.failures = failures
        self.coverage_data = coverage_data if coverage_data else {}
```

Represents the result of a test run, including success status, test count, failures, and coverage data.

### Example Usage

```python
# Initialize runner
runner = TestRunner("/path/to/repo")

# Run all tests
result = runner.run_tests()

# Check if tests succeeded
if result.success:
    print(f"All {result.test_count} tests passed!")
else:
    print(f"{len(result.failures)} of {result.test_count} tests failed.")
    for failure in result.failures:
        print(f"Failed: {failure['name']} - {failure['message']}")

# Run a specific test file
result = runner.run_specific_test("tests/test_module.py")

# Run a specific test function
result = runner.run_specific_test("tests/test_module.py", "test_specific_function")

# Extract coverage data
coverage_data = runner.collect_coverage_data(result)
```

## TestValidator

```python
from test_execution.test_validator import TestValidator, ValidationRule
```

The `TestValidator` class validates test quality against best practices and provides improvement recommendations.

### Constructor

```python
def __init__(self):
    """Initialize a TestValidator with default validation rules."""
```

### Methods

#### validate_test_file

```python
def validate_test_file(self, file_path: str) -> Dict[str, Any]:
    """Validate a single test file.

    Args:
        file_path: Path to the test file

    Returns:
        Dict containing validation results
    """
```

Validates a single test file and returns the results.

#### validate_test_directory

```python
def validate_test_directory(self, directory_path: str) -> Dict[str, Any]:
    """Validate all test files in a directory.

    Args:
        directory_path: Path to the directory containing tests

    Returns:
        Dict containing validation results for all tests
    """
```

Validates all test files in a directory and returns the results.

#### calculate_quality_score

```python
def calculate_quality_score(self, validation_results: Dict[str, Any]) -> float:
    """Calculate an overall quality score from validation results.

    Args:
        validation_results: Results from validation

    Returns:
        Quality score between 0.0 and 1.0
    """
```

Calculates an overall quality score from validation results.

#### add_validation_rule

```python
def add_validation_rule(self, rule: ValidationRule) -> None:
    """Add a custom validation rule.

    Args:
        rule: ValidationRule instance to add
    """
```

Adds a custom validation rule to the validator.

### ValidationRule Class

```python
class ValidationRule:
    """Base class for test validation rules."""
    
    def validate(self, test_content: str, test_name: Optional[str] = None, 
                 file_path: Optional[str] = None) -> Dict[str, Any]:
        """Validate a test against this rule.

        Args:
            test_content: Content of the test
            test_name: Optional name of the test
            file_path: Optional path to the test file

        Returns:
            Dict with at least a 'result' key (True if passed, False if failed)
        """
        raise NotImplementedError("Subclasses must implement this method")
```

Base class for test validation rules that can be extended with custom validation logic.

### Example Usage

```python
# Initialize validator
validator = TestValidator()

# Create custom validation rule
class CustomRule(ValidationRule):
    def validate(self, test_content, test_name=None, file_path=None):
        if "assert" not in test_content:
            return {
                "result": False,
                "issue_type": "missing_assertion",
                "severity": "high",
                "message": "Test doesn't contain any assertions",
                "recommendation": "Add at least one assertion to verify behavior"
            }
        return {"result": True}

# Add custom rule
validator.add_validation_rule(CustomRule())

# Validate a test file
results = validator.validate_test_file("tests/test_module.py")

# Validate all tests in a directory
all_results = validator.validate_test_directory("tests")

# Calculate quality score
score = validator.calculate_quality_score(all_results)
print(f"Test quality score: {score * 100:.1f}%")

# Process validation issues
for file_path, file_results in all_results.items():
    for issue in file_results.get("issues", []):
        print(f"Issue in {file_path}: {issue['message']}")
        print(f"Recommendation: {issue['recommendation']}")
```

## CoverageReporter

```python
from test_execution.coverage_reporter import CoverageReporter
```

The `CoverageReporter` class generates human-readable reports based on coverage analysis.

### Constructor

```python
def __init__(self, repository_path: str):
    """Initialize a CoverageReporter.

    Args:
        repository_path: Path to the repository
    """
```

### Methods

#### generate_summary_report

```python
def generate_summary_report(self) -> str:
    """Generate a summary coverage report.

    Returns:
        String containing the summary report
    """
```

Generates a summary coverage report as a string.

#### generate_detailed_report

```python
def generate_detailed_report(self, format: str = "text", output_path: Optional[str] = None) -> str:
    """Generate a detailed coverage report.

    Args:
        format: Report format (text, html, json, markdown)
        output_path: Optional path to write the report

    Returns:
        String containing the report or path to the report file
    """
```

Generates a detailed coverage report in the specified format.

#### export_report

```python
def export_report(self, report_data: Dict[str, Any], format: str = "json", 
                 output_path: str = "coverage_report") -> str:
    """Export coverage data in the specified format.

    Args:
        report_data: Coverage data to export
        format: Export format (json, html, xml, markdown)
        output_path: Path to write the report

    Returns:
        Path to the exported report
    """
```

Exports coverage data in the specified format to the given path.

### Example Usage

```python
# Initialize reporter
reporter = CoverageReporter("/path/to/repo")

# Generate summary report
summary = reporter.generate_summary_report()
print(summary)

# Generate detailed HTML report
html_report_path = reporter.generate_detailed_report(
    format="html",
    output_path="./coverage_report.html"
)

# Generate JSON report
json_report = reporter.generate_detailed_report(format="json")

# Export specific coverage data
from test_execution.test_runner import TestRunner
runner = TestRunner("/path/to/repo")
result = runner.run_tests()
coverage_data = runner.collect_coverage_data(result)

export_path = reporter.export_report(
    report_data=coverage_data,
    format="markdown",
    output_path="./custom_report.md"
)
```