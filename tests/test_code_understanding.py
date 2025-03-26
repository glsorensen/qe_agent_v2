import os
import ast
import pytest
import tempfile

from test_coverage_agent.test_generation.code_understanding import CodeUnderstandingModule, Function, Class


class TestCodeUnderstanding:
    """Tests for the CodeUnderstandingModule class."""
    
    @pytest.fixture
    def sample_code_file(self):
        """Create a temporary Python file with sample code."""
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(b"""
class Calculator:
    \"\"\"A simple calculator class.\"\"\"
    
    def __init__(self, initial_value=0):
        \"\"\"Initialize the calculator with a value.\"\"\"
        self.value = initial_value
    
    def add(self, x: int, y: int) -> int:
        \"\"\"Add two numbers.\"\"\"
        return x + y
    
    def subtract(self, x: int, y: int) -> int:
        \"\"\"Subtract y from x.\"\"\"
        return x - y

def multiply(x: int, y: int) -> int:
    \"\"\"Multiply two numbers.\"\"\"
    return x * y

def test_multiply():
    \"\"\"Test multiply function.\"\"\"
    assert multiply(2, 3) == 6
""")
            file_path = temp.name
        
        yield file_path
        
        # Clean up
        os.unlink(file_path)
    
    def test_function_init(self):
        """Test initializing a Function object."""
        function = Function(
            name="test_function",
            file_path="/path/to/file.py",
            line_start=10,
            line_end=15,
            code="def test_function():\n    pass",
            docstring="Test function docstring",
            params=["param1", "param2"],
            return_type="int",
            is_method=False
        )
        
        assert function.name == "test_function"
        assert function.file_path == "/path/to/file.py"
        assert function.line_start == 10
        assert function.line_end == 15
        assert function.code == "def test_function():\n    pass"
        assert function.docstring == "Test function docstring"
        assert function.params == ["param1", "param2"]
        assert function.return_type == "int"
        assert function.is_method is False
        assert function.class_name is None
    
    def test_class_init(self):
        """Test initializing a Class object."""
        methods = [
            Function(
                name="method1",
                file_path="/path/to/file.py",
                line_start=12,
                line_end=14,
                code="def method1(self):\n    pass",
                docstring="Method docstring",
                params=[],
                is_method=True,
                class_name="TestClass"
            )
        ]
        
        class_obj = Class(
            name="TestClass",
            file_path="/path/to/file.py",
            line_start=10,
            line_end=15,
            code="class TestClass:\n    pass",
            docstring="Class docstring",
            methods=methods,
            base_classes=["BaseClass"]
        )
        
        assert class_obj.name == "TestClass"
        assert class_obj.file_path == "/path/to/file.py"
        assert class_obj.line_start == 10
        assert class_obj.line_end == 15
        assert class_obj.code == "class TestClass:\n    pass"
        assert class_obj.docstring == "Class docstring"
        assert len(class_obj.methods) == 1
        assert class_obj.methods[0].name == "method1"
        assert class_obj.base_classes == ["BaseClass"]
    
    def test_code_understanding_init(self, sample_code_file):
        """Test initializing the CodeUnderstandingModule."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        assert module.repo_path == repo_path
        assert module.source_files == [sample_code_file]
        assert module.functions == {}
        assert module.classes == {}
    
    def test_analyze_python_file(self, sample_code_file):
        """Test analyzing a Python file."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        functions, classes = module.analyze_python_file(sample_code_file)
        
        # Check that we have at least the multiply function
        multiply_func = None
        for func in functions:
            if func.name == "multiply":
                multiply_func = func
                break
        
        assert multiply_func is not None
        assert multiply_func.docstring == "Multiply two numbers."
        assert multiply_func.params == ["x", "y"]
        assert multiply_func.return_type == "int"
        assert multiply_func.is_method is False
        
        # Check classes
        assert len(classes) >= 1
        calculator_class = None
        for cls in classes:
            if cls.name == "Calculator":
                calculator_class = cls
                break
                
        assert calculator_class is not None
        assert calculator_class.docstring == "A simple calculator class."
        
        # Check methods in the class
        assert len(classes[0].methods) == 3  # __init__, add, subtract
        
        # Check specific method
        add_method = None
        for method in classes[0].methods:
            if method.name == "add":
                add_method = method
                break
                
        assert add_method is not None
        assert add_method.docstring == "Add two numbers."
        assert add_method.params == ["x", "y"]
        assert add_method.return_type == "int"
        assert add_method.is_method is True
        assert add_method.class_name == "Calculator"
    
    def test_analyze_all_files(self, sample_code_file):
        """Test analyzing all files."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        module.analyze_all_files()
        
        # Check that functions and classes were stored
        assert len(module.functions) > 0  # We should have some functions
        assert len(module.classes) > 0  # We should have some classes
        
        # Check function and class names
        function_names = [func.name for func in module.functions.values()]
        class_names = [cls.name for cls in module.classes.values()]
        
        assert "multiply" in function_names
        assert "add" in function_names
        assert "subtract" in function_names
        assert "Calculator" in class_names
    
    def test_get_function_by_name(self, sample_code_file):
        """Test getting a function by name."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        module.analyze_all_files()
        
        function = module.get_function_by_name("multiply")
        
        assert function is not None
        assert function.name == "multiply"
        assert function.docstring == "Multiply two numbers."
        
        # Test getting a non-existent function
        function = module.get_function_by_name("non_existent")
        assert function is None
    
    def test_get_class_by_name(self, sample_code_file):
        """Test getting a class by name."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        module.analyze_all_files()
        
        class_obj = module.get_class_by_name("Calculator")
        
        assert class_obj is not None
        assert class_obj.name == "Calculator"
        assert class_obj.docstring == "A simple calculator class."
        
        # Test getting a non-existent class
        class_obj = module.get_class_by_name("non_existent")
        assert class_obj is None
    
    def test_get_dependencies(self, sample_code_file):
        """Test getting dependencies of a function."""
        # Create a file with dependencies
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(b"""
def helper_function(x):
    return x * 2

class Helper:
    def utility(self):
        return "utility"

def main_function():
    result = helper_function(5)
    helper = Helper()
    return result + len(helper.utility())
""")
            file_path = temp.name
        
        try:
            repo_path = os.path.dirname(file_path)
            module = CodeUnderstandingModule(repo_path, [file_path])
            
            module.analyze_all_files()
            
            main_function = module.get_function_by_name("main_function")
            dependencies = module.get_dependencies(main_function)
            
            assert "helper_function" in dependencies
            assert "Helper" in dependencies
            
        finally:
            # Clean up
            os.unlink(file_path)
    
    def test_get_all_functions(self, sample_code_file):
        """Test getting all functions."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        module.analyze_all_files()
        
        functions = module.get_all_functions()
        
        # Check that we have some functions
        assert len(functions) > 0
        
        # Check that we have the right functions
        function_names = [f.name for f in functions]
        assert "multiply" in function_names
        assert "add" in function_names
        assert "subtract" in function_names
    
    def test_get_all_classes(self, sample_code_file):
        """Test getting all classes."""
        repo_path = os.path.dirname(sample_code_file)
        module = CodeUnderstandingModule(repo_path, [sample_code_file])
        
        module.analyze_all_files()
        
        classes = module.get_all_classes()
        
        assert len(classes) == 1
        assert classes[0].name == "Calculator"