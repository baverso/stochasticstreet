import logging
from stochasticstreet.ib_api.ib_connector import IBConnector

class IBRequests(IBConnector):
    """
    Handles all API requests for the Interactive Brokers API.
    Inherits from IBConnector to access connection methods.
    """

    def request_account_summary(self, req_id, verbose=False):
        """
        Request account summary based on the verbosity.

        Args:
            req_id (int): A unique request ID.
            verbose (bool): If True, returns all account summary tags. Defaults to False.

        Returns:
            None
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

        # Select tags based on the verbosity
        tags = ",".join(verbose_tags if verbose else regular_tags)

        # Make the API request
        self.reqAccountSummary(req_id, "All", tags)

        # Log the request
        logging.info(
            "Account summary request made. Mode: %s, Tags: %s",
            "Verbose" if verbose else "Regular",
            tags,
        )