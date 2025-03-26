# API Reference

This section provides detailed documentation for all modules and classes in the Test Coverage Agent.

## Core Modules

- [Repository Module](./repository.md) - Components for repository scanning and analysis
- [Test Execution Module](./test_execution.md) - Components for running and validating tests
- [Test Generation Module](./test_generation.md) - Components for generating tests
- [UI Module](./ui.md) - User interface components

## Data Models

- [Data Models](./data_models.md) - Key data structures used throughout the application

## Extending the API

- [Extension API](./extension_api.md) - APIs for extending the agent with plugins

## Using the API Programmatically

The Test Coverage Agent can be used as a library in your own Python code. Here's a simple example of using the API programmatically:

```python
from test_coverage_agent import TestCoverageAgent
from repository.scanner import RepositoryScanner
from repository.test_detector import TestDetector
from repository.coverage_analyzer import CoverageAnalyzer
from test_execution.coverage_reporter import CoverageReporter

# Initialize the main agent
agent = TestCoverageAgent("/path/to/repository")

# Or use individual components
scanner = RepositoryScanner("/path/to/repository")
detector = TestDetector("/path/to/repository")
analyzer = CoverageAnalyzer("/path/to/repository")
reporter = CoverageReporter("/path/to/repository")

# Scan repository structure
structure = scanner.scan()

# Find test files
test_files = detector.find_test_files()

# Calculate coverage metrics
coverage = analyzer.calculate_coverage_metrics()

# Generate coverage report
report = reporter.generate_summary_report()

# Print report
print(report)
```

## API Versioning

The Test Coverage Agent follows semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR version increments for incompatible API changes
- MINOR version increments for functionality added in a backward-compatible manner
- PATCH version increments for backward-compatible bug fixes

You can check the current version with:

```python
from test_coverage_agent import __version__
print(__version__)
```