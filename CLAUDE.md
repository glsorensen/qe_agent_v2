# CLAUDE.md - Guidelines for Test Coverage Enhancement Agent

## Commands
- Setup: `pip install -e .` or `python -m pip install -r requirements.txt`
- Run: `python run.py <repository_path>` or `python -m test-coverage-agent.main <repository_path>`
- Web interface: `python run.py --web`
- Lint: `flake8 test-coverage-agent/ tests/`
- Format: `black test-coverage-agent/ tests/`
- Type check: `mypy test-coverage-agent/ tests/`
- Tests: `pytest tests/`
- Single test: `pytest tests/test_file.py::TestClass::test_function -v`

## Code Style Guidelines
- **Formatting**: Black with 88 char line length, 4 spaces for indentation
- **Imports**: Group standard library, third-party, then local imports; sort alphabetically
- **Types**: Type hints required for all functions/methods; use Optional[] for nullable types
- **Naming**: snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Docstrings**: Google style docstrings with Args/Returns sections for all public functions
- **Error Handling**: Use specific exceptions with context in error messages
- **Classes**: Create clear responsibility boundaries between modules/components
- **Testing**: Write tests for all new functionality following existing patterns

## Directory Structure
The project follows a modular structure: repository/, test_generation/, test_execution/, and ui/ modules with clear separation of concerns.