"""
ib_connector.py

Manages connection to the Interactive Brokers API. Combines EWrapper and EClient
into a single IBConnector class, ensuring robust connection lifecycle management.
"""
import logging
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from stochasticstreet.ib_api.logging_config import setup_logging
import threading
import time
import socket

class IBConnector(EWrapper, EClient):
    """
    IBConnector combines EWrapper and EClient to manage the connection to the IB API.
    """

    def __init__(self, host="127.0.0.1", port=7497, client_id=1):
        """
        Initializes the IBConnector.

        Args:
            host (str): Hostname of the IB Gateway or TWS.
            port (int): Port number of the IB Gateway or TWS.
            client_id (int): A unique client ID for this session.
        """
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.host = host
        self.port = port
        self.client_id = client_id
        self.thread = None
    def get_local_ip(self):
        """
        Retrieves the local IP address of the machine.

        Returns:
            str: The local IP address of the machine.
        """
        try:
            # Use a dummy connection to determine the local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # Connect to an external address; the actual packet won't be sent
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            return ip
        except Exception as e:
            return f"Unable to determine local IP: {e}"

    def start_connection(self):
        """
        Starts the connection to the IB Gateway or TWS.
        """
        try:
            logging.info("Attempting to connect to IB API... on %s:%s", self.host, self.port)
            self.connect(self.host, self.port, self.client_id)

            if self.isConnected():
                logging.info("Connection established to IB API")

            # Start the API event loop in a separate thread
            self.thread = threading.Thread(target=self.run, name="IBAPI-Thread", daemon=True)
            self.thread.start()

            # Log the thread details
            logging.info("API event loop started on thread: %s", self.thread.name)
            logging.info("Client ID %s is active on thread %s", self.client_id, self.thread.name)

        except Exception as e:
            logging.error(f"Error during connection setup: {e}")

    def stop_connection(self):
        """
        Stops the connection to the IB Gateway or TWS.
        """
        logging.info(f"Connection status is: {self.isConnected()} for client ID: {self.client_id}")

        if not self.isConnected():
            logging.warning("Attempted to disconnect, but no active connection exists.")
            return

        logging.info("Stopping connection: Client ID=%s", self.client_id)
        self.disconnect()

        # Optional: Give time for clean disconnect
        time.sleep(1)

        if not self.isConnected():
            logging.info("Successfully disconnected from IB API.")
        else:
            logging.error("Failed to properly disconnect from IB API.")

    def get_connection_status(self):
        """
        Logs the status of all active threads and connection details.
        """
        logging.info("Checking connection status...")

        if self.isConnected():
            logging.info(
                "Active Connection:\n"
                " - Host: %s\n"
                " - Port: %s\n"
                " - Client ID: %s\n"
                " - Thread Name: %s\n",
                self.host,
                self.port,
                self.client_id,
                self.thread.name if self.thread else "No Thread",
            )
        else:
            logging.warning("No active connection found.")
            ip = self.get_local_ip()
            logging.error(f"Connection inactive. Try running the IB Gateway or TWS on {ip}:{self.port}")

        # Log all threads
        logging.info("All running threads:")
        for thread in threading.enumerate():
            logging.info("Thread Name: %s, Is Daemon: %s", thread.name, thread.daemon)

def create_ib_connector(host="127.0.0.1", port=7497, client_id=1):
    """
    Creates and connects an IBConnector instance.

    Args:
        host (str): The hostname of the IB Gateway or TWS.
        port (int): The port number of the IB Gateway or TWS.
        client_id (int): A unique client ID.

    Returns:
        IBConnector: A connected IBConnector instance.
    """
    connector = IBConnector(host, port, client_id)

    if connector.isConnected():
        logging.info("IB is already connected on %s:%s", host, port)
        connector.get_connection_status()
    else:
        logging.info("IB is not connected on %s:%s", host, port)
        connector.start_connection()
        logging.info("Successfully connected to IB API.")
        connector.get_connection_status()

    return connector


if __name__ == "__main__":
    try:
        # Initialize and start the connection
        connector = create_ib_connector(host="127.0.0.1", port=4002, client_id=1)

        # Keep the connection active for testing purposes
        logging.info("Connection active. Sleeping for 5 seconds...")
        time.sleep(5)

    except KeyboardInterrupt:
        connector.stop_connection()
        logging.info("KeyboardInterrupt received. Exiting...")

    finally:
        # Ensure clean disconnection
        connector.stop_connection()
        logging.info("IBConnector stopped.")

