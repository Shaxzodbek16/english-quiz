# ✅ FastAPI Testing Strategy

This project uses a 3-level testing architecture to ensure reliability, scalability, and clean code. Below is the explanation of **Unit**, **Integration**, and **End-to-End (E2E)** tests with examples and structure.

---

## 🧪 Unit Tests

> Test individual functions or methods in isolation without any external dependencies (like DB, Redis, etc.)

**Example:**

```python
def test_hash_password():
    password = "secret"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
```

---

## 🔗 Integration Tests

> Test how multiple parts of the system (e.g., API + DB) work together. Useful to test actual request/response cycles, database transactions, etc.

**Example:**

```python
from httpx import AsyncClient

async def test_create_user(async_client: AsyncClient):
    response = await async_client.post("/users/", json={
        "username": "testuser",
        "password": "secure123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
```

---

## 🢍 End-to-End (E2E) Tests

> Simulate real user workflows by testing the entire system — from HTTP requests to DB responses, including auth flow, UI interactions (if any), etc.

**Example:**

```python
async def test_register_and_login(async_client: AsyncClient):
    await async_client.post("/register", json={"username": "a", "password": "123"})
    res = await async_client.post("/login", data={"username": "a", "password": "123"})
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert token
```

---

## 📊 Test Type Comparison

| Feature         | Unit Test              | Integration Test           | End-to-End (E2E) Test       |
|----------------|------------------------|-----------------------------|-----------------------------|
| Scope           | Single function         | Multiple modules/services   | Full app from user view     |
| Speed           | ⚡ Very Fast            | ⚠️ Medium                  | 🐃 Slow                     |
| Complexity      | 🔹 Low                  | 🔸 Medium                  | 🔺 High                     |
| Dependencies    | ❌ None                 | ✅ Some (DB, etc.)         | ✅ All (UI, APIs, DB)        |
| Use Case        | Business logic          | API + DB interaction        | Full user workflow          |

---

## 🧪 Testing Stack

| Layer         | Tools Used                                                   |
|---------------|--------------------------------------------------------------|
| Unit Tests     | `pytest`, `unittest`, `unittest.mock`                       |
| Integration    | `httpx.AsyncClient`, `pytest-asyncio`, test DB (Postgres)   |
| E2E Tests      | `httpx`, `docker-compose`, optionally `Playwright` or `Selenium` |

---

## 🚀 Structure (Recommended)

```
project/
│
├── app/
│   └── ...
├── tests/
│   ├── unit/
│   │   └── test_utils.py
│   ├── integration/
│   │   └── test_users.py
│   └── e2e/
│       └── test_full_flow.py
├── docker-compose.test.yml
└── README.md
```

---

## 🛠 Run Tests

**Run all tests:**

```bash
pytest
```

**Run a specific folder:**

```bash
pytest tests/integration/
```

**Run with coverage:**

```bash
pytest --cov=app
```

---

## 🧠 Pro Tip

Use `docker-compose` or `testcontainers` to spin up isolated DB/Redis environments for your integration & E2E tests.

---

Happy testing! 🧪🔥


**Note:** This is a simplified example. In a real-world scenario, you would also want to handle exceptions, edge cases, and possibly use fixtures for setup/teardown of test data.**

```python
# tests/unit/test_level_utils.py
import pytest
from app.api.repositories.levels import LevelRepository


@pytest.mark.asyncio
async def test_get_level_by_name_returns_correct_count(mocker):
    mock_session = mocker.Mock()
    repo = LevelRepository(mock_session)

    mock_session.execute.return_value.scalars.return_value.all.return_value = ["level1"]

    count = await repo.get_level_by_name("Test")

    assert count == 1
    mock_session.execute.assert_called_once()


# tests/integration/test_levels.py
import pytest
from app.api.schemas.levels import CreateLevelSchema


@pytest.mark.asyncio
async def test_create_and_get_level(db_session):
    from app.api.repositories.levels import LevelRepository

    repo = LevelRepository(db_session)
    test_level = CreateLevelSchema(name="Beginner")
    created = await repo.create_level(test_level)

    all_levels = await repo.get_all_levels()

    assert any(l.name == "Beginner" for l in all_levels)
    assert created.name == "Beginner"


# tests/e2e/test_levels.py
def test_full_level_flow(http_client):
    # Create level
    response = http_client.post("/levels/", json={"name": "Pro"})
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Pro"

    # Get all levels
    response = http_client.get("/levels/")
    assert response.status_code == 200
    levels = response.json()
    assert any(level["name"] == "Pro" for level in levels)

    # Update level
    level_id = created["id"]
    response = http_client.put(f"/levels/{level_id}/", json={"name": "Super Pro"})
    assert response.status_code == 200
    assert response.json()["name"] == "Super Pro"

    # Delete level
    response = http_client.delete(f"/levels/{level_id}/")
    assert response.status_code == 204

    # Verify deletion
    response = http_client.get(f"/levels/{level_id}/")
    assert response.status_code == 404
```