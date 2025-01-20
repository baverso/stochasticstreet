"""
main.py

This module is the entry point for the IB API client application.
Initialize the IBConnector, start the connection, and handle user input for the client application.
This module is responsible for managing the lifecycle of the IB API client application.
"""
import logging
import argparse
from stochasticstreet.ib_api import IBCallbacks, IBRequests, IBConnector
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
    connector = IBConnector(host=host, port=port, client_id=client_id)

    # Properly instantiate and register callbacks to the connector instance
    callbacks = IBCallbacks()
    connector.register_callbacks(callbacks)

    # Initialize the IBRequests class
    requests = IBRequests(connector)  # Pass the connector instance to the requests class

    # Start the connection
    logging.info("Starting connection to IB API...")
    connector.start_connection()
    logging.info("Press Ctrl+C to stop the connection.")
    connector.get_connection_status()
    time.sleep(5)

    # Perform account summary requests
    logging.info("Requesting account summaries...")
    requests.request_account_summary(req_id=9001)  # Regular mode
    requests.request_account_summary(req_id=9002, verbose=True)  # Verbose mode

    # Close the connection
    connector.stop_connection()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IB API client application")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Hostname of the IB Gateway or TWS")
    parser.add_argument("--port", type=int, default=4002, help="Port number of the IB Gateway or TWS")
    parser.add_argument("--client_id", type=int, default=1, help="Unique client ID")

    args = parser.parse_args()
    main(args.host, args.port, args.client_id)