import logging
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# from stochasticstreet.ib_api.ib_base import IBBase

# class IBApp(IBBase):
class IBApp(EClient, EWrapper):
    """
    A standalone Interactive Brokers API application.
    """
    def __init__(self, host="127.0.0.1", port=4002, client_id=1):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False

    def accountSummary(self, reqId, account, tag, value, currency):
        logging.info(
            "Account Summary - ReqId: %d, Account: %s, Tag: %s, Value: %s, Currency: %s",
            reqId, account, tag, value, currency,
        )

    def connect_to_ib(self):
        """
        Connects to the IB Gateway or TWS.
        """
        logging.info("Connecting to IB API...")
        self.connect(self.host, self.port, self.client_id)

        # Start the API event loop in a separate thread
        self.thread = self._start_thread()
        logging.info("Connection initiated. Waiting for server response...")

    def _start_thread(self):
        """
        Starts the event loop in a separate thread.
        """
        from threading import Thread
        thread = Thread(target=self.run, name="IBAPI-Thread", daemon=True)
        thread.start()
        return thread

    def disconnect_from_ib(self):
        """
        Disconnects from the IB Gateway or TWS.
        """
        logging.info("Disconnecting from IB API...")
        self.disconnect()
        if self.thread.is_alive():
            self.thread.join()
        logging.info("Disconnected from IB API.")

    def request_account_summary(self, req_id):
        """
        Sends a request for the account summary.

        Args:
            req_id (int): A unique request ID.
        """
        logging.info("Requesting account summary...")
        self.reqAccountSummary(req_id, "All", "FullInitMarginReq,TotalCashValue,NetLiquidation,TotalCashValue")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Initialize the IBApp
    host = "127.0.0.1"
    port = 4002
    client_id = 1
    app = IBApp(host, port, client_id)

    try:
        # Connect to the IB Gateway or TWS
        app.connect_to_ib()

        # Wait for the connection to be established
        time.sleep(2)

        # Request account summary
        req_id = 9001
        app.request_account_summary(req_id)

        # Keep the script running to process callbacks
        time.sleep(2)

    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")
    finally:
        app.disconnect_from_ib()