"""
main.py

This module is the entry point for the IB API client application.
Initialize the IBConnector, start the connection, and handle user input for the client application.
This module is responsible for managing the lifecycle of the IB API client application.
"""
import logging
import argparse
from .ib_connector import IBConnector
from .ib_callbacks import IBCallbacks
from .ib_requests import IBRequests
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

def main():
    # Create single connector instance that handles both EClient and EWrapper
    connector = IBConnector()
    
    # Initialize requests and callbacks with the connector
    callbacks = IBCallbacks(connector)
    requests = IBRequests(connector)
    
    # Start the connection
    connector.start(host="127.0.0.1", port=7496, clientId=1)
    
    # Now you can use requests and callbacks will work
    # Example:
    contract = create_contract()  # Your contract creation logic
    requests.request_market_data(contract)

if __name__ == "__main__":
    main()