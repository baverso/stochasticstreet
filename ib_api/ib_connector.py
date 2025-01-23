"""
ib_connector.py

Defines a connector class that inherits from EClient and manages
connect/disconnect logic. It also delegates callback handling
to the IBCallbacks class.
"""

import logging
import socket
import threading

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IBConnector(EClient):
    """
    Manages the connection to the IB Gateway or TWS instance.
    """

    def __init__(self, callbacks: EWrapper):
        """
        Initialize the IBConnector.

        Args:
            callbacks: An instance of a class inheriting EWrapper (e.g., IBCallbacks).
        """
        EClient.__init__(self, wrapper=callbacks)
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self, host: str = "127.0.0.1", port: int = 7497, client_id: int = 1):
        """
        Connect to a running TWS/IB Gateway instance.

        Args:
            host (str): The hostname or IP address of the IB Gateway/TWS.
            port (int): The port number of the IB Gateway/TWS.
            client_id (int): A unique client ID for this session.
        """
        self.logger.info(f"Connecting to IB on host={host}, port={port}, clientId={client_id}")
        super().connect(host, port, client_id)

    def start(self):
        """
        Launch the worker thread that processes messages from IB TWS/Gateway.
        """
        self.logger.info("Starting the network processing thread for IB.")
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def disconnect(self):
        """
        Disconnect from IB TWS/Gateway.
        """
        self.logger.info("Disconnecting from IB.")
        super().disconnect()

    def server_version(self):
        """
        Retrieves the server version of the connected TWS/Gateway.

        Returns:
            int: The server version.
        """
        version = super().serverVersion()
        self.logger.info(f"Connected to IB server version: {version}")
        return version

    def get_local_ip(self):
        """
        Retrieves the local IP address of the machine.

        Returns:
            str: The local IP address of the machine.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            return ip
        except Exception as e:
            return f"Unable to determine local IP: {e}"

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
                self.clientId,
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