# Data Models API

This document describes the key data structures and models used throughout the Test Coverage Agent.

## Core Data Models

The Test Coverage Agent uses several core data models to represent various aspects of repository structure, test coverage, and analysis results.

### RepositoryStructure

Represents the structure of a repository, including files, modules, classes, and methods.

```python
class RepositoryStructure:
    """Represents the structure of a repository."""
    
    def __init__(self, repository_path: str):
        """Initialize a RepositoryStructure.
        
        Args:
            repository_path: Path to the repository
        """
        self.repository_path = repository_path
        self.files: List[str] = []
        self.modules: Dict[str, ModuleInfo] = {}
        self.directory_tree: Dict[str, Any] = {}
        
    def add_file(self, file_path: str) -> None:
        """Add a file to the structure.
        
        Args:
            file_path: Path to the file
        """
        self.files.append(file_path)
        
    def add_module(self, module_name: str, module_info: 'ModuleInfo') -> None:
        """Add a module to the structure.
        
        Args:
            module_name: Name of the module
            module_info: Information about the module
        """
        self.modules[module_name] = module_info
```

### ModuleInfo

Contains information about a Python module, including its classes and functions.

```python
class ModuleInfo:
    """Information about a Python module."""
    
    def __init__(self, name: str, file_path: str):
        """Initialize a ModuleInfo.
        
        Args:
            name: Name of the module
            file_path: Path to the module file
        """
        self.name = name
        self.file_path = file_path
        self.classes: Dict[str, ClassInfo] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.imports: List[str] = []
        
    def add_class(self, class_name: str, class_info: 'ClassInfo') -> None:
        """Add a class to the module.
        
        Args:
            class_name: Name of the class
            class_info: Information about the class
        """
        self.classes[class_name] = class_info
        
    def add_function(self, function_name: str, function_info: 'FunctionInfo') -> None:
        """Add a function to the module.
        
        Args:
            function_name: Name of the function
            function_info: Information about the function
        """
        self.functions[function_name] = function_info
        
    def add_import(self, import_name: str) -> None:
        """Add an import to the module.
        
        Args:
            import_name: Name of the imported module
        """
        self.imports.append(import_name)
```

### ClassInfo

Contains information about a Python class, including its methods and attributes.

```python
class ClassInfo:
    """Information about a Python class."""
    
    def __init__(self, name: str, module: str):
        """Initialize a ClassInfo.
        
        Args:
            name: Name of the class
            module: Name of the module containing the class
        """
        self.name = name
        self.module = module
        self.methods: Dict[str, MethodInfo] = {}
        self.attributes: List[str] = []
        self.parent_classes: List[str] = []
        
    def add_method(self, method_name: str, method_info: 'MethodInfo') -> None:
        """Add a method to the class.
        
        Args:
            method_name: Name of the method
            method_info: Information about the method
        """
        self.methods[method_name] = method_info
        
    def add_attribute(self, attribute_name: str) -> None:
        """Add an attribute to the class.
        
        Args:
            attribute_name: Name of the attribute
        """
        self.attributes.append(attribute_name)
        
    def add_parent_class(self, parent_class: str) -> None:
        """Add a parent class.
        
        Args:
            parent_class: Name of the parent class
        """
        self.parent_classes.append(parent_class)
```

### FunctionInfo and MethodInfo

Contain information about functions and methods, including parameters and return types.

```python
class FunctionInfo:
    """Information about a Python function."""
    
    def __init__(self, name: str, module: str):
        """Initialize a FunctionInfo.
        
        Args:
            name: Name of the function
            module: Name of the module containing the function
        """
        self.name = name
        self.module = module
        self.parameters: List[str] = []
        self.return_type: Optional[str] = None
        self.docstring: Optional[str] = None
        self.line_range: Tuple[int, int] = (0, 0)
        
    def add_parameter(self, parameter_name: str) -> None:
        """Add a parameter to the function.
        
        Args:
            parameter_name: Name of the parameter
        """
        self.parameters.append(parameter_name)
        
    def set_return_type(self, return_type: str) -> None:
        """Set the return type of the function.
        
        Args:
            return_type: Return type as a string
        """
        self.return_type = return_type
        
    def set_docstring(self, docstring: str) -> None:
        """Set the docstring of the function.
        
        Args:
            docstring: Function docstring
        """
        self.docstring = docstring
        
    def set_line_range(self, start: int, end: int) -> None:
        """Set the line range of the function.
        
        Args:
            start: Start line number
            end: End line number
        """
        self.line_range = (start, end)


class MethodInfo(FunctionInfo):
    """Information about a Python method."""
    
    def __init__(self, name: str, module: str, class_name: str):
        """Initialize a MethodInfo.
        
        Args:
            name: Name of the method
            module: Name of the module containing the method
            class_name: Name of the class containing the method
        """
        super().__init__(name, module)
        self.class_name = class_name
        self.is_static = False
        self.is_class_method = False
        self.is_property = False
        
    def set_static(self, is_static: bool = True) -> None:
        """Set whether the method is static.
        
        Args:
            is_static: Whether the method is a static method
        """
        self.is_static = is_static
        
    def set_class_method(self, is_class_method: bool = True) -> None:
        """Set whether the method is a class method.
        
        Args:
            is_class_method: Whether the method is a class method
        """
        self.is_class_method = is_class_method
        
    def set_property(self, is_property: bool = True) -> None:
        """Set whether the method is a property.
        
        Args:
            is_property: Whether the method is a property
        """
        self.is_property = is_property
```

## Test Coverage Models

Models related to test coverage analysis and reporting.

### TestCoverage

Represents test coverage metrics for a repository.

```python
class TestCoverage:
    """Represents test coverage metrics for a repository."""
    
    def __init__(self, repository_path: str):
        """Initialize a TestCoverage.
        
        Args:
            repository_path: Path to the repository
        """
        self.repository_path = repository_path
        self.line_coverage: float = 0.0
        self.branch_coverage: float = 0.0
        self.method_coverage: float = 0.0
        self.class_coverage: float = 0.0
        self.module_coverage: Dict[str, ModuleCoverage] = {}
        
    def set_overall_metrics(self, line: float, branch: float, method: float, class_coverage: float) -> None:
        """Set overall coverage metrics.
        
        Args:
            line: Line coverage percentage (0-100)
            branch: Branch coverage percentage (0-100)
            method: Method coverage percentage (0-100)
            class_coverage: Class coverage percentage (0-100)
        """
        self.line_coverage = line
        self.branch_coverage = branch
        self.method_coverage = method
        self.class_coverage = class_coverage
        
    def add_module_coverage(self, module_name: str, coverage: 'ModuleCoverage') -> None:
        """Add coverage data for a module.
        
        Args:
            module_name: Name of the module
            coverage: Coverage data for the module
        """
        self.module_coverage[module_name] = coverage
```

### ModuleCoverage

Represents test coverage metrics for a specific module.

```python
class ModuleCoverage:
    """Represents test coverage metrics for a module."""
    
    def __init__(self, module_name: str):
        """Initialize a ModuleCoverage.
        
        Args:
            module_name: Name of the module
        """
        self.module_name = module_name
        self.line_coverage: float = 0.0
        self.branch_coverage: float = 0.0
        self.covered_lines: List[int] = []
        self.missing_lines: List[int] = []
        self.class_coverage: Dict[str, ClassCoverage] = {}
        self.function_coverage: Dict[str, FunctionCoverage] = {}
        
    def set_metrics(self, line: float, branch: float) -> None:
        """Set coverage metrics.
        
        Args:
            line: Line coverage percentage (0-100)
            branch: Branch coverage percentage (0-100)
        """
        self.line_coverage = line
        self.branch_coverage = branch
        
    def set_line_data(self, covered: List[int], missing: List[int]) -> None:
        """Set line coverage data.
        
        Args:
            covered: List of covered line numbers
            missing: List of missing line numbers
        """
        self.covered_lines = covered
        self.missing_lines = missing
        
    def add_class_coverage(self, class_name: str, coverage: 'ClassCoverage') -> None:
        """Add coverage data for a class.
        
        Args:
            class_name: Name of the class
            coverage: Coverage data for the class
        """
        self.class_coverage[class_name] = coverage
        
    def add_function_coverage(self, function_name: str, coverage: 'FunctionCoverage') -> None:
        """Add coverage data for a function.
        
        Args:
            function_name: Name of the function
            coverage: Coverage data for the function
        """
        self.function_coverage[function_name] = coverage
```

### ClassCoverage and FunctionCoverage

Represent test coverage metrics for classes and functions.

```python
class ClassCoverage:
    """Represents test coverage metrics for a class."""
    
    def __init__(self, class_name: str, module_name: str):
        """Initialize a ClassCoverage.
        
        Args:
            class_name: Name of the class
            module_name: Name of the module containing the class
        """
        self.class_name = class_name
        self.module_name = module_name
        self.line_coverage: float = 0.0
        self.method_coverage: Dict[str, MethodCoverage] = {}
        
    def set_line_coverage(self, coverage: float) -> None:
        """Set line coverage percentage.
        
        Args:
            coverage: Line coverage percentage (0-100)
        """
        self.line_coverage = coverage
        
    def add_method_coverage(self, method_name: str, coverage: 'MethodCoverage') -> None:
        """Add coverage data for a method.
        
        Args:
            method_name: Name of the method
            coverage: Coverage data for the method
        """
        self.method_coverage[method_name] = coverage


class FunctionCoverage:
    """Represents test coverage metrics for a function."""
    
    def __init__(self, function_name: str, module_name: str):
        """Initialize a FunctionCoverage.
        
        Args:
            function_name: Name of the function
            module_name: Name of the module containing the function
        """
        self.function_name = function_name
        self.module_name = module_name
        self.line_coverage: float = 0.0
        self.branch_coverage: float = 0.0
        self.covered_lines: List[int] = []
        self.missing_lines: List[int] = []
        
    def set_metrics(self, line: float, branch: float) -> None:
        """Set coverage metrics.
        
        Args:
            line: Line coverage percentage (0-100)
            branch: Branch coverage percentage (0-100)
        """
        self.line_coverage = line
        self.branch_coverage = branch
        
    def set_line_data(self, covered: List[int], missing: List[int]) -> None:
        """Set line coverage data.
        
        Args:
            covered: List of covered line numbers
            missing: List of missing line numbers
        """
        self.covered_lines = covered
        self.missing_lines = missing


class MethodCoverage(FunctionCoverage):
    """Represents test coverage metrics for a method."""
    
    def __init__(self, method_name: str, module_name: str, class_name: str):
        """Initialize a MethodCoverage.
        
        Args:
            method_name: Name of the method
            module_name: Name of the module containing the method
            class_name: Name of the class containing the method
        """
        super().__init__(method_name, module_name)
        self.class_name = class_name
```

## Test Execution Models

Models related to test execution and validation.

### TestRunResult

Represents the result of a test run, including success status, test count, failures, and coverage data.

```python
class TestRunResult:
    """Represents the result of a test run."""
    
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
        
    def get_failure_count(self) -> int:
        """Get the number of test failures.
        
        Returns:
            Number of test failures
        """
        return len(self.failures)
        
    def has_coverage_data(self) -> bool:
        """Check if coverage data is available.
        
        Returns:
            True if coverage data is available, False otherwise
        """
        return bool(self.coverage_data)
```

### ValidationResult

Contains the results of test validation against best practices.

```python
class ValidationResult:
    """Contains the results of test validation against best practices."""
    
    def __init__(self, file_path: str):
        """Initialize a ValidationResult.
        
        Args:
            file_path: Path to the validated test file
        """
        self.file_path = file_path
        self.test_count: int = 0
        self.passed_validations: int = 0
        self.failed_validations: int = 0
        self.quality_score: float = 0.0
        self.issues: List[ValidationIssue] = []
        
    def add_issue(self, issue: 'ValidationIssue') -> None:
        """Add a validation issue.
        
        Args:
            issue: Validation issue to add
        """
        self.issues.append(issue)
        self.failed_validations += 1
        
    def set_test_count(self, count: int) -> None:
        """Set the number of tests.
        
        Args:
            count: Number of tests
        """
        self.test_count = count
        
    def set_passed_validations(self, count: int) -> None:
        """Set the number of passed validations.
        
        Args:
            count: Number of passed validations
        """
        self.passed_validations = count
        
    def calculate_quality_score(self) -> float:
        """Calculate the quality score.
        
        Returns:
            Quality score between 0.0 and 1.0
        """
        total = self.passed_validations + self.failed_validations
        self.quality_score = self.passed_validations / total if total > 0 else 0.0
        return self.quality_score
```

### ValidationIssue

Represents an issue found during test validation.

```python
class ValidationIssue:
    """Represents an issue found during test validation."""
    
    def __init__(self, test_name: str, issue_type: str, severity: str, 
                 message: str, recommendation: str):
        """Initialize a ValidationIssue.
        
        Args:
            test_name: Name of the test with the issue
            issue_type: Type of the issue
            severity: Severity of the issue (low, medium, high)
            message: Description of the issue
            recommendation: Recommendation to fix the issue
        """
        self.test_name = test_name
        self.issue_type = issue_type
        self.severity = severity
        self.message = message
        self.recommendation = recommendation
```

## Test Generation Models

Models related to test generation and code understanding.

### CodeAnalysis

Represents the analysis of code for test generation.

```python
class CodeAnalysis:
    """Represents the analysis of code for test generation."""
    
    def __init__(self, module_path: str):
        """Initialize a CodeAnalysis.
        
        Args:
            module_path: Path to the analyzed module
        """
        self.module_path = module_path
        self.purpose: str = ""
        self.classes: List[str] = []
        self.functions: List[str] = []
        self.dependencies: List[str] = []
        self.complexity: Dict[str, int] = {}
        
    def set_purpose(self, purpose: str) -> None:
        """Set the purpose of the module.
        
        Args:
            purpose: Purpose description
        """
        self.purpose = purpose
        
    def add_class(self, class_name: str) -> None:
        """Add a class to the analysis.
        
        Args:
            class_name: Name of the class
        """
        self.classes.append(class_name)
        
    def add_function(self, function_name: str) -> None:
        """Add a function to the analysis.
        
        Args:
            function_name: Name of the function
        """
        self.functions.append(function_name)
        
    def add_dependency(self, dependency: str) -> None:
        """Add a dependency to the analysis.
        
        Args:
            dependency: Name of the dependency
        """
        self.dependencies.append(dependency)
        
    def set_complexity(self, entity_name: str, complexity: int) -> None:
        """Set the complexity of an entity.
        
        Args:
            entity_name: Name of the entity (function or class)
            complexity: Cyclomatic complexity
        """
        self.complexity[entity_name] = complexity
```

### MethodAnalysis

Represents the analysis of a method for test generation.

```python
class MethodAnalysis:
    """Represents the analysis of a method for test generation."""
    
    def __init__(self, method_name: str, module_name: str, class_name: Optional[str] = None):
        """Initialize a MethodAnalysis.
        
        Args:
            method_name: Name of the method
            module_name: Name of the module containing the method
            class_name: Optional name of the class containing the method
        """
        self.method_name = method_name
        self.module_name = module_name
        self.class_name = class_name
        self.purpose: str = ""
        self.parameters: List[Dict[str, str]] = []
        self.return_type: Optional[str] = None
        self.exceptions: List[str] = []
        self.complexity: int = 0
        self.test_cases: List[Dict[str, Any]] = []
        
    def set_purpose(self, purpose: str) -> None:
        """Set the purpose of the method.
        
        Args:
            purpose: Purpose description
        """
        self.purpose = purpose
        
    def add_parameter(self, name: str, type_hint: Optional[str] = None, description: Optional[str] = None) -> None:
        """Add a parameter to the method analysis.
        
        Args:
            name: Name of the parameter
            type_hint: Optional type hint for the parameter
            description: Optional description of the parameter
        """
        self.parameters.append({
            'name': name,
            'type': type_hint,
            'description': description
        })
        
    def set_return_type(self, return_type: str) -> None:
        """Set the return type of the method.
        
        Args:
            return_type: Return type as a string
        """
        self.return_type = return_type
        
    def add_exception(self, exception: str) -> None:
        """Add an exception that the method can raise.
        
        Args:
            exception: Name of the exception
        """
        self.exceptions.append(exception)
        
    def set_complexity(self, complexity: int) -> None:
        """Set the cyclomatic complexity of the method.
        
        Args:
            complexity: Cyclomatic complexity
        """
        self.complexity = complexity
        
    def add_test_case(self, inputs: Dict[str, Any], expected_output: Any, description: str) -> None:
        """Add a test case for the method.
        
        Args:
            inputs: Dictionary of input parameter values
            expected_output: Expected output value
            description: Description of the test case
        """
        self.test_cases.append({
            'inputs': inputs,
            'expected_output': expected_output,
            'description': description
        })
```

## Using Data Models

Examples of how to use these data models in the Test Coverage Agent.

### Creating Repository Structure

```python
# Create repository structure
repo_structure = RepositoryStructure("/path/to/repo")

# Add a module
module = ModuleInfo("my_module", "/path/to/repo/my_module.py")

# Add a function to the module
function = FunctionInfo("calculate_total", "my_module")
function.add_parameter("amount")
function.add_parameter("tax_rate")
function.set_return_type("float")
function.set_docstring("Calculate total amount with tax.")
function.set_line_range(10, 15)
module.add_function("calculate_total", function)

# Add a class to the module
class_info = ClassInfo("ShoppingCart", "my_module")
module.add_class("ShoppingCart", class_info)

# Add a method to the class
method = MethodInfo("add_item", "my_module", "ShoppingCart")
method.add_parameter("self")
method.add_parameter("item")
method.add_parameter("price")
method.set_line_range(20, 25)
class_info.add_method("add_item", method)

# Add module to repository structure
repo_structure.add_module("my_module", module)
```

### Creating Test Coverage Data

```python
# Create test coverage
coverage = TestCoverage("/path/to/repo")

# Set overall metrics
coverage.set_overall_metrics(
    line=75.5,
    branch=68.2,
    method=80.0,
    class_coverage=85.0
)

# Create module coverage
module_coverage = ModuleCoverage("my_module")
module_coverage.set_metrics(line=80.0, branch=75.0)
module_coverage.set_line_data(
    covered=[1, 2, 3, 4, 5, 8, 9, 10],
    missing=[6, 7]
)

# Create class coverage
class_coverage = ClassCoverage("ShoppingCart", "my_module")
class_coverage.set_line_coverage(90.0)

# Create method coverage
method_coverage = MethodCoverage("add_item", "my_module", "ShoppingCart")
method_coverage.set_metrics(line=100.0, branch=100.0)
method_coverage.set_line_data(
    covered=[21, 22, 23, 24],
    missing=[]
)

# Add method coverage to class coverage
class_coverage.add_method_coverage("add_item", method_coverage)

# Add class coverage to module coverage
module_coverage.add_class_coverage("ShoppingCart", class_coverage)

# Add module coverage to test coverage
coverage.add_module_coverage("my_module", module_coverage)
```

### Working with Test Run Results

```python
# Create test run result
result = TestRunResult(
    success=False,
    test_count=10,
    failures=[
        {
            'name': 'test_calculate_total',
            'message': 'AssertionError: Expected 110, got 105',
            'traceback': '...'
        }
    ],
    coverage_data={
        'line_coverage': 75.5,
        'branch_coverage': 68.2
    }
)

# Use test run result
if result.success:
    print(f"All {result.test_count} tests passed!")
else:
    print(f"{result.get_failure_count()} of {result.test_count} tests failed.")
    for failure in result.failures:
        print(f"Failed: {failure['name']} - {failure['message']}")

if result.has_coverage_data():
    print(f"Line coverage: {result.coverage_data['line_coverage']}%")
    print(f"Branch coverage: {result.coverage_data['branch_coverage']}%")
```

### Working with Validation Results

```python
# Create validation result
validation = ValidationResult("/path/to/tests/test_module.py")
validation.set_test_count(5)
validation.set_passed_validations(4)

# Add validation issue
issue = ValidationIssue(
    test_name="test_calculate_total",
    issue_type="insufficient_assertions",
    severity="medium",
    message="Test has only one assertion",
    recommendation="Add assertions to verify all aspects of behavior"
)
validation.add_issue(issue)

# Calculate quality score
quality_score = validation.calculate_quality_score()
print(f"Test quality score: {quality_score * 100:.1f}%")

# Process validation issues
for issue in validation.issues:
    print(f"Issue in {issue.test_name}: {issue.message} (Severity: {issue.severity})")
    print(f"Recommendation: {issue.recommendation}")
```