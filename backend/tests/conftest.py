import os
from pathlib import Path

TEST_DATABASE = Path(__file__).resolve().parents[2] / "test-api.sqlite3"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE.as_posix()}"
os.environ["JWT_SECRET"] = "test-only-secret"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def authenticated_client(client):
    response = client.post("/api/auth/register", json={"email": "test@example.com", "full_name": "Test User", "password": "TestPass123!"})
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client, token


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    TEST_DATABASE.unlink(missing_ok=True)
