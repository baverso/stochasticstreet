"""
main.py

This module is the entry point for the IB API client application.
Initialize the IBConnector, start the connection, and handle user input for the client application.
This module is responsible for managing the lifecycle of the IB API client application.
"""

import logging
import argparse
from stochasticstreet.ib_api.ib_connector import IBConnector
from stochasticstreet.ib_api.ib_utils import get_local_ip
import os
import time

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/ib_api_connection.log"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)

def main(host, port, client_id):
    """
    Main entry point for the IB API client application.
    Initialize the IBConnector, start the connection, and handle user input for the client application.
    """
    logger.info("Starting IB API client...")

    # Initialize the IBConnector
    app = IBConnector(host=host, port=port, client_id=client_id)

    # Start the connection
    try:
        logger.info("Starting connection to IB API...")
        app.start_connection()
        time.sleep(10)
        app.disconnect()
    except Exception as e:
        ip = get_local_ip()
        logger.error(f"Error starting connection: {e}, try running the IB Gateway or TWS on {ip}:{port}")
        return
    except KeyboardInterrupt:
        logger.info("Connection interrupted by user.")
        return
    finally:
        # Stop the connection
        app.stop_connection()
        logger.info("IB API client stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IB API client application")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Hostname of the IB Gateway or TWS")
    parser.add_argument("--port", type=int, default=7497, help="Port number of the IB Gateway or TWS")
    parser.add_argument("--client_id", type=int, default=1, help="Unique client ID")

    args = parser.parse_args()
    main(args.host, args.port, args.client_id)