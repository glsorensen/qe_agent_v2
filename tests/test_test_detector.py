import os
import pytest
import tempfile
from pathlib import Path

from test_coverage_agent.repository.scanner import RepositoryScanner
from test_coverage_agent.repository.test_detector import TestDetector, TestFramework


class TestTestDetector:
    """Tests for the TestDetector class."""
    
    @pytest.fixture
    def pytest_repo(self):
        """Create a temporary repository with pytest tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some source files
            os.makedirs(os.path.join(temp_dir, "src"), exist_ok=True)
            with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
                f.write("def hello_world():\n    return 'Hello, World!'\n")
            
            # Create pytest test files
            os.makedirs(os.path.join(temp_dir, "tests"), exist_ok=True)
            with open(os.path.join(temp_dir, "tests", "test_main.py"), "w") as f:
                f.write("""
import pytest
from src.main import hello_world

def test_hello_world():
    assert hello_world() == 'Hello, World!'
""")
            
            # Create pytest config file
            with open(os.path.join(temp_dir, "pytest.ini"), "w") as f:
                f.write("[pytest]\naddopts = -v\n")
            
            yield temp_dir
    
    @pytest.fixture
    def unittest_repo(self):
        """Create a temporary repository with unittest tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some source files
            os.makedirs(os.path.join(temp_dir, "src"), exist_ok=True)
            with open(os.path.join(temp_dir, "src", "calculator.py"), "w") as f:
                f.write("""
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
""")
            
            # Create unittest test files
            os.makedirs(os.path.join(temp_dir, "tests"), exist_ok=True)
            with open(os.path.join(temp_dir, "tests", "test_calculator.py"), "w") as f:
                f.write("""
import unittest
from src.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(1, 2), 3)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 2), 3)

if __name__ == '__main__':
    unittest.main()
""")
            
            yield temp_dir
    
    def test_detect_pytest_framework(self, pytest_repo):
        """Test detecting pytest framework."""
        scanner = RepositoryScanner(pytest_repo)
        scanner.scan()
        source_files, test_files = scanner.get_source_and_test_files()
        
        detector = TestDetector(pytest_repo, source_files, test_files)
        frameworks = detector.detect_test_frameworks()
        
        assert "pytest" in frameworks
        assert frameworks["pytest"].language == "python"
    
    def test_detect_unittest_framework(self, unittest_repo):
        """Test detecting unittest framework."""
        scanner = RepositoryScanner(unittest_repo)
        scanner.scan()
        source_files, test_files = scanner.get_source_and_test_files()
        
        detector = TestDetector(unittest_repo, source_files, test_files)
        frameworks = detector.detect_test_frameworks()
        
        assert "unittest" in frameworks
        assert frameworks["unittest"].language == "python"
    
    def test_get_test_files_by_framework(self, pytest_repo, unittest_repo):
        """Test grouping test files by framework."""
        # Test with pytest repo
        scanner = RepositoryScanner(pytest_repo)
        scanner.scan()
        source_files, test_files = scanner.get_source_and_test_files()
        
        detector = TestDetector(pytest_repo, source_files, test_files)
        detector.detect_test_frameworks()
        test_files_by_framework = detector.get_test_files_by_framework()
        
        assert "pytest" in test_files_by_framework
        assert len(test_files_by_framework["pytest"]) == 1
        
        # Test with unittest repo
        scanner = RepositoryScanner(unittest_repo)
        scanner.scan()
        source_files, test_files = scanner.get_source_and_test_files()
        
        detector = TestDetector(unittest_repo, source_files, test_files)
        detector.detect_test_frameworks()
        test_files_by_framework = detector.get_test_files_by_framework()
        
        assert "unittest" in test_files_by_framework
        assert len(test_files_by_framework["unittest"]) == 1
    
    def test_analyze_test_structure(self, pytest_repo, unittest_repo):
        """Test analyzing test structure."""
        # Test with pytest repo
        scanner = RepositoryScanner(pytest_repo)
        scanner.scan()
        source_files, test_files = scanner.get_source_and_test_files()
        
        detector = TestDetector(pytest_repo, source_files, test_files)
        detector.detect_test_frameworks()
        analysis = detector.analyze_test_structure()
        
        assert analysis["test_count"] == 1
        assert "pytest" in analysis["frameworks"]
        assert analysis["test_to_source_ratio"] == 0.5  # 1 test file / 2 source files
        assert "pytest" in analysis["files_by_framework"]