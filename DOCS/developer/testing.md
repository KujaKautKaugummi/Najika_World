# Najika World - Testing Guide

**Version:** 1.0.0
**Last Updated:** 2025-01-17

---

## Testing Overview

Najika World uses a comprehensive testing strategy covering:
- **Backend Tests** - pytest for Python backend
- **Frontend Tests** - Jest for JavaScript/Three.js
- **Integration Tests** - End-to-end workflows
- **Performance Tests** - Load testing and benchmarks

---

## Backend Testing (pytest)

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_user_registration

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto
```

### Test Structure

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db, Base, engine

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_user_registration(test_db):
    """Test user registration endpoint"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert "access_token" in response.json()
```

---

## Frontend Testing (Jest)

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- test_biome_system.js

# Watch mode
npm test -- --watch
```

### Test Example

```javascript
// tests/test_biome_system.js
describe('BiomeSystem', () => {
    let scene, camera, biomeSystem;

    beforeEach(() => {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera();
        biomeSystem = new BiomeSystem(scene, camera);
    });

    test('should load biomes from data', () => {
        const biomeData = {
            biomes: {
                forest: { name: "Forest", colors: { ground: "#228B22" } }
            }
        };

        biomeSystem.loadBiomes(biomeData);

        expect(biomeSystem.biomes.size).toBe(1);
        expect(biomeSystem.biomes.get('forest').name).toBe("Forest");
    });
});
```

---

## Integration Testing

### Example Integration Test

```python
def test_training_job_workflow(test_db):
    """Test complete training job workflow"""
    # 1. Register user
    register_response = client.post(
        "/api/v1/auth/register",
        json={"username": "trainer", "password": "pass123", "email": "t@test.com"}
    )
    token = register_response.json()["access_token"]

    # 2. Create training job
    create_response = client.post(
        "/api/v1/training/jobs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "job_name": "Test Job",
            "training_type": "lora",
            "config": {"epochs": 1}
        }
    )
    job_id = create_response.json()["id"]
    assert create_response.status_code == 201

    # 3. Check job status
    status_response = client.get(
        f"/api/v1/training/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert status_response.json()["status"] == "queued"
```

---

## Test Coverage Goals

- **Backend:** 80%+ coverage
- **Frontend:** 70%+ coverage
- **Integration:** Core workflows covered
- **E2E:** Critical paths tested

---

**Testing Guide Version:** 1.0.0
**Status:** ✅ Complete
