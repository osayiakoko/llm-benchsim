import sys
from loguru import logger
from src.config import settings


def get_logger():
    """
    Initializes and configures a logger instance.

    Removes the default logger to prevent duplicate log entries, sets a custom log format,
    and adds a file handler with rotation. Optionally, console logging is enabled if
    specified in the settings.

    Returns:
        logger: A configured logger instance.
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
        rotation="5 MB",
    )

    # Optionally add console logging if enabled in settings
    if settings.CONSOLE_LOGGING:
        logger.add(sys.stdout, format=format)

    return logger


# Initialize the logger
logger = get_logger()
