import os
import tempfile
import streamlit as st
import json
from typing import Dict, List, Optional, Set, Tuple, Any

# Import necessary components
from test_coverage_agent.repository import RepositoryScanner, TestDetector, CoverageAnalyzer
from test_coverage_agent.test_generation import CodeUnderstandingModule, TestTemplateManager, AIPoweredTestWriter
from test_coverage_agent.test_execution import TestRunner, TestValidator, CoverageReporter


def main():
    """Streamlit web interface for the Test Coverage Enhancement Agent."""
    st.set_page_config(
        page_title="Test Coverage Enhancement Agent",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("Test Coverage Enhancement Agent")
    st.write("AI-powered test coverage enhancement for your code repositories")
    
    # Sidebar
    st.sidebar.title("Configuration")
    
    # LLM provider selection
    llm_provider = st.sidebar.selectbox(
        "LLM Provider",
        ["claude", "gemini"],
        index=0
    )
    
    # API key input
    api_key_label = "Claude API Key" if llm_provider == "claude" else "Gemini API Key"
    api_key = st.sidebar.text_input(api_key_label, type="password")
    
    # Repository path input
    repo_path = st.sidebar.text_input("Repository Path", value="")
    
    # Option to use a sample repository
    use_sample = st.sidebar.checkbox("Use sample repository")
    if use_sample:
        repo_path = "/Users/gunnar.sorensen/Documents/taskstream"  # Sample repository path
    
    # Main section tabs
    tab1, tab2, tab3 = st.tabs(["Repository Analysis", "Test Generation", "Results & Reports"])
    
    # Tab 1: Repository Analysis
    with tab1:
        st.header("Repository Analysis")
        
        if st.button("Analyze Repo", disabled=not repo_path, key="analyze_repo_button"):
            if not os.path.exists(repo_path):
                st.error(f"Repository path does not exist: {repo_path}")
                return
            
            with st.spinner("Analyzing repository..."):
                # Initialize scanner
                scanner = RepositoryScanner(repo_path)
                st.write("Scanning repository files...")
                scanner.scan()
                
                # Get source and test files
                source_files, test_files = scanner.get_source_and_test_files()
                
                # Display file stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Source Files", len(source_files))
                with col2:
                    st.metric("Test Files", len(test_files))
                with col3:
                    if len(source_files) > 0:
                        test_ratio = len(test_files) / len(source_files)
                        st.metric("Test Ratio", f"{test_ratio:.2f}")
                    else:
                        st.metric("Test Ratio", "N/A")
                
                # Detect test frameworks
                st.write("Detecting test frameworks...")
                detector = TestDetector(repo_path, source_files, test_files)
                frameworks = detector.detect_test_frameworks()
                
                st.write("Detected test frameworks:")
                if frameworks:
                    for name, framework in frameworks.items():
                        st.write(f"- {name} ({framework.language})")
                else:
                    st.write("No test frameworks detected")
                
                # Analyze test structure
                test_analysis = detector.analyze_test_structure()
                
                # Store analysis results in session state
                st.session_state.repo_analysis = {
                    'repo_path': repo_path,
                    'source_files': source_files,
                    'test_files': test_files,
                    'frameworks': frameworks,
                    'test_analysis': test_analysis
                }
                
                # Analyze coverage if possible
                st.write("Analyzing test coverage...")
                try:
                    analyzer = CoverageAnalyzer(repo_path, source_files, test_files)
                    
                    # Try to use detected frameworks
                    framework = next(iter(frameworks.keys()), 'pytest')
                    coverage_info = analyzer.run_coverage_analysis(framework)
                    
                    # Store coverage info in session state
                    st.session_state.coverage_info = coverage_info
                    
                    # Display coverage stats
                    st.subheader("Coverage Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Overall Coverage", f"{coverage_info['coverage_percentage']:.2f}%")
                    with col2:
                        st.metric("Covered Files", len(coverage_info['covered_files']))
                    with col3:
                        st.metric("Uncovered Files", len(coverage_info['uncovered_files']))
                    
                    # Show uncovered files
                    if coverage_info['uncovered_files']:
                        with st.expander("Uncovered Files"):
                            for file in coverage_info['uncovered_files']:
                                st.write(os.path.relpath(file, repo_path))
                    
                    # Identify coverage gaps
                    gaps = analyzer.identify_coverage_gaps()
                    st.session_state.gaps = gaps
                    
                except Exception as e:
                    st.error(f"Error analyzing coverage: {str(e)}")
        
        # Display saved analysis results
        if hasattr(st.session_state, 'repo_analysis'):
            analysis = st.session_state.repo_analysis
            
            st.success(f"Repository analysis completed for: {analysis['repo_path']}")
            
            # Re-display stats if we're returning to this tab
            if not st.button("Analyze Repository", disabled=not repo_path, key="analyze_repo_again_button"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Source Files", len(analysis['source_files']))
                with col2:
                    st.metric("Test Files", len(analysis['test_files']))
                with col3:
                    if len(analysis['source_files']) > 0:
                        test_ratio = len(analysis['test_files']) / len(analysis['source_files'])
                        st.metric("Test Ratio", f"{test_ratio:.2f}")
                    else:
                        st.metric("Test Ratio", "N/A")
                
                if hasattr(st.session_state, 'coverage_info'):
                    coverage_info = st.session_state.coverage_info
                    
                    st.subheader("Coverage Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Overall Coverage", f"{coverage_info['coverage_percentage']:.2f}%")
                    with col2:
                        st.metric("Covered Files", len(coverage_info['covered_files']))
                    with col3:
                        st.metric("Uncovered Files", len(coverage_info['uncovered_files']))
    
    # Tab 2: Test Generation
    with tab2:
        st.header("Test Generation")
        
        # Check if we have analysis results
        if hasattr(st.session_state, 'repo_analysis') and hasattr(st.session_state, 'coverage_info'):
            analysis = st.session_state.repo_analysis
            coverage_info = st.session_state.coverage_info
            
            # Configuration options
            st.subheader("Generation Options")
            
            col1, col2 = st.columns(2)
            with col1:
                # Number of tests to generate
                if hasattr(st.session_state, 'gaps'):
                    gaps = st.session_state.gaps
                    max_files = len(gaps['priority_files'])
                    num_files = st.slider("Number of files to generate tests for", 1, max(max_files, 1), min(5, max_files))
                else:
                    num_files = st.slider("Number of files to generate tests for", 1, 5, 3)
            
            with col2:
                # Framework selection
                if analysis['frameworks']:
                    framework_options = list(analysis['frameworks'].keys())
                    framework = st.selectbox("Test framework", framework_options)
                else:
                    framework_options = ["pytest", "unittest", "jest"]
                    framework = st.selectbox("Test framework", framework_options)
            
            # API key check
            if not api_key:
                st.warning(f"Please enter your {llm_provider.capitalize()} API key in the sidebar to generate tests")
            
            # Generate button
            if st.button("Generate Tests", disabled=not api_key):
                with st.spinner("Generating tests..."):
                    try:
                        repo_path = analysis['repo_path']
                        source_files = analysis['source_files']
                        
                        # Get priority files
                        if hasattr(st.session_state, 'gaps'):
                            gaps = st.session_state.gaps
                            priority_files = gaps['priority_files'][:num_files]
                        else:
                            # Default to uncovered files
                            priority_files = coverage_info['uncovered_files'][:num_files]
                        
                        # Initialize code understanding module
                        code_understanding = CodeUnderstandingModule(repo_path, source_files)
                        code_understanding.analyze_all_files()
                        
                        # Initialize test template manager
                        template_manager = TestTemplateManager()
                        
                        # Initialize test writer
                        test_writer = AIPoweredTestWriter(api_key, code_understanding, template_manager, llm_provider)
                        
                        # Initialize test validator
                        test_validator = TestValidator(repo_path, api_key, llm_provider)
                        
                        # Generate tests
                        generated_tests = {}
                        validation_results = {}
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, file_path in enumerate(priority_files):
                            status_text.write(f"Generating tests for {os.path.relpath(file_path, repo_path)}")
                            
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
                                    
                                    # Store test
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
                                
                                # Store test
                                test_key = f"{rel_path}::{cls.name}"
                                generated_tests[test_key] = test_code
                                validation_results[test_key] = {
                                    'is_valid': validation.is_valid,
                                    'issues': validation.issues,
                                    'suggestions': validation.suggestions
                                }
                            
                            # Update progress
                            progress_bar.progress((i + 1) / len(priority_files))
                        
                        # Store generated tests in session state
                        st.session_state.generated_tests = generated_tests
                        st.session_state.validation_results = validation_results
                        
                        # Generate report
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
                        st.session_state.report_path = report_path
                        
                        status_text.success(f"Generated {len(generated_tests)} tests")
                    
                    except Exception as e:
                        st.error(f"Error generating tests: {str(e)}")
            
            # Display generated tests
            if hasattr(st.session_state, 'generated_tests'):
                generated_tests = st.session_state.generated_tests
                validation_results = st.session_state.validation_results
                
                st.subheader("Generated Tests")
                
                # Summary
                valid_tests = sum(1 for result in validation_results.values() if result['is_valid'])
                st.metric("Valid Tests", f"{valid_tests}/{len(validation_results)} ({valid_tests / max(len(validation_results), 1) * 100:.2f}%)")
                
                # Test viewer
                for test_key, test_code in generated_tests.items():
                    with st.expander(test_key):
                        st.code(test_code, language="python")
                        
                        # Show validation results
                        if test_key in validation_results:
                            validation = validation_results[test_key]
                            if validation['is_valid']:
                                st.success("Test is valid")
                            else:
                                st.warning("Test has issues:")
                                for issue in validation['issues']:
                                    st.write(f"- {issue}")
                                
                                if validation['suggestions']:
                                    st.write("Suggestions:")
                                    for suggestion in validation['suggestions']:
                                        st.write(f"- {suggestion}")
                
                # Export option
                if st.button("Export Tests"):
                    # Create a temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Write tests to files
                        for test_key, test_code in generated_tests.items():
                            # Parse test key to get file path and entity name
                            parts = test_key.split("::")
                            rel_path = parts[0]
                            entity_name = parts[1]
                            
                            # Create test file name
                            if framework == 'pytest':
                                test_file_name = f"test_{os.path.basename(rel_path)}"
                            else:
                                base_name = os.path.basename(rel_path)
                                if base_name.endswith('.py'):
                                    base_name = base_name[:-3]
                                test_file_name = f"{base_name}_test.py"
                            
                            # Create test directory
                            test_dir = os.path.join(temp_dir, os.path.dirname(rel_path))
                            os.makedirs(test_dir, exist_ok=True)
                            
                            # Write test file
                            test_file_path = os.path.join(test_dir, test_file_name)
                            with open(test_file_path, 'w', encoding='utf-8') as f:
                                f.write(test_code)
                        
                        # Create a zip file
                        import shutil
                        zip_path = os.path.join(temp_dir, "generated_tests.zip")
                        shutil.make_archive(zip_path[:-4], 'zip', temp_dir)
                        
                        # Offer download
                        with open(zip_path, "rb") as f:
                            st.download_button(
                                label="Download Tests",
                                data=f,
                                file_name="generated_tests.zip",
                                mime="application/zip"
                            )
        else:
            st.info("Please analyze a repository first in the Repository Analysis tab")
    
    # Tab 3: Results & Reports
    with tab3:
        st.header("Results & Reports")
        
        if hasattr(st.session_state, 'report_path'):
            report_path = st.session_state.report_path
            st.success(f"Report generated: {os.path.basename(report_path)}")
            
            # Display report summary
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    if report_path.endswith('.json'):
                        report_data = json.load(f)
                        
                        # Show summary stats
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Overall Coverage", f"{report_data['overall_coverage']:.2f}%")
                        with col2:
                            st.metric("Generated Tests", report_data['generated_tests_count'])
                        with col3:
                            st.metric("Validation Success", f"{report_data['validation_success_rate']:.2f}%")
                        
                        # Show report details
                        with st.expander("Report Details"):
                            st.json(report_data)
                    else:
                        # Text report
                        st.text(f.read())
            except Exception as e:
                st.error(f"Error loading report: {str(e)}")
            
            # Download report
            with open(report_path, "rb") as f:
                st.download_button(
                    label="Download Report",
                    data=f,
                    file_name=os.path.basename(report_path),
                    mime="application/octet-stream"
                )
        else:
            st.info("No reports generated yet. Generate tests in the Test Generation tab to create a report.")


if __name__ == "__main__":
    main()