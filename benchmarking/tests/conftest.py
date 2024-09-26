import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from src.repository import BenchmarkRepository


@pytest.fixture
def mock_db_session():
    """
    A pytest fixture that returns a mock SQLAlchemy ORM session.

    Returns:
        Session: A mock SQLAlchemy ORM session.
    """
    return MagicMock(spec=Session)


@pytest.fixture
def benchmark_repository(mock_db_session) -> BenchmarkRepository:
    """
    A pytest fixture that returns a BenchmarkRepository instance.

    Args:
        mock_db_session: A mock SQLAlchemy ORM session.

    Returns:
        BenchmarkRepository: A BenchmarkRepository instance.
    """
    return BenchmarkRepository(mock_db_session)
