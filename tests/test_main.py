import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the main module
from test_coverage_agent.main import main


@pytest.fixture
def mock_argparse():
    """Fixture to mock argparse.ArgumentParser"""
    with patch('argparse.ArgumentParser', autospec=True) as mock_parser_cls:
        mock_parser = MagicMock()
        mock_parser_cls.return_value = mock_parser
        mock_args = MagicMock()
        mock_parser.parse_args.return_value = mock_args
        yield mock_parser, mock_args


@pytest.fixture
def mock_cli():
    """Fixture to mock test_coverage_agent.ui.cli.cli"""
    with patch('test_coverage_agent.ui.cli.cli') as mock_cli:
        yield mock_cli


@pytest.fixture
def mock_subprocess():
    """Fixture to mock subprocess.run"""
    with patch('subprocess.run') as mock_run:
        yield mock_run


class TestMain:
    """Test cases for the main module"""

    def test_web_interface(self, mock_argparse, mock_subprocess):
        """Test starting the web interface"""
        # Setup
        mock_parser, mock_args = mock_argparse
        mock_args.web = True
        mock_args.repo_path = None

        # Execute
        main()

        # Verify
        mock_subprocess.assert_called_once()
        args, kwargs = mock_subprocess.call_args
        assert args[0][0] == 'streamlit'
        assert args[0][1] == 'run'
        assert 'web.py' in args[0][2]

    def test_cli_with_repo_path(self, mock_argparse, mock_cli):
        """Test CLI execution with repository path"""
        # Setup
        mock_parser, mock_args = mock_argparse
        mock_args.web = False
        mock_args.repo_path = '/path/to/repo'

        # Execute
        main()

        # Verify
        mock_cli.assert_called_once_with(['analyze', '/path/to/repo'])

    def test_print_help_without_repo_path(self, mock_argparse):
        """Test printing help when no repository path is provided"""
        # Setup
        mock_parser, mock_args = mock_argparse
        mock_args.web = False
        mock_args.repo_path = None

        # Execute
        main()

        # Verify
        mock_parser.print_help.assert_called_once()

    def test_argument_parsing(self):
        """Test argument parsing configuration"""
        # Use patch.object to inspect argument configuration without running parser
        with patch('argparse.ArgumentParser', autospec=True) as mock_parser_cls, \
             patch('test_coverage_agent.ui.web') as mock_web, \
             patch('test_coverage_agent.ui.cli.cli') as mock_cli:
            
            mock_parser = MagicMock()
            mock_parser_cls.return_value = mock_parser
            mock_args = MagicMock()
            mock_args.web = False
            mock_args.repo_path = None
            mock_parser.parse_args.return_value = mock_args
            
            # Execute the function
            main()
            
            # Verify argument configuration
            calls = mock_parser.add_argument.call_args_list
            arg_names = [call.args[0] if call.args else call.kwargs.get('dest', '') for call in calls]
            
            # Check for required and optional arguments
            assert 'repo_path' in str(arg_names)
            assert any('--api-key' in str(arg) or '-k' in str(arg) for arg in arg_names)
            assert any('--llm-provider' in str(arg) or '-p' in str(arg) for arg in arg_names)
            assert any('--output' in str(arg) or '-o' in str(arg) for arg in arg_names)
            assert any('--analyze-only' in str(arg) or '-a' in str(arg) for arg in arg_names)
            assert any('--web' in str(arg) or '-w' in str(arg) for arg in arg_names)