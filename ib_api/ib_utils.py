"""
ib_utils.py

Utility functions for the IB API platform, including logging setup and reusable helpers.
"""

import logging
import os
from datetime import datetime


def setup_logging(log_dir="logs", log_file=None, log_level=logging.INFO):
    """
    Sets up logging for the application.

    Args:
        log_dir (str): Directory where log files will be stored.
        log_file (str): Name of the log file. If None, uses a timestamped file.
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        None
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Default log file name with timestamp
    if log_file is None:
        log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    # Full path to the log file
    log_path = os.path.join(log_dir, log_file)

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler(log_path),  # Log to file
        ],
    )

    logging.info(f"Logging initialized. Logs will be saved to: {log_path}")

def get_local_ip():
    import socket
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return f"Error retrieving IP: {e}"