import os
import sys
import click
from typing import Dict, List, Optional, Tuple, Any
import json

# Import necessary components
from test_coverage_agent.repository import RepositoryScanner, TestDetector, CoverageAnalyzer
from test_coverage_agent.test_generation import CodeUnderstandingModule, TestTemplateManager, AIPoweredTestWriter
from test_coverage_agent.test_execution import TestRunner, TestValidator, CoverageReporter


@click.group()
def cli():
    """Test Coverage Enhancement Agent - CLI Interface"""
    pass


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Path to save the analysis report')
def analyze(repo_path: str, output: Optional[str] = None):
    """Analyze a repository for test coverage."""
    click.echo(f"Analyzing repository: {repo_path}")
    
    # Initialize scanner
    scanner = RepositoryScanner(repo_path)
    click.echo("Scanning repository files...")
    scanner.scan()
    
    # Get source and test files
    source_files, test_files = scanner.get_source_and_test_files()
    click.echo(f"Found {len(source_files)} source files and {len(test_files)} test files")
    
    # Detect test frameworks
    click.echo("Detecting test frameworks...")
    detector = TestDetector(repo_path, source_files, test_files)
    frameworks = detector.detect_test_frameworks()
    
    click.echo(f"Detected test frameworks: {', '.join(frameworks.keys()) or 'None'}")
    
    # Analyze test structure
    test_analysis = detector.analyze_test_structure()
    test_ratio = test_analysis['test_to_source_ratio']
    click.echo(f"Test to source ratio: {test_ratio:.2f}")
    
    # Analyze coverage if possible
    click.echo("Analyzing test coverage...")
    analyzer = CoverageAnalyzer(repo_path, source_files, test_files)
    
    # Try to use detected frameworks
    framework = next(iter(frameworks.keys()), 'pytest')
    coverage_info = analyzer.run_coverage_analysis(framework)
    
    coverage_percentage = coverage_info['coverage_percentage']
    click.echo(f"Overall coverage: {coverage_percentage:.2f}%")
    click.echo(f"Covered files: {len(coverage_info['covered_files'])}")
    click.echo(f"Partially covered files: {len(coverage_info['partially_covered_files'])}")
    click.echo(f"Uncovered files: {len(coverage_info['uncovered_files'])}")
    
    # Save report if output path is provided
    if output:
        report = {
            'repo_path': repo_path,
            'source_files_count': len(source_files),
            'test_files_count': len(test_files),
            'test_to_source_ratio': test_ratio,
            'detected_frameworks': list(frameworks.keys()),
            'coverage_percentage': coverage_percentage,
            'covered_files_count': len(coverage_info['covered_files']),
            'partially_covered_files_count': len(coverage_info['partially_covered_files']),
            'uncovered_files_count': len(coverage_info['uncovered_files']),
            'uncovered_files': [os.path.relpath(f, repo_path) for f in coverage_info['uncovered_files']]
        }
        
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        click.echo(f"Analysis report saved to: {output}")


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--api-key', '-k', required=True, help='API key for LLM provider')
@click.option('--llm-provider', '-p', type=click.Choice(['claude', 'gemini']), default='claude', help='LLM provider to use')
@click.option('--output-dir', '-o', help='Directory to save generated tests')
@click.option('--limit', '-l', type=int, help='Limit the number of tests to generate')
def generate(repo_path: str, api_key: str, llm_provider: str = 'claude', output_dir: Optional[str] = None, limit: Optional[int] = None):
    """Generate tests for uncovered or poorly covered code."""
    click.echo(f"Generating tests for repository: {repo_path}")
    
    # Initialize scanner
    scanner = RepositoryScanner(repo_path)
    click.echo("Scanning repository files...")
    scanner.scan()
    
    # Get source and test files
    source_files, test_files = scanner.get_source_and_test_files()
    click.echo(f"Found {len(source_files)} source files and {len(test_files)} test files")
    
    # Detect test frameworks
    click.echo("Detecting test frameworks...")
    detector = TestDetector(repo_path, source_files, test_files)
    frameworks = detector.detect_test_frameworks()
    
    if not frameworks:
        click.echo("No test frameworks detected. Defaulting to pytest.")
        framework = "pytest"
    else:
        # Use the first detected framework
        framework = next(iter(frameworks.keys()))
        click.echo(f"Using detected framework: {framework}")
    
    # Analyze coverage
    click.echo("Analyzing test coverage...")
    analyzer = CoverageAnalyzer(repo_path, source_files, test_files)
    coverage_info = analyzer.run_coverage_analysis(framework)
    
    # Identify coverage gaps
    click.echo("Identifying coverage gaps...")
    gaps = analyzer.identify_coverage_gaps()
    
    priority_files = gaps['priority_files']
    if limit and limit < len(priority_files):
        priority_files = priority_files[:limit]
    
    click.echo(f"Found {len(priority_files)} files with coverage gaps")
    
    # Initialize code understanding module
    click.echo("Analyzing code structure...")
    code_understanding = CodeUnderstandingModule(repo_path, source_files)
    code_understanding.analyze_all_files()
    
    # Initialize test template manager
    template_manager = TestTemplateManager()
    
    # Initialize test writer
    click.echo(f"Initializing AI-powered test writer with {llm_provider}...")
    test_writer = AIPoweredTestWriter(api_key, code_understanding, template_manager, llm_provider)
    
    # Initialize test validator
    test_validator = TestValidator(repo_path, api_key, llm_provider)
    
    # Generate tests for priority files
    generated_tests = {}
    validation_results = {}
    
    with click.progressbar(priority_files, label='Generating tests') as files:
        for file_path in files:
            # Check if file is a Python file
            if not file_path.endswith('.py'):
                continue
                
            # Get file content
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Get classes and functions in file
            rel_path = os.path.relpath(file_path, repo_path)
            functions = []
            classes = []
            
            for func in code_understanding.get_all_functions():
                if func.file_path == file_path and not func.is_method:
                    functions.append(func)
            
            for cls in code_understanding.get_all_classes():
                if cls.file_path == file_path:
                    classes.append(cls)
            
            # Generate tests for functions
            for function in functions:
                if not function.name.startswith('_'):  # Skip private functions
                    test_code = test_writer.generate_function_test(function, framework)
                    
                    # Validate test
                    validation = test_validator.validate_test(test_code, function.code, "python", run_test=False)
                    
                    # Create test file path
                    if output_dir:
                        module_path = rel_path.replace('/', '.').replace('\\', '.')
                        if module_path.endswith('.py'):
                            module_path = module_path[:-3]
                        
                        # Create test file name
                        if framework == 'pytest':
                            test_file_name = f"test_{os.path.basename(file_path)}"
                        else:
                            test_file_name = f"{os.path.basename(file_path)[:-3]}_test.py"
                        
                        # Create test directory
                        test_dir = os.path.join(output_dir, os.path.dirname(rel_path))
                        os.makedirs(test_dir, exist_ok=True)
                        
                        # Write test file
                        test_file_path = os.path.join(test_dir, test_file_name)
                        with open(test_file_path, 'w', encoding='utf-8') as f:
                            f.write(test_code)
                        
                        # Store test
                        generated_tests[test_file_path] = test_code
                        validation_results[test_file_path] = {
                            'is_valid': validation.is_valid,
                            'issues': validation.issues,
                            'suggestions': validation.suggestions
                        }
                    else:
                        # Just store in memory
                        test_key = f"{rel_path}::{function.name}"
                        generated_tests[test_key] = test_code
                        validation_results[test_key] = {
                            'is_valid': validation.is_valid,
                            'issues': validation.issues,
                            'suggestions': validation.suggestions
                        }
            
            # Generate tests for classes
            for cls in classes:
                test_code = test_writer.generate_class_test(cls, framework)
                
                # Validate test
                validation = test_validator.validate_test(test_code, cls.code, "python", run_test=False)
                
                # Create test file path
                if output_dir:
                    module_path = rel_path.replace('/', '.').replace('\\', '.')
                    if module_path.endswith('.py'):
                        module_path = module_path[:-3]
                    
                    # Create test file name
                    if framework == 'pytest':
                        test_file_name = f"test_{os.path.basename(file_path)}"
                    else:
                        test_file_name = f"{os.path.basename(file_path)[:-3]}_test.py"
                    
                    # Create test directory
                    test_dir = os.path.join(output_dir, os.path.dirname(rel_path))
                    os.makedirs(test_dir, exist_ok=True)
                    
                    # Write test file
                    test_file_path = os.path.join(test_dir, test_file_name)
                    with open(test_file_path, 'w', encoding='utf-8') as f:
                        f.write(test_code)
                    
                    # Store test
                    generated_tests[test_file_path] = test_code
                    validation_results[test_file_path] = {
                        'is_valid': validation.is_valid,
                        'issues': validation.issues,
                        'suggestions': validation.suggestions
                    }
                else:
                    # Just store in memory
                    test_key = f"{rel_path}::{cls.name}"
                    generated_tests[test_key] = test_code
                    validation_results[test_key] = {
                        'is_valid': validation.is_valid,
                        'issues': validation.issues,
                        'suggestions': validation.suggestions
                    }
    
    # Generate coverage report
    click.echo("Generating coverage report...")
    reporter = CoverageReporter(repo_path)
    
    report = reporter.generate_report(
        overall_coverage=coverage_info['coverage_percentage'],
        file_coverage={file: 0.0 for file in priority_files},  # Placeholder
        uncovered_files=coverage_info['uncovered_files'],
        generated_tests=generated_tests,
        validation_results=validation_results
    )
    
    # Save report
    report_path = reporter.save_report(report)
    click.echo(f"Report saved to: {report_path}")
    
    # Summary
    click.echo(f"\nSummary:")
    click.echo(f"Generated {len(generated_tests)} tests")
    
    valid_tests = sum(1 for result in validation_results.values() if result['is_valid'])
    click.echo(f"Valid tests: {valid_tests} ({valid_tests / max(len(validation_results), 1) * 100:.2f}%)")
    
    if output_dir:
        click.echo(f"Tests saved to: {output_dir}")


if __name__ == '__main__':
    cli()