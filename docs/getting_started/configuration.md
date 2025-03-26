# Configuration Options

The Test Coverage Agent can be configured through command-line arguments or a configuration file.

## Command-Line Arguments

```
usage: python run.py [repository_path] [options]
```

### General Options

- `repository_path`: Path to the repository to analyze
- `--verbose`: Enable verbose output
- `--debug`: Enable debug-level logging
- `--config FILE`: Specify a configuration file
- `--web`: Start the web interface
- `--port PORT`: Specify port for web interface (default: 8000)

### Analysis Options

- `--include MODULES`: Only include specified modules (comma-separated)
- `--exclude MODULES`: Exclude specified modules (comma-separated)
- `--min-coverage PERCENT`: Set minimum coverage threshold (default: 80)
- `--test-pattern PATTERN`: Custom pattern to identify test files

### Output Options

- `--report`: Generate a coverage report
- `--format FORMAT`: Report format (text, html, json, markdown)
- `--output PATH`: Output directory for reports

### Test Generation Options

- `--generate-tests`: Generate tests for untested methods
- `--template TEMPLATE`: Specify test template (standard, minimal, comprehensive)
- `--ai-mode MODE`: AI assistance level (suggest, review, generate)

## Configuration File

You can create a `.test-coverage-agent.yaml` file in your repository root with the following structure:

```yaml
# General settings
verbose: false
test_pattern: "test_*.py"

# Analysis settings
include:
  - core
  - utils
exclude:
  - vendors
  - migrations
min_coverage: 85

# Report settings
report:
  format: html
  output: "./coverage_reports"

# Test generation settings
generation:
  template: standard
  ai_mode: generate
```

## Environment Variables

The following environment variables can be used to configure the agent:

- `TEST_COVERAGE_AGENT_DEBUG`: Set to "true" for debug mode
- `TEST_COVERAGE_AGENT_CONFIG`: Path to configuration file
- `TEST_COVERAGE_AGENT_API_KEY`: API key for AI services (if required)