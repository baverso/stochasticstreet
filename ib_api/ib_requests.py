import logging
from ib_base import IBBase
class IBRequests:
    """
    Handles all API requests through the connector.
    No longer inherits from IBBase - works through connector instead.
    """
    def __init__(self, connector):
        self.connector = connector
        
    def request_market_data(self, contract, tick_list=""):
        """Example request method"""
        if not self.connector.connected:
            raise ConnectionError("Not connected to IB")
        reqId = self.connector.next_valid_id
        self.connector.reqMktData(reqId, contract, tick_list, False, False, [])
        return reqId

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