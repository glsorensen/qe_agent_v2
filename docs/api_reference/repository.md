# Repository Module API

The Repository module provides components for analyzing repository structure, detecting tests, and calculating coverage metrics.

## RepositoryScanner

```python
from repository.scanner import RepositoryScanner
```

The `RepositoryScanner` class scans a repository to identify its structure, including files, modules, classes, and methods.

### Constructor

```python
def __init__(self, repository_path: str):
    """Initialize a RepositoryScanner.

    Args:
        repository_path: Path to the repository to scan
    """
```

### Methods

#### scan

```python
def scan(self) -> Dict[str, Any]:
    """Scan the repository and return its structure.

    Returns:
        Dict containing the repository structure
    """
```

Performs a full scan of the repository and returns a dictionary representing its structure.

#### get_python_files

```python
def get_python_files(self) -> List[str]:
    """Get all Python files in the repository.

    Returns:
        List of paths to Python files
    """
```

Returns a list of all Python files in the repository.

#### get_directory_structure

```python
def get_directory_structure(self) -> Dict[str, Any]:
    """Get the directory structure as a tree.

    Returns:
        Dict representing the directory tree
    """
```

Returns a dictionary representing the directory structure as a nested tree.

#### filter_files

```python
def filter_files(self, filter_func: Callable[[str], bool]) -> List[str]:
    """Filter files using a custom function.

    Args:
        filter_func: Function that takes a file path and returns bool

    Returns:
        List of file paths that match the filter
    """
```

Filters files using a custom function that takes a file path and returns a boolean.

### Example Usage

```python
# Initialize scanner
scanner = RepositoryScanner("/path/to/repo")

# Get all Python files
python_files = scanner.get_python_files()

# Get directory structure
structure = scanner.get_directory_structure()

# Filter for model files
model_files = scanner.filter_files(lambda f: "model" in f or "/models/" in f)

# Get full repository structure
repo_structure = scanner.scan()
```

## TestDetector

```python
from repository.test_detector import TestDetector
```

The `TestDetector` class identifies test files and maps them to their corresponding implementation files.

### Constructor

```python
def __init__(self, repository_path: str, test_pattern: str = "test_*.py"):
    """Initialize a TestDetector.

    Args:
        repository_path: Path to the repository
        test_pattern: Glob pattern to identify test files
    """
```

### Methods

#### find_test_files

```python
def find_test_files(self) -> List[str]:
    """Find all test files in the repository.

    Returns:
        List of paths to test files
    """
```

Identifies and returns a list of all test files in the repository.

#### map_tests_to_implementation

```python
def map_tests_to_implementation(self) -> Dict[str, str]:
    """Map test files to their implementation files.

    Returns:
        Dict mapping test file paths to implementation file paths
    """
```

Returns a dictionary mapping test files to their corresponding implementation files.

#### find_untested_modules

```python
def find_untested_modules(self) -> List[str]:
    """Find modules that don't have corresponding tests.

    Returns:
        List of paths to untested modules
    """
```

Identifies and returns a list of modules that don't have corresponding tests.

#### add_custom_mapping

```python
def add_custom_mapping(self, test_file: str, implementation_file: str) -> None:
    """Add a custom mapping between test and implementation files.

    Args:
        test_file: Path to the test file
        implementation_file: Path to the implementation file
    """
```

Adds a custom mapping between a test file and an implementation file.

### Example Usage

```python
# Initialize detector
detector = TestDetector("/path/to/repo")

# Find all test files
test_files = detector.find_test_files()

# Map tests to implementation
mapping = detector.map_tests_to_implementation()

# Find untested modules
untested = detector.find_untested_modules()

# Add custom mapping
detector.add_custom_mapping(
    "tests/special_case_test.py",
    "src/deeply/nested/special_case.py"
)
```

## CoverageAnalyzer

```python
from repository.coverage_analyzer import CoverageAnalyzer
```

The `CoverageAnalyzer` class analyzes test coverage and identifies gaps in testing.

### Constructor

```python
def __init__(self, repository_path: str):
    """Initialize a CoverageAnalyzer.

    Args:
        repository_path: Path to the repository
    """
```

### Methods

#### calculate_coverage_metrics

```python
def calculate_coverage_metrics(self) -> Dict[str, Any]:
    """Calculate coverage metrics for the repository.

    Returns:
        Dict containing coverage metrics
    """
```

Calculates and returns coverage metrics for the repository.

#### find_untested_methods

```python
def find_untested_methods(self) -> List[Dict[str, str]]:
    """Find methods and functions that don't have tests.

    Returns:
        List of dicts with 'module', 'class', and 'method' keys
    """
```

Identifies and returns a list of methods and functions that don't have tests.

#### prioritize_testing_targets

```python
def prioritize_testing_targets(self) -> List[Dict[str, Any]]:
    """Rank untested code components by priority for testing.

    Returns:
        List of dicts with component info and priority score
    """
```

Ranks untested code components by priority for testing, considering factors like complexity and importance.

#### calculate_weighted_coverage

```python
def calculate_weighted_coverage(self) -> float:
    """Calculate coverage weighted by component complexity.

    Returns:
        Weighted coverage percentage
    """
```

Calculates coverage weighted by component complexity, giving more importance to complex code.

### Example Usage

```python
# Initialize analyzer
analyzer = CoverageAnalyzer("/path/to/repo")

# Get coverage metrics
coverage = analyzer.calculate_coverage_metrics()

# Find untested methods
untested_methods = analyzer.find_untested_methods()

# Get prioritized list of components to test
priorities = analyzer.prioritize_testing_targets()

# Get complexity-weighted coverage
weighted_coverage = analyzer.calculate_weighted_coverage()
```