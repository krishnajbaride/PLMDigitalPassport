# Contributing to ThreadPass PLM

Thank you for your interest in contributing to ThreadPass PLM! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Docker (optional)

### Local Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/PLMDigitalPassport.git
cd PLMDigitalPassport

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Copy environment template
cp .env.example .env

# 5. Run tests to verify setup
pytest

# 6. Start development server
uvicorn app.main:app --reload
```

Access the application:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update main branch
git fetch origin
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming Convention:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Adding/updating tests
- `chore/description` - Maintenance tasks

### 2. Make Your Changes

#### Code Style

We use automated tools to maintain consistent code style:

```bash
# Format code with black
black app tests

# Sort imports with isort
isort app tests

# Check style with flake8
flake8 app tests
```

#### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function arguments and returns
- Write clear, descriptive variable names
- Maximum line length: 120 characters
- Use docstrings for all public functions/classes

**Example:**

```python
def calculate_impact_score(
    affected_products: int,
    affected_components: int,
    cost_impact: float
) -> float:
    """
    Calculate overall impact score for a change.
    
    Args:
        affected_products: Number of products affected
        affected_components: Number of components affected
        cost_impact: Cost impact percentage
        
    Returns:
        Impact score between 0 and 100
    """
    base_score = (affected_products * 10) + (affected_components * 5)
    cost_factor = cost_impact / 10
    return min(base_score + cost_factor, 100)
```

### 3. Write/Update Tests

All new code must include tests. We aim for >80% coverage.

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_module.py::test_function -v
```

**Test Structure:**

```python
import pytest
from app.services import YourService

class TestYourService:
    """Test suite for YourService"""
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing"""
        return YourService()
    
    def test_happy_path(self, service):
        """Test successful operation"""
        result = service.do_something()
        assert result is not None
    
    def test_error_handling(self, service):
        """Test error scenarios"""
        with pytest.raises(ValueError):
            service.do_something_invalid()
```

### 4. Commit Your Changes

**Commit Message Format:**

```
<type>: <subject>

<body>

<footer>
```

**Type:**
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that don't affect code meaning (formatting, missing semicolons, etc)
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `perf:` Code change that improves performance
- `test:` Adding or updating tests
- `chore:` Changes to build process, dependencies, etc

**Examples:**

```bash
git commit -m "feat: Add CSV BOM import functionality"

git commit -m "fix: Resolve null pointer in change impact analysis

- Check for null values before processing
- Add validation tests
- Fixes #123"

git commit -m "docs: Update API documentation for parts endpoint"
```

### 5. Push and Create Pull Request

```bash
# Push branch to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

**Pull Request Template:**

Please fill out this information when creating a PR:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Breaking change

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe testing you performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] All tests pass locally

## Related Issues
Fixes #123
Related to #456
```

---

## Code Review Process

1. **Automated Checks:**
   - GitHub Actions runs tests automatically
   - Code quality tools check formatting
   - Security scanners run

2. **Peer Review:**
   - At least one maintainer reviews your code
   - Focus on logic, readability, and testing
   - All comments should be constructive

3. **Approval & Merge:**
   - After approval, maintainers will merge your PR
   - Your contribution is now part of ThreadPass PLM!

---

## Testing Guidelines

### Unit Tests
Test individual functions/methods in isolation:

```python
def test_parse_csv_with_valid_data():
    """Test parsing valid CSV data"""
    importer = CSVBOMImporter()
    result = importer.import_bom(valid_csv_bytes, "test.csv")
    assert result["success"] == True
    assert len(result["parts"]) > 0
```

### Integration Tests
Test how components work together:

```python
def test_create_bom_and_analyze_impact():
    """Test full workflow from BOM creation to impact analysis"""
    bom = create_test_bom()
    change = create_test_change()
    impact = analyze_change(change, bom)
    assert len(impact["affected_products"]) > 0
```

### API Tests
Test HTTP endpoints:

```python
def test_create_part_endpoint(client):
    """Test POST /api/v1/parts endpoint"""
    response = client.post("/api/v1/parts", json={
        "part_number": "TEST-001",
        "description": "Test Part"
    })
    assert response.status_code == 201
    assert response.json()["part_number"] == "TEST-001"
```

---

## Documentation

### Updating Documentation

1. Update relevant `.md` files in `docs/` or root
2. Keep documentation in sync with code changes
3. Include examples for new features
4. Update API documentation with endpoint changes

### Docstring Standard

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Short description of what the function does.
    
    Longer description with more details about behavior,
    edge cases, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
        
    Example:
        >>> result = function_name("input", 123)
        >>> print(result)
    """
    pass
```

---

## Development Tasks

### Good First Issues

Perfect for getting started:

- ✅ Add CSV BOM import functionality (v0.2)
- ✅ Add Excel BOM import (v0.2)
- ✅ Create Markdown export templates (v0.2)
- ✅ Add supplier search filtering (v0.2)
- ✅ Improve error messages
- ✅ Update documentation
- ✅ Fix reported bugs

### Medium Difficulty

- Add graph visualization components (v0.3)
- Implement scenario comparison UI (v0.3)
- Build authentication system (v0.4)
- Add database migrations (v0.4)

### Advanced Issues

- Implement ERP connectors (v1.0)
- Build policy engine (v1.0)
- Implement digital passport signing (v1.0)

---

## Performance Considerations

- **Database Queries:** Use indexing, avoid N+1 queries
- **API Response:** Keep under 2 seconds for ~1000 items
- **Memory:** Watch for memory leaks in long-running processes
- **Caching:** Use caching for frequently accessed data

---

## Security Guidelines

- ✅ Never commit secrets or API keys
- ✅ Validate all user inputs
- ✅ Use SQL parameterized queries (SQLAlchemy handles this)
- ✅ Sanitize data before storing
- ✅ Use HTTPS in production
- ✅ Keep dependencies updated
- ✅ Report security issues privately

---

## Getting Help

- **GitHub Issues:** Search for similar issues or create new one
- **GitHub Discussions:** Ask questions about contributing
- **Documentation:** Check DEVELOPMENT_SETUP.md and docs/
- **Code Examples:** Review existing implementation

---

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes for their version
- GitHub contributors page

---

## Additional Resources

- [Development Setup Guide](DEVELOPMENT_SETUP.md)
- [Architecture Overview](DEVELOPMENT_PHASES.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Best Practices](https://pep8.org/)
- [Git Workflow](https://docs.github.com/en/get-started/quickstart/github-flow)

---

## Questions?

Feel free to:
1. Check existing GitHub Issues
2. Start a GitHub Discussion
3. Comment on a Pull Request
4. Email the maintainers

We appreciate your contributions! 🎉
