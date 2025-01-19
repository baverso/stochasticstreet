import logging
import os

def setup_logging():
    """
    Sets up logging for the application. If logging is already configured, it does nothing.
    Creates a 'logs' directory if it doesn't exist and sets up logging to both a file and the console.
    The log messages include timestamps and log levels.

    The log file is named 'app.log' and is located in the 'logs' directory.
    The log format is: '%(asctime)s [%(levelname)s] %(message)s'
    The date format is: '%Y-%m-%d %H:%M:%S'
    """
    if len(logging.getLogger().handlers) > 0:
        return

    # Directory for log files
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    # Path to the log file
    LOG_FILE = os.path.join(LOG_DIR, "app.log")

    # Formatter for log messages
    formatter = logging.Formatter(
        fmt="%(asctime)s moo [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler for logging to a file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Basic configuration for logging
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )

    # Log a message indicating that logging setup is complete
    logging.getLogger(__name__).info("Logging setup complete. Logs will be written to: %s", LOG_FILE)