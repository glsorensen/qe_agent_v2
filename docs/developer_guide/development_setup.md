# Development Setup

This guide will help you set up your development environment for working on the Test Coverage Agent.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: The core programming language used
- **Git**: For version control
- **Pip**: Python package manager
- **virtualenv** or **venv**: For creating isolated Python environments

## Setting up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/test-coverage-agent.git
cd test-coverage-agent
```

### 2. Create and Activate a Virtual Environment

```bash
# Using venv (built into Python 3)
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Development Dependencies

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Development Tools

The project uses several tools to maintain code quality and consistency:

### Code Formatting

We use Black for code formatting, with a line length of 88 characters:

```bash
# Format all files
black test-coverage-agent/ tests/
```

### Linting

We use flake8 for code linting:

```bash
# Run linter
flake8 test-coverage-agent/ tests/
```

### Type Checking

We use mypy for static type checking:

```bash
# Run type checker
mypy test-coverage-agent/ tests/
```

### Testing

We use pytest for running tests:

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/test_repository_scanner.py

# Run a specific test
pytest tests/test_repository_scanner.py::TestRepositoryScanner::test_scan
```

## IDE Setup

### Visual Studio Code

If you're using VS Code, here are recommended settings for your workspace:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": ["tests"]
}
```

Recommended extensions:
- Python (microsoft.python)
- Pylance (ms-python.vscode-pylance)
- Python Test Explorer (littlefoxteam.vscode-python-test-adapter)
- autoDocstring (njpwerner.autodocstring)

### PyCharm

If you're using PyCharm:

1. Open the project in PyCharm
2. Configure the Python interpreter to use your virtual environment
3. Install the following plugins:
   - Black formatter
   - Mypy
   - Flake8 support

## Development Workflow

### 1. Create a Feature Branch

When working on a new feature or bug fix, create a dedicated branch:

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Implement your changes, following the code style guidelines outlined in CLAUDE.md.

### 3. Run Tests

Ensure all tests pass and add new tests for your changes:

```bash
pytest tests/
```

### 4. Run Linters and Formatters

Ensure your code meets style guidelines:

```bash
black test-coverage-agent/ tests/
flake8 test-coverage-agent/ tests/
mypy test-coverage-agent/ tests/
```

### 5. Commit Changes

Commit your changes with a clear message:

```bash
git add .
git commit -m "Add feature: your feature description"
```

### 6. Submit Pull Request

Push your branch and create a pull request:

```bash
git push origin feature/your-feature-name
```

## Troubleshooting Common Setup Issues

### Import Errors

If you're experiencing import errors, ensure:

1. Your virtual environment is activated
2. The package is installed in development mode (`pip install -e .`)
3. Your PYTHONPATH includes the project root directory

### Dependency Conflicts

If you encounter dependency conflicts:

```bash
# Create a clean virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate

# Install dependencies in order
pip install -r requirements.txt
pip install -e .
```

### Test Failures

If tests are failing:

1. Check that all dependencies are installed
2. Run with verbose output to see detailed errors: `pytest -v tests/`
3. Run a specific failing test: `pytest tests/test_file.py::TestClass::test_function -v`