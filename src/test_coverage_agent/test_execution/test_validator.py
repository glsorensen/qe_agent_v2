import os
import re
from typing import Dict, List, Optional, Set, Tuple, Any

from langchain_core.messages import HumanMessage, SystemMessage

from .test_runner import TestRunner, TestRunResult
from ..test_generation.llm_provider import LLMProvider, LLMProviderFactory


class TestValidationResult:
    """Class representing the result of test validation."""
    
    def __init__(
        self,
        is_valid: bool,
        issues: List[str] = None,
        suggestions: List[str] = None,
        run_result: Optional[TestRunResult] = None
    ):
        """Initialize a test validation result.
        
        Args:
            is_valid: Whether the test is valid
            issues: List of issues found in the test
            suggestions: List of suggestions for improving the test
            run_result: TestRunResult from running the test
        """
        self.is_valid = is_valid
        self.issues = issues or []
        self.suggestions = suggestions or []
        self.run_result = run_result


class TestValidator:
    """Validator for verifying generated tests."""
    
    def __init__(self, repo_path: str, api_key: Optional[str] = None, provider_name: str = "claude"):
        """Initialize the test validator.
        
        Args:
            repo_path: Path to the repository
            api_key: API key for LLM provider (optional)
            provider_name: Name of the LLM provider to use (default: "claude")
        """
        self.repo_path = repo_path
        self.api_key = api_key
        self.test_runner = TestRunner(repo_path)
        
        # Initialize LLM provider if API key is provided
        self.model = None
        self.llm_provider = None
        if api_key:
            self.llm_provider = LLMProviderFactory.create_provider(provider_name, api_key)
            self.model = self.llm_provider.get_model()
    
    def validate_test(
        self, 
        test_code: str, 
        source_code: str, 
        language: str,
        run_test: bool = True
    ) -> TestValidationResult:
        """Validate a test against its source code.
        
        Args:
            test_code: Test code to validate
            source_code: Source code being tested
            language: Programming language
            run_test: Whether to run the test
            
        Returns:
            TestValidationResult with validation results
        """
        issues = []
        suggestions = []
        
        # Basic syntax validation
        syntax_result = self.validate_syntax(test_code, language)
        issues.extend(syntax_result.issues)
        suggestions.extend(syntax_result.suggestions)
        
        # Run the test if requested
        run_result = None
        if run_test and not issues:  # Only run if no syntax issues
            run_result = self.test_runner.run_test_code(test_code, language)
            if not run_result.success:
                issues.append(f"Test failed to run: {run_result.error_message}")
        
        # AI-based validation if available
        if self.model and not issues:
            ai_result = self.validate_with_ai(test_code, source_code, language)
            issues.extend(ai_result.issues)
            suggestions.extend(ai_result.suggestions)
        
        # Determine if the test is valid
        is_valid = len(issues) == 0
        if run_result and not run_result.success:
            is_valid = False
        
        return TestValidationResult(
            is_valid=is_valid,
            issues=issues,
            suggestions=suggestions,
            run_result=run_result
        )
    
    def validate_syntax(self, test_code: str, language: str) -> TestValidationResult:
        """Validate the syntax of test code.
        
        Args:
            test_code: Test code to validate
            language: Programming language
            
        Returns:
            TestValidationResult with syntax validation results
        """
        issues = []
        suggestions = []
        
        if language.lower() == 'python':
            try:
                # Try to compile the code to check for syntax errors
                compile(test_code, 'test_code', 'exec')
            except SyntaxError as e:
                issues.append(f"Syntax error: {str(e)}")
                
            # Check for common issues
            if 'import ' not in test_code:
                issues.append("Missing imports")
                suggestions.append("Add necessary imports for the code being tested")
                
            if 'test_' not in test_code and 'class Test' not in test_code:
                issues.append("No test functions found")
                suggestions.append("Test functions should be named with 'test_' prefix")
                
            if 'assert' not in test_code:
                issues.append("No assertions found")
                suggestions.append("Add assertions to verify the code behavior")
        
        elif language.lower() in ['javascript', 'typescript']:
            # Basic JavaScript validation
            if 'describe(' not in test_code and 'test(' not in test_code and 'it(' not in test_code:
                issues.append("No test blocks found")
                suggestions.append("Use describe(), it(), or test() blocks")
                
            if 'expect(' not in test_code and 'assert' not in test_code:
                issues.append("No assertions found")
                suggestions.append("Add expectations or assertions to verify the code behavior")
        
        return TestValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            suggestions=suggestions
        )
    
    def validate_with_ai(
        self, 
        test_code: str, 
        source_code: str, 
        language: str
    ) -> TestValidationResult:
        """Validate test code using AI.
        
        Args:
            test_code: Test code to validate
            source_code: Source code being tested
            language: Programming language
            
        Returns:
            TestValidationResult with AI validation results
        """
        if not self.model:
            return TestValidationResult(is_valid=True)
            
        # Prepare the prompt
        prompt = f"""
Please evaluate this test code against the source code it's meant to test:

Source code:
```{language}
{source_code}
```

Test code:
```{language}
{test_code}
```

Identify any issues with the test code, including:
1. Missing test cases or edge cases
2. Incorrect assumptions about the source code
3. Testing implementation details instead of behavior
4. Insufficient assertions
5. Brittleness or fragility in the tests

Format your response as a JSON object with two arrays:
{{
  "issues": ["issue 1", "issue 2", ...],
  "suggestions": ["suggestion 1", "suggestion 2", ...]
}}

If there are no issues, return empty arrays.
        """
        
        # Call the model
        system_message = """
You are an expert test engineer reviewing test code. 
Provide a critical evaluation focusing on test quality, completeness, and correctness.
Respond ONLY with the requested JSON format.
        """
        
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        
        # Extract JSON from response
        json_pattern = r"```json\n(.*?)```"
        json_matches = re.findall(json_pattern, response.content, re.DOTALL)
        
        if json_matches:
            import json
            try:
                result = json.loads(json_matches[0])
                return TestValidationResult(
                    is_valid=len(result.get('issues', [])) == 0,
                    issues=result.get('issues', []),
                    suggestions=result.get('suggestions', [])
                )
            except:
                pass
        
        # Try to find a JSON-like structure without code block
        try:
            # Find content between { and } that spans multiple lines
            json_pattern = r"({[^{]*?\"issues\"[^}]*?\"suggestions\"[^}]*?})"
            json_matches = re.findall(json_pattern, response.content, re.DOTALL)
            
            if json_matches:
                import json
                result = json.loads(json_matches[0])
                return TestValidationResult(
                    is_valid=len(result.get('issues', [])) == 0,
                    issues=result.get('issues', []),
                    suggestions=result.get('suggestions', [])
                )
        except:
            pass
        
        # Fallback if we can't parse JSON
        return TestValidationResult(is_valid=True)