# tests/test_service.py
import pytest
from pytest_mock import mocker
from datetime import datetime, timezone
from src.service import BenchmarkingService
from src.repository import BenchmarkRepository
from src.schemas import SimulationResultRead


@pytest.fixture
def benchmarking_service(mock_db_session) -> BenchmarkingService:
    """
    Returns a BenchmarkingService instance with a BenchmarkRepository.

    Args:
        mock_db_session (Session): A mock SQLAlchemy ORM session.

    Returns:
        BenchmarkingService: A BenchmarkingService instance.
    """
    repository = BenchmarkRepository(mock_db_session)
    return BenchmarkingService(repository)


def test_calculate_rankings(benchmarking_service: BenchmarkingService):
    """
    Tests the calculate_rankings method of the BenchmarkingService class.

    Args:
        benchmarking_service (BenchmarkingService): An instance of the BenchmarkingService class.

    Returns:
        None
    """
    simulation_results = [
        SimulationResultRead(
            llm_name="LLM1",
            metric="TTFT",
            values=[1.0, 1.2, 0.8],
            timestamp=datetime.now(timezone.utc),
        ),
        SimulationResultRead(
            llm_name="LLM2",
            metric="TTFT",
            values=[2.0, 1.8, 2.2],
            timestamp=datetime.now(timezone.utc),
        ),
        SimulationResultRead(
            llm_name="LLM1",
            metric="TPS",
            values=[100.0, 95.0, 105.0],
            timestamp=datetime.now(timezone.utc),
        ),
        SimulationResultRead(
            llm_name="LLM2",
            metric="TPS",
            values=[50.0, 55.0, 45.0],
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    rankings = benchmarking_service.calculate_rankings(simulation_results)

    assert "TTFT" in rankings
    assert "TPS" in rankings
    assert rankings["TTFT"][0][0] == "LLM1"
    assert rankings["TPS"][0][0] == "LLM1"


def test_process_simulation_results(benchmarking_service: BenchmarkingService, mocker):
    """
    Tests the process_simulation_results method of the BenchmarkingService class.

    Args:
        benchmarking_service (BenchmarkingService): An instance of the BenchmarkingService class.
        mocker: A pytest mocker instance.

    Returns:
        None
    """
    mock_store_rankings = mocker.patch.object(benchmarking_service, "store_rankings")

    simulation_results = [
        {
            "llm_name": "LLM1",
            "metric": "TTFT",
            "values": [1.0, 1.2, 0.8],
            "timestamp": "2023-01-01T00:00:00",
        },
        {
            "llm_name": "LLM2",
            "metric": "TTFT",
            "values": [2.0, 1.8, 2.2],
            "timestamp": "2023-01-01T00:00:00",
        },
        {
            "llm_name": "LLM1",
            "metric": "TPS",
            "values": [100.0, 95.0, 105.0],
            "timestamp": "2023-01-01T00:00:00",
        },
        {
            "llm_name": "LLM2",
            "metric": "TPS",
            "values": [50.0, 55.0, 45.0],
            "timestamp": "2023-01-01T00:00:00",
        },
    ]

    benchmarking_service.process_simulation_results(simulation_results)

    mock_store_rankings.assert_called_once()
    rankings = mock_store_rankings.call_args[0][0]
    assert "TTFT" in rankings
    assert "TPS" in rankings
    assert rankings["TTFT"][0][0] == "LLM1"
    assert rankings["TPS"][0][0] == "LLM1"
