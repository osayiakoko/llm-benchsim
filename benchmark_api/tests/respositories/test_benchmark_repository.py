from datetime import datetime, timezone
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.repositories import BenchmarkRepository
from src.models import BenchmarkResult
from src.core import RedisCache


def test_get_by_metric(mock_db_session: Session, mock_cache: RedisCache):
    """
    Tests the get_by_metric method of the BenchmarkRepository class.

    Args:
        mock_db_session (Session): A mock of the SQLAlchemy session object used to interact with the database.
        mock_cache (RedisCache): A mock of the RedisCache instance used for caching.

    Returns:
        None
    """
    mock_results = [
        BenchmarkResult(
            id="706f8077-4243-4159-9542-39031237e6bb",
            metric="TTFT",
            llm_name="TestLLM1",
            mean_value=1.5,
            rank=1,
            timestamp=datetime.now(timezone.utc),
        ),
        BenchmarkResult(
            id="46ea7de2-668f-4c23-8d85-2610fe5f5235",
            metric="TTFT",
            llm_name="TestLLM2",
            mean_value=100,
            rank=2,
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    mock_query = MagicMock()
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_results
    mock_db_session.query.return_value = mock_query

    repository = BenchmarkRepository(mock_db_session, mock_cache)
    results = repository.get_by_metric("TTFT")

    assert len(results) == 2

    assert str(results[0].id) == mock_results[0].id
    assert results[0].metric == "TTFT"
    assert results[0].llm_name == "TestLLM1"
    assert results[0].mean_value == 1.5
    assert results[0].rank == 1
    assert results[0].timestamp == mock_results[0].timestamp

    assert str(results[1].id) == mock_results[1].id
    assert results[1].metric == "TTFT"
    assert results[1].llm_name == "TestLLM2"
    assert results[1].mean_value == 100
    assert results[1].rank == 2
    assert results[1].timestamp == mock_results[1].timestamp
