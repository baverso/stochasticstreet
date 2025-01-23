"""
main.py

Entry point for the IB API application. Demonstrates how to use the
IBConnector, IBRequests, and IBCallbacks classes together.
"""

import logging
import time

from ib_connector import IBConnector
from ib_requests import IBRequests
from ib_callbacks import IBCallbacks


def main():
    # Configure logging (optional)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )

    # Create an instance of our custom EWrapper
    callbacks = IBCallbacks()

    # Create a connector (EClient) and pass in our callbacks
    ib = IBConnector(callbacks=callbacks)

    # Connect to the IB gateway / TWS.
    # By default, TWS runs on 127.0.0.1:7497 or 7496
    # IB Gateway runs on 127.0.0.1:4001 or 4002
    ib.connect(host="127.0.0.1", port=4001, client_id=1)

    # Start the networking thread to process messages from IB
    ib.start()

    # Give IB a moment to finalize the connection
    time.sleep(2)

    ib.get_connection_status()

    # Make some example requests
    requests = IBRequests(ib)

    # Example: Request the current time (simple test)
    requests.request_current_time()
    time.sleep(2)

    # Example: Request Market Data for a given symbol
    # Here, you'd need to set up a Contract object
    from ibapi.contract import Contract

    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    requests.request_market_data(req_id=1, contract=contract)

    # Let some data flow in
    time.sleep(10)

    # Disconnect
    ib.disconnect()


if __name__ == "__main__":
    main()