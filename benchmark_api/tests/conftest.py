import pytest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from src.config import settings
from src.create_app import create_app
from src.database import Base, get_db
from src.repositories.benchmark import BenchmarkRepository
from src.core.cache import RedisCache


@pytest.fixture(scope="session")
def engine():
    _ = create_engine(settings.get_database_url("postgres"))

    TEST_DB_URL = settings.get_database_url("test_db")

    if not database_exists(TEST_DB_URL):
        create_database(TEST_DB_URL)

    engine = create_engine(TEST_DB_URL)
    yield engine
    drop_database(TEST_DB_URL)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session(engine, tables):
    """
    A pytest fixture that creates a database session object.

    Args:
        engine: A SQLAlchemy engine object, which is used to connect to the database.
        tables: A pytest fixture that creates the database tables.

    Yields:
        Session: A SQLAlchemy session object, which is used to interact with the database.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """
    A pytest fixture that creates a FastAPI test client instance.

    Args:
        db_session (Session): A SQLAlchemy session object, which is used to interact with the database.

    Yields:
        TestClient: A FastAPI test client instance, which is used to make HTTP requests to the application.
    """
    app = create_app(False)

    app.dependency_overrides[get_db] = lambda: db_session

    client = TestClient(
        app,
        headers={"X-API-Key": settings.API_KEY},
    )
    yield client


@pytest.fixture
def mock_db_session():
    """
    A pytest fixture that returns a mock SQLAlchemy ORM session.

    Returns:
        Session: A mock SQLAlchemy ORM session.
    """
    return MagicMock(spec=Session)


@pytest.fixture
def mock_cache() -> BenchmarkRepository:
    """
    A pytest fixture that returns a mock RedisCache instance.

    Returns:
        BenchmarkRepository: A mock RedisCache instance.
    """
    cache = MagicMock(spec=RedisCache)
    cache.get.return_value = None
    cache.set.side_effect = None
    return cache
