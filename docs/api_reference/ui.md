# UI Module API

The UI module provides command-line and web interfaces for interacting with the Test Coverage Agent.

## CLI

```python
from ui.cli import CLI
```

The `CLI` class implements the command-line interface for the Test Coverage Agent.

### Constructor

```python
def __init__(self):
    """Initialize the CLI with argument parser."""
```

### Methods

#### parse_arguments

```python
def parse_arguments(self, args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: Command-line arguments to parse. If None, use sys.argv.

    Returns:
        Parsed arguments as a Namespace object
    """
```

Parses command-line arguments and returns the parsed arguments.

#### run

```python
def run(self) -> None:
    """Run the CLI with the provided arguments."""
```

Runs the CLI with the provided arguments, executing the requested commands.

#### display_results

```python
def display_results(self, results: Dict[str, Any]) -> None:
    """Display results to the user.

    Args:
        results: Results to display
    """
```

Displays results to the user in the console.

### Example Usage

```python
# Initialize CLI
cli = CLI()

# Parse specific arguments
args = cli.parse_arguments(["--web", "--port", "8080"])

# Run with parsed arguments
cli.run()

# Or run directly with defaults
cli = CLI()
cli.run()  # Uses sys.argv

# Display custom results
results = {
    "coverage": {
        "line": 75.5,
        "branch": 68.2,
        "method": 80.0
    },
    "untested_modules": ["module1.py", "module2.py"],
    "recommendations": ["Add tests for module1.py", "Improve branch coverage"]
}
cli.display_results(results)
```

## WebUI

```python
from ui.web import WebUI
```

The `WebUI` class implements a web-based interface for the Test Coverage Agent.

### Constructor

```python
def __init__(self, host: str = "localhost", port: int = 8000):
    """Initialize the WebUI.

    Args:
        host: Host to bind the web server to
        port: Port to bind the web server to
    """
```

### Methods

#### start_server

```python
def start_server(self, debug: bool = False) -> None:
    """Start the web server.

    Args:
        debug: Whether to run in debug mode
    """
```

Starts the web server to serve the UI.

#### handle_request

```python
def handle_request(self, path: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a request from the web interface.

    Args:
        path: Request path
        request_data: Request data

    Returns:
        Response data
    """
```

Handles a request from the web interface and returns the response data.

#### render_dashboard

```python
def render_dashboard(self, repository_path: str) -> str:
    """Render the main dashboard page.

    Args:
        repository_path: Path to the repository to show in the dashboard

    Returns:
        HTML content for the dashboard
    """
```

Renders the main dashboard page for a repository.

### Example Usage

```python
# Initialize WebUI
web_ui = WebUI(host="0.0.0.0", port=8080)

# Start the server
web_ui.start_server(debug=True)

# Handle a request manually (usually done by the web framework)
response = web_ui.handle_request(
    path="/analyze",
    request_data={"repository_path": "/path/to/repo"}
)

# Render dashboard manually (usually done by the web framework)
dashboard_html = web_ui.render_dashboard("/path/to/repo")
```

## CLI and Web Interface Integration

```python
from test_coverage_agent import TestCoverageAgent
from ui.cli import CLI
from ui.web import WebUI
```

The Test Coverage Agent integrates with both UI components to provide a unified experience.

### Command-Line Interface Integration

```python
# Initialize agent
agent = TestCoverageAgent()

# Create CLI
cli = CLI()

# Set up CLI to use agent
cli.set_agent(agent)

# Run CLI
cli.run()
```

### Web Interface Integration

```python
# Initialize agent
agent = TestCoverageAgent()

# Create WebUI
web_ui = WebUI()

# Set up WebUI to use agent
web_ui.set_agent(agent)

# Start web server
web_ui.start_server()
```

### Combined Interface

```python
# Initialize agent
agent = TestCoverageAgent()

# Check if web interface is requested
if "--web" in sys.argv:
    # Create and start web interface
    web_ui = WebUI()
    web_ui.set_agent(agent)
    web_ui.start_server()
else:
    # Create and run CLI
    cli = CLI()
    cli.set_agent(agent)
    cli.run()
```

## Special Testing Interfaces

The UI module also includes special versions of the interfaces for testing purposes.

### CLIForTesting

```python
from ui.cli_for_testing import CLIForTesting
```

A version of the CLI designed for use in tests, with methods to simulate user input and capture output.

### WebUIForTesting

```python
from ui.web_for_testing import WebUIForTesting
```

A version of the WebUI designed for use in tests, with methods to simulate web requests and responses without starting an actual server.

### Example Testing Usage

```python
# Test the CLI
test_cli = CLIForTesting()
test_cli.set_input(["--analyze", "/path/to/repo"])
test_cli.run()
output = test_cli.get_output()
assert "Coverage: 80%" in output

# Test the WebUI
test_web = WebUIForTesting()
response = test_web.simulate_request("/analyze", {"repository_path": "/path/to/repo"})
assert response["status"] == "success"
assert "coverage" in response["data"]
```