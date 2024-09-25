import time, sys
from datetime import datetime, timezone

from src.config import settings
from src.logger import logger
from src.service import get_simulation_service
from src.utils import GracefulShutdown


def main():
    """
    The main entry point of the simulation service application.

    This function initializes the simulation service, runs simulations in a loop,
    and handles shutdown signals.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting simulation service")
    shutdown_handler = GracefulShutdown()

    while not shutdown_handler.terminate:
        try:
            logger.info(
                f"Starting simulation at {datetime.now(timezone.utc).isoformat()}"
            )
            with get_simulation_service() as service:
                num_simulation = service.run_simulation()
                logger.info(
                    f"Simulation completed at {datetime.now(timezone.utc).isoformat()}, {num_simulation} simulations generated"
                )
        except Exception as e:
            logger.exception(e)

        for _ in range(settings.SIMULATION_INTERVAL):
            if shutdown_handler.terminate:
                break
            time.sleep(1)

    logger.info("Shutting down simulation service")
    sys.exit(0)


if __name__ == "__main__":
    main()
