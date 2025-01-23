
# ib_api Package Overview

The `ib_api` package is the core integration layer with Interactive Brokers. It includes:

### 1. `__init__.py`
- Imports and re-exports the main classes (`IBConnector`, `IBCallbacks`, `IBRequests`, `LoggingConfig`).
- Calls `LoggingConfig.setup_logging()` to initialize logging at package load.
- Defines package-level constants (`PACKAGE_NAME`, `VERSION`).

### 2. `ib_connector.py`
- **Class:** `IBConnector` (inherits from `EClient`)
  - Manages the connection to IB TWS/Gateway.
  - Requires an `EWrapper`-derived instance (e.g., `IBCallbacks`) passed in the constructor.
  - Handles `connect()`, `disconnect()`, and starts the networking thread for IB communication (`start()`).

### 3. `ib_callbacks.py`
- **Class:** `IBCallbacks` (inherits from `EWrapper`)
  - Receives asynchronous data/events from IB TWS/Gateway and routes them for processing or logging.
  - Overrides callback methods like `error()`, `currentTime()`, `tickPrice()`, etc.

### 4. `ib_requests.py`
- **Class:** `IBRequests`
  - Encapsulates high-level request methods to IB, such as:
    - `req_current_time()`
    - `req_market_data()` / `cancel_market_data()`
    - `request_historical_data()` / `cancel_historical_data()`
    - `req_account_updates()`
  - Requires an instance of `IBConnector` to call EClient methods (e.g., `reqMktData`, `reqHistoricalData`).

### 5. `ib_orders.py`
- **Class:** `IBOrders`
  - Specialized helper for order-related requests:
    - `exercise_options()`, `cancel_order()`, `req_open_orders()`, `req_auto_open_orders()`, etc.
  - Takes an `IBConnector` (or any `EClient`-derived object) to send these requests to IB.

### 6. `ib_contract.py`
- **Class:** `IBContract`
  - Provides static methods to build Contract objects (e.g., for stocks, options, futures).
  - Simplifies contract creation by setting the relevant attributes (`symbol`, `secType`, `exchange`, etc.).

### 7. `logging_config.py`
- **Module:** `LoggingConfig`
  - Contains a `setup_logging()` function to ensure consistent logging:
    - Creates a `logs/` directory if needed.
    - Configures a `FileHandler` and `StreamHandler`, ensuring consistent log formatting.
  - Called automatically when the `ib_api` package is imported (via `__init__.py`).
```
ROOT DIRECTORY
|
|-- ib_api/
|   |-- __init__.py           # Package initialization for ib_api
|   |-- ib_callbacks.py       # Custom EWrapper callbacks
|   |-- ib_connector.py       # EClient-based connection logic
|   |-- ib_requests.py        # High-level request methods to IB
|   |-- ib_orders.py          # Order-related request methods
|   |-- ib_contract.py        # Helpers to create Contract objects
|   |-- logging_config.py     # Central logging configuration
|
|-- data_processing/
|   |-- __init__.py
|   |-- historical_data.py    # Handling/storage of historical data
|   |-- realtime_data.py      # Handling storage of real-time data
|   |-- timeseries_db.py      # Interface to time-series database
|
|-- data_storage/
|   |-- __init__.py
|   |-- local_storage.py      # Local storage (e.g., external drive)
|
|-- notebooks/
|   |-- main.ipynb            # Jupyter notebook for interactive tests
|   |-- historical_analysis.ipynb   # Analyzing historical data
|   |-- trading_strategy.ipynb      # Building/testing trading strategies
|
|-- config/
|   |-- settings.py           # Configuration for API keys, DB connections, etc.
|
|-- logs/
|   |-- ib_api.log            # IB API operations log (default location)
|
|-- requirements.txt          # Dependencies
|-- README.md                 # Overview & instructions
|-- main.py                   # Script entry point with argparse
```
---

## Data Flow and Network Map

Here’s how the data typically flows between the modules and the IB API:

```plaintext
[IB API]
|
v
[ib_connector.py] -- initializes --> [ib_callbacks.py]
|                                      |
v                                      v
[ib_requests.py] <------ requests ------ [ib_callbacks.py]
|                                      |
v                                      v
[ib_orders.py] <------- manages -------- [ib_callbacks.py]
|                                      |
v                                      v
[Real-Time Data] ------------------> [data_processing/realtime_data.py]
|                                      |
v                                      v
[Trading Algorithms] -----------------> [External SSD (Snapshots)]
|                                      |
v                                      v
[Execution Layer] ------------------> [IB API]

[ib_callbacks.py] -------> [data_processing/historical_data.py]
|                                      |
v                                      v
[Historical Data] -----------------> [Timeseries DB Interface]
|                                      |
v                                      v
[External SSD (Backups)] ------------> [Jupyter Notebooks]

```




1. **[IB API]**
   - External IB TWS or Gateway that we connect to.
   - Sends real-time market data, order status updates, historical data, etc.
   - Receives order requests, market data requests, etc.

2. **[ib_connector.py → IBConnector (EClient)]**
   - Establishes the socket connection to TWS/Gateway (`connect(host, port, client_id)`).
   - Spawns the networking thread (`start()`) to continuously read messages.
   - Delegates inbound messages to the attached `EWrapper` instance (i.e., `IBCallbacks`).

3. **[ib_callbacks.py → IBCallbacks (EWrapper)]**
   - Receives all asynchronous event callbacks (`tickPrice`, `historicalData`, `error`, etc.).
   - Decodes or logs data, and passes it to other modules (e.g., real-time or historical data handlers in `data_processing`).

4. **[ib_requests.py → IBRequests]**
   - High-level request interface that calls methods on `IBConnector` (like `reqMarketData`, `reqHistoricalData`).
   - Simplifies making requests by providing user-friendly function signatures.

5. **[ib_orders.py → IBOrders]**
   - Focuses on order placement and management (e.g., `exercise_options`, `cancel_order`, `req_open_orders`).
   - References the same `IBConnector` to send requests to IB.

6. **Data Processing & Storage**
   - Once data arrives in `IBCallbacks`, it is passed to:
     - `data_processing/realtime_data.py` for immediate usage (e.g., trading signals).
     - `data_processing/historical_data.py` for cleaning and archiving historical data.
     - `timeseries_db.py` or local storage for long-term record-keeping.

7. **Logging**
   - All modules use the Python `logging` module, configured by `logging_config.py`.
   - A single log file (e.g., `logs/app.log` or `logs/ib_api.log`) receives all structured logs.

---

## Script Entry Points

### `main.py`
- The primary script entry point for your IB integration.
- Uses `argparse` to accept runtime parameters (`--host`, `--port`, `--client-id`, `--account`).
- Demonstrates how to:
  1. Create an `IBCallbacks` instance.
  2. Pass it to `IBConnector` for establishing the TWS/Gateway connection.
  3. Create an `IBRequests` (and optionally `IBOrders`) instance for making requests.
  4. Run test calls, then gracefully disconnect.

### Jupyter Notebooks
- `notebooks/main.ipynb`:
  - For interactive testing of functionality in a Jupyter environment.
  - Import the same `ib_api` modules, create a connector, and run requests step by step.

---

## Inheritance & Relationships

1. **`IBCallbacks` → `EWrapper`**
   - Fundamental interface for receiving data from IB.
   - Overrides methods like `error()`, `tickPrice()`, `historicalData()`, etc.

2. **`IBConnector` → `EClient`**
   - Fundamental interface for sending data to IB (`connect`, request market data, place orders, etc.).
   - Must be paired with an `EWrapper` instance (e.g., `IBCallbacks`).

3. **`IBRequests`**
   - Uses `IBConnector` internally to call methods like `reqMktData()`.
   - Not an `EClient` subclass—just a convenience layer.

4. **`IBOrders`**
   - Uses `IBConnector` to call `placeOrder()`, `cancelOrder()`, etc.
   - Also not an `EClient` subclass—just a specialized interface.

5. **`IBContract`**
   - Utility class for building `Contract` objects.
   - No inheritance from IB classes.

6. **`LoggingConfig`**
   - Helper module to set up Python logging across the codebase.

---

## Summary

The `ib_api` package is the central layer for connecting to Interactive Brokers and managing data.

### Main Components:
- `IBConnector` (`EClient`) – Connection layer.
- `IBCallbacks` (`EWrapper`) – Callback/event layer.
- `IBRequests` – High-level request interface.
- `IBOrders` – High-level order interface.
- `IBContract` – Contract-building utility.
- `LoggingConfig` – Logging configuration.

### Data Flow:
Data flows from IB API → `IBConnector` → `IBCallbacks` and out via `IBRequests`/`IBOrders`.

### Entry Points:
- `main.py`: Demonstrates usage.
- Jupyter notebooks: Enable interactive testing.

This modular architecture separates concerns, ensuring the codebase is clean, testable, and extensible.

