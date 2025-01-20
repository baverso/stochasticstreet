import logging
from stochasticstreet.ib_api import IBBase

class IBCallbacks(IBBase):
    """
    Handles all callbacks from the Interactive Brokers API.
    Processes data returned by the API and forwards it to the appropriate handlers.
    """

    def __init__(self):
        """
        Initializes the IBRequests class.
        """
        super().__init__()

    # Connection-related callbacks
    def connectAck(self):
        """
        Called when the API acknowledges the connection.
        """
        logging.info("Connection acknowledged by IB API.")

    def connectionClosed(self):
        """
        Called when the connection to the IB API is closed.
        """
        logging.warning("Connection to IB API closed.")

    def error(self, reqId, errorCode, errorMsg, advancedOrderRejectJson=""):
        """
        Handles errors received from the API.

        Args:
            reqId (int): The request ID associated with the error.
            errorCode (int): The error code returned by the API.
            errorMsg (str): A descriptive error message.
            advancedOrderRejectJson (str, optional): Advanced order rejection details.
        """
        if advancedOrderRejectJson:
            logging.error(
                f"Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorMsg}, AdvancedReject: {advancedOrderRejectJson}"
            )
        else:
            logging.error(f"ERROR ReqId: {reqId}, Code: {errorCode}, Msg: {errorMsg}")

    # Account summary-related callbacks
    def accountSummary(self, reqId, account, tag, value, currency):
        logging.info(
            "Account Summary - ReqId: %d, Account: %s, Tag: %s, Value: %s, Currency: %s",
            reqId, account, tag, value, currency,
        )

    def accountSummaryEnd(self, reqId):
        """
        Called when all account summary data for a request has been received.

        Args:
            reqId (int): The request ID for this summary.
        """
        logging.info("Account Summary End: ReqId=%s", reqId)

    # Position-related callbacks
    def position(self, account, contract, position, avgCost):
        """
        Called when position data is received.

        Args:
            account (str): The account identifier.
            contract (Contract): The contract for this position.
            position (float): The number of units held.
            avgCost (float): The average cost of the position.
        """
        logging.info(
            "Position: Account=%s, Contract=%s, Position=%s, AvgCost=%s",
            account,
            contract.symbol,
            position,
            avgCost,
        )

    def positionEnd(self):
        """
        Called when all position data has been received.
        """
        logging.info("Position data received completely.")

    # Market data-related callbacks
    def tickPrice(self, reqId, tickType, price, attrib):
        """
        Called when tick price data is received.

        Args:
            reqId (int): The request ID for this tick data.
            tickType (int): The type of tick (e.g., bid, ask, last).
            price (float): The price value.
            attrib (TickAttrib): Additional tick attributes.
        """
        logging.info(
            "Tick Price: ReqId=%s, TickType=%s, Price=%s", reqId, tickType, price
        )

    def tickSize(self, reqId, tickType, size):
        """
        Called when tick size data is received.

        Args:
            reqId (int): The request ID for this tick data.
            tickType (int): The type of tick (e.g., bid size, ask size).
            size (int): The size value.
        """
        logging.info(
            "Tick Size: ReqId=%s, TickType=%s, Size=%s", reqId, tickType, size
        )

    def tickSnapshotEnd(self, reqId):
        """
        Called when a tick snapshot is complete.

        Args:
            reqId (int): The request ID for this snapshot.
        """
        logging.info("Tick Snapshot End: ReqId=%s", reqId)

    # Contract details callbacks
    def contractDetails(self, reqId, contractDetails):
        """
        Called when contract details are received.

        Args:
            reqId (int): The request ID for this data.
            contractDetails (ContractDetails): The details of the contract.
        """
        logging.info(
            "Contract Details: ReqId=%s, Symbol=%s, Exchange=%s",
            reqId,
            contractDetails.contract.symbol,
            contractDetails.contract.exchange,
        )

    def contractDetailsEnd(self, reqId):
        """
        Called when all contract details for a request have been received.

        Args:
            reqId (int): The request ID for this data.
        """
        logging.info("Contract Details End: ReqId=%s", reqId)

    # Order-related callbacks
    def openOrder(self, orderId, contract, order, orderState):
        """
        Called when an open order is received.

        Args:
            orderId (int): The order ID.
            contract (Contract): The contract for the order.
            order (Order): The details of the order.
            orderState (OrderState): The state of the order.
        """
        logging.info(
            "Open Order: OrderId=%s, Contract=%s, OrderType=%s, Status=%s",
            orderId,
            contract.symbol,
            order.orderType,
            orderState.status,
        )

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        """
        Called when order status is updated.

        Args:
            orderId (int): The order ID.
            status (str): The order status.
            filled (float): The number of units filled.
            remaining (float): The number of units remaining.
            avgFillPrice (float): The average fill price.
        """
        logging.info(
            "Order Status: OrderId=%s, Status=%s, Filled=%s, Remaining=%s, AvgFillPrice=%s",
            orderId,
            status,
            filled,
            remaining,
            avgFillPrice,
        )

    def execDetails(self, reqId, contract, execution):
        """
        Called when execution details are received.

        Args:
            reqId (int): The request ID.
            contract (Contract): The contract for the execution.
            execution (Execution): The execution details.
        """
        logging.info(
            "Execution Details: ReqId=%s, Contract=%s, ExecId=%s, Shares=%s",
            reqId,
            contract.symbol,
            execution.execId,
            execution.shares,
        )