from src.database import get_db
from src.repository import BenchmarkRepository
from src.service import BenchmarkingService
from src.rabbitmq_consumer import RabbitMQConsumer
from src.logger import logger


def main():
    """
    The main entry point of the benchmarking service application.

    This function initializes the database connection, sets up the benchmarking service,
    and starts consuming messages from the RabbitMQ queue. It also handles keyboard
    interrupts to ensure the service is properly stopped.

    Returns:
        None
    """
    logger.info("Starting benchmarking service")
    db = next(get_db())
    repository = BenchmarkRepository(db)
    benchmarking_service = BenchmarkingService(repository)
    consumer = RabbitMQConsumer(benchmarking_service)
    try:
        consumer.consume()
    except KeyboardInterrupt:
        logger.info("Stopping benchmarking service")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
