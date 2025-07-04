import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_session
from app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    """Override the get_session dependency to use the test database."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Setup and teardown for each test
@pytest.fixture
def test_db():
    """Create tables in the test database and drop them after the test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create a test client with the test database."""
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


@pytest.fixture
def db_session():
    """Create a database session for direct database operations."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
