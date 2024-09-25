import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
import json
import pika

from src.rabbitmq_publisher import RabbitMQPublisher
from src.schema import SimulationResultCreate
from src.config import settings


@pytest.fixture
def mock_pika_connection():
    """
    A pytest fixture that creates a mock pika connection for testing purposes.

    Yields:
        tuple: A tuple containing the mock connection and mock channel objects.
    """
    with patch("src.rabbitmq_publisher.pika.BlockingConnection") as mock_connection:
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        yield mock_connection, mock_channel


@patch("pika.BlockingConnection")
def test_connect(mock_blocking_connection):
    # Create a mock connection and channel
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_connection

    # Instantiate RabbitMQPublisher, which will call connect() automatically
    publisher = RabbitMQPublisher()

    # Verify that BlockingConnection and channel were created
    mock_blocking_connection.assert_called_once_with(
        pika.URLParameters(settings.RABBITMQ_URL)
    )
    mock_connection.channel.assert_called_once()

    # Check that the connection and channel are set correctly
    assert publisher.connection == mock_connection
    assert publisher.channel == mock_channel


def test_publish_message(mock_pika_connection):
    """
    Tests the publish_message method of the RabbitMQPublisher class.

    This test case verifies that the publish_message method publishes the given message to the RabbitMQ queue.

    Parameters:
        mock_pika_connection (tuple): A tuple containing the mock connection and mock channel objects.

    Returns:
        None
    """
    _, mock_channel = mock_pika_connection
    publisher = RabbitMQPublisher()

    test_message = "Test message"
    publisher.publish_message(test_message)

    mock_channel.basic_publish.assert_called_once_with(
        exchange="", routing_key="benchmarking_service", body=test_message
    )


def test_publish_results(mock_pika_connection):
    """
    Tests the publish_results method of the RabbitMQPublisher class.

    This test case verifies that the publish_results method publishes the given simulation results to the RabbitMQ queue.

    Parameters:
        mock_pika_connection (tuple): A tuple containing the mock connection and mock channel objects.

    Returns:
        None
    """
    _, mock_channel = mock_pika_connection
    publisher = RabbitMQPublisher()

    test_results = [
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

    publisher.publish_results(test_results)

    expected_message = json.dumps(
        [result.model_dump() for result in test_results],
        default=publisher._json_serializer,
    )
    mock_channel.basic_publish.assert_called_once_with(
        exchange="", routing_key="benchmarking_service", body=expected_message
    )


def test_close_connection(mock_pika_connection):
    """
    Tests the close_connection method of the RabbitMQPublisher class.

    This test case verifies that the close_connection method closes the RabbitMQ connection.

    Parameters:
        mock_pika_connection (tuple): A tuple containing the mock connection and mock channel objects.

    Returns:
        None
    """
    mock_connection, _ = mock_pika_connection
    publisher = RabbitMQPublisher()
    publisher.close()
    mock_connection.return_value.close.assert_called_once()
