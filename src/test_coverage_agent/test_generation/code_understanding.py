import ast
import os
import re
from typing import Dict, List, Optional, Set, Tuple, Any


class Function:
    """Class representing a function or method in the codebase."""
    
    def __init__(
        self, 
        name: str, 
        file_path: str, 
        line_start: int, 
        line_end: int, 
        code: str,
        docstring: Optional[str] = None,
        params: List[str] = None,
        return_type: Optional[str] = None,
        is_method: bool = False,
        class_name: Optional[str] = None
    ):
        """Initialize a function or method.
        
        Args:
            name: Function or method name
            file_path: Path to the file containing the function
            line_start: Starting line number
            line_end: Ending line number
            code: Function source code
            docstring: Function docstring if available
            params: List of parameter names
            return_type: Return type annotation if available
            is_method: Whether this is a method of a class
            class_name: Name of the class if this is a method
        """
        self.name = name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.code = code
        self.docstring = docstring
        self.params = params or []
        self.return_type = return_type
        self.is_method = is_method
        self.class_name = class_name


class Class:
    """Class representing a class in the codebase."""
    
    def __init__(
        self, 
        name: str, 
        file_path: str, 
        line_start: int, 
        line_end: int, 
        code: str,
        docstring: Optional[str] = None,
        methods: List[Function] = None,
        base_classes: List[str] = None
    ):
        """Initialize a class.
        
        Args:
            name: Class name
            file_path: Path to the file containing the class
            line_start: Starting line number
            line_end: Ending line number
            code: Class source code
            docstring: Class docstring if available
            methods: List of class methods
            base_classes: List of base class names
        """
        self.name = name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.code = code
        self.docstring = docstring
        self.methods = methods or []
        self.base_classes = base_classes or []


class CodeUnderstandingModule:
    """Module for understanding code structure and extracting entities."""
    
    def __init__(self, repo_path: str, source_files: List[str]):
        """Initialize the code understanding module.
        
        Args:
            repo_path: Path to the repository
            source_files: List of source code file paths
        """
        self.repo_path = repo_path
        self.source_files = source_files
        self.functions: Dict[str, Function] = {}
        self.classes: Dict[str, Class] = {}
        
    def analyze_python_file(self, file_path: str) -> Tuple[List[Function], List[Class]]:
        """Analyze a Python file to extract functions and classes.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Tuple of (functions, classes) extracted from the file
        """
        functions: List[Function] = []
        classes: List[Class] = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                
            # Parse the Python file
            tree = ast.parse(file_content)
            
            # Extract file content as lines for reference
            file_lines = file_content.splitlines()
            
            # Extract functions and classes
            for node in ast.walk(tree):
                # Functions
                if isinstance(node, ast.FunctionDef):
                    # Skip test functions
                    if node.name.startswith('test_') or node.name.endswith('_test'):
                        continue
                        
                    # Extract function details
                    code_lines = file_lines[node.lineno-1:node.end_lineno]
                    func_code = '\n'.join(code_lines)
                    
                    # Extract docstring
                    docstring = ast.get_docstring(node)
                    
                    # Extract parameters
                    params = [arg.arg for arg in node.args.args]
                    
                    # Extract return type
                    return_type = None
                    if node.returns:
                        if isinstance(node.returns, ast.Name):
                            return_type = node.returns.id
                        elif isinstance(node.returns, ast.Subscript):
                            # Handle more complex return types (e.g., List[int])
                            try:
                                return_type = ast.unparse(node.returns)
                            except:
                                return_type = "complex_type"
                    
                    # Create function object
                    function = Function(
                        name=node.name,
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                        code=func_code,
                        docstring=docstring,
                        params=params,
                        return_type=return_type,
                        is_method=False
                    )
                    
                    functions.append(function)
                
                # Classes
                elif isinstance(node, ast.ClassDef):
                    # Extract class details
                    code_lines = file_lines[node.lineno-1:node.end_lineno]
                    class_code = '\n'.join(code_lines)
                    
                    # Extract docstring
                    docstring = ast.get_docstring(node)
                    
                    # Extract base classes
                    base_classes = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            base_classes.append(base.id)
                    
                    # Extract methods
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            # Skip test methods
                            if item.name.startswith('test_') or item.name.endswith('_test'):
                                continue
                                
                            # Extract method details
                            method_lines = file_lines[item.lineno-1:item.end_lineno]
                            method_code = '\n'.join(method_lines)
                            
                            # Extract docstring
                            method_docstring = ast.get_docstring(item)
                            
                            # Extract parameters (skip 'self')
                            params = [arg.arg for arg in item.args.args]
                            if params and (params[0] == 'self' or params[0] == 'cls'):
                                params = params[1:]
                            
                            # Extract return type
                            return_type = None
                            if item.returns:
                                if isinstance(item.returns, ast.Name):
                                    return_type = item.returns.id
                                elif isinstance(item.returns, ast.Subscript):
                                    try:
                                        return_type = ast.unparse(item.returns)
                                    except:
                                        return_type = "complex_type"
                            
                            # Create method object
                            method = Function(
                                name=item.name,
                                file_path=file_path,
                                line_start=item.lineno,
                                line_end=item.end_lineno,
                                code=method_code,
                                docstring=method_docstring,
                                params=params,
                                return_type=return_type,
                                is_method=True,
                                class_name=node.name
                            )
                            
                            methods.append(method)
                    
                    # Create class object
                    class_obj = Class(
                        name=node.name,
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                        code=class_code,
                        docstring=docstring,
                        methods=methods,
                        base_classes=base_classes
                    )
                    
                    classes.append(class_obj)
                    
            return functions, classes
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {str(e)}")
            return [], []
    
    def analyze_all_files(self) -> None:
        """Analyze all source files to extract functions and classes."""
        for file_path in self.source_files:
            if file_path.endswith('.py'):
                functions, classes = self.analyze_python_file(file_path)
                
                # Store functions
                for func in functions:
                    key = f"{os.path.relpath(file_path, self.repo_path)}::{func.name}"
                    self.functions[key] = func
                
                # Store classes
                for cls in classes:
                    key = f"{os.path.relpath(file_path, self.repo_path)}::{cls.name}"
                    self.classes[key] = cls
                    
                    # Also store methods
                    for method in cls.methods:
                        method_key = f"{os.path.relpath(file_path, self.repo_path)}::{cls.name}.{method.name}"
                        self.functions[method_key] = method
    
    def get_function_by_name(self, name: str) -> Optional[Function]:
        """Get a function by its name.
        
        Args:
            name: Function name to search for
            
        Returns:
            Function object if found, None otherwise
        """
        for key, func in self.functions.items():
            if func.name == name:
                return func
        return None
    
    def get_class_by_name(self, name: str) -> Optional[Class]:
        """Get a class by its name.
        
        Args:
            name: Class name to search for
            
        Returns:
            Class object if found, None otherwise
        """
        for key, cls in self.classes.items():
            if cls.name == name:
                return cls
        return None
    
    def get_dependencies(self, function: Function) -> List[str]:
        """Identify dependencies (other functions/classes) used by a function.
        
        Args:
            function: Function to analyze
            
        Returns:
            List of dependency names
        """
        dependencies = []
        
        # Extract function calls and class instantiations from the code
        for key, func in self.functions.items():
            if func.name != function.name and func.name in function.code:
                dependencies.append(func.name)
        
        for key, cls in self.classes.items():
            if cls.name in function.code:
                dependencies.append(cls.name)
        
        return dependencies
    
    def get_all_functions(self) -> List[Function]:
        """Get all extracted functions.
        
        Returns:
            List of all functions
        """
        return list(self.functions.values())
    
    def get_all_classes(self) -> List[Class]:
        """Get all extracted classes.
        
        Returns:
            List of all classes
        """
        return list(self.classes.values())