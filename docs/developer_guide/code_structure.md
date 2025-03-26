# Code Structure

This document provides a detailed overview of the Test Coverage Agent's code structure, helping new developers understand the organization and relationships between components.

## Directory Structure

The codebase follows a modular organization:

```
test-coverage-agent/
├── __init__.py                 # Package initialization
├── run.py                      # CLI entry script
├── pyproject.toml              # Project metadata and dependencies
├── requirements.txt            # Dependencies list
│
├── src/                        # Source code directory
│   └── test_coverage_agent/    # Main package
│       ├── __init__.py         # Package initialization
│       ├── main.py             # Entry point
│       │
│       ├── repository/         # Repository analysis components
│       │   ├── __init__.py
│       │   ├── scanner.py      # Repository structure scanner
│       │   ├── test_detector.py # Test file detection
│       │   └── coverage_analyzer.py # Coverage analysis
│       │
│       ├── test_execution/     # Test execution components
│       │   ├── __init__.py
│       │   ├── test_runner.py  # Test execution
│       │   ├── test_validator.py # Test quality validation
│       │   └── coverage_reporter.py # Coverage reporting
│       │
│       ├── test_generation/    # Test generation components
│       │   ├── __init__.py
│       │   ├── code_understanding.py # Code analysis for test generation
│       │   ├── template_manager.py # Test template management
│       │   └── test_writer.py  # AI-powered test generation
│       │
│       └── ui/                 # User interfaces
│           ├── __init__.py
│           ├── cli.py          # Command-line interface
│           ├── cli_for_testing.py # Test-specific CLI version
│           ├── web.py          # Web interface
│           └── web_for_testing.py # Test-specific web version
│
└── tests/                      # Test suite
    ├── __init__.py
    ├── test_repository_scanner.py
    ├── test_test_detector.py
    ├── test_coverage_analyzer.py
    └── ...
```

## Module Dependencies

Here's a diagram of the dependencies between major modules:

```
                  +------+
                  | Main |
                  +------+
                     |
           +---------+---------+
           |                   |
      +----v----+        +-----v----+
      | CLI UI  |        | Web UI   |
      +---------+        +----------+
           |
           v
+---------------------+
| Repository Analysis |
+---------------------+
           |
           v
+---------------------+     +---------------------+
| Coverage Analysis   |---->| Test Execution     |
+---------------------+     +---------------------+
           |                       |
           v                       v
+---------------------+     +---------------------+
| Test Generation     |<----| Coverage Reporting  |
+---------------------+     +---------------------+
```

## Key Files and Their Responsibilities

### Application Entry Points

- **main.py**: Contains the main application logic and orchestrates the workflow between components
- **run.py**: Command-line entry point script that processes arguments and launches the agent

### Repository Analysis

- **repository/scanner.py**: Scans repository structure and identifies Python modules, classes, and methods
- **repository/test_detector.py**: Detects test files and maps them to implementation code
- **repository/coverage_analyzer.py**: Analyzes test coverage and identifies gaps

### Test Execution

- **test_execution/test_runner.py**: Executes tests and collects results
- **test_execution/test_validator.py**: Validates test quality and structure
- **test_execution/coverage_reporter.py**: Generates coverage reports

### Test Generation

- **test_generation/code_understanding.py**: Analyzes code to understand its purpose and behavior
- **test_generation/template_manager.py**: Manages test templates
- **test_generation/test_writer.py**: Generates tests using AI and templates

### User Interfaces

- **ui/cli.py**: Command-line interface implementation
- **ui/web.py**: Web interface implementation

## Class Hierarchy

The project uses a class-based structure with well-defined responsibilities:

### Repository Analysis Classes

```
RepositoryScanner
└── scan() - Scans repository and returns structure
└── get_python_files() - Returns all Python files
└── get_directory_structure() - Returns directory tree

TestDetector
└── find_test_files() - Discovers test files
└── map_tests_to_implementation() - Maps tests to implementations
└── find_untested_modules() - Identifies untested code

CoverageAnalyzer
└── calculate_coverage_metrics() - Calculates coverage metrics
└── find_untested_methods() - Finds methods without tests
└── prioritize_testing_targets() - Ranks code by testing priority
```

### Test Execution Classes

```
TestRunner
└── run_tests() - Executes tests and returns results
└── run_specific_test() - Runs a single test
└── collect_coverage_data() - Collects coverage information

TestValidator
└── validate_test_file() - Validates a single test file
└── validate_test_directory() - Validates all tests in directory
└── calculate_quality_score() - Scores test quality

CoverageReporter
└── generate_summary_report() - Creates a summary report
└── generate_detailed_report() - Creates a detailed report
└── export_report() - Exports report in specified format
```

### Test Generation Classes

```
CodeUnderstandingModule
└── analyze_module() - Analyzes a module's structure and purpose
└── analyze_method() - Analyzes a specific method
└── extract_dependencies() - Identifies dependencies

TemplateManager
└── get_template() - Retrieves a template by name
└── apply_template() - Applies a template with parameters
└── register_template() - Adds a new template

AIPoweredTestWriter
└── generate_function_tests() - Generates tests for a function
└── generate_class_tests() - Generates tests for a class
└── refine_tests() - Improves generated tests
```

### UI Classes

```
CLI
└── parse_arguments() - Processes command-line arguments
└── run() - Executes the requested command
└── display_results() - Shows results to the user

WebUI
└── start_server() - Starts the web server
└── handle_request() - Processes web requests
└── render_dashboard() - Renders the main dashboard
```

## Data Models

The project uses several data models to represent concepts:

- **RepositoryStructure**: Represents the structure of a repository
- **TestCoverage**: Contains coverage metrics and information
- **TestResult**: Represents the result of test execution
- **ValidationResult**: Contains test validation information
- **CodeAnalysis**: Represents analysis of code for test generation

## Extension Points

The codebase includes several extension points where functionality can be added without modifying existing code:

- **Template System**: Test templates can be added in `test_generation/template_manager.py`
- **Validation Rules**: New validation rules can be added in `test_execution/test_validator.py`
- **Reporters**: Custom report formats can be added in `test_execution/coverage_reporter.py`
- **Analyzers**: Specialized analyzers can be added to the repository module

## Configuration Management

Configuration is managed through:

- **Command-line arguments**: Processed in `ui/cli.py`
- **Configuration files**: YAML configuration files
- **Environment variables**: For sensitive or environment-specific settings

The configuration system follows a layered approach, with command-line arguments taking precedence over configuration files, which take precedence over environment variables and defaults.