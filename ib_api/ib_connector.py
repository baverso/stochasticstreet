"""
ib_connector.py

Manages connection to the Interactive Brokers API. Combines EWrapper and EClient
into a single IBConnector class, ensuring robust connection lifecycle management.
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import logging
import threading
import time


class IBConnector(EWrapper, EClient):
    """
    IBConnector combines EWrapper and EClient to manage the connection to the IB API.
    """

    def __init__(self, host="127.0.0.1", port=7497, client_id=0):
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
        self.connected = False
        self.thread = None

    def start_connection(self):
        """
        Starts the connection to the IB Gateway or TWS.
        """
        try:
            logging.info("Attempting to connect to IB API... on %s:%s", self.host, self.port)
            self.connect(self.host, self.port, self.client_id)

            # Start the API event loop in a separate thread
            self.thread = threading.Thread(target=self.run, name="IBAPI-Thread", daemon=True)
            self.thread.start()
        except Exception as e:
            logging.error(f"Error during connection setup: {e}")

    def stop_connection(self):
        """
        Stops the connection to the IB Gateway or TWS.
        """
        if self.connected:
            logging.info("Disconnecting from IB API...")
            self.disconnect()
            self.connected = False

            # Optional: Give time for clean disconnect
            time.sleep(1)
            logging.info("Disconnected from IB API.")

    # Override required EWrapper methods
    def nextValidId(self, orderId: int):
        """
        Callback triggered when the IB API sends the first valid order ID.

        Args:
            orderId (int): The next valid order ID provided by the IB API.
        """
        self.connected = True
        logging.info(f"Connected to IB API. Next valid order ID: {orderId}")

    def error(self, reqId: int, errorCode: int, errorMsg: str, advancedOrderRejectJson=None):
        """
        Handles errors received from the IB API.

        Args:
            reqId (int): The request ID associated with the error.
            errorCode (int): The error code from IB API.
            errorMsg (str): A descriptive message for the error.
            advancedOrderRejectJson (str, optional): JSON with advanced order rejection details (if provided).
        """
        if advancedOrderRejectJson:
            logging.error(
                f"Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorMsg}, AdvancedReject: {advancedOrderRejectJson}")
        else:
            logging.error(f"Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorMsg}")

    def connectionClosed(self):
        """
        Callback triggered when the connection to the IB API is closed.
        """
        logging.warning("Connection to IB API closed.")
        self.connected = False


def create_ib_connector(host="127.0.0.1", port=7497, client_id=0):
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
    connector.start_connection()

    # Allow time for the connection to establish
    time.sleep(10)
    if connector.isConnected():
        connector.connected = True
        logging.info("Successfully connected to IB API.")
    else:
        raise ConnectionError("Connection failed: Not connected to IB API.")

    return connector


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    try:
        # Initialize and start the connection
        connector = create_ib_connector(host="127.0.0.1", port=7497, client_id=123)

        # Keep the connection active for testing purposes
        logging.info("Connection active. Sleeping for 5 seconds...")
        time.sleep(5)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Exiting...")

    finally:
        # Ensure clean disconnection
        connector.stop_connection()
        logging.info("IBConnector stopped.")