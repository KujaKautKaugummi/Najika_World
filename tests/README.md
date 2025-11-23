# Najika World Testing Suite

Comprehensive testing suite for backend and frontend components.

## 📋 Overview

This testing suite includes:
- **Backend Tests** (Python/Pytest) - API endpoints, database, services
- **Frontend Tests** (JavaScript/Jest) - UI components, utilities, systems
- **Integration Tests** - End-to-end workflows
- **Performance Tests** - Response times, load testing

## 🚀 Quick Start

### Backend Tests (Python)

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all backend tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_backend.py

# Run specific test class
pytest tests/test_backend.py::TestAuthentication

# Run specific test
pytest tests/test_backend.py::TestAuthentication::test_register_user
```

### Frontend Tests (JavaScript)

```bash
# Install test dependencies
npm install --save-dev jest @testing-library/jest-dom

# Run all frontend tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- tests/test_frontend.js

# Watch mode (re-run on file changes)
npm test -- --watch
```

## 📁 Test Structure

```
tests/
├── README.md                    # This file
├── test_backend.py              # Backend unit & integration tests
├── test_frontend.js             # Frontend unit tests
├── setup.js                     # Test setup/configuration
└── __mocks__/                   # Mock files for testing
```

## 🧪 Test Categories

### Backend Tests

1. **Authentication Tests**
   - User registration
   - Login/logout
   - Token validation
   - Password hashing

2. **User Tests**
   - Profile management
   - User CRUD operations
   - Permissions

3. **Character Tests**
   - Character creation
   - Leveling system
   - Stats management

4. **Battle System Tests**
   - Battle initialization
   - Attack mechanics
   - Victory/defeat logic
   - Rewards system

5. **Nemesis Arena Tests**
   - Monster creation
   - Rank promotion
   - Grudge system
   - Resurrection mechanics

6. **Finisher System Tests**
   - Category-based creation
   - Brutality/humor levels
   - Animation generation

7. **WebSocket Tests**
   - Connection handling
   - Message broadcasting
   - Channel subscriptions

8. **Admin Tests**
   - Admin endpoints
   - Statistics
   - User management

9. **Performance Tests**
   - API response times
   - Database query performance
   - Load testing

### Frontend Tests

1. **Resource Loader Tests**
   - Module loading
   - Caching
   - Statistics tracking

2. **Cache Manager Tests**
   - Cache operations
   - TTL expiration
   - LRU eviction

3. **Performance Monitor Tests**
   - FPS tracking
   - Frame time analysis
   - Warning system

4. **WebSocket Client Tests**
   - Connection management
   - Channel subscriptions
   - Event handling

5. **Particle System Tests**
   - Particle pooling
   - Emission limits
   - Performance

6. **Audio System Tests**
   - Audio pooling
   - Volume control
   - Sound limits

7. **Nemesis Arena UI Tests**
   - Monster display
   - Grudge visualization
   - Arena hierarchy

8. **Finisher System UI Tests**
   - Category selection
   - Ingredient input
   - Animation playback

9. **Admin Dashboard Tests**
   - View switching
   - Data loading
   - Statistics display

## 📊 Coverage Goals

| Component | Target Coverage | Current |
|-----------|----------------|---------|
| Backend API | 70%+ | TBD |
| Backend Services | 60%+ | TBD |
| Frontend UI | 50%+ | TBD |
| Frontend Utils | 70%+ | TBD |

## 🔧 Configuration Files

### pytest.ini
```ini
[pytest]
testpaths = tests
addopts = -v --tb=short --cov=backend --cov-report=html
```

### jest.config.js
```javascript
module.exports = {
    testEnvironment: 'jsdom',
    collectCoverageFrom: ['digivice/js/**/*.js'],
    coverageThreshold: { global: { lines: 40 } }
};
```

## 🏃 Continuous Integration

Tests run automatically on:
- Every commit to `main` branch
- All pull requests
- Scheduled daily runs

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      - name: Run tests
        run: pytest --cov=backend

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: 18
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test -- --coverage
```

## 🐛 Writing New Tests

### Backend Test Template

```python
def test_my_feature(db_session, test_user):
    """Test my new feature"""
    # Arrange
    data = {"key": "value"}

    # Act
    result = my_feature(data, test_user)

    # Assert
    assert result.success is True
    assert result.data == expected_data
```

### Frontend Test Template

```javascript
describe('MyComponent', () => {
    test('should do something', () => {
        // Arrange
        const component = new MyComponent();

        // Act
        const result = component.doSomething();

        // Assert
        expect(result).toBe(expected);
    });
});
```

## 📝 Best Practices

1. **Test Naming**
   - Use descriptive names: `test_user_can_login_with_valid_credentials`
   - Follow pattern: `test_<what>_<condition>_<result>`

2. **Test Structure**
   - Follow AAA pattern: Arrange, Act, Assert
   - One assertion per test (when possible)
   - Keep tests independent

3. **Test Data**
   - Use fixtures for common test data
   - Clean up after tests
   - Avoid hardcoded values

4. **Mocking**
   - Mock external dependencies
   - Mock slow operations
   - Use realistic mock data

5. **Coverage**
   - Aim for high coverage, but don't obsess
   - Focus on critical paths
   - Test edge cases

## 🔍 Debugging Tests

### Failed Test Investigation

```bash
# Run with more verbose output
pytest -vv tests/test_backend.py

# Run with print statements visible
pytest -s tests/test_backend.py

# Run with debugger on failure
pytest --pdb tests/test_backend.py

# Run only failed tests from last run
pytest --lf
```

### Common Issues

1. **Database Issues**
   - Ensure test database is clean
   - Check migrations are applied
   - Verify fixtures are created

2. **Import Errors**
   - Check Python path
   - Verify dependencies installed
   - Check circular imports

3. **Async Issues**
   - Use `@pytest.mark.asyncio` decorator
   - Ensure event loop is running
   - Check for proper await usage

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://testdriven.io/blog/modern-tdd/)

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain coverage above thresholds
4. Update this README if needed

## 📞 Support

If you encounter issues:
1. Check test logs
2. Verify dependencies
3. Review recent code changes
4. Ask in project Discord/Slack

---

**Last Updated:** 2025-01-17
**Maintainer:** Najika World Team
