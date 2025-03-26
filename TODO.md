# TODO List for Test Coverage Agent

## Test Improvements

### High Priority
- [ ] Fix and implement CLI command tests in `test_real_cli.py`:
  - [ ] Implement proper mocking for filesystem operations in `test_generate_command`
  - [ ] Implement proper mocking for filesystem operations in `test_generate_with_limit` 
- [ ] Fix AI-powered test generation tests in `test_test_writer.py`:
  - [ ] Properly mock AI responses for `test_generate_test_with_ai_fallback`

### Medium Priority
- [ ] Address pytest collection warnings for classes with `__init__` constructors:
  - [ ] Rename test classes to avoid collisions with implementation classes
  - [ ] Consider using pytest naming conventions to avoid these warnings
- [ ] Improve test coverage for `template_manager.py` (currently at 29%)
- [ ] Improve test coverage for `web.py` (currently at 4%)

### Lower Priority
- [ ] Add tests for edge cases in `test_coverage_agent/ui/cli.py`
- [ ] Add integration tests that test multiple components together

## Code Improvements

- [ ] Refactor `web.py` to make it more testable
- [ ] Standardize error handling across all modules
- [ ] Consider breaking down complex methods into smaller, more testable functions
- [ ] Review naming conventions for consistency across the codebase
- [ ] Add more type annotations to improve static type checking