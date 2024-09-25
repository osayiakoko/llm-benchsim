import json
import pika
from datetime import datetime
from src.schema import SimulationResultCreate
from src.config import settings
from src.logger import logger


class RabbitMQPublisher:
    def __init__(self):
        """
        Initializes a RabbitMQPublisher object.

        Establishes a connection to the RabbitMQ server specified in the settings.RABBITMQ_URL
        and creates a channel. Declares a queue with the name specified in settings.RABBITMQ_QUEUE.

        Parameters:
            None

        Returns:
            None
        """
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establish a new connection and channel to RabbitMQ."""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Error connecting to RabbitMQ: {str(e)}")
            raise

    def ensure_connection(self):
        """Ensure the connection and channel are alive, or reconnect if needed."""
        if self.connection is None or self.connection.is_closed:
            logger.warning("RabbitMQ connection lost, reconnecting...")
            self.connect()
        elif self.channel is None or self.channel.is_closed:
            logger.warning("RabbitMQ channel lost, reconnecting...")
            self.connect()

    def publish_message(self, message: any):
        """
        Publishes a message to the RabbitMQ queue.

        Parameters:
            message (any): The message to be published.

        Returns:
            None
        """
        self.ensure_connection()
        try:
            self.channel.basic_publish(
                exchange="", routing_key=settings.RABBITMQ_QUEUE, body=message
            )
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise

    def publish_results(self, results: list[SimulationResultCreate]):
        """
        Publishes a list of simulation results to the RabbitMQ queue.

        Parameters:
            results (list[SimulationResultCreate]): A list of simulation results to be published.

        Returns:
            None
        """
        message = json.dumps(
            [result.model_dump() for result in results], default=self._json_serializer
        )
        self.publish_message(message)

    def close(self):
        """
        Closes the RabbitMQ connection.

        Parameters:
            None

        Returns:
            None
        """
        if self.connection != None:
            self.connection.close()

    @staticmethod
    def _json_serializer(obj):
        """
        A static method to serialize objects into JSON format.

        This method is used to convert datetime objects into ISO format strings.
        If the object is not a datetime instance, it raises a TypeError.

        Parameters:
            obj: The object to be serialized.

        Returns:
            str: The ISO format string representation of the datetime object.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
