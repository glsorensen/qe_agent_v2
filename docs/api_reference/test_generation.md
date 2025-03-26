# Test Generation Module API

The Test Generation module provides components for analyzing code, managing test templates, and generating tests using AI.

## CodeUnderstandingModule

```python
from test_generation.code_understanding import CodeUnderstandingModule
```

The `CodeUnderstandingModule` class analyzes code to understand its purpose, behavior, and testing needs.

### Constructor

```python
def __init__(self):
    """Initialize a CodeUnderstandingModule."""
```

### Methods

#### analyze_module

```python
def analyze_module(self, module_path: str) -> Dict[str, Any]:
    """Analyze a module to understand its structure and purpose.

    Args:
        module_path: Path to the module file

    Returns:
        Dict containing module analysis
    """
```

Analyzes a module to understand its structure and purpose.

#### analyze_method

```python
def analyze_method(self, module_name: str, method_name: str) -> Dict[str, Any]:
    """Analyze a specific method to understand its behavior.

    Args:
        module_name: Name of the module containing the method
        method_name: Name of the method to analyze

    Returns:
        Dict containing method analysis
    """
```

Analyzes a specific method to understand its behavior.

#### extract_dependencies

```python
def extract_dependencies(self, module_path: str) -> List[str]:
    """Extract dependencies from a module.

    Args:
        module_path: Path to the module file

    Returns:
        List of dependency module names
    """
```

Extracts dependencies from a module.

### Example Usage

```python
# Initialize code understanding module
code_understanding = CodeUnderstandingModule()

# Analyze a module
module_analysis = code_understanding.analyze_module("/path/to/module.py")
print(f"Module purpose: {module_analysis['purpose']}")
print(f"Module classes: {', '.join(module_analysis['classes'])}")
print(f"Module functions: {', '.join(module_analysis['functions'])}")

# Analyze a specific method
method_analysis = code_understanding.analyze_method("my_module", "calculate_total")
print(f"Method purpose: {method_analysis['purpose']}")
print(f"Parameters: {', '.join(method_analysis['parameters'])}")
print(f"Return type: {method_analysis['return_type']}")

# Extract dependencies
dependencies = code_understanding.extract_dependencies("/path/to/module.py")
print(f"Dependencies: {', '.join(dependencies)}")
```

## TemplateManager

```python
from test_generation.template_manager import TemplateManager
```

The `TemplateManager` class manages and applies test templates based on code type and testing requirements.

### Constructor

```python
def __init__(self):
    """Initialize a TemplateManager with default templates."""
```

### Methods

#### get_template

```python
def get_template(self, template_name: str) -> str:
    """Get a template by name.

    Args:
        template_name: Name of the template

    Returns:
        Template string

    Raises:
        ValueError: If template_name is not found
    """
```

Retrieves a template by name.

#### register_template

```python
def register_template(self, name: str, template: str) -> None:
    """Register a new template.

    Args:
        name: Name for the template
        template: Template string
    """
```

Registers a new template.

#### apply_template

```python
def apply_template(self, template_name: str, **kwargs) -> str:
    """Apply a template with the given parameters.

    Args:
        template_name: Name of the template to apply
        **kwargs: Parameters to fill in the template

    Returns:
        Filled template string

    Raises:
        ValueError: If template_name is not found
        KeyError: If a required template parameter is missing
    """
```

Applies a template with the given parameters and returns the filled template.

#### list_templates

```python
def list_templates(self) -> List[str]:
    """List all available template names.

    Returns:
        List of template names
    """
```

Lists all available template names.

### Example Usage

```python
# Initialize template manager
template_manager = TemplateManager()

# List available templates
templates = template_manager.list_templates()
print(f"Available templates: {', '.join(templates)}")

# Get a template
function_template = template_manager.get_template("function")
print(function_template)

# Register a custom template
template_manager.register_template(
    name="api_test",
    template="""import requests

def test_{endpoint}_{scenario}():
    # Arrange
    url = "{base_url}/{endpoint}"
    
    # Act
    response = requests.{method}(url)
    
    # Assert
    assert response.status_code == {expected_status}
    {additional_assertions}
"""
)

# Apply a template
test_code = template_manager.apply_template(
    template_name="function",
    function_name="calculate_total",
    scenario="valid_input",
    arrange_code="amount = 100\ntax_rate = 0.1",
    parameters="amount, tax_rate",
    expected_result="110"
)

print(test_code)
```

## AIPoweredTestWriter

```python
from test_generation.test_writer import AIPoweredTestWriter
```

The `AIPoweredTestWriter` class uses AI to generate test cases based on code analysis and templates.

### Constructor

```python
def __init__(self, model_name: str = "default"):
    """Initialize an AIPoweredTestWriter.

    Args:
        model_name: Name of the AI model to use
    """
```

### Methods

#### generate_function_tests

```python
def generate_function_tests(self, function_path: str, function_name: str) -> str:
    """Generate tests for a specific function.

    Args:
        function_path: Path to the file containing the function
        function_name: Name of the function to test

    Returns:
        String containing the generated test code
    """
```

Generates tests for a specific function.

#### generate_class_tests

```python
def generate_class_tests(self, class_path: str, class_name: str) -> str:
    """Generate tests for a specific class.

    Args:
        class_path: Path to the file containing the class
        class_name: Name of the class to test

    Returns:
        String containing the generated test code
    """
```

Generates tests for a specific class.

#### refine_tests

```python
def refine_tests(self, test_code: str, implementation_code: str) -> str:
    """Refine generated tests based on implementation code.

    Args:
        test_code: The generated test code
        implementation_code: The implementation code

    Returns:
        Refined test code
    """
```

Refines generated tests based on implementation code.

### Example Usage

```python
# Initialize AI-powered test writer
writer = AIPoweredTestWriter()

# Generate tests for a function
function_tests = writer.generate_function_tests(
    function_path="/path/to/module.py",
    function_name="calculate_total"
)

# Generate tests for a class
class_tests = writer.generate_class_tests(
    class_path="/path/to/module.py",
    class_name="ShoppingCart"
)

# Write tests to file
with open("tests/test_module.py", "w") as f:
    f.write(function_tests)

with open("tests/test_shopping_cart.py", "w") as f:
    f.write(class_tests)

# Refine tests based on implementation
with open("/path/to/module.py", "r") as f:
    implementation_code = f.read()

refined_tests = writer.refine_tests(function_tests, implementation_code)

with open("tests/test_module_refined.py", "w") as f:
    f.write(refined_tests)
```