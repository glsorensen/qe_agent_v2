# 🧪 Test Coverage Enhancement Agent

<div align="center">

![Test Coverage](https://img.shields.io/badge/Test%20Coverage-Enhanced-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

An AI-powered tool that intelligently analyzes code repositories, identifies test coverage gaps, and automatically generates high-quality tests to improve coverage.

## ✨ Features

- 🔍 **Smart Repository Scanning** - Automatically analyzes codebases in multiple languages
- 🔬 **Framework Detection** - Identifies testing frameworks and patterns in your code
- 📊 **Coverage Analysis** - Pinpoints untested code and prioritizes what to test next
- 🤖 **AI-Powered Test Generation** - Creates meaningful tests with proper assertions
- ✅ **Test Validation** - Ensures generated tests are correct and comprehensive
- 📈 **Detailed Reporting** - Provides metrics and insights about test coverage
- 🖥️ **Multiple Interfaces** - Choose between CLI or web interface based on your needs

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/test-coverage-agent.git
cd test-coverage-agent

# Install dependencies
pip install -r requirements.txt

# Run the tool on a repository
python run.py /path/to/your/repo
```

## 📊 Usage Examples

### Command Line Interface

```bash
# Analyze a repository
python run.py /path/to/repo

# Run with web interface
python run.py --web

# Generate tests
python run.py /path/to/repo --generate --api-key YOUR_ANTHROPIC_API_KEY
```

### Web Interface

```bash
# Start the web server
python run.py --web

# Optionally specify a repository path 
python run.py --web /path/to/your/repo

# Then open http://localhost:8501 in your browser
```

## 📝 How It Works

1. **Repository Scanning**: The agent first scans your repository to identify source files and existing tests.
2. **Test Detection**: It detects testing frameworks and analyzes the current test structure.
3. **Coverage Analysis**: The agent runs coverage tools to identify untested code.
4. **Test Generation**: Using AI, the agent generates comprehensive tests for uncovered code.
5. **Validation**: Generated tests are validated to ensure they run correctly.
6. **Reporting**: A detailed report is generated showing coverage improvements.

## 🛠️ Development

```bash
# Setup development environment
pip install -e .

# Run tests
pytest tests/

# Run linting
flake8 .

# Run type checking
mypy .
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory and can be viewed as a static site using MkDocs:

```bash
# Install MkDocs
pip install mkdocs

# Build the documentation
mkdocs build

# Serve the documentation locally (with live reloading)
mkdocs serve
```

Then open http://localhost:8000 in your browser to view the documentation.

Documentation structure:

- **Getting Started**: Installation, basic usage, and quick examples
- **User Guide**: Detailed explanations of features and use cases
- **Developer Guide**: Contributing, architecture, and design decisions
- **API Reference**: Detailed documentation for all modules and classes

Code organization:

- `repository/`: Modules for scanning and analyzing repositories
- `test_execution/`: Tools for running and validating tests
- `test_generation/`: AI-powered test generation components
- `ui/`: Command line and web interfaces

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.