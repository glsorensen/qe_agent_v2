import os
import pytest
import tempfile
from pathlib import Path

from test_coverage_agent.repository.scanner import RepositoryScanner


class TestRepositoryScanner:
    """Tests for the RepositoryScanner class."""
    
    @pytest.fixture
    def sample_repo(self):
        """Create a temporary sample repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some source files
            os.makedirs(os.path.join(temp_dir, "src"), exist_ok=True)
            with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
                f.write("def hello_world():\n    return 'Hello, World!'\n")
                
            with open(os.path.join(temp_dir, "src", "utils.py"), "w") as f:
                f.write("def add(a, b):\n    return a + b\n")
            
            # Create some test files
            os.makedirs(os.path.join(temp_dir, "tests"), exist_ok=True)
            with open(os.path.join(temp_dir, "tests", "test_main.py"), "w") as f:
                f.write("def test_hello_world():\n    assert hello_world() == 'Hello, World!'\n")
            
            # Create some ignored directories and files
            os.makedirs(os.path.join(temp_dir, ".git"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "__pycache__"), exist_ok=True)
            
            yield temp_dir
    
    def test_scan(self, sample_repo):
        """Test scanning a repository."""
        scanner = RepositoryScanner(sample_repo)
        
        # Test scanning
        files = scanner.scan()
        
        # Check that we have the right number of files
        assert "py" in files
        assert len(files["py"]) == 3  # main.py, utils.py, test_main.py
        
        # Verify file paths
        file_paths = {os.path.basename(f) for f in files["py"]}
        assert "main.py" in file_paths
        assert "utils.py" in file_paths
        assert "test_main.py" in file_paths
    
    def test_get_common_languages(self, sample_repo):
        """Test identifying common languages."""
        scanner = RepositoryScanner(sample_repo)
        scanner.scan()
        
        languages = scanner.get_common_languages()
        
        # Check that Python is detected
        assert "python" in languages
        assert len(languages["python"]) == 3  # main.py, utils.py, test_main.py
    
    def test_get_source_and_test_files(self, sample_repo):
        """Test separating source and test files."""
        scanner = RepositoryScanner(sample_repo)
        scanner.scan()
        
        source_files, test_files = scanner.get_source_and_test_files()
        
        # Check counts
        assert len(source_files) == 2  # main.py, utils.py
        assert len(test_files) == 1  # test_main.py
        
        # Check specific files
        source_basenames = {os.path.basename(f) for f in source_files}
        test_basenames = {os.path.basename(f) for f in test_files}
        
        assert "main.py" in source_basenames
        assert "utils.py" in source_basenames
        assert "test_main.py" in test_basenames
    
    def test_get_file_content(self, sample_repo):
        """Test reading file content."""
        scanner = RepositoryScanner(sample_repo)
        
        # Test reading a file that exists
        main_path = os.path.join(sample_repo, "src", "main.py")
        content = scanner.get_file_content(main_path)
        
        assert content is not None
        assert "def hello_world()" in content
        
        # Test reading a file that doesn't exist
        nonexistent_path = os.path.join(sample_repo, "nonexistent.py")
        content = scanner.get_file_content(nonexistent_path)
        
        assert content is None