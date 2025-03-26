# Example Usage

This page provides practical examples of using the Test Coverage Agent in various scenarios.

## Basic Repository Analysis

```bash
# Analyze a local repository
python run.py /path/to/your/project

# Analyze with verbose output
python run.py /path/to/your/project --verbose
```

## Generating Test Reports

```bash
# Generate a comprehensive test coverage report
python run.py /path/to/your/project --report

# Generate a report in specific format
python run.py /path/to/your/project --report --format html
```

## Focusing on Specific Modules

```bash
# Analyze only specific modules or packages
python run.py /path/to/your/project --include core,utils

# Exclude certain modules from analysis
python run.py /path/to/your/project --exclude tests,vendors
```

## AI-Powered Test Generation

```bash
# Generate tests for untested methods
python run.py /path/to/your/project --generate-tests

# Generate tests with specific template
python run.py /path/to/your/project --generate-tests --template standard
```

## Web Interface Features

Start the web interface:

```bash
python run.py --web
```

You can also specify a repository path, but it's optional since you can provide it in the web interface:

```bash
python run.py --web /path/to/your/project
```

The web interface provides:

- Repository overview dashboard
- Visual test coverage metrics
- Interactive test generation
- Detailed method-level coverage views
- Export options for reports