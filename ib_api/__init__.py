"""
ib_api Package Initialization

This package handles all interactions with the Interactive Brokers API, including:
- Managing connections
- Handling callbacks for real-time and historical data
- Making requests for account, contract, and market data
- Providing utilities for data formatting and logging
"""

from stochasticstreet.ib_api.ib_connector import IBConnector
# from stochasticstreet.ib_api.ib_callbacks import IBCallbacks
# from stochasticstreet.ib_api.ib_requests import IBRequests
from stochasticstreet.ib_api.ib_utils import setup_logging

# Initialize logging for the package
setup_logging()

# Package-level constants (customize as needed)
PACKAGE_NAME = "IB API Integrationh for stochasticstreet"
VERSION = "1.0.0"

__all__ = [
    "IBConnector",
    # "IBCallbacks",
    # "IBRequests",
    "setup_logging",
    "PACKAGE_NAME",
    "VERSION",
]