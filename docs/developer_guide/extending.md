# Extending the Agent

This guide explains how to extend the Test Coverage Agent with custom components and plugins. The agent is designed with extensibility in mind, allowing you to add new functionality without modifying the core codebase.

## Extension Points

The Test Coverage Agent provides several key extension points:

1. **LLM Providers**: Add support for additional language model providers
2. **Test Templates**: Add custom templates for generating tests
3. **Validation Rules**: Define custom rules for validating test quality
4. **Report Formats**: Add new formats for coverage reports
5. **Analyzers**: Create specialized code analyzers
6. **UI Extensions**: Extend the CLI or web interfaces

## Adding a New LLM Provider

The agent uses an abstraction layer for LLM providers, making it easy to add support for new models. Follow these steps to add a new provider:

### 1. Create a New Provider Class

Add a new class in `src/test_coverage_agent/test_generation/llm_provider.py` that inherits from the `LLMProvider` abstract base class:

```python
class NewProvider(LLMProvider):
    """New LLM provider implementation."""
    
    def __init__(self, api_key: str, model_name: str = "model-name", temperature: float = 0.2):
        """Initialize the new provider.
        
        Args:
            api_key: Provider API key
            model_name: Model name to use
            temperature: Temperature parameter for generation
        """
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self._model = None
    
    def get_model(self) -> BaseChatModel:
        """Get the model instance.
        
        Returns:
            An instance of the model
        """
        if self._model is None:
            from new_provider_library import ChatModel
            self._model = ChatModel(
                api_key=self.api_key,
                model=self.model_name,
                temperature=self.temperature
            )
        return self._model
    
    def get_name(self) -> str:
        """Get the name of the provider.
        
        Returns:
            Provider name as a string
        """
        return "new_provider"
```

### 2. Update the Factory Class

Modify the `LLMProviderFactory.create_provider` method to support your new provider:

```python
@staticmethod
def create_provider(provider_name: str, api_key: str, **kwargs) -> LLMProvider:
    """Create an LLM provider instance based on name."""
    if provider_name.lower() == "claude":
        return ClaudeProvider(api_key, **kwargs)
    elif provider_name.lower() == "gemini":
        return GeminiProvider(api_key, **kwargs)
    elif provider_name.lower() == "new_provider":
        return NewProvider(api_key, **kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
```

### 3. Add Dependencies

Update `pyproject.toml` and `requirements.txt` to include the necessary libraries for your provider:

```toml
# In pyproject.toml
dependencies = [
    # ... existing dependencies
    "new-provider-library>=1.0.0",
]
```

### 4. Update CLI and Web Interface

Modify the CLI and web interface to include your new provider as an option:

```python
# In src/test_coverage_agent/main.py
parser.add_argument(
    "--llm-provider", "-p",
    choices=["claude", "gemini", "new_provider"],
    default="claude",
    help="LLM provider to use for test generation"
)
```

### 5. Add Documentation

Document your new provider in `docs/user_guide/llm_providers.md`.

### 6. Write Tests

Create tests for your new provider in `tests/test_llm_provider.py`.

## Adding Custom Test Templates

Test templates define the structure and patterns for generated tests. You can add custom templates for specific testing scenarios.

### Template Structure

Templates are stored in the `TemplateManager` class in `test_generation/template_manager.py`. Each template is a string with placeholders for variable content.

### Registering a Custom Template

```python
from test_generation.template_manager import TemplateManager

def register_custom_templates():
    template_manager = TemplateManager()
    
    # Register a custom template for API testing
    template_manager.register_template(
        name="api_endpoint_test",
        template="""import requests
        
def test_{endpoint_name}_{scenario}():
    # Arrange
    url = "{base_url}/{endpoint_path}"
    headers = {headers}
    payload = {payload}
    
    # Act
    response = requests.{http_method}(url, json=payload, headers=headers)
    
    # Assert
    assert response.status_code == {expected_status}
    {additional_assertions}
"""
    )
    
    # Register a custom template for database testing
    template_manager.register_template(
        name="database_test",
        template="""import pytest
from unittest.mock import patch

def test_{function_name}_{scenario}():
    # Arrange
    mock_db = patch('{module_name}.get_db_connection').start()
    mock_db.execute.return_value = {mock_return_value}
    
    # Act
    result = {function_name}({parameters})
    
    # Assert
    assert mock_db.execute.called_with({expected_query})
    assert result == {expected_result}
    
    # Cleanup
    patch.stopall()
"""
    )
    
    return template_manager
```

### Using Custom Templates

```python
template_manager = register_custom_templates()

# Apply the API endpoint test template
api_test = template_manager.apply_template(
    template_name="api_endpoint_test",
    endpoint_name="get_user",
    scenario="returns_user_details",
    base_url="https://api.example.com",
    endpoint_path="users/{id}",
    http_method="get",
    headers="{\"Authorization\": \"Bearer token\"}",
    payload="{\"id\": 123}",
    expected_status=200,
    additional_assertions="assert response.json()[\"name\"] == \"Test User\""
)

# Write the test to a file
with open("tests/test_api.py", "w") as f:
    f.write(api_test)
```

## Creating Custom Validation Rules

Validation rules check test quality against specific criteria. You can add custom rules for project-specific requirements.

### Validation Rule Structure

Validation rules are classes that implement a `validate` method. They're used by the `TestValidator` class in `test_execution/test_validator.py`.

### Implementing a Custom Rule

```python
from test_execution.test_validator import ValidationRule, TestValidator

class DatabaseTransactionRule(ValidationRule):
    """Rule that checks if database tests use transaction rollback."""
    
    def validate(self, test_content, test_name=None, file_path=None):
        """Validate that database tests properly use transaction rollback.
        
        Args:
            test_content (str): The content of the test
            test_name (str, optional): The name of the test function/method
            file_path (str, optional): Path to the test file
            
        Returns:
            dict: Result with keys for result, issue_type, severity, message, and recommendation
        """
        if "database" in test_content.lower() or "db" in test_content.lower():
            if "transaction" not in test_content.lower() and "rollback" not in test_content.lower():
                return {
                    "result": False,
                    "issue_type": "missing_transaction_rollback",
                    "severity": "medium",
                    "message": f"Test '{test_name}' uses database but doesn't use transaction rollback",
                    "recommendation": "Add transaction setup and rollback to prevent test data persistence"
                }
        
        # Return success if rule doesn't apply or passes
        return {"result": True}

class AsyncTestRule(ValidationRule):
    """Rule that checks if async tests use proper async/await syntax."""
    
    def validate(self, test_content, test_name=None, file_path=None):
        if "async def test_" in test_content:
            if "await" not in test_content:
                return {
                    "result": False,
                    "issue_type": "async_test_missing_await",
                    "severity": "high",
                    "message": f"Async test '{test_name}' doesn't use 'await'",
                    "recommendation": "Use 'await' with async calls to ensure proper test execution"
                }
        
        return {"result": True}
```

### Registering and Using Custom Rules

```python
# Create validator with custom rules
validator = TestValidator()
validator.add_validation_rule(DatabaseTransactionRule())
validator.add_validation_rule(AsyncTestRule())

# Validate tests with custom rules
results = validator.validate_test_file("tests/test_database.py")

# Process validation results
for issue in results["issues"]:
    print(f"Issue: {issue['message']}")
    print(f"Recommendation: {issue['recommendation']}")
```

## Adding Custom Report Formats

You can extend the reporting system with custom formats for different needs.

### Implementing a Custom Reporter

Custom reporters are added to the `CoverageReporter` class in `test_execution/coverage_reporter.py`.

```python
from test_execution.coverage_reporter import CoverageReporter

class CustomCoverageReporter(CoverageReporter):
    def __init__(self, repository_path):
        super().__init__(repository_path)
        
    def generate_custom_format(self, format_name, output_path=None):
        """Generate a custom format report.
        
        Args:
            format_name (str): The name of the custom format (e.g., 'xml', 'custom_html')
            output_path (str, optional): Path to write the report
            
        Returns:
            str: The generated report content
        """
        # Get coverage data
        coverage_data = self._collect_coverage_data()
        
        if format_name == "xml":
            return self._generate_xml_report(coverage_data, output_path)
        elif format_name == "custom_html":
            return self._generate_custom_html_report(coverage_data, output_path)
        else:
            raise ValueError(f"Unknown format: {format_name}")
    
    def _generate_xml_report(self, coverage_data, output_path=None):
        """Generate an XML format report."""
        # XML generation logic here
        xml_content = "<coverage>\n"
        
        for module, data in coverage_data.items():
            xml_content += f"  <module name=\"{module}\" coverage=\"{data['coverage']}\" />\n"
        
        xml_content += "</coverage>"
        
        if output_path:
            with open(output_path, "w") as f:
                f.write(xml_content)
        
        return xml_content
    
    def _generate_custom_html_report(self, coverage_data, output_path=None):
        """Generate a custom HTML report."""
        # Custom HTML generation logic here
        html_content = "<!DOCTYPE html>\n<html>\n<head>\n"
        html_content += "  <title>Custom Coverage Report</title>\n"
        html_content += "  <style>/* Custom CSS here */</style>\n"
        html_content += "</head>\n<body>\n"
        
        # Add content
        html_content += "  <h1>Custom Coverage Report</h1>\n"
        html_content += "  <table>\n"
        
        for module, data in coverage_data.items():
            html_content += f"    <tr><td>{module}</td><td>{data['coverage']}%</td></tr>\n"
        
        html_content += "  </table>\n"
        html_content += "</body>\n</html>"
        
        if output_path:
            with open(output_path, "w") as f:
                f.write(html_content)
        
        return html_content
```

### Using Custom Reporters

```python
# Create custom reporter
reporter = CustomCoverageReporter("/path/to/repo")

# Generate XML report
xml_report = reporter.generate_custom_format("xml", output_path="coverage.xml")

# Generate custom HTML report
html_report = reporter.generate_custom_format("custom_html", output_path="custom_coverage.html")
```

## Creating Custom Analyzers

You can create specialized analyzers for specific code patterns or project-specific analysis.

### Implementing a Custom Analyzer

```python
import re
from repository.scanner import RepositoryScanner

class SecurityAnalyzer:
    """Analyzer that checks for security issues in code."""
    
    def __init__(self, repository_path):
        self.repository_path = repository_path
        self.scanner = RepositoryScanner(repository_path)
    
    def scan_for_security_issues(self):
        """Scan repository for potential security issues.
        
        Returns:
            dict: Security issues found in the codebase
        """
        python_files = self.scanner.get_python_files()
        security_issues = []
        
        for file_path in python_files:
            with open(file_path, "r") as f:
                content = f.read()
                
                # Check for hardcoded secrets
                if self._check_for_hardcoded_secrets(content):
                    security_issues.append({
                        "file": file_path,
                        "issue_type": "hardcoded_secret",
                        "severity": "high"
                    })
                
                # Check for SQL injection vulnerabilities
                if self._check_for_sql_injection(content):
                    security_issues.append({
                        "file": file_path,
                        "issue_type": "sql_injection",
                        "severity": "high"
                    })
                
                # Check for other security issues
                # ...
        
        return security_issues
    
    def _check_for_hardcoded_secrets(self, content):
        """Check for hardcoded secrets like passwords or API keys."""
        patterns = [
            r"password\s*=\s*[\'\"]\w+[\'\"]\s*",
            r"api_key\s*=\s*[\'\"]\w+[\'\"]\s*",
            r"secret\s*=\s*[\'\"]\w+[\'\"]\s*"
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _check_for_sql_injection(self, content):
        """Check for potential SQL injection vulnerabilities."""
        # Look for string concatenation with SQL queries
        patterns = [
            r"execute\s*\(\s*[\'\"]SELECT.*?\%s",
            r"execute\s*\(\s*[\'\"]INSERT.*?\%s",
            r"execute\s*\(\s*[\'\"]UPDATE.*?\%s",
            r"execute\s*\(\s*[\'\"]DELETE.*?\%s",
            r"execute\s*\(\s*[\'\"].*?\"\\s*\\+\\s*\""
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
```

### Using Custom Analyzers

```python
# Create security analyzer
security_analyzer = SecurityAnalyzer("/path/to/repo")

# Scan for security issues
security_issues = security_analyzer.scan_for_security_issues()

# Print security issues
for issue in security_issues:
    print(f"Security issue found in {issue['file']}: {issue['issue_type']} (Severity: {issue['severity']})")
```

## Extending the UI

You can extend both the CLI and web interfaces to add new commands and views.

### Adding CLI Commands

Extend the CLI by adding new commands to the `CLI` class in `ui/cli.py`.

```python
from ui.cli import CLI

class ExtendedCLI(CLI):
    def __init__(self):
        super().__init__()
        self._register_custom_commands()
    
    def _register_custom_commands(self):
        """Register custom CLI commands."""
        self.parser.add_argument(
            "--security-scan",
            action="store_true",
            help="Scan repository for security issues"
        )
        
        self.parser.add_argument(
            "--export-format",
            choices=["json", "html", "xml", "custom_html"],
            help="Export format for reports"
        )
    
    def run(self):
        """Run the CLI with extended commands."""
        args = self.parser.parse_args()
        
        # Handle custom commands
        if args.security_scan:
            self._run_security_scan(args)
        else:
            # Run standard commands
            super().run()
    
    def _run_security_scan(self, args):
        """Run a security scan on the repository."""
        from my_custom_module import SecurityAnalyzer
        
        print("Running security scan...")
        security_analyzer = SecurityAnalyzer(args.repository_path)
        security_issues = security_analyzer.scan_for_security_issues()
        
        if security_issues:
            print(f"Found {len(security_issues)} security issues:")
            for issue in security_issues:
                print(f"- {issue['file']}: {issue['issue_type']} (Severity: {issue['severity']})")
        else:
            print("No security issues found.")
```

### Adding Web UI Components

Extend the web interface by adding new routes and views.

```python
from ui.web import WebUI
import flask

class ExtendedWebUI(WebUI):
    def __init__(self):
        super().__init__()
        self._register_custom_routes()
    
    def _register_custom_routes(self):
        """Register custom web routes."""
        @self.app.route("/security-scan")
        def security_scan():
            from my_custom_module import SecurityAnalyzer
            
            repository_path = flask.request.args.get("repository", self.current_repository)
            security_analyzer = SecurityAnalyzer(repository_path)
            security_issues = security_analyzer.scan_for_security_issues()
            
            return flask.render_template(
                "security_scan.html",
                repository=repository_path,
                issues=security_issues
            )
        
        @self.app.route("/custom-report")
        def custom_report():
            from test_execution.coverage_reporter import CustomCoverageReporter
            
            repository_path = flask.request.args.get("repository", self.current_repository)
            format_type = flask.request.args.get("format", "custom_html")
            
            reporter = CustomCoverageReporter(repository_path)
            report_content = reporter.generate_custom_format(format_type)
            
            return flask.render_template(
                "custom_report.html",
                repository=repository_path,
                report=report_content
            )
```

## Creating Extension Plugins

For more complex extensions, you can create plugin packages that integrate with the Test Coverage Agent.

### Plugin Structure

```
my_coverage_plugin/
├── __init__.py
├── templates/
│   ├── custom_test_template.py.j2
│   └── custom_report_template.html.j2
├── rules/
│   ├── __init__.py
│   └── custom_validation_rules.py
├── analyzers/
│   ├── __init__.py
│   └── security_analyzer.py
└── ui/
    ├── __init__.py
    ├── cli_extension.py
    └── web_extension.py
```

### Plugin Registration

In the plugin's `__init__.py`:

```python
from .rules.custom_validation_rules import DatabaseTransactionRule, AsyncTestRule
from .analyzers.security_analyzer import SecurityAnalyzer

class TestCoverageAgentPlugin:
    """Plugin for Test Coverage Agent."""
    
    def __init__(self):
        self.name = "my_coverage_plugin"
        self.version = "1.0.0"
    
    def register(self, agent):
        """Register this plugin with the Test Coverage Agent.
        
        Args:
            agent: The TestCoverageAgent instance
        """
        # Register templates
        self._register_templates(agent)
        
        # Register validation rules
        self._register_validation_rules(agent)
        
        # Register analyzers
        self._register_analyzers(agent)
        
        # Register UI extensions
        self._register_ui_extensions(agent)
    
    def _register_templates(self, agent):
        """Register custom templates."""
        template_manager = agent.get_template_manager()
        
        # Register templates from file
        import os
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        with open(os.path.join(template_dir, "custom_test_template.py.j2"), "r") as f:
            template_content = f.read()
            template_manager.register_template(
                name="custom_plugin_template",
                template=template_content
            )
    
    def _register_validation_rules(self, agent):
        """Register custom validation rules."""
        validator = agent.get_test_validator()
        validator.add_validation_rule(DatabaseTransactionRule())
        validator.add_validation_rule(AsyncTestRule())
    
    def _register_analyzers(self, agent):
        """Register custom analyzers."""
        agent.register_analyzer("security", SecurityAnalyzer)
    
    def _register_ui_extensions(self, agent):
        """Register UI extensions."""
        from .ui.cli_extension import register_cli_extensions
        from .ui.web_extension import register_web_extensions
        
        # Register CLI extensions
        register_cli_extensions(agent.get_cli())
        
        # Register web extensions
        register_web_extensions(agent.get_web_ui())

# Create plugin instance for automatic discovery
plugin = TestCoverageAgentPlugin()
```

## Integrating Extensions

To use these extensions, integrate them with the main application:

```python
from test_coverage_agent import TestCoverageAgent

# Create agent instance
agent = TestCoverageAgent()

# Register custom extensions
from my_coverage_plugin import plugin
plugin.register(agent)

# Use the agent with extensions
agent.run()
```

By following these patterns, you can create powerful extensions that enhance the Test Coverage Agent with new capabilities while maintaining a clean separation from the core functionality.