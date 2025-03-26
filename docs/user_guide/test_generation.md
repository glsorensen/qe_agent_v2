# Test Generation

The Test Generation module uses AI to create high-quality test cases for untested code. This feature helps developers quickly improve test coverage by automatically generating appropriate tests.

## How Test Generation Works

The test generation process follows these steps:

1. **Code Understanding**: Analyzing untested code to understand its purpose and behavior
2. **Test Strategy Selection**: Determining the most appropriate testing approach
3. **Template Application**: Applying test templates based on the code type
4. **AI Enhancement**: Using AI to generate context-aware tests
5. **Test Validation**: Verifying that generated tests are valid and effective

## Key Components

### CodeUnderstandingModule

The `CodeUnderstandingModule` class (found in `test_generation/code_understanding.py`) analyzes code to determine its purpose, inputs, outputs, and dependencies. This information is crucial for generating appropriate tests.

```python
# Example usage of CodeUnderstandingModule
from test_generation.code_understanding import CodeUnderstandingModule

code_understanding = CodeUnderstandingModule()

# Analyze a specific module
module_analysis = code_understanding.analyze_module("/path/to/repo/module.py")

# Analyze a specific method
method_analysis = code_understanding.analyze_method("ModuleName", "method_name")
```

### TemplateManager

The `TemplateManager` class (found in `test_generation/template_manager.py`) manages and applies test templates based on code type and testing requirements.

```python
# Example usage of TemplateManager
from test_generation.template_manager import TemplateManager

template_manager = TemplateManager()

# Get template for class testing
class_template = template_manager.get_template("class")

# Apply template to generate test structure
test_structure = template_manager.apply_template(
    template_name="function",
    function_name="calculate_total",
    parameters=["amount", "tax_rate"],
    return_type="float"
)
```

### AIPoweredTestWriter

The `AIPoweredTestWriter` class (found in `test_generation/test_writer.py`) uses AI to generate test cases based on code analysis and templates.

```python
# Example usage of AIPoweredTestWriter
from test_generation.test_writer import AIPoweredTestWriter

writer = AIPoweredTestWriter()

# Generate tests for a specific function
test_code = writer.generate_function_tests(
    function_path="/path/to/repo/module.py",
    function_name="calculate_total"
)

# Generate tests for an entire class
class_tests = writer.generate_class_tests(
    class_path="/path/to/repo/module.py",
    class_name="ShoppingCart"
)
```

## Test Templates

The agent includes several predefined test templates for common testing scenarios:

### Function Test Template

Template for testing simple functions with inputs and outputs:

```python
def test_{function_name}_{scenario}():
    # Arrange
    {arrange_code}
    
    # Act
    result = {function_name}({parameters})
    
    # Assert
    assert result == {expected_result}
```

### Class Test Template

Template for testing class behavior and methods:

```python
class Test{ClassName}:
    
    @pytest.fixture
    def {fixture_name}(self):
        # Setup code
        {setup_code}
        return {fixture_return}
    
    def test_{method_name}_{scenario}(self, {fixture_name}):
        # Arrange
        {arrange_code}
        
        # Act
        result = {fixture_name}.{method_name}({parameters})
        
        # Assert
        {assertions}
```

### Integration Test Template

Template for testing component interactions:

```python
def test_{component1}_{component2}_integration_{scenario}():
    # Arrange
    {arrange_code}
    
    # Act
    {act_code}
    
    # Assert
    {assertions}
```

## Configuration Options

Test generation can be customized with several options:

- **Template Selection**: Choose which templates to use for different code types
- **AI Assistance Level**: Configure how much AI assistance to use in test generation
- **Test Style**: Select testing style (e.g., pytest, unittest)
- **Coverage Goals**: Set specific coverage targets for generated tests

## Advanced Usage

### Custom Test Templates

You can create custom test templates for specific testing needs:

```python
from test_generation.template_manager import TemplateManager

template_manager = TemplateManager()

# Register custom template
template_manager.register_template(
    name="custom_api_test",
    template="""def test_{endpoint}_api_{scenario}():
    # Arrange
    client = get_test_client()
    payload = {payload}
    
    # Act
    response = client.{method}('{endpoint}', json=payload)
    
    # Assert
    assert response.status_code == {expected_status}
    assert response.json() == {expected_response}
    """
)

# Use custom template
api_test = template_manager.apply_template(
    template_name="custom_api_test",
    endpoint="/users",
    method="post",
    payload="{\"name\": \"test_user\"}",
    expected_status=201,
    expected_response="{\"id\": 1, \"name\": \"test_user\"}"
)
```

### Adjusting AI Test Generation

Configure how AI generates tests:

```bash
# Generate minimal tests quickly
python run.py /path/to/repo --generate-tests --ai-mode minimal

# Generate comprehensive tests with extensive coverage
python run.py /path/to/repo --generate-tests --ai-mode comprehensive
```

## Common Issues and Solutions

### Generated Tests Fail to Run

If generated tests fail to run, it may be due to missing dependencies or incorrect assumptions. Try:

```bash
# Generate tests with more context information
python run.py /path/to/repo --generate-tests --ai-mode comprehensive --include-context
```

### Tests Don't Match Coding Style

Ensure generated tests match your project's coding style:

```yaml
# In .test-coverage-agent.yaml
test_generation:
  style: "pytest"  # or "unittest"
  indentation: 4
  quotes: "single"  # or "double"
```

### Handling Complex Dependencies

For code with complex dependencies, provide dependency configuration:

```yaml
# In .test-coverage-agent.yaml
test_generation:
  mocking_strategy: "auto"  # or "manual"
  fixture_strategy: "function"  # or "class", "module", "session"
  dependency_injection: true
```