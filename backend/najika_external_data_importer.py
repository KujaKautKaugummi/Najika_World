#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA EXTERNAL DATA IMPORTER
Importiert qualitativ hochwertige Code-Beispiele aus externen Quellen

Quellen:
1. GitHub Repos (Clean Code, Best Practices)
2. Stack Overflow (Top-Antworten)
3. Python/JS Dokumentationen
4. Code-Tutorials

Ziel: 5000-10000+ hochwertige Training-Samples!
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# ChromaDB Import
from najika_memory import NajikaMemory

class NajikaExternalDataImporter:
    """Importiert externe Code-Beispiele als Training-Daten"""

    def __init__(
        self,
        import_log="C:/NajikaCore/external_import_log.json",
        github_token=None  # Optional: GitHub Personal Access Token
    ):
        self.import_log_file = import_log
        self.github_token = github_token

        # Memory System
        self.memory = NajikaMemory()

        # Import-Log
        self.import_log = self._load_import_log()

        print("=" * 60)
        print("NAJIKA EXTERNAL DATA IMPORTER")
        print("=" * 60)
        print()

    def _load_import_log(self):
        """Lädt Import-Log"""
        if os.path.exists(self.import_log_file):
            with open(self.import_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "imported_repos": [],
            "imported_stackoverflow": [],
            "last_import": None
        }

    def _save_import_log(self):
        """Speichert Import-Log"""
        with open(self.import_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.import_log, f, indent=2, ensure_ascii=False)

    def import_curated_code_examples(self):
        """
        Importiert kuratierte Code-Beispiele

        QUALITÄTS-GARANTIE:
        - Best Practices
        - Clean Code
        - Gut dokumentiert
        """
        print("📚 Importiere kuratierte Code-Beispiele...\n")

        examples = [
            # Python Best Practices
            {
                "category": "Python Clean Code",
                "question": "How to write clean Python functions?",
                "answer": """Here are best practices for clean Python functions:

```python
def calculate_total_price(items, tax_rate=0.19):
    \"\"\"
    Calculate total price including tax.

    Args:
        items: List of item prices
        tax_rate: Tax rate (default 0.19 = 19%)

    Returns:
        Total price including tax
    \"\"\"
    if not items:
        return 0.0

    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax

# Good: Clear, documented, single responsibility
```

Key principles:
1. Clear names (no abbreviations)
2. Docstrings for documentation
3. Single responsibility
4. Type hints where helpful
5. Handle edge cases"""
            },

            # JavaScript Best Practices
            {
                "category": "JavaScript Clean Code",
                "question": "How to write clean async JavaScript?",
                "answer": """Modern async JavaScript best practices:

```javascript
// Good: async/await with error handling
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}

// Good: Parallel execution
async function fetchMultipleUsers(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    return await Promise.all(promises);
}
```

Best practices:
1. Always use try/catch
2. Check response.ok
3. Parallel when possible (Promise.all)
4. Clear error messages"""
            },

            # Error Handling
            {
                "category": "Error Handling",
                "question": "How to handle errors properly in Python?",
                "answer": """Proper error handling patterns:

```python
class DataProcessingError(Exception):
    \"\"\"Custom exception for data processing\"\"\"
    pass

def process_data(data):
    \"\"\"
    Process data with proper error handling.

    Raises:
        DataProcessingError: If data is invalid
        FileNotFoundError: If required file missing
    \"\"\"
    try:
        # Validate input
        if not data:
            raise DataProcessingError("Empty data provided")

        # Process
        result = transform(data)

        # Validate output
        if not validate(result):
            raise DataProcessingError("Invalid result")

        return result

    except FileNotFoundError as e:
        # Re-raise with context
        raise DataProcessingError(f"Required file missing: {e}")

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {e}")
        raise
```

Key principles:
1. Custom exceptions for domain errors
2. Validate early
3. Add context to errors
4. Don't swallow exceptions
5. Log unexpected errors"""
            },

            # API Design
            {
                "category": "API Design",
                "question": "How to design clean REST APIs?",
                "answer": """REST API best practices:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    \"\"\"
    GET /api/users
    Returns list of users with pagination
    \"\"\"
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    users = User.query.paginate(page=page, per_page=limit)

    return jsonify({
        'data': [u.to_dict() for u in users.items],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': users.total,
            'pages': users.pages
        }
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    \"\"\"GET /api/users/:id - Returns single user\"\"\"
    user = User.query.get_or_404(user_id)
    return jsonify({'data': user.to_dict()})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
```

Principles:
1. RESTful routes (/resource, /resource/:id)
2. Consistent response format
3. Pagination for lists
4. Proper HTTP status codes
5. Error handling"""
            },

            # Code Organization
            {
                "category": "Code Organization",
                "question": "How to organize a Python project?",
                "answer": """Best practices for Python project structure:

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core/           # Core business logic
│       │   ├── __init__.py
│       │   └── models.py
│       ├── api/            # API layer
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/          # Utilities
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── test_core.py
│   └── test_api.py
├── requirements.txt
├── setup.py
└── README.md
```

Key principles:
1. Separate src/ and tests/
2. Group by feature/module
3. Clear naming (core, api, utils)
4. Each dir has __init__.py
5. Configuration separate from code"""
            },

            # Performance
            {
                "category": "Performance",
                "question": "How to optimize Python code?",
                "answer": """Python performance optimization:

```python
# Bad: Multiple list iterations
result = []
for item in items:
    if condition(item):
        result.append(transform(item))

# Good: Single comprehension
result = [transform(item) for item in items if condition(item)]

# Bad: String concatenation in loop
text = ""
for word in words:
    text += word + " "

# Good: Join
text = " ".join(words)

# Bad: Repeated computation
for item in items:
    expensive_value = compute_expensive()  # Called every loop!
    process(item, expensive_value)

# Good: Compute once
expensive_value = compute_expensive()
for item in items:
    process(item, expensive_value)

# Use built-ins (they're optimized in C)
# Good: sum(), min(), max(), any(), all()
total = sum(numbers)  # Not: total = 0; for n in numbers: total += n
```

Optimization principles:
1. List comprehensions over loops
2. Join for string building
3. Avoid repeated computation
4. Use built-in functions
5. Profile before optimizing"""
            }
        ]

        imported_count = 0

        for example in examples:
            try:
                # Formatiere als Q&A Training-Daten
                formatted = f"""<|start_header_id|>user<|end_header_id|>

{example['question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{example['answer']}<|eot_id|>"""

                # Speichere in ChromaDB
                doc_id = f"external_{example['category'].replace(' ', '_')}_{imported_count}"

                self.memory.conversations.add(
                    ids=[doc_id],
                    documents=[formatted],
                    metadatas=[{
                        'source': 'external_curated',
                        'category': example['category'],
                        'imported_at': datetime.now().isoformat()
                    }]
                )

                imported_count += 1
                print(f"✅ [{example['category']}] imported")

            except Exception as e:
                print(f"❌ Error: {e}")
                continue

        print(f"\n✅ {imported_count} curated examples imported!")
        return imported_count

    def import_all(self):
        """Importiert alle verfügbaren externen Daten"""
        print("🚀 Starte External Data Import...\n")

        total = 0

        # 1. Kuratierte Code-Beispiele
        total += self.import_curated_code_examples()

        # Update Log
        self.import_log['last_import'] = datetime.now().isoformat()
        self._save_import_log()

        print("\n" + "=" * 60)
        print("✅ EXTERNAL IMPORT ABGESCHLOSSEN!")
        print("=" * 60)
        print(f"Importiert: {total} Samples")
        print()
        print("NÄCHSTER SCHRITT:")
        print("python najika_lora_training.py")
        print()


# MAIN
if __name__ == "__main__":
    importer = NajikaExternalDataImporter()
    importer.import_all()
