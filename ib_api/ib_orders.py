"""
ib_orders.py

This module provides wrapper functions for handling order-related requests in Interactive Brokers (IB) API.
It encapsulates native IBAPI functions, making them easier to use and understand.

All functions include detailed documentation, examples, and identification of callbacks where applicable.
"""

import logging
from ibapi.contract import Contract
from ibapi.order import Order


class IBOrders:
    """
    A helper class for handling order-related requests using the IB API.
    """

    def __init__(self, ib_connector):
        """
        Initialize the IBOrders class.

        Args:
            ib_connector: An instance of IBConnector (EClient).
        """
        self.ib = ib_connector
        self.logger = logging.getLogger(self.__class__.__name__)

    def exercise_options(self, req_id: int, contract: Contract, exercise_action: int, exercise_quantity: int,
                         account: str, override: int):
        """
        Exercise options for a given contract.

        Args:
            req_id (int): A unique request ID.
            contract (Contract): An IBAPI Contract object representing the option to be exercised.
            exercise_action (int): Action to perform. 1 for exercise, 2 for lapse.
            exercise_quantity (int): Number of contracts to exercise.
            account (str): The account identifier.
            override (int): Set to 1 to override restrictions, 0 otherwise.

        Example:
            # Exercise an AAPL call option
            contract = Contract()
            contract.symbol = "AAPL"
            contract.secType = "OPT"
            contract.currency = "USD"
            contract.exchange = "SMART"
            contract.lastTradeDateOrContractMonth = "20250119"
            contract.strike = 150.0
            contract.right = "C"

            orders.exercise_options(
                req_id=1001,
                contract=contract,
                exercise_action=1,
                exercise_quantity=1,
                account="DU123456",
                override=0
            )
        """
        self.logger.info(f"Exercising options for ReqId={req_id}, Contract={contract.symbol}.")
        self.ib.exerciseOptions(req_id, contract, exercise_action, exercise_quantity, account, override)

    def cancel_order(self, order_id: int):
        """
        Cancels an open order by order ID.

        Args:
            order_id (int): The ID of the order to cancel.

        Example:
            # Cancel an order with ID 1001
            orders.cancel_order(order_id=1001)
        """
        self.logger.info(f"Cancelling order with OrderId={order_id}.")
        self.ib.cancelOrder(order_id)

    def req_open_orders(self):
        """
        Request a list of all open orders.

        Callback:
            openOrder(): Provides details about each open order.
            orderStatus(): Provides the status of each order.

        Example:
            # Request open orders
            orders.req_open_orders()
        """
        self.logger.info("Requesting list of open orders.")
        self.ib.reqOpenOrders()

    def req_auto_open_orders(self, auto_bind: bool):
        """
        Automatically bind newly created orders to this client.

        Args:
            auto_bind (bool): Set to True to automatically bind orders, False otherwise.

        Example:
            # Automatically bind orders to this client
            orders.req_auto_open_orders(auto_bind=True)
        """
        self.logger.info(f"Requesting auto-binding of orders: {auto_bind}.")
        self.ib.reqAutoOpenOrders(auto_bind)

    def req_all_open_orders(self):
        """
        Request a list of all open orders from all clients.

        Callback:
            openOrder(): Provides details about each open order.
            orderStatus(): Provides the status of each order.

        Example:
            # Request all open orders
            orders.req_all_open_orders()
        """
        self.logger.info("Requesting all open orders.")
        self.ib.reqAllOpenOrders()

    def req_global_cancel(self):
        """
        Cancels all active orders globally across all clients.

        Example:
            # Cancel all active orders globally
            orders.req_global_cancel()
        """
        self.logger.info("Requesting global cancellation of all active orders.")
        self.ib.reqGlobalCancel()

    def req_ids(self, num_ids: int):
        """
        Request unique order IDs.

        Args:
            num_ids (int): Number of IDs to request.

        Callback:
            nextValidId(): Provides the next valid ID.

        Example:
            # Request 10 unique order IDs
            orders.req_ids(num_ids=10)
        """
        self.logger.info(f"Requesting {num_ids} unique order IDs.")
        self.ib.reqIds(num_ids)

    def req_completed_orders(self, api_only: bool = True):
        """
        Request a list of completed orders.

        Args:
            api_only (bool): If True, request only orders created via the API.
                             If False, include manually created orders as well.

        Callback:
            completedOrder(): Provides details about each completed order.

        Example:
            # Request completed orders created via the API
            orders.req_completed_orders(api_only=True)
        """
        self.logger.info(f"Requesting completed orders with API-only={api_only}.")
        self.ib.reqCompletedOrders(api_only)