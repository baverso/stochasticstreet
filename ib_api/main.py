"""
main.py

This module is the entry point for the IB API client application.
Initialize the IBConnector, start the connection, and handle user input for the client application.
This module is responsible for managing the lifecycle of the IB API client application.
"""
import logging
import argparse
from ibapi.contract import Contract
from ib_connector import IBConnector
from ib_callbacks import IBCallbacks
from ib_requests import IBRequests
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

def create_contract():
    """Create a sample contract for testing"""
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract

def main():
    # Create single connector instance that handles both EClient and EWrapper
    connector = IBConnector()
    
    # Initialize requests and callbacks with the connector
    callbacks = IBCallbacks(connector)
    requests = IBRequests(connector)
    
    try:
        # Start the connection
        connector.start(host="127.0.0.1", port=7497, clientId=1)  # Changed port to 7497 for paper trading
        
        # Wait for connection to be established
        print("Connecting to IB...")
        max_wait = 10  # Maximum seconds to wait
        wait_time = 0
        while not connector.connected and wait_time < max_wait:
            time.sleep(1)
            wait_time += 1
            
        if not connector.connected:
            print("Failed to connect to IB after {} seconds".format(max_wait))
            return
            
        print("Successfully connected to IB")
        
        # Now you can use requests and callbacks will work
        contract = create_contract()
        requests.request_market_data(contract)
        
        # Keep the main thread running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except ConnectionError as e:
        print(f"Connection error: {e}")
        print("Please ensure that:")
        print("1. TWS or IB Gateway is running")
        print("2. API connections are enabled in TWS/Gateway")
        print("3. You're using the correct port (7496 for live, 7497 for paper trading)")
    finally:
        if hasattr(connector, 'connected') and connector.connected:
            connector.stop_connection()

if __name__ == "__main__":
    main()