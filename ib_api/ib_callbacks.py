"""
ib_callbacks.py

This module contains a class (IBCallbacks) that inherits from EWrapper
and overrides callback methods. You can add methods to handle all events
such as tickPrice, orderStatus, historicalData, etc.
"""

import logging
from ibapi.wrapper import EWrapper

from datetime import datetime, timezone, timedelta


class IBCallbacks(EWrapper):
    """
    A dedicated class to handle all callbacks from the IB API (EWrapper).
    Custom logic for data handling, logging, or data frames can be placed here.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        """
        Handles errors sent from TWS/IB gateway.
        """
        if reqId > 0:
            self.logger.error(
                f"Error. Id: {reqId}, Code: {errorCode}, Msg: {errorString}. "
                f"AdvancedOrderRejectJson: {advancedOrderRejectJson}"
            )
        else:
            self.logger.warning(
                f"TWS Warning. Code: {errorCode}, Msg: {errorString}. "
                f"AdvancedOrderRejectJson: {advancedOrderRejectJson}"
            )



    def currentTime(self, time_from_server):
        """
        Callback when the current time is returned from IB.
        Converts the Unix timestamp to a human-readable format in EST.
        """
        # Convert the timestamp to UTC datetime
        utc_time = datetime.fromtimestamp(time_from_server, tz=timezone.utc)

        # Convert UTC to EST (adjusting for daylight saving time if necessary)
        est_offset = timedelta(hours=-5)  # EST is UTC-5
        est_time = utc_time + est_offset

        # Log both UTC and EST time
        self.logger.info(f"Current IB server time (UTC): {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        self.logger.info(f"Current IB server time (EST): {est_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    def tickPrice(self, reqId, tickType, price, attrib):
        """
        Handles tick price events for market data.
        You can also handle tickSize, tickString, etc.
        """
        self.logger.info(
            f"Tick Price. Ticker Id: {reqId}, Field: {tickType}, Price: {price}"
        )

    # Add more callbacks as needed...
    # def tickSize(self, reqId, tickType, size):
    #     pass

    # def historicalData(self, reqId, bar):
    #     pass

    # def orderStatus(self, orderId, status, filled, remaining, avgFillPrice,
    #                 permId, parentId, lastFillPrice, clientId,
    #                 whyHeld, mktCapPrice):
    #     pass