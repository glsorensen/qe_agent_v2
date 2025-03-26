# Getting Started

This guide will help you quickly install and start using the Test Coverage Agent.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Install from Source

Clone the repository and install using pip:

```bash
# Clone the repository
git clone https://github.com/yourusername/test-coverage-agent.git
cd test-coverage-agent

# Install in development mode
pip install -e .
```

Alternatively, you can install the required dependencies directly:

```bash
python -m pip install -r requirements.txt
```

## Quick Start

### Analyzing a Repository

To analyze a repository for test coverage:

```bash
python run.py /path/to/your/repository
```

### Using the Web Interface

For a visual interface to analyze and view test coverage:

```bash
python run.py --web
```

Then open your browser and navigate to `http://localhost:8000`.

## Next Steps

- Check the [User Guide](../user_guide/index.md) for detailed information on all features
- View [Example Usage](./examples.md) for common scenarios
- Learn about [Configuration Options](./configuration.md) to customize the agent's behavior