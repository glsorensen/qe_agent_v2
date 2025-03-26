import os
import re
from typing import Dict, List, Optional, Set, Any


class TestFramework:
    """Class representing a test framework."""
    
    def __init__(self, name: str, language: str):
        """Initialize a test framework.
        
        Args:
            name: Name of the framework
            language: Programming language
        """
        self.name = name
        self.language = language


class TestDetector:
    """Detector for test frameworks and test files in a repository."""
    
    def __init__(self, repo_path: str, source_files: List[str], test_files: List[str]):
        """Initialize the test detector.
        
        Args:
            repo_path: Path to the repository
            source_files: List of source code file paths
            test_files: List of test file paths
        """
        self.repo_path = repo_path
        self.source_files = source_files
        self.test_files = test_files
        self.detected_frameworks: Dict[str, TestFramework] = {}
        
        # Mapping of common test framework signatures
        self.framework_signatures = {
            'pytest': {
                'language': 'python',
                'patterns': [r'import\s+pytest', r'from\s+pytest', r'@pytest\.', r'assert\s+']
            },
            'unittest': {
                'language': 'python',
                'patterns': [r'import\s+unittest', r'from\s+unittest', r'class\s+\w+\(.*TestCase\)']
            },
            'jest': {
                'language': 'javascript',
                'patterns': [r'import\s+.*from\s+[\'|"]jest[\'|"]', r'jest\.', r'describe\(', r'it\(', r'test\(']
            },
            'mocha': {
                'language': 'javascript',
                'patterns': [r'import\s+.*from\s+[\'|"]mocha[\'|"]', r'describe\(', r'it\(', r'before\(']
            },
            'junit': {
                'language': 'java',
                'patterns': [r'import\s+org\.junit', r'@Test', r'Assert\.']
            },
            'testng': {
                'language': 'java',
                'patterns': [r'import\s+org\.testng', r'@Test', r'Assert\.']
            },
            'googletest': {
                'language': 'cpp',
                'patterns': [r'#include\s+[\"<]gtest', r'TEST\(', r'EXPECT_']
            },
            'rspec': {
                'language': 'ruby',
                'patterns': [r'require\s+[\'|"]rspec[\'|"]', r'describe\s+', r'it\s+', r'expect\(']
            }
        }
    
    def detect_test_frameworks(self) -> Dict[str, TestFramework]:
        """Detect test frameworks used in the repository.
        
        Returns:
            Dictionary mapping framework names to TestFramework objects
        """
        # Look for configuration files that indicate test frameworks
        config_indicators = {
            'pytest.ini': 'pytest',
            'conftest.py': 'pytest',
            'jest.config.js': 'jest',
            'karma.conf.js': 'karma',
            'phpunit.xml': 'phpunit',
            '.rspec': 'rspec'
        }
        
        # Check test files for framework patterns
        for test_file in self.test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for framework, info in self.framework_signatures.items():
                        if framework in self.detected_frameworks:
                            continue
                            
                        for pattern in info['patterns']:
                            if re.search(pattern, content):
                                self.detected_frameworks[framework] = TestFramework(
                                    name=framework,
                                    language=info['language']
                                )
                                break
            except (IOError, UnicodeDecodeError):
                continue
        
        # Check for config files
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file in config_indicators:
                    framework = config_indicators[file]
                    if framework not in self.detected_frameworks:
                        language = next(
                            (info['language'] for fw, info in self.framework_signatures.items() 
                             if fw == framework), 
                            'unknown'
                        )
                        self.detected_frameworks[framework] = TestFramework(name=framework, language=language)
        
        return self.detected_frameworks
    
    def get_test_files_by_framework(self) -> Dict[str, List[str]]:
        """Group test files by detected framework.
        
        Returns:
            Dictionary mapping framework names to lists of test files
        """
        if not self.detected_frameworks:
            self.detect_test_frameworks()
            
        result: Dict[str, List[str]] = {framework: [] for framework in self.detected_frameworks}
        result['unknown'] = []
        
        for test_file in self.test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    matched = False
                    for framework, info in self.framework_signatures.items():
                        if framework not in self.detected_frameworks:
                            continue
                            
                        for pattern in info['patterns']:
                            if re.search(pattern, content):
                                result[framework].append(test_file)
                                matched = True
                                break
                        
                        if matched:
                            break
                    
                    if not matched:
                        result['unknown'].append(test_file)
            except (IOError, UnicodeDecodeError):
                result['unknown'].append(test_file)
        
        # Remove empty entries
        return {k: v for k, v in result.items() if v}
    
    def analyze_test_structure(self) -> Dict[str, Any]:
        """Analyze the structure of tests in the repository.
        
        Returns:
            Dictionary with analysis results including:
            - test_count: Total number of test files
            - frameworks: Detected test frameworks
            - test_to_source_ratio: Ratio of test files to source files
            - files_by_framework: Test files grouped by framework
        """
        if not self.detected_frameworks:
            self.detect_test_frameworks()
            
        files_by_framework = self.get_test_files_by_framework()
        
        return {
            'test_count': len(self.test_files),
            'frameworks': list(self.detected_frameworks.keys()),
            'test_to_source_ratio': len(self.test_files) / max(len(self.source_files), 1),
            'files_by_framework': {k: len(v) for k, v in files_by_framework.items()}
        }