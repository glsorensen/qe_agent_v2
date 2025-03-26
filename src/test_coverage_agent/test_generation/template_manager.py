import os
from typing import Dict, List, Optional, Set, Tuple, Any


class TestTemplate:
    """Class representing a test template."""
    
    def __init__(
        self, 
        name: str, 
        language: str, 
        framework: str, 
        template: str,
        description: str = ""
    ):
        """Initialize a test template.
        
        Args:
            name: Template name
            language: Programming language
            framework: Test framework
            template: Template content
            description: Template description
        """
        self.name = name
        self.language = language
        self.framework = framework
        self.template = template
        self.description = description


class TestTemplateManager:
    """Manager for test templates."""
    
    def __init__(self):
        """Initialize the test template manager."""
        self.templates: Dict[str, TestTemplate] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self) -> None:
        """Initialize default test templates for various languages and frameworks."""
        # Python - pytest
        pytest_function_template = TestTemplate(
            name="pytest_function",
            language="python",
            framework="pytest",
            description="Template for testing a Python function with pytest",
            template="""
import pytest
from {module_path} import {target_name}

def test_{function_name}():
    \"\"\"Test {function_name} functionality.\"\"\"
    # Arrange
    {arrange_code}
    
    # Act
    result = {function_call}
    
    # Assert
    {assert_code}
"""
        )
        self.add_template(pytest_function_template)
        
        # Python - pytest for class methods
        pytest_method_template = TestTemplate(
            name="pytest_method",
            language="python",
            framework="pytest",
            description="Template for testing a Python class method with pytest",
            template="""
import pytest
from {module_path} import {class_name}

def test_{method_name}():
    \"\"\"Test {class_name}.{method_name} functionality.\"\"\"
    # Arrange
    {instance_create}
    {arrange_code}
    
    # Act
    result = {method_call}
    
    # Assert
    {assert_code}
"""
        )
        self.add_template(pytest_method_template)
        
        # Python - pytest for class
        pytest_class_template = TestTemplate(
            name="pytest_class",
            language="python",
            framework="pytest",
            description="Template for testing a Python class with pytest",
            template="""
import pytest
from {module_path} import {class_name}

class Test{class_name}:
    \"\"\"Tests for the {class_name} class.\"\"\"
    
    @pytest.fixture
    def {fixture_name}(self):
        \"\"\"Create a {class_name} instance for testing.\"\"\"
        {fixture_code}
        return {instance_creation}
    
{test_methods}
"""
        )
        self.add_template(pytest_class_template)
        
        # JavaScript - Jest for function
        jest_function_template = TestTemplate(
            name="jest_function",
            language="javascript",
            framework="jest",
            description="Template for testing a JavaScript function with Jest",
            template="""
import { {function_name} } from '{module_path}';

describe('{function_name}', () => {
  test('should {test_description}', () => {
    // Arrange
    {arrange_code}
    
    // Act
    const result = {function_call};
    
    // Assert
    {assert_code}
  });
});
"""
        )
        self.add_template(jest_function_template)
        
        # JavaScript - Jest for class/component
        jest_class_template = TestTemplate(
            name="jest_class",
            language="javascript",
            framework="jest",
            description="Template for testing a JavaScript class with Jest",
            template="""
import { {class_name} } from '{module_path}';

describe('{class_name}', () => {
  let instance;
  
  beforeEach(() => {
    {beforeEach_code}
    instance = new {class_name}({constructor_args});
  });
  
{test_methods}
});
"""
        )
        self.add_template(jest_function_template)
    
    def add_template(self, template: TestTemplate) -> None:
        """Add a template to the manager.
        
        Args:
            template: Template to add
        """
        key = f"{template.language}_{template.framework}_{template.name}"
        self.templates[key] = template
    
    def get_template(
        self, 
        language: str, 
        framework: str, 
        name: str
    ) -> Optional[TestTemplate]:
        """Get a template by language, framework, and name.
        
        Args:
            language: Programming language
            framework: Test framework
            name: Template name
            
        Returns:
            TestTemplate if found, None otherwise
        """
        key = f"{language}_{framework}_{name}"
        return self.templates.get(key)
    
    def get_templates_for_language_framework(
        self, 
        language: str, 
        framework: str
    ) -> List[TestTemplate]:
        """Get all templates for a specific language and framework.
        
        Args:
            language: Programming language
            framework: Test framework
            
        Returns:
            List of TestTemplate objects
        """
        prefix = f"{language}_{framework}_"
        return [
            template for key, template in self.templates.items() 
            if key.startswith(prefix)
        ]
    
    def create_test_from_template(
        self, 
        template: TestTemplate, 
        variables: Dict[str, str]
    ) -> str:
        """Create a test from a template by replacing variables.
        
        Args:
            template: Template to use
            variables: Dictionary of variable replacements
            
        Returns:
            Generated test code
        """
        test_code = template.template
        
        for key, value in variables.items():
            test_code = test_code.replace(f"{{{key}}}", value)
        
        return test_code