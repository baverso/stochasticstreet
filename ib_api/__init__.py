"""
ib_api Package Initialization

This package handles all interactions with the Interactive Brokers API, including:
- Managing connections
- Handling callbacks for real-time and historical data
- Making requests for account, contract, and market data
- Providing utilities for data formatting and logging
"""

from .ib_base import IBBase
from .ib_connector import IBConnector
from .ib_callbacks import IBCallbacks
from .ib_requests import IBRequests
from .logging_config import LoggingConfig

# Initialize logging for the package
LoggingConfig.setup_logging()

# Package-level constants (customize as needed)
PACKAGE_NAME = "IB API Integration for stochasticstreet"
VERSION = "1.0.0"

__all__ = [
    "IBConnector",
    "IBCallbacks",
    "IBRequests",
    "IBBase",
    "LoggingConfig",
    "PACKAGE_NAME",
    "VERSION",
]