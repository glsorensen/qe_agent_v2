# Test Coverage Enhancement Agent

An AI-powered tool to analyze code repositories, identify test coverage gaps, and generate appropriate test code.

## Features

- Repository scanning and analysis
- Test coverage assessment
- AI-powered test generation
- Test execution and validation
- Coverage reporting

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/test-coverage-agent.git
cd test-coverage-agent

# Install dependencies
pip install -e .
```

## Usage

```bash
# CLI usage
python -m test_coverage_agent.main <repository_path>

# Start web interface
python -m test_coverage_agent.ui.web
```

## Development

```bash
# Run tests
pytest tests/

# Run linting
flake8 test_coverage_agent/ tests/

# Run type checking
mypy test_coverage_agent/ tests/
```

## License

MIT
