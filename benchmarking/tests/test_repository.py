from unittest.mock import call, MagicMock
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.schemas import BenchmarkResultCreate
from src.models import BenchmarkResult
from src.repository import BenchmarkRepository


def test_insert_results(
    benchmark_repository: BenchmarkRepository, mock_db_session: Session
):
    """
    Tests the insert_results method of the BenchmarkRepository class.

    This test case prepares a list of BenchmarkResultCreate objects and passes it to the insert_results method.
    It then asserts that the add_all method of the mock database session was called with the correct data and that the commit method was called.

    Args:
        benchmark_repository (BenchmarkRepository): The BenchmarkRepository instance to be tested.
        mock_db_session (Session): A mock database session.

    Returns:
        None
    """
    # Prepare test data
    results = [
        BenchmarkResultCreate(
            metric="TTFT",
            llm_name="TestLLM",
            mean_value=1.5,
            rank=1,
            timestamp=datetime.now(timezone.utc),
        )
    ]

    # Call the method
    benchmark_repository.insert_results(results)

    # Assert that a transaction was started
    mock_db_session.begin.assert_called_once()

    # Assert that existing benchmarks were deleted
    mock_db_session.query.assert_called_once_with(BenchmarkResult)
    mock_db_session.query().delete.assert_called_once()

    # Assert that add_all was called with the correct data
    mock_db_session.add_all.assert_called_once()
    added_results = mock_db_session.add_all.call_args[0][0]
    assert len(added_results) == 1
    assert isinstance(added_results[0], BenchmarkResult)
    assert added_results[0].llm_name == "TestLLM"
    assert added_results[0].metric == "TTFT"

    # Assert that commit was called (implicitly by the context manager)
    # Assert that the transaction context was entered and exited
    mock_db_session.begin.return_value.__enter__.assert_called_once()
    mock_db_session.begin.return_value.__exit__.assert_called_once()


def test_get_latest_results(benchmark_repository, mock_db_session):
    """
    Tests the get_latest_results method of the BenchmarkRepository class.

    This test case prepares a list of mock BenchmarkResult objects and sets up a mock database session.
    It then calls the get_latest_results method and asserts that the results are correct and that the query was constructed correctly.

    Args:
        benchmark_repository (BenchmarkRepository): The BenchmarkRepository instance to be tested.
        mock_db_session (Session): A mock database session.

    Returns:
        None
    """
    # Prepare mock data
    mock_results = [
        BenchmarkResult(
            id="845aa3c2-4790-49b3-a60f-2404b1d61521",
            metric="TTFT",
            llm_name="TestLLM1",
            mean_value=1.5,
            rank=1,
            timestamp=datetime.now(timezone.utc),
        ),
        BenchmarkResult(
            id="f7211482-3333-43c2-98d2-0e75cf04e53f",
            metric="TPS",
            llm_name="TestLLM2",
            mean_value=100,
            rank=2,
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    # Set up the mock query
    mock_query = MagicMock()
    mock_query.order_by.return_value.all.return_value = mock_results
    mock_db_session.query.return_value = mock_query

    # Call the method
    results = benchmark_repository.get_latest_results()

    # Assert the results
    assert len(results) == 2
    assert isinstance(results[0], BenchmarkResult)
    assert results[0].llm_name == "TestLLM1"
    assert results[1].llm_name == "TestLLM2"

    # Verify that the query was constructed correctly
    mock_db_session.query.assert_called_once_with(BenchmarkResult)
    mock_query.order_by.assert_called_once()
    mock_query.order_by.return_value.all.assert_called_once()

    # Check that order_by was called with the correct argument
    order_by_arg = mock_query.order_by.call_args[0][0]
    assert str(order_by_arg) == str(BenchmarkResult.timestamp.desc())
