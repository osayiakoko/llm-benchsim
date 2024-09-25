import pytest
from unittest.mock import Mock
from src.service import SimulationService
from src.repository import SimulationRepository
from src.rabbitmq_publisher import RabbitMQPublisher
from src.config import settings


@pytest.fixture
def simulation_service():
    """
    A pytest fixture that creates a mock simulation service for testing purposes.

    Returns:
        SimulationService: A SimulationService instance with mock repository and publisher.
    """
    mock_repository = Mock(spec=SimulationRepository)
    mock_publisher = Mock(spec=RabbitMQPublisher)
    return SimulationService(mock_repository, mock_publisher)


def test_generate_data_point(simulation_service: SimulationService):
    """
    Tests the generation of data points for a given metric.

    Parameters:
        simulation_service (SimulationService): The simulation service to test.

    Returns:
        None
    """
    for metric in simulation_service.METRICS:
        values = simulation_service.generate_data_points(metric)
        assert isinstance(values, list)
        assert len(values) == settings.NUM_DATA_POINTS
        assert all(isinstance(value, float) for value in values)


def test_simulate(simulation_service: SimulationService):
    """
    Tests the simulate method of the SimulationService class.

    Parameters:
        simulation_service (SimulationService): The simulation service to test.

    Returns:
        None
    """
    results = simulation_service.simulate()
    expected_count = len(settings.LLM_MODELS) * len(SimulationService.METRICS)
    assert len(results) == expected_count
    assert all(
        len(results[index].values) == settings.NUM_DATA_POINTS
        for index in range(len(results))
    )


def test_run_simulation(simulation_service: SimulationService):
    """
    Tests the run_simulation method of the SimulationService class.

    Parameters:
        simulation_service (SimulationService): The simulation service to test.

    Returns:
        None
    """
    num_results = simulation_service.run_simulation()
    assert num_results > 0
    simulation_service.repository.insert_results.assert_called_once()
    simulation_service.publisher.publish_results.assert_called_once()

    # Check that the number of results passed to publish_results matches the return value
    args, _ = simulation_service.publisher.publish_results.call_args
    assert len(args[0]) == num_results
