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


    ### TEST CONTRACT REQUESTS ###

    # Example: Request Market Data for a given symbol
    # Here, you'd need to set up a Contract object
    from ib_contract import IBContract

    # Example 1: Stock contract for Apple Inc. on SMART exchange
    stock_contract = IBContract.create_contract(
        symbol="AAPL",
        sec_type="STK",
        exchange="SMART",
        currency="USD",
        primary_exchange="NASDAQ"
    )
    logging.info(f"Stock Contract: {stock_contract}")

    # Example 2: Options contract for Apple Inc. Call option
    option_contract = IBContract.create_contract(
        symbol="AAPL",
        sec_type="OPT",
        exchange="SMART",
        currency="USD",
        last_trade_date="20250321",
        strike=150.0,
        right="C",
        multiplier="100"
    )
    logging.info(f"Options Contract: {option_contract}")

    # Example 3: Futures contract for S&P 500 Index (ES) on CME
    futures_contract = IBContract.create_contract(
        symbol="ES",
        sec_type="FUT",
        exchange="CME",
        currency="USD",
        last_trade_date="20250321"
    )
    logging.info(f"Futures Contract: {futures_contract}")

    # Example 4: Forex pair for EUR/USD
    forex_contract = IBContract.create_contract(
        symbol="EUR",
        sec_type="CASH",
        exchange="IDEALPRO",
        currency="USD"
    )
    logging.info(f"Forex Contract: {forex_contract}")

    # Example 5: Commodity contract for Gold on COMEX
    commodity_contract = IBContract.create_contract(
        symbol="GC",
        sec_type="CMDTY",
        exchange="COMEX",
        currency="USD",
        last_trade_date="20250321"
    )
    logging.info(f"Commodity Contract: {commodity_contract}")

    logging.info("Contracts created successfully.")


    # Example: Request Market Data for a given contract
    contracts = [stock_contract, option_contract, futures_contract, forex_contract, commodity_contract]

    # Request historical market data for each contract
    # Request historical market data for all contracts
    for idx, contract in enumerate(contracts, start=1):
        logging.info("Requesting historical data for contract: %s", contract.symbol)
        requests.request_historical_data(
            req_id=idx,
            contract=contract,
            end_date_time="",  # Empty string for current time
            duration_str="1 D",  # 1 Day of historical data
            bar_size_setting="1 min",  # 1-minute bars
            what_to_show="TRADES",  # Data type (e.g., TRADES, MIDPOINT)
            use_rth=1,  # 1 = Regular Trading Hours only
            format_date=1,  # 1 = Date format in YYYYMMDD HH:MM:SS
        )

    # not functioning without a premium data subscription
    # requests.request_market_data(req_id=1, contract=contract)


    # Let some data flow in
    time.sleep(10)

    # Disconnect
    ib.disconnect()


if __name__ == "__main__":
    main()