import pytest
from src.repository import SimulationRepository
from src.schema import SimulationResultCreate
from src.models import SimulationResult
from datetime import datetime, timezone


def test_insert_results(db_session):
    """
    Tests the insert_results method of the SimulationRepository class.

    This test case creates a SimulationRepository instance with a given database session,
    inserts a list of simulation results into the repository, and then asserts that the
    data was inserted correctly into the database.

    Parameters:
        db_session: The database session to be used by the repository.

    Returns:
        None
    """
    repository = SimulationRepository(db_session)
    results = [
        SimulationResultCreate(
            llm_name="TestLLM",
            metric="TTFT",
            values=[1.5, 1.6, 1.7],
            timestamp=datetime.now(timezone.utc),
        ),
        SimulationResultCreate(
            llm_name="TestLLM",
            metric="TPS",
            values=[50.0, 51.0, 52.0],
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    repository.insert_results(results)

    assert db_session.query(SimulationResult).count() == 2

    # Check that the data was inserted correctly
    for result in results:
        db_result = (
            db_session.query(SimulationResult).filter_by(metric=result.metric).first()
        )
        assert db_result is not None
        assert db_result.llm_name == result.llm_name
        assert db_result.metric == result.metric
        assert db_result.values == result.values
