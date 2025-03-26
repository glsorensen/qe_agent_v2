import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class RepositoryScanner:
    """Scanner for code repositories that identifies and organizes files by type."""

    def __init__(self, repo_path: str):
        """Initialize the repository scanner.
        
        Args:
            repo_path: Path to the repository to scan
        """
        self.repo_path = os.path.abspath(repo_path)
        self.ignored_dirs = {'.git', '.github', '__pycache__', '.venv', 'venv', 'node_modules'}
        self.source_files: Dict[str, List[str]] = {}
        self.file_extensions: Set[str] = set()
        
    def scan(self) -> Dict[str, List[str]]:
        """Scan the repository and organize files by extension.
        
        Returns:
            Dictionary mapping file extensions to lists of file paths
        """
        for root, dirs, files in os.walk(self.repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                _, extension = os.path.splitext(file)
                
                if extension:
                    extension = extension[1:]  # Remove the dot
                    self.file_extensions.add(extension)
                    
                    if extension not in self.source_files:
                        self.source_files[extension] = []
                        
                    self.source_files[extension].append(file_path)
        
        return self.source_files
    
    def get_common_languages(self) -> Dict[str, List[str]]:
        """Identify common programming languages based on file extensions.
        
        Returns:
            Dictionary mapping languages to lists of file paths
        """
        if not self.source_files:
            self.scan()
            
        language_map = {
            'python': ['py', 'pyx', 'pyi'],
            'javascript': ['js', 'jsx', 'ts', 'tsx'],
            'java': ['java'],
            'c': ['c', 'h'],
            'cpp': ['cpp', 'hpp', 'cc', 'cxx'],
            'ruby': ['rb'],
            'go': ['go'],
            'rust': ['rs'],
            'php': ['php'],
            'csharp': ['cs'],
        }
        
        result = {}
        for lang, exts in language_map.items():
            lang_files = []
            for ext in exts:
                if ext in self.source_files:
                    lang_files.extend(self.source_files[ext])
            
            if lang_files:
                result[lang] = lang_files
                
        return result
    
    def get_source_and_test_files(self) -> Tuple[List[str], List[str]]:
        """Separate source code files from test files.
        
        Returns:
            Tuple of (source files, test files)
        """
        if not self.source_files:
            self.scan()
            
        source_files = []
        test_files = []
        
        test_indicators = ['test_', '_test', 'spec', 'Test', 'Spec']
        test_dirs = ['test', 'tests', 'spec', 'specs', 'testing']
        
        for files in self.source_files.values():
            for file_path in files:
                rel_path = os.path.relpath(file_path, self.repo_path)
                file_name = os.path.basename(file_path)
                path_parts = Path(rel_path).parts
                
                # Check if file is in a test directory or has a test name pattern
                is_test = any(part.lower() in test_dirs for part in path_parts)
                if not is_test:
                    is_test = any(indicator in file_name for indicator in test_indicators)
                
                if is_test:
                    test_files.append(file_path)
                else:
                    source_files.append(file_path)
        
        return source_files, test_files

    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get the content of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content as string or None if file can't be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, UnicodeDecodeError):
            # Handle binary files or encoding issues
            return None