import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, StaticPool

from src.common.storage.db_storage import get_session
from src.server.server import app

# This file contains fixtures for the tests that can be accessed by any test file


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_session] = lambda: test_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
