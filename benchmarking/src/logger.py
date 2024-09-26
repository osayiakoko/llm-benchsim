import sys
from loguru import logger
from .config import settings


def setup_logger():
    """
    Configures and sets up the application logger.

    Removes the default logger to prevent duplicate log messages, sets the log format,
    and adds a file handler with rotation. Optionally adds console logging if enabled.

    Returns:
        logger: The configured logger instance
    """
    # Remove default logger to avoid duplicate logs
    logger.remove()

    # log format
    format = "{time} - {name} - {level} - {message}"

    # Add file handler with rotation
    logger.add(
        settings.LOG_FILE,
        format=format,
        level="INFO",
        rotation="5 MB",  # Rotate log files after they reach 5 MB
    )

    # Optionally add console logging if enabled in settings
    if settings.CONSOLE_LOGGING:
        logger.add(sys.stdout, format=format)

    return logger


logger = setup_logger()
