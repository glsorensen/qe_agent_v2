import os
import re
from typing import Dict, List, Optional, Set, Tuple, Any

from langchain.chains import LLMChain
from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from .code_understanding import CodeUnderstandingModule, Function, Class
from .template_manager import TestTemplateManager, TestTemplate


class AIPoweredTestWriter:
    """AI-powered test writer using Anthropic's Claude."""
    
    def __init__(
        self, 
        api_key: str,
        code_understanding: CodeUnderstandingModule,
        template_manager: TestTemplateManager
    ):
        """Initialize the AI-powered test writer.
        
        Args:
            api_key: Anthropic API key
            code_understanding: Code understanding module instance
            template_manager: Test template manager instance
        """
        self.api_key = api_key
        self.code_understanding = code_understanding
        self.template_manager = template_manager
        
        # Initialize the Claude model
        self.model = ChatAnthropic(
            anthropic_api_key=api_key,
            model_name="claude-3-7-sonnet-20250219",
            temperature=0.2
        )
        
        # System prompt for the model
        self.system_prompt = """
You are an expert software developer and test engineer. Your task is to generate
high-quality test code for the given code snippets. Follow these guidelines:

1. Analyze the code carefully to understand its functionality
2. Identify edge cases and common failure modes
3. Create comprehensive tests that validate both normal and edge cases
4. Use mocks or stubs for external dependencies
5. Follow the test framework's conventions
6. Create readable, maintainable tests
7. Focus on testing behavior, not implementation details
8. Include helpful comments explaining the test's purpose

Respond only with the test code - no explanations unless specifically requested.
        """
    
    def generate_function_test(
        self, 
        function: Function, 
        framework: str = "pytest"
    ) -> str:
        """Generate a test for a function.
        
        Args:
            function: Function to test
            framework: Test framework to use
            
        Returns:
            Generated test code
        """
        # Get appropriate template
        language = "python"  # Default to Python for now
        if framework in ["pytest", "unittest"]:
            language = "python"
        elif framework in ["jest", "mocha"]:
            language = "javascript"
        
        templates = self.template_manager.get_templates_for_language_framework(language, framework)
        if not templates:
            # No template found, fall back to AI generation without template
            return self._generate_test_with_ai(function, framework)
        
        # Select appropriate template
        template = None
        if function.is_method:
            # Look for method template
            for t in templates:
                if "method" in t.name:
                    template = t
                    break
        else:
            # Look for function template
            for t in templates:
                if "function" in t.name and "method" not in t.name:
                    template = t
                    break
        
        if not template and templates:
            template = templates[0]  # Use first template as fallback
        
        if not template:
            # No template found, fall back to AI generation without template
            return self._generate_test_with_ai(function, framework)
        
        # Prepare variables for template
        file_path = function.file_path
        rel_path = os.path.relpath(file_path, self.code_understanding.repo_path)
        module_path = self._file_path_to_module_path(rel_path)
        
        variables = {
            "module_path": module_path,
            "function_name": function.name,
            "target_name": function.name
        }
        
        if function.is_method:
            variables["class_name"] = function.class_name
            variables["method_name"] = function.name
            
            # Get method call details from AI
            ai_method_details = self._get_method_test_details(function, framework)
            
            # Add AI-generated details to variables
            variables.update(ai_method_details)
        else:
            # Get function call details from AI
            ai_function_details = self._get_function_test_details(function, framework)
            
            # Add AI-generated details to variables
            variables.update(ai_function_details)
        
        # Generate test code from template
        test_code = self.template_manager.create_test_from_template(template, variables)
        
        # Clean up any unfilled template variables
        test_code = re.sub(r'\{[^}]+\}', '', test_code)
        
        return test_code
    
    def generate_class_test(
        self, 
        cls: Class, 
        framework: str = "pytest"
    ) -> str:
        """Generate a test for a class.
        
        Args:
            cls: Class to test
            framework: Test framework to use
            
        Returns:
            Generated test code
        """
        # Get appropriate template
        language = "python"  # Default to Python for now
        if framework in ["pytest", "unittest"]:
            language = "python"
        elif framework in ["jest", "mocha"]:
            language = "javascript"
        
        templates = self.template_manager.get_templates_for_language_framework(language, framework)
        class_templates = [t for t in templates if "class" in t.name]
        
        if not class_templates:
            # No template found, fall back to AI generation without template
            return self._generate_class_test_with_ai(cls, framework)
        
        template = class_templates[0]
        
        # Prepare variables for template
        file_path = cls.file_path
        rel_path = os.path.relpath(file_path, self.code_understanding.repo_path)
        module_path = self._file_path_to_module_path(rel_path)
        
        variables = {
            "module_path": module_path,
            "class_name": cls.name,
            "fixture_name": cls.name.lower(),
        }
        
        # Get class test details from AI
        ai_class_details = self._get_class_test_details(cls, framework)
        
        # Add AI-generated details to variables
        variables.update(ai_class_details)
        
        # Generate test code from template
        test_code = self.template_manager.create_test_from_template(template, variables)
        
        # Clean up any unfilled template variables
        test_code = re.sub(r'\{[^}]+\}', '', test_code)
        
        return test_code
    
    def _generate_test_with_ai(
        self, 
        function: Function, 
        framework: str = "pytest"
    ) -> str:
        """Generate a test for a function using pure AI without templates.
        
        Args:
            function: Function to test
            framework: Test framework to use
            
        Returns:
            Generated test code
        """
        # Prepare the prompt
        prompt = f"""
Please generate a test for the following function using {framework}:

```python
{function.code}
```

Focus on thoroughly testing the function's behavior and handling edge cases.
Just provide the test code without explanations.
        """
        
        # Call the model
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        test_code = response.content
        
        # Extract code block if present
        code_pattern = r"```(?:python)?\n(.*?)```"
        code_matches = re.findall(code_pattern, test_code, re.DOTALL)
        if code_matches:
            test_code = code_matches[0]
        
        return test_code
    
    def _generate_class_test_with_ai(
        self, 
        cls: Class, 
        framework: str = "pytest"
    ) -> str:
        """Generate a test for a class using pure AI without templates.
        
        Args:
            cls: Class to test
            framework: Test framework to use
            
        Returns:
            Generated test code
        """
        # Prepare the prompt
        prompt = f"""
Please generate tests for the following class using {framework}:

```python
{cls.code}
```

Focus on thoroughly testing the class's behavior and methods. Create a test class
that tests the main functionality, initialization, and important methods.
Just provide the test code without explanations.
        """
        
        # Call the model
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        test_code = response.content
        
        # Extract code block if present
        code_pattern = r"```(?:python)?\n(.*?)```"
        code_matches = re.findall(code_pattern, test_code, re.DOTALL)
        if code_matches:
            test_code = code_matches[0]
        
        return test_code
    
    def _get_function_test_details(
        self, 
        function: Function, 
        framework: str
    ) -> Dict[str, str]:
        """Get test details for a function from the AI.
        
        Args:
            function: Function to test
            framework: Test framework to use
            
        Returns:
            Dictionary with test details
        """
        # Prepare the prompt
        prompt = f"""
Analyze this function and provide test details:

```python
{function.code}
```

I need the following details formatted as JSON:
1. arrange_code: Code to set up inputs and dependencies
2. function_call: How to call the function with appropriate arguments
3. assert_code: Assertions to verify the function's behavior
4. test_description: Brief description of what the test verifies

Example format:
{{
  "arrange_code": "x = 5\\ny = 10",
  "function_call": "add(x, y)",
  "assert_code": "assert result == 15",
  "test_description": "correctly adds two positive numbers"
}}
        """
        
        # Call the model
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        
        # Extract JSON from response
        json_pattern = r"```json\n(.*?)```"
        json_matches = re.findall(json_pattern, response.content, re.DOTALL)
        
        if json_matches:
            import json
            try:
                details = json.loads(json_matches[0])
                return details
            except:
                pass
        
        # Fallback values if parsing fails
        return {
            "arrange_code": "# TODO: Set up test inputs",
            "function_call": f"{function.name}()",
            "assert_code": "# TODO: Add assertions",
            "test_description": f"tests {function.name} functionality"
        }
    
    def _get_method_test_details(
        self, 
        method: Function, 
        framework: str
    ) -> Dict[str, str]:
        """Get test details for a class method from the AI.
        
        Args:
            method: Method to test
            framework: Test framework to use
            
        Returns:
            Dictionary with test details
        """
        # Prepare the prompt
        prompt = f"""
Analyze this class method and provide test details:

```python
{method.code}
```

This is a method of the class {method.class_name}.

I need the following details formatted as JSON:
1. instance_create: Code to create an instance of the class
2. arrange_code: Code to set up inputs and dependencies
3. method_call: How to call the method with appropriate arguments
4. assert_code: Assertions to verify the method's behavior

Example format:
{{
  "instance_create": "instance = MyClass(param1, param2)",
  "arrange_code": "x = 5\\ny = 10",
  "method_call": "instance.method(x, y)",
  "assert_code": "assert result == 15"
}}
        """
        
        # Call the model
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        
        # Extract JSON from response
        json_pattern = r"```json\n(.*?)```"
        json_matches = re.findall(json_pattern, response.content, re.DOTALL)
        
        if json_matches:
            import json
            try:
                details = json.loads(json_matches[0])
                return details
            except:
                pass
        
        # Fallback values if parsing fails
        return {
            "instance_create": f"instance = {method.class_name}()",
            "arrange_code": "# TODO: Set up test inputs",
            "method_call": f"instance.{method.name}()",
            "assert_code": "# TODO: Add assertions"
        }
    
    def _get_class_test_details(
        self, 
        cls: Class, 
        framework: str
    ) -> Dict[str, str]:
        """Get test details for a class from the AI.
        
        Args:
            cls: Class to test
            framework: Test framework to use
            
        Returns:
            Dictionary with test details
        """
        # Prepare the prompt
        prompt = f"""
Analyze this class and provide test details:

```python
{cls.code}
```

I need the following details formatted as JSON:
1. fixture_code: Code to set up any dependencies needed for the fixture
2. instance_creation: How to create an instance of the class
3. test_methods: Complete test methods for the class's key functionality

Example format:
{{
  "fixture_code": "param1 = 'test'\\nparam2 = 42",
  "instance_creation": "MyClass(param1, param2)",
  "test_methods": "def test_method1(self, my_class_fixture):\\n    result = my_class_fixture.method1()\\n    assert result == expected\\n\\ndef test_method2(self, my_class_fixture):\\n    result = my_class_fixture.method2(param)\\n    assert result == expected"
}}
        """
        
        # Call the model
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        
        # Extract JSON from response
        json_pattern = r"```json\n(.*?)```"
        json_matches = re.findall(json_pattern, response.content, re.DOTALL)
        
        if json_matches:
            import json
            try:
                details = json.loads(json_matches[0])
                return details
            except:
                pass
        
        # Fallback values if parsing fails
        return {
            "fixture_code": "# TODO: Set up dependencies",
            "instance_creation": f"{cls.name}()",
            "test_methods": f"def test_initialization(self, {cls.name.lower()}):\n    assert {cls.name.lower()} is not None"
        }
    
    def _file_path_to_module_path(self, file_path: str) -> str:
        """Convert a file path to a Python module path.
        
        Args:
            file_path: File path (relative to repo root)
            
        Returns:
            Module path
        """
        # Remove extension
        if file_path.endswith('.py'):
            module_path = file_path[:-3]
        else:
            module_path = file_path
            
        # Replace directory separators with dots
        module_path = module_path.replace('/', '.').replace('\\', '.')
        
        # Remove __init__ from the end
        if module_path.endswith('__init__'):
            module_path = module_path[:-9]
            if module_path.endswith('.'):
                module_path = module_path[:-1]
                
        return module_path