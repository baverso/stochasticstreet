import logging


class IBCallbacks:
    """
    Handles all callbacks for the Interactive Brokers API.
    Processes data returned by the API.
    """

    def __init__(self, app):
        """
        Initialize with a reference to the main application instance.

        Args:
            app (object): The main IBApp instance.
        """
        self.app = app

    # Connection-related callbacks
    def connectAck(self):
        """
        Called when the server acknowledges the connection.
        """
        logging.info("Connection acknowledged by IB API.")
        self.app.connected = True

    # Account summary-related callbacks
    def accountSummary(self, reqId, account, tag, value, currency):
        """
        Handles account summary data received.

        Args:
            reqId (int): Request ID.
            account (str): Account name.
            tag (str): The tag of the data (e.g., NetLiquidation).
            value (str): The value of the tag.
            currency (str): Currency of the value.
        """
        logging.info(
            "Account Summary - ReqId: %d, Account: %s, Tag: %s, Value: %s, Currency: %s",
            reqId, account, tag, value, currency,
        )

    def accountSummaryEnd(self, reqId):
        """
        Called when the account summary request is complete.

        Args:
            reqId (int): Request ID.
        """
        logging.info("Account summary request completed: ReqId=%s", reqId)
        self.app.disconnect_from_ib()