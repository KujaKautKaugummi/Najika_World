# Najika World - Code Style Guide

**Version:** 1.0.0
**Last Updated:** 2025-01-17

---

## Table of Contents

1. [Python Style Guide](#python-style-guide)
2. [JavaScript Style Guide](#javascript-style-guide)
3. [Git Commit Messages](#git-commit-messages)
4. [Documentation](#documentation)
5. [API Design](#api-design)

---

## Python Style Guide

### General Rules

- Follow **PEP 8** - Python's official style guide
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Maximum line length: **88 characters** (Black default)

### Code Formatting

```python
# ✅ Good
def calculate_damage(
    attacker_power: int,
    defender_defense: int,
    critical_hit: bool = False
) -> int:
    """
    Calculate battle damage.

    Args:
        attacker_power: Attacker's power stat
        defender_defense: Defender's defense stat
        critical_hit: Whether this is a critical hit

    Returns:
        Calculated damage value
    """
    base_damage = max(1, attacker_power - defender_defense)
    if critical_hit:
        base_damage *= 2
    return base_damage


# ❌ Bad
def calc_dmg(ap,dp,c=False):
    bd=max(1,ap-dp)
    if c: bd*=2
    return bd
```

### Naming Conventions

```python
# Classes: PascalCase
class TrainingScheduler:
    pass

# Functions and variables: snake_case
def get_user_by_id(user_id: int) -> User:
    current_user = ...
    return current_user

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com"

# Private methods: _leading_underscore
def _internal_helper():
    pass

# Type variables: PascalCase with T prefix
TModel = TypeVar('TModel')
```

### Imports

```python
# Order: Standard library, third-party, local
import os
import sys
from typing import List, Optional, Dict

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import numpy as np

from backend.config import settings
from backend.models import User, Character
from backend.services.training_launcher import TrainingLauncher
```

### Docstrings

```python
def create_training_job(
    db: Session,
    user_id: int,
    training_type: str,
    config: Dict[str, Any]
) -> TrainingJob:
    """
    Create a new training job.

    Creates a database record and adds the job to the training queue.

    Args:
        db: Database session
        user_id: ID of the user creating the job
        training_type: Type of training (lora, session, code, voice)
        config: Training configuration dictionary

    Returns:
        Created TrainingJob instance

    Raises:
        ValueError: If training_type is invalid
        DatabaseError: If database operation fails

    Example:
        >>> job = create_training_job(
        ...     db=db,
        ...     user_id=1,
        ...     training_type="lora",
        ...     config={"epochs": 3}
        ... )
        >>> print(job.id)
        42
    """
    # Implementation
    pass
```

### Error Handling

```python
# ✅ Good - Specific exceptions
try:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User {user_id} not found")
except ValueError as e:
    logger.error(f"Invalid user: {e}")
    raise
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    raise DatabaseError("Failed to retrieve user")

# ❌ Bad - Bare except
try:
    user = get_user(user_id)
except:
    pass
```

### Type Hints

```python
from typing import List, Optional, Dict, Any, Union, Callable

# Function type hints
def process_items(
    items: List[str],
    callback: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for item in items:
        result[item] = len(item)
    return result

# Class type hints
class TrainingJob:
    id: int
    user_id: int
    config: Dict[str, Any]
    status: str

    def __init__(self, user_id: int, config: Dict[str, Any]):
        self.user_id = user_id
        self.config = config
```

---

## JavaScript Style Guide

### General Rules

- Use **ES6+** syntax
- Use **const** for constants, **let** for variables
- Avoid **var**
- Use **arrow functions** for callbacks
- Maximum line length: **100 characters**

### Code Formatting

```javascript
// ✅ Good
const calculateDamage = (attackerPower, defenderDefense, criticalHit = false) => {
    const baseDamage = Math.max(1, attackerPower - defenderDefense);
    return criticalHit ? baseDamage * 2 : baseDamage;
};

// ❌ Bad
var calc_dmg=function(ap,dp,c){var bd=Math.max(1,ap-dp);if(c)bd*=2;return bd;}
```

### Naming Conventions

```javascript
// Classes: PascalCase
class BiomeSystem {
    constructor() {
        this.currentBiome = null;
    }
}

// Functions and variables: camelCase
function getUserById(userId) {
    const currentUser = users.find(u => u.id === userId);
    return currentUser;
}

// Constants: UPPER_SNAKE_CASE or camelCase
const MAX_RETRIES = 3;
const apiBaseUrl = "https://api.example.com";

// Private properties: _leadingUnderscore (convention)
class TrainingManager {
    constructor() {
        this._internalState = {};
    }

    _privateMethod() {
        // Internal use only
    }
}
```

### JSDoc Comments

```javascript
/**
 * Create a new training job
 *
 * @param {number} userId - User ID
 * @param {string} trainingType - Type of training
 * @param {Object} config - Training configuration
 * @param {number} config.epochs - Number of epochs
 * @param {number} config.batchSize - Batch size
 * @returns {Promise<TrainingJob>} Created training job
 * @throws {Error} If training type is invalid
 *
 * @example
 * const job = await createTrainingJob(1, 'lora', { epochs: 3 });
 * console.log(job.id);
 */
async function createTrainingJob(userId, trainingType, config) {
    // Implementation
}
```

### Async/Await

```javascript
// ✅ Good
async function loadUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const user = await response.json();
        return user;
    } catch (error) {
        console.error('Failed to load user:', error);
        throw error;
    }
}

// ❌ Bad - Callback hell
function loadUserData(userId, callback) {
    fetch(`/api/users/${userId}`, function(response) {
        response.json(function(user) {
            callback(null, user);
        }, function(error) {
            callback(error);
        });
    });
}
```

### Destructuring

```javascript
// ✅ Good
const { username, email, isAdmin } = user;
const [first, second, ...rest] = items;

// Function parameter destructuring
function createUser({ username, email, password }) {
    return { username, email, hashedPassword: hash(password) };
}

// ❌ Bad
const username = user.username;
const email = user.email;
const isAdmin = user.isAdmin;
```

### Arrow Functions

```javascript
// ✅ Good
const numbers = [1, 2, 3, 4, 5];

// Single expression
const doubled = numbers.map(n => n * 2);

// Multiple lines
const filtered = numbers.filter(n => {
    const isEven = n % 2 === 0;
    return isEven;
});

// ❌ Bad
const doubled = numbers.map(function(n) {
    return n * 2;
});
```

---

## Git Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat** - New feature
- **fix** - Bug fix
- **docs** - Documentation only
- **style** - Code style (formatting, no logic change)
- **refactor** - Code refactoring
- **perf** - Performance improvement
- **test** - Adding or fixing tests
- **chore** - Maintenance tasks

### Examples

```
# ✅ Good
feat(training): Add LoRA training scheduler

Implemented a priority-based training scheduler that supports:
- Job queueing with priority
- Scheduled (future) jobs
- Recurring training jobs
- Progress tracking

Closes #42

# ✅ Good
fix(api): Fix authentication token expiration

Token expiration was not being validated correctly, allowing
expired tokens to be used. Added proper expiration check.

Fixes #123

# ✅ Good
docs(readme): Update installation instructions

Added Docker deployment instructions and updated
dependency requirements.

# ❌ Bad
updated stuff
```

### Commit Size

- **Small commits** - One logical change per commit
- **Atomic** - Each commit should work independently
- **Descriptive** - Message explains what and why

---

## Documentation

### Code Comments

```python
# ✅ Good - Explain WHY, not WHAT
# Use exponential backoff to avoid overwhelming the API
# during network issues
retry_delay = base_delay * (2 ** attempt)

# ❌ Bad - Obvious comment
# Multiply base_delay by 2 to the power of attempt
retry_delay = base_delay * (2 ** attempt)
```

### README Structure

```markdown
# Project Name

Brief description (1-2 sentences)

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Quick Start

\`\`\`python
from module import function
result = function()
\`\`\`

## Documentation

- [API Documentation](docs/api.md)
- [Developer Guide](docs/developer.md)
- [Deployment Guide](docs/deployment.md)

## License

MIT License
```

---

## API Design

### RESTful URLs

```
# ✅ Good - Resource-based, plural nouns
GET    /api/v1/users              # List users
GET    /api/v1/users/123          # Get specific user
POST   /api/v1/users              # Create user
PUT    /api/v1/users/123          # Update user (full)
PATCH  /api/v1/users/123          # Update user (partial)
DELETE /api/v1/users/123          # Delete user

GET    /api/v1/users/123/characters   # Nested resource
POST   /api/v1/training/jobs           # Create training job

# ❌ Bad - Verbs in URL
POST   /api/v1/createUser
GET    /api/v1/getUserById/123
POST   /api/v1/deleteUser/123
```

### Response Format

```json
{
  "status": "success",
  "data": {
    "id": 123,
    "username": "najika",
    "email": "najika@example.com"
  },
  "message": "User retrieved successfully"
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid username format",
    "details": {
      "field": "username",
      "constraint": "min_length"
    }
  }
}
```

---

## Testing

### Test Naming

```python
# ✅ Good - Descriptive names
def test_user_registration_with_valid_data():
    pass

def test_user_registration_fails_with_duplicate_username():
    pass

def test_training_job_creation_adds_to_queue():
    pass

# ❌ Bad
def test_1():
    pass

def test_registration():
    pass
```

### Test Structure (Arrange-Act-Assert)

```python
def test_calculate_damage_with_critical_hit():
    # Arrange
    attacker_power = 50
    defender_defense = 20
    critical_hit = True

    # Act
    damage = calculate_damage(attacker_power, defender_defense, critical_hit)

    # Assert
    expected_damage = (50 - 20) * 2  # Critical multiplier
    assert damage == expected_damage
```

---

## Tools

### Recommended Tools

**Python:**
- **Black** - Code formatting
- **Flake8** - Linting
- **mypy** - Type checking
- **isort** - Import sorting
- **pytest** - Testing

**JavaScript:**
- **ESLint** - Linting
- **Prettier** - Code formatting
- **Jest** - Testing
- **JSDoc** - Documentation

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Format Python code
black backend/

# Sort imports
isort backend/

# Lint Python code
flake8 backend/

# Format JavaScript code
prettier --write digivice/

# Lint JavaScript
eslint digivice/
```

---

**Style Guide Version:** 1.0.0
**Last Updated:** 2025-01-17
**Status:** ✅ Complete
