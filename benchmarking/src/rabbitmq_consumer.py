import json
from json.decoder import JSONDecodeError
import pika
from pika.channel import Channel
from pika.spec import Basic
from pika.spec import BasicProperties
from src.config import settings
from src.logger import logger
from src.service import BenchmarkingService


class RabbitMQConsumer:
    def __init__(self, benchmarking_service: BenchmarkingService):
        """
        Initializes a RabbitMQConsumer instance.

        Args:
            benchmarking_service (BenchmarkingService): The BenchmarkingService instance.

        Returns:
            None
        """
        self.connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
        self.benchmarking_service = benchmarking_service

    def message_callback(
        self, ch: Channel, method: Basic, properties: BasicProperties, body: bytes
    ):
        """
        Handles incoming messages from a RabbitMQ queue.

        Args:
            ch (Channel): The RabbitMQ channel.
            method (Basic): The RabbitMQ method.
            properties (BasicProperties): The RabbitMQ message properties.
            body (bytes): The message body.

        Returns:
            None
        """
        queue_name = method.routing_key
        logger.info(f"Received message from queue: {queue_name}")
        try:
            message = body.decode("utf-8")
            json_data = json.loads(message)
            self.benchmarking_service.process_simulation_results(json_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except JSONDecodeError as e:
            logger.error(f"Failed to decode message as JSON: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def consume(self):
        """
        Starts consuming messages from the RabbitMQ queue specified in the settings.

        This function sets up a consumer for the RabbitMQ channel, using the message callback
        function `self.message_callback`. The consumer will consume messages from the queue
        specified in the settings, and will not automatically acknowledge the messages.

        Parameters:
            None

        Returns:
            None
        """
        self.channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE,
            on_message_callback=self.message_callback,
            auto_ack=False,
        )
        logger.info(f"Started consuming messages from queue: {settings.RABBITMQ_QUEUE}")
        self.channel.start_consuming()

    def close(self):
        """
        Closes the connection to the RabbitMQ server.

        This function calls the `close` method of the `connection` object to close the connection to the RabbitMQ server.

        Parameters:
            None

        Returns:
            None
        """
        self.connection.close()
