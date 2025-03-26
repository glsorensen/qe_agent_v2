# Migrating to src Layout

This document describes the migration of the Test Coverage Agent project from a flat layout to a src-based layout.

## Benefits of src Layout

1. **Prevents import errors**: No accidental imports from the development environment
2. **Clearer separation**: Package code is clearly separated from tests and other files
3. **Best practices**: Follows PEP 517/518 standards and modern Python packaging practices
4. **Prevents circular imports**: Makes import structure more explicit

## Changes Made in This Migration

1. Moved all source code to a src-based structure:
   ```
   src/
   └── test_coverage_agent/
       ├── __init__.py
       ├── main.py
       ├── repository/
       ├── test_execution/
       ├── test_generation/
       └── ui/
   ```

2. Updated all imports to use the package name:
   ```python
   # Before
   from repository import RepositoryScanner
   from test_execution import TestRunner

   # After
   from test_coverage_agent.repository import RepositoryScanner
   from test_coverage_agent.test_execution import TestRunner
   ```

3. Updated the test suite to work with the new structure:
   - All test imports now reference the full package path
   - All mocks and patches updated to use the correct module paths

4. Updated documentation to reflect new package structure

## Using the New Package

After this migration, there are two ways to run the tool:

1. Using the run.py entry script:
   ```bash
   python run.py /path/to/your/repo
   ```

2. Using the module directly:
   ```bash
   python -m test_coverage_agent.main /path/to/your/repo
   ```

## Installation

The project should now be installed as a package:

```bash
pip install -e .
```

This ensures that imports work correctly for both development and production use.

## For Developers

If you're developing features for the Test Coverage Agent:

1. Always use the full package path in imports:
   ```python
   from test_coverage_agent.repository import RepositoryScanner
   ```

2. Run tests using pytest after installing the package:
   ```bash
   pip install -e .
   pytest tests/
   ```

3. When creating new modules, place them in the appropriate directory under `src/test_coverage_agent/`