import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from src.database import Base
from src.config import settings


@pytest.fixture(scope="session")
def engine():
    """
    Returns a SQLAlchemy engine object for the test database connection.

    Yields:
        Engine: A SQLAlchemy engine object.
    """

    # Create engine for the admin connection
    _ = create_engine(settings.get_database_url("postgres"))

    # format the test database url
    TEST_DB_URL = settings.get_database_url("test_db")

    # Ensure the test database doesn't already exist
    if not database_exists(TEST_DB_URL):
        create_database(TEST_DB_URL)

    # Create engine for the test database
    test_engine = create_engine(TEST_DB_URL)

    # Yield the engine and sessionmaker to the tests
    yield test_engine

    # Drop the test database after the tests complete
    drop_database(TEST_DB_URL)


@pytest.fixture(scope="session")
def tables(engine):
    """
    Creates all tables in the database schema and then drops them after the test session is finished.

    Args:
        engine: A SQLAlchemy engine object.

    Yields:
        None

    Notes:
        This fixture is used to create and drop tables in the database for testing purposes.
    """
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """
    Returns a database session object for testing purposes.

    Args:
        engine: A SQLAlchemy engine object.
        tables: A fixture that creates and drops tables in the database.

    Yields:
        Session: A database session object.

    Notes:
        This fixture is used to create a database session for testing purposes.
        The session is automatically closed and the transaction is rolled back when it goes out of scope.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
