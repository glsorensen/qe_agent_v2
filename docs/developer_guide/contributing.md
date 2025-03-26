# Contributing Guidelines

Thank you for your interest in contributing to the Test Coverage Agent! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate of others when participating in this project.

## Getting Started

Before contributing, please:

1. **Read the documentation**: Familiarize yourself with the existing documentation, especially the [Developer Guide](./index.md) and [Code Structure](./code_structure.md) documents.

2. **Set up your development environment**: Follow the instructions in the [Development Setup](./development_setup.md) guide.

3. **Check existing issues**: Look for open issues, especially those labeled "good first issue" or "help wanted."

## Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fixing issues in the existing codebase
- **Feature implementations**: Adding new functionality
- **Documentation improvements**: Enhancing or correcting documentation
- **Test additions**: Improving test coverage
- **Performance optimizations**: Making the code run faster or use fewer resources
- **Code quality improvements**: Refactoring for better maintainability

## Contribution Process

### 1. Find or Create an Issue

- Search for existing issues that you'd like to work on
- If you have a new idea or found a bug, create a new issue describing it
- Wait for the issue to be approved or assigned to you before starting work

### 2. Fork and Clone the Repository

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/test-coverage-agent.git
cd test-coverage-agent
git remote add upstream https://github.com/originalowner/test-coverage-agent.git
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the work you're doing, such as:
- `feature/add-xml-report-format`
- `bugfix/fix-test-detection-regex`
- `docs/improve-extending-guide`

### 4. Make Your Changes

- Follow the [code style guidelines](#code-style-guidelines)
- Keep your changes focused on a single issue
- Write clear, descriptive commit messages
- Add or update tests as necessary
- Update documentation to reflect your changes

### 5. Write Tests

All new features and bug fixes should include appropriate tests:

```bash
# Run existing tests to ensure they pass
pytest tests/

# Add your own tests
# Example: Add tests for a new feature in the coverage analyzer
touch tests/test_coverage_analyzer_new_feature.py
```

### 6. Ensure Code Quality

Before submitting a pull request, make sure your code passes all checks:

```bash
# Format your code
black test-coverage-agent/ tests/

# Run the linter
flake8 test-coverage-agent/ tests/

# Run type checking
mypy test-coverage-agent/ tests/

# Run all tests
pytest tests/
```

### 7. Push Changes and Create Pull Request

```bash
git add .
git commit -m "Add descriptive commit message"
git push origin feature/your-feature-name
```

Then, go to GitHub and create a pull request against the main repository:

- Use a clear, descriptive title
- Reference the issue number in the description
- Provide a detailed description of the changes
- Complete the provided pull request template

### 8. Code Review

- Be responsive to feedback and questions
- Make requested changes promptly
- Keep the pull request updated if the main branch changes
- Be patient—reviewers are often busy

## Code Style Guidelines

We follow the style guidelines outlined in [CLAUDE.md](../CLAUDE.md), which include:

### Python Coding Style

- Use [Black](https://black.readthedocs.io/) for code formatting with a line length of 88 characters
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions
- Use 4 spaces for indentation (no tabs)
- Use type hints for all function parameters and return values
- Use Google-style docstrings for all public methods and functions

### Documentation Style

- Use clear, concise language
- Include examples where appropriate
- Keep documentation up to date with code changes
- Use Markdown for all documentation files

### Commit Message Style

- Use the imperative mood ("Add feature" not "Added feature")
- Include the issue number if applicable
- Keep the subject line under 50 characters
- Provide a detailed description in the commit body if necessary

Example:
```
Add XML report format (#123)

- Implement XML reporter in coverage_reporter.py
- Add unit tests for XML report generation
- Update documentation with XML format details
```

## Testing Guidelines

- Write tests for all new features and bug fixes
- Aim for high test coverage, especially for critical components
- Use pytest fixtures for test setup
- Mock external dependencies when necessary
- Test edge cases and error conditions

## Documentation Guidelines

- Update documentation for all user-facing changes
- Write documentation with both new and experienced users in mind
- Include code examples for complex features
- Ensure documentation is accurate and complete

## Review Process

Pull requests will be reviewed by project maintainers. We look for:

- Code quality and adherence to style guidelines
- Appropriate test coverage
- Clear, comprehensive documentation
- Focused, discrete changes that address a single concern

## Continuous Integration

The project uses continuous integration to automatically run tests and checks on pull requests:

- All tests must pass
- Code must meet linting standards
- Type checking must pass
- Test coverage should not decrease

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the project's license (MIT).

## Recognition

Contributors will be acknowledged in the project's documentation and release notes.

## Getting Help

If you need help with the contribution process or have questions, you can:

- Comment on the relevant issue
- Contact the project maintainers
- Join the project's communication channels (if available)

Thank you for contributing to the Test Coverage Agent!