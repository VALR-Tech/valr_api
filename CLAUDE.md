# VALR API Python Client Guidelines

## Commands
- Install: `pip install -e .` or `pip install valr-api`
- Build: `python -m build`
- Test all: `pytest`
- Test single: `pytest tests/test_file.py::TestClass::test_function`
- Coverage: `pytest --cov=valr_api`
- Lint: `flake8 valr_api tests`
- Type check: `mypy valr_api`
- Format: `black valr_api tests && isort valr_api tests`

## Code Style
- Docstrings: Use triple-quoted strings with parameter descriptions
- Type hints: Use modern Python typing (Optional, Union, Dict, List)
- Imports order: Standard library → third-party → local (sorted alphabetically)
- Naming: snake_case for functions/variables, PascalCase for classes
- Error handling: Use custom exception hierarchy (ValrApiError as base)
- Python 3.8+ support required