import logging
import os
import json

# Custom JSON formatter for logs
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Initialize log record with timestamp and level first
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname
        }

        # If the message is a dictionary, merge it into the log record
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        else:
            # Fallback for non-dictionary messages
            log_record["message"] = record.getMessage()

        # Return the JSON-formatted string with indentation
        return json.dumps(log_record, indent=2)


class LoggingConfig:
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

        # File handler for logging to a file
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(JsonFormatter())

        # Console handler for logging to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JsonFormatter())

        # Basic configuration for logging
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler]
        )

        # Log a message indicating that logging setup is complete
        logging.getLogger(__name__).info("Logging setup complete. Logs will be written to: %s", LOG_FILE)