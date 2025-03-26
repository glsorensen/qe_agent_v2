# Migrating to src Layout

This document describes how to migrate the project from a flat layout to a src-based layout.

## Benefits of src Layout

1. **Prevents import errors**: No accidental imports from the development environment
2. **Clearer separation**: Package code is clearly separated from tests and other files
3. **Best practices**: Follows PEP 517/518 standards and modern Python packaging practices
4. **Prevents circular imports**: Makes import structure more explicit

## Migration Steps

1. Move the existing modules to the src structure:

```bash
# Move modules
mv repository/ src/test_coverage_agent/
mv test_execution/ src/test_coverage_agent/
mv test_generation/ src/test_coverage_agent/
mv ui/ src/test_coverage_agent/
mv main.py src/test_coverage_agent/
```

2. Update imports in all Python files to use the new package name:

```python
# Before
from repository import RepositoryScanner
from test_execution import TestRunner

# After
from test_coverage_agent.repository import RepositoryScanner
from test_coverage_agent.test_execution import TestRunner
```

3. Update pyproject.toml to use the src layout (see src/pyproject.toml.example)

4. Update run.py to import from the package (see src/run.py.example)

5. Install the package in development mode:

```bash
pip install -e .
```

## Testing After Migration

After migration, run the tests to ensure everything works:

```bash
pytest tests/
```

## CI Configuration

Update GitHub Actions workflow to use the src layout:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install pytest flake8 mypy black
    python -m pip install -e .
```