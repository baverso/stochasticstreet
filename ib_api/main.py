"""
main.py

This module is the entry point for the IB API client application.
Initialize the IBConnector, start the connection, and handle user input for the client application.
This module is responsible for managing the lifecycle of the IB API client application.
"""
import logging
import argparse
from stochasticstreet.ib_api.ib_connector import IBConnector
from stochasticstreet.ib_api.logging_config import setup_logging

import time

def main(host, port, client_id):
    """
    Main entry point for the IB API client application.
    Initialize the IBConnector, start the connection, and handle user input for the client application.

    Args:
        host (str): Hostname of the IB Gateway or TWS.
        port (int): Port number of the IB Gateway or TWS.
        client_id (int): Unique client ID for this session.
    """
    logging.info("Starting IB API client...")

    # Initialize the IBConnector
    app = IBConnector(host=host, port=port, client_id=client_id)

    # Start the connection
    try:
        logging.info("Starting connection to IB API...")
        app.start_connection()
        time.sleep(10)
        app.get_connection_status()

    except Exception as e:
        logging.error(f"Error starting connection: {e}, try running the IB Gateway or TWS first.")
        return
    except KeyboardInterrupt:
        logging.info("Connection interrupted by user.")
        return
    finally:
        # Stop the connection
        app.stop_connection()
        logging.info("IB API client stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IB API client application")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Hostname of the IB Gateway or TWS")
    parser.add_argument("--port", type=int, default=7497, help="Port number of the IB Gateway or TWS")
    parser.add_argument("--client_id", type=int, default=1, help="Unique client ID")

    args = parser.parse_args()
    main(args.host, args.port, args.client_id)