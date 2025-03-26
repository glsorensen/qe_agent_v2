# Repository Analysis

The repository analysis module is responsible for scanning a codebase to identify its structure, components, and organization.

## How It Works

The repository analysis process consists of several steps:

1. **Directory Scanning**: The agent recursively traverses the directory structure of the repository
2. **File Classification**: Files are classified as code, test, or auxiliary files based on naming patterns and content
3. **Module Identification**: Python modules and packages are identified and analyzed
4. **Class and Method Extraction**: Classes and methods/functions are extracted and cataloged
5. **Dependency Mapping**: Relationships between modules are mapped to understand the codebase structure

## Key Components

### RepositoryScanner

The `RepositoryScanner` class (found in `repository/scanner.py`) is the primary component responsible for analyzing the structure of a repository. It provides methods to:

- Traverse directory structures
- Identify Python modules
- Extract classes and methods
- Filter files based on patterns

```python
# Example usage of RepositoryScanner
from repository.scanner import RepositoryScanner

scanner = RepositoryScanner("/path/to/repo")
modules = scanner.scan()

# Get all Python files
python_files = scanner.get_python_files()

# Get file structure as a tree
structure = scanner.get_directory_structure()
```

### TestDetector

The `TestDetector` class (found in `repository/test_detector.py`) analyzes the repository to identify test files and their relationships to implementation code. It provides methods to:

- Identify test files based on naming patterns
- Map tests to implementation code
- Calculate basic test coverage metrics

```python
# Example usage of TestDetector
from repository.test_detector import TestDetector

detector = TestDetector("/path/to/repo")
test_files = detector.find_test_files()

# Get mapping of tests to implementation
test_mapping = detector.map_tests_to_implementation()

# Get untested modules
untested = detector.find_untested_modules()
```

## Configuration Options

Repository analysis can be configured with various options:

- **Inclusion/Exclusion Patterns**: Specify patterns to include or exclude certain files or directories
- **Test Naming Patterns**: Customize patterns used to identify test files
- **Depth Limit**: Set a limit on how deep to scan in the directory structure
- **File Type Filtering**: Focus only on specific file types

## Advanced Usage

### Custom File Filters

You can create custom file filters to focus on specific parts of the codebase:

```python
scanner = RepositoryScanner("/path/to/repo")

# Custom filter for only model files
model_files = scanner.filter_files(lambda f: "model" in f or "/models/" in f)

# Custom filter for utility modules
util_files = scanner.filter_files(lambda f: "/utils/" in f or f.endswith("_util.py"))
```

### Analyzing Specific Subdirectories

To focus analysis on specific subdirectories:

```python
# Analyze only the core module
core_scanner = RepositoryScanner("/path/to/repo/core")
core_modules = core_scanner.scan()
```

## Common Issues and Solutions

- **Performance with Large Repositories**: Use inclusion/exclusion patterns to focus on relevant parts
- **Non-Standard Directory Structures**: Configure custom test detection patterns
- **Mixed Language Repositories**: Use file type filtering to focus on Python files
- **Symlinks and Special Files**: Configure to either follow or ignore symbolic links