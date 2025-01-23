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
        Callback is handled in IBCallbacks.historicalData().
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
            False,
            []
        )

    # Example placeholder for placing an order:
    # def place_order(self, order_id: int, contract: Contract, order: Order):
    #     self.logger.info(f"Placing order Id={order_id}, Symbol={contract.symbol}.")
    #     self.ib.placeOrder(order_id, contract, order)