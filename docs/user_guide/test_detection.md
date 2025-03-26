# Test Detection

Test detection is the process of identifying and analyzing test files in a repository and establishing their relationships to implementation code.

## How Test Detection Works

The Test Detection component performs several key functions:

1. **Test File Identification**: Locates test files based on naming patterns and location
2. **Test-to-Implementation Mapping**: Establishes relationships between tests and the code they test
3. **Coverage Gap Analysis**: Identifies implementation code that lacks corresponding tests
4. **Test Structure Analysis**: Analyzes test files to understand their structure and quality

## Key Components

### TestDetector

The `TestDetector` class found in `repository/test_detector.py` is responsible for discovering and analyzing test files. It provides methods to:

- Find test files based on configurable patterns
- Map tests to their implementation counterparts
- Identify untested code components
- Analyze test quality and structure

```python
# Example usage of TestDetector
from repository.test_detector import TestDetector

detector = TestDetector("/path/to/repo")

# Find all test files
test_files = detector.find_test_files()

# Map tests to implementation
mapping = detector.map_tests_to_implementation()

# Find untested modules
untested_modules = detector.find_untested_modules()
```

## Test Discovery Strategies

The Test Coverage Agent uses several strategies to discover tests:

### Pattern-Based Discovery

By default, files matching these patterns are identified as tests:

- Files with names starting with `test_`
- Files with names ending with `_test.py`
- Files located within directories named `tests`, `test`, or `testing`

This behavior can be customized using the `--test-pattern` option.

### Content-Based Discovery

In addition to pattern matching, the agent can analyze file contents to identify tests by looking for:

- Import statements for test frameworks like `pytest` or `unittest`
- Test class definitions (classes inheriting from `TestCase`)
- Test method definitions (methods starting with `test_`)
- Test decorators like `@pytest.fixture` or `@unittest.mock`

## Test-to-Implementation Mapping

The agent uses several heuristics to map tests to their implementation:

1. **Name Correlation**: Matches `test_module.py` with `module.py`
2. **Import Analysis**: Examines imports in test files to identify tested modules
3. **Method Name Analysis**: Analyzes test method names to identify tested classes/methods
4. **Content Analysis**: Examines test assertions and method calls to determine tested functionality

## Configuration Options

Test detection can be customized with several options:

- **Test Patterns**: Custom patterns to identify test files (`--test-pattern`)
- **Exclusion Patterns**: Patterns to exclude from test detection
- **Mapping Strategy**: Configure how tests are mapped to implementation
- **Discovery Depth**: Control how deep to search for test relationships

## Common Issues and Solutions

### Non-Standard Test Organization

If your project uses non-standard test organization patterns, you can customize the test detection:

```bash
# Custom test pattern example
python run.py /path/to/repo --test-pattern "spec_*.py,*_spec.py"
```

### Missing Test-to-Implementation Mappings

If the automatic mapping is incomplete, you can provide hints to improve detection:

```yaml
# In .test-coverage-agent.yaml
test_mapping:
  custom_mappings:
    - test_file: "tests/special_test.py"
      implementation_file: "src/special_module.py"
    - test_file: "tests/custom/validators_test.py"
      implementation_file: "src/validation/validators.py"
```

### Handling Third-Party Code

Exclude third-party code or vendor directories from analysis:

```bash
python run.py /path/to/repo --exclude "vendor,node_modules,third_party"
```

## Advanced Features

### Manual Mapping Override

For complex cases, you can manually specify test-to-implementation mappings:

```python
from repository.test_detector import TestDetector

detector = TestDetector("/path/to/repo")

# Add custom mapping
detector.add_custom_mapping(
    test_file="tests/special_case_test.py",
    implementation_file="src/deeply/nested/special_case.py"
)

# Continue with analysis
mapping = detector.map_tests_to_implementation()
```