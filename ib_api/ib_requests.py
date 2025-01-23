"""
ib_requests.py

Contains classes or methods for sending requests to the IB API
(e.g., requesting market data, historical data, orders, etc.).
By putting requests in a dedicated class, we keep them separate
from connection logic and callback logic.
"""

import logging
from ibapi.contract import Contract


class IBRequests:
    """
    A helper class for sending IB API requests through an active
    IBConnector instance.
    """

    def __init__(self, ib_connector):
        """
        :param ib_connector: An instance of IBConnector (EClient).
        """
        self.ib = ib_connector
        self.logger = logging.getLogger(self.__class__.__name__)

    def request_current_time(self):
        """
        A simple request to get current time from IB server.
        Callback is handled in IBCallbacks.currentTime().
        """
        self.logger.info("Requesting current time...")
        self.ib.reqCurrentTime()

    def request_market_data(self, req_id: int, contract: Contract, generic_tick_list: str = "", snapshot: bool = False,
                            regulatory_snapshot: bool = False):
        """
        Requests market data for a specified contract.
        For real-time streaming data, snapshot=False is typical.

        :param req_id: Request identifier.
        :param contract: IBAPI Contract object.
        :param generic_tick_list: Comma-separated list of tick types.
        :param snapshot: If True, only one-time snapshot data is returned.
        :param regulatory_snapshot: If True, a regulatory snapshot is requested.
        """
        self.logger.info(f"Requesting market data for ReqId={req_id}, Contract={contract.symbol}.")
        self.ib.reqMktData(req_id, contract, generic_tick_list, snapshot, regulatory_snapshot, [])

    def cancel_market_data(self, req_id: int):
        """
        Cancels market data subscription for a given request ID.
        """
        self.logger.info(f"Cancelling market data for ReqId={req_id}.")
        self.ib.cancelMktData(req_id)

    # Example for requesting historical data:
    def request_historical_data(self, req_id: int, contract: Contract, end_date_time: str, duration_str: str,
                                bar_size_setting: str, what_to_show: str, use_rth: int, format_date: int):
        """
        Request historical data from IB for a given contract.
        The data is returned via the `historicalData` callback.

        Args:
            req_id (int):
                A unique identifier for the request.
                Example: 1001

            contract (Contract):
                An IBAPI Contract object representing the financial instrument for which historical data is requested.
                Example: A Contract object for "AAPL" (Apple Inc.) or ES futures.

            end_date_time (str):
                The request's end date and time in the format 'YYYYMMDD HH:MM:SS' (in the local time zone).
                This defines the most recent point in time for the data requested.
                Example: '20250122 23:59:59'

            duration_str (str):
                The duration of the data request, specifying how much historical data is retrieved.
                Valid examples:
                - '1 D' (1 day)
                - '1 W' (1 week)
                - '1 M' (1 month)
                - '3 Y' (3 years)

            bar_size_setting (str):
                The size of the bars (candlesticks) in the returned data.
                Examples:
                - '1 min' (1-minute bars)
                - '5 mins' (5-minute bars)
                - '1 day' (daily bars)
                - '1 hour' (hourly bars)

            what_to_show (str):
                Specifies the type of data to retrieve. Common values include:
                - 'TRADES': Trade prices.
                - 'MIDPOINT': The midpoint of the bid and ask.
                - 'BID': Bid prices.
                - 'ASK': Ask prices.
                - 'BID_ASK': Both bid and ask data.
                - 'HISTORICAL_VOLATILITY': Historical volatility data.
                - 'OPTION_IMPLIED_VOLATILITY': Option implied volatility data.

            use_rth (int):
                Whether to use regular trading hours (RTH) only:
                - 1: Yes, retrieve data from regular trading hours only.
                - 0: No, include all available hours (e.g., pre-market and after-hours).

            format_date (int):
                Specifies the format of the returned dates:
                - 1: Date and time in the format 'YYYYMMDD HH:MM:SS'.
                - 2: Epoch time (number of seconds since January 1, 1970).

        Returns:
            None. The data is retrieved asynchronously and delivered via the `historicalData` callback.

        Example Usage:
            # Create a Contract for Apple Inc.
            contract = Contract()
            contract.symbol = "AAPL"
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"

            # Request 1 week of 1-hour bars for Apple Inc., showing trade prices
            self.request_historical_data(
                req_id=1001,
                contract=contract,
                end_date_time='20250122 23:59:59',
                duration_str='1 W',
                bar_size_setting='1 hour',
                what_to_show='TRADES',
                use_rth=1,
                format_date=1
            )
        """
        self.logger.info(f"Requesting historical data for ReqId={req_id}, Symbol={contract.symbol}.")
        self.ib.reqHistoricalData(
            req_id,
            contract,
            end_date_time,
            duration_str,
            bar_size_setting,
            what_to_show,
            use_rth,
            format_date,
            False,  # False for historical data only (not streaming updates)
            []
        )
    # Example placeholder for placing an order:
    # def place_order(self, order_id: int, contract: Contract, order: Order):
    #     self.logger.info(f"Placing order Id={order_id}, Symbol={contract.symbol}.")
    #     self.ib.placeOrder(order_id, contract, order)