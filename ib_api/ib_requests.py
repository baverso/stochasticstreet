import logging
from .ib_base import IBBase

class IBRequests(IBBase):
    """
    Handles all API requests for the Interactive Brokers API.
    """

    def __init__(self, connector):
        """
        Initializes the IBRequests class with a connector.

        Args:
            connector (IBConnector): An instance of IBConnector for managing the connection.
        """
        if not isinstance(connector, IBBase):
            raise ValueError("Connector must inherit from IBBase.")
        self.connector = connector
        if not self.connector.isConnected():
            logging.error("No active connection to IB API found in IBRequests")
            raise ConnectionError("Connector may be connected but IBRequests cannot find.")

    def accountSummary(self, reqId, account, tag, value, currency):
        logging.info(
            "Account Summary - ReqId: %d, Account: %s, Tag: %s, Value: %s, Currency: %s",
            reqId, account, tag, value, currency,
        )

    def request_account_summary(self, req_id, verbose=False):
        """
        Request account summary based on verbosity.

        Args:
            req_id (int): A unique request ID.
            verbose (bool): If True, returns all account summary tags. Defaults to False.

        Example:
            requests.request_account_summary(req_id=9001, verbose=True)
        """
        # Define tags for verbose and regular modes
        verbose_tags = [
            "AccountType", "NetLiquidation", "TotalCashValue", "SettledCash", "AccruedCash",
            "BuyingPower", "EquityWithLoanValue", "PreviousEquityWithLoanValue", "GrossPositionValue",
            "RegTEquity", "RegTMargin", "SMA", "InitMarginReq", "MaintMarginReq", "AvailableFunds",
            "ExcessLiquidity", "Cushion", "FullInitMarginReq", "FullMaintMarginReq", "FullAvailableFunds",
            "FullExcessLiquidity", "LookAheadNextChange", "LookAheadInitMarginReq", "LookAheadMaintMarginReq",
            "LookAheadAvailableFunds", "LookAheadExcessLiquidity", "HighestSeverity", "DayTradesRemaining",
            "Leverage", "$LEDGER", "$LEDGER:ALL"
        ]

        regular_tags = [
            "NetLiquidation", "TotalCashValue", "BuyingPower", "ExcessLiquidity", "Leverage"
        ]

        # Select tags based on verbosity
        tags = ",".join(verbose_tags if verbose else regular_tags)

        try:
            # Make the API request
            self.connector.reqAccountSummary(req_id, "All", tags)
            logging.info(
                "Account summary request made. Mode: %s, Tags: %s",
                "Verbose" if verbose else "Regular",
                tags,
            )
        except Exception as e:
            logging.error("Error during account summary request: %s", e)