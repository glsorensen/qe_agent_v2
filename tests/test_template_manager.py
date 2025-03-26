import pytest

from test_coverage_agent.test_generation.template_manager import TestTemplateManager, TestTemplate


class TestTestTemplateManager:
    """Tests for the TestTemplateManager class."""
    
    def test_init(self):
        """Test initializing the TestTemplateManager."""
        manager = TestTemplateManager()
        
        # Check that default templates were initialized
        assert len(manager.templates) > 0
        
        # Verify some common template keys
        assert "python_pytest_pytest_function" in manager.templates
        assert "python_pytest_pytest_method" in manager.templates
        assert "python_pytest_pytest_class" in manager.templates
        assert "javascript_jest_jest_function" in manager.templates
    
    def test_add_template(self):
        """Test adding a template to the manager."""
        manager = TestTemplateManager()
        
        # Create a custom template
        template = TestTemplate(
            name="custom_template",
            language="python",
            framework="unittest",
            template="def test_custom(): assert True",
            description="Custom test template"
        )
        
        # Add the template
        manager.add_template(template)
        
        # Check that the template was added
        assert "python_unittest_custom_template" in manager.templates
        
        # Verify the template was stored correctly
        stored_template = manager.templates["python_unittest_custom_template"]
        assert stored_template.name == "custom_template"
        assert stored_template.language == "python"
        assert stored_template.framework == "unittest"
        assert stored_template.template == "def test_custom(): assert True"
        assert stored_template.description == "Custom test template"
    
    def test_get_template(self):
        """Test getting a template by language, framework, and name."""
        manager = TestTemplateManager()
        
        # Get a template that exists
        template = manager.get_template("python", "pytest", "pytest_function")
        
        assert template is not None
        assert template.name == "pytest_function"
        assert template.language == "python"
        assert template.framework == "pytest"
        
        # Try to get a template that doesn't exist
        template = manager.get_template("python", "unknown_framework", "unknown_template")
        assert template is None
    
    def test_get_templates_for_language_framework(self):
        """Test getting all templates for a specific language and framework."""
        manager = TestTemplateManager()
        
        # Get all pytest templates
        templates = manager.get_templates_for_language_framework("python", "pytest")
        
        assert len(templates) >= 3  # function, method, class templates
        
        # Check template names
        template_names = [t.name for t in templates]
        assert "pytest_function" in template_names
        assert "pytest_method" in template_names
        assert "pytest_class" in template_names
        
        # Try to get templates for a non-existent combination
        templates = manager.get_templates_for_language_framework("unknown", "unknown")
        assert len(templates) == 0
    
    def test_create_test_from_template(self):
        """Test creating a test from a template by replacing variables."""
        manager = TestTemplateManager()
        
        # Get a template
        template = manager.get_template("python", "pytest", "pytest_function")
        
        # Define variables for substitution
        variables = {
            "module_path": "app.calculator",
            "target_name": "add",
            "function_name": "add",
            "arrange_code": "a = 5\nb = 3",
            "function_call": "add(a, b)",
            "assert_code": "assert result == 8"
        }
        
        # Create test from template
        test_code = manager.create_test_from_template(template, variables)
        
        # Check that variables were replaced
        assert "import pytest" in test_code
        assert "from app.calculator import add" in test_code
        assert "def test_add():" in test_code
        assert "a = 5\nb = 3" in test_code
        assert "result = add(a, b)" in test_code
        assert "assert result == 8" in test_code
    
    def test_create_test_from_template_missing_variables(self):
        """Test creating a test with missing variables."""
        manager = TestTemplateManager()
        
        # Get a template
        template = manager.get_template("python", "pytest", "pytest_function")
        
        # Define incomplete variables
        variables = {
            "module_path": "app.calculator",
            "target_name": "add",
            "function_name": "add"
            # Missing arrange_code, function_call, assert_code
        }
        
        # Create test from template
        test_code = manager.create_test_from_template(template, variables)
        
        # Check that variables were replaced where possible
        assert "import pytest" in test_code
        assert "from app.calculator import add" in test_code
        assert "def test_add():" in test_code
        
        # The implementation may or may not replace missing variables, 
        # so we just verify the variables we provided were replaced
        assert "app.calculator" in test_code