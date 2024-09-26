import pytest
from unittest.mock import Mock, patch
from json.decoder import JSONDecodeError
from src.rabbitmq_consumer import RabbitMQConsumer
from src.service import BenchmarkingService
from src.config import settings


@pytest.fixture
def mock_benchmarking_service():
    """
    A pytest fixture that returns a mock BenchmarkingService instance.

    Returns:
        Mock: A mock BenchmarkingService instance.
    """
    return Mock(spec=BenchmarkingService)


@pytest.fixture
def mock_pika():
    """
    A pytest fixture that returns a mock pika instance.

    Returns:
        Mock: A mock pika instance.
    """
    with patch("src.rabbitmq_consumer.pika") as mock:
        yield mock


def test_rabbitmq_consumer(mock_benchmarking_service, mock_pika):
    # Setup
    """
    Tests the RabbitMQConsumer class to ensure it correctly sets up a connection to RabbitMQ,
    declares a queue, consumes messages from the queue, and handles message processing.

    Args:
        mock_benchmarking_service (Mock): A mock BenchmarkingService instance.
        mock_pika (Mock): A mock pika instance.

    Returns:
        None
    """
    mock_channel = Mock()
    mock_connection = Mock()
    mock_connection.channel.return_value = mock_channel
    mock_pika.BlockingConnection.return_value = mock_connection

    # Create consumer
    consumer = RabbitMQConsumer(mock_benchmarking_service)

    # Test connection and channel creation
    mock_pika.BlockingConnection.assert_called_once_with(
        mock_pika.URLParameters(settings.RABBITMQ_URL)
    )
    mock_connection.channel.assert_called_once()

    # Test queue declaration
    mock_channel.queue_declare.assert_called_once_with(queue=settings.RABBITMQ_QUEUE)

    # Test consume method
    consumer.consume()

    # Now basic_consume should be called
    mock_channel.basic_consume.assert_called_once()
    call_args = mock_channel.basic_consume.call_args
    assert call_args[1]["queue"] == settings.RABBITMQ_QUEUE
    assert call_args[1]["auto_ack"] == False

    # Get the callback function
    callback = call_args[1]["on_message_callback"]

    # Test successful message processing
    mock_channel.reset_mock()
    mock_method = Mock()
    mock_method.delivery_tag = "test_tag"
    callback(mock_channel, mock_method, None, b'{"test": "data"}')

    mock_benchmarking_service.process_simulation_results.assert_called_once_with(
        {"test": "data"}
    )
    mock_channel.basic_ack.assert_called_once_with(delivery_tag="test_tag")

    # Test JSON decode error
    mock_channel.reset_mock()
    mock_benchmarking_service.process_simulation_results.reset_mock()

    with patch("json.loads", side_effect=JSONDecodeError("Invalid JSON", "", 0)):
        callback(mock_channel, mock_method, None, b"invalid json")

    mock_channel.basic_nack.assert_called_once_with(
        delivery_tag="test_tag", requeue=False
    )

    # Test general exception
    mock_channel.reset_mock()
    mock_benchmarking_service.process_simulation_results.side_effect = Exception(
        "Test error"
    )
    callback(mock_channel, mock_method, None, b'{"test": "data"}')

    mock_channel.basic_nack.assert_called_once_with(
        delivery_tag="test_tag", requeue=True
    )

    # Test close method
    consumer.close()
    mock_connection.close.assert_called_once()
