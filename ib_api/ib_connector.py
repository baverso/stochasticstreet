"""
ib_connector.py

Manages connection to the Interactive Brokers API. Combines EWrapper and EClient
into a single IBConnector class, ensuring robust connection lifecycle management.
"""
import logging
from stochasticstreet.ib_api import IBBase
import threading
import time
import socket

class IBConnector(IBBase):
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
        super().__init__()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.thread = None
        self.callbacks = None  # Placeholder for callback handler

    def register_callbacks(self, callback_handler):
        """
        Registers a callback handler to handle events from the IB API.

        Args:
            callback_handler: An instance of the callback handler (e.g., IBCallbacks).
        """
        self.callbacks = callback_handler
        logging.info("Callbacks registered successfully.")

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
        if self.isConnected():
            logging.warning(
                "Already connected to IB API: Host=%s, Port=%s, Client ID=%s",
                self.host, self.port, self.client_id,
            )
            return

        try:
            logging.info(
                "Starting connection: Host=%s, Port=%s, Client ID=%s",
                self.host, self.port, self.client_id,
            )

            # Connect to the IB Gateway or TWS
            self.connect(self.host, self.port, self.client_id)

            # Start the API event loop in a separate thread
            self.thread = threading.Thread(target=self.run, name=f"IBAPI-Thread-{self.client_id}", daemon=True)
            self.thread.start()

            # Wait for the connection to establish
            timeout = 10  # Maximum wait time in seconds
            start_time = time.time()
            while not self.isConnected():
                if time.time() - start_time > timeout:
                    raise TimeoutError("Connection timed out.")
                time.sleep(0.1)  # Polling interval

            logging.info("Successfully connected to IB API.")
        except Exception as e:
            logging.error("Error starting connection: %s", e)

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
        time.sleep(10)

    except KeyboardInterrupt:
        connector.stop_connection()
        logging.info("KeyboardInterrupt received. Exiting...")

    finally:
        # Ensure clean disconnection
        connector.stop_connection()
        logging.info("IBConnector stopped.")

