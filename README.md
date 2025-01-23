![Banner Image](images/bannerimage.jpeg "StochasticStreet Banner")

# StochasticStreet: An Open-Source Algotrading Platform

**StochasticStreet** is an open-source project dedicated to building flexible, modular utilities for algorithmic trading using Interactive Brokers (IBKR), Denali/CME data feeds, Sierra Chart (via DTC protocol), and Python-based machine learning workflows. By clearly separating concerns (data collection, real-time feeds, trading logic, order execution, and research notebooks), we aim to create a maintainable and extensible foundation for **backtesting**, **forward-testing**, **simulation**, and **live trading**.

> Inspired by projects like [ib_insync](https://github.com/erdewit/ib_insync) (for its clean design and user-friendliness), **StochasticStreet** adds additional layers of data plumbing—from Denali/CME feeds to Sierra Chart’s DTC server—alongside the Interactive Brokers API for order routing and account management.

---

## Table of Contents

1. [Features](#features)  
2. [Overview & Architecture](#overview--architecture)  
   - [High-Level Diagram](#high-level-diagram)  
   - [Explanation](#explanation)  
3. [Why Another Platform?](#why-another-platform)  
4. [Installation](#installation)  
5. [Usage Examples](#usage-examples)  
6. [Directory Structure](#directory-structure)  
7. [Project Status & Roadmap](#project-status--roadmap)  
8. [Contributing](#contributing)  
9. [License](#license)

---

## Features

- **Modular IBKR Integration:**  
  - Leverages **Interactive Brokers** TWS or Gateway via the native Python **ibapi**.  
  - Clear separation of **EWrapper** (callbacks) and **EClient** (requests) in dedicated modules.

- **Denali / CME Data Feed Support:**  
  - Uses **Sierra Chart** (running locally or on a VM) as a DTC server.  
  - Python scripts on the host OS can subscribe to real-time and historical **futures** data via **DTC**.

- **Robust Data Plumbing & Storage:**  
  - Tools to store historical and real-time data in local or remote time-series databases.  
  - Integration with external drives or SSDs for backups and snapshots.

- **Strategy Workflow:**  
  - End-to-end environment to **backtest** (historical), **paper trade** (forward test), and **go live** (real capital) using a consistent codebase.

- **Machine Learning & Notebook-Friendly:**  
  - Jupyter notebooks for data exploration, strategy design, and model training.  
  - Entire codebase in Python, making advanced data science workflows more seamless.

---

## Overview & Architecture

### High-Level Diagram

```plaintext
+-------------------------------------------+
|  Denali / CME Data Feed Service           |
|  (Real-time & historical futures data)    |
+-------------------^-----------------------+
                                        |
            DTC Protocol (Real-time)    |
                                        |
+---------------------------------+     |
| Local Environment (Host OS)     |     |
| - Python Strategies / Scripts   |     |
| - Connects to IBKR API          |     |
+----------------^----------------+     |
                 |                      |
                 | IBKR API             |
                 |                      v
     +------------------------+     +-------------------------+
     |  Interactive Brokers   |     | Virtual Machine (VM)    |
     |   TWS or IB Gateway    |     | running Sierra Chart    |
     +------------------------+     | - Subscribes to Denali  |
                                    | - Provides DTC Server   |
                                    +-----------^-------------+
                                                |
                                                |
                                         (DTC Protocol)
                                                |
                                                |
                                 +--------------v--------------+
                                 |   Python on Host OS         |
                                 |   requests data/trade info  |
                                 +-----------------------------+


```
# StochasticStreet Documentation

## Explanation

### 1. Denali/CME Data Feed
- Supplies futures market data (real-time & historical) to Sierra Chart.
- Typically requires a subscription through Sierra Chart.

### 2. Virtual Machine (VM) (or local Windows instance if preferred)
- Runs Sierra Chart to receive Denali data.
- Exposes a DTC server, allowing external processes to subscribe to streaming market data.

### 3. Local Environment (Host OS)
- Your Python code requests real-time quotes/market depth via DTC.
- For order execution and account data, it connects to Interactive Brokers API (TWS or Gateway).

### 4. Interactive Brokers
- The “live” brokerage interface for order routing.
- Hosted on your machine at 127.0.0.1:7497 (TWS) or 127.0.0.1:4001 (IB Gateway).

### 5. Data & Order Flow
- **Data**: Denali/CME → Sierra Chart → DTC → Python
- **Orders**: Python → IBKR API → Exchanges

> For many Windows users, Sierra Chart can run directly on the host OS without a VM. The above diagram simply illustrates one recommended approach to isolating the charting software if desired.

---

## Why Another Platform?

### 1. Separation of Concerns
We isolate:
- Connection to IBKR via `ib_connector`
- Callbacks and real-time data handling via `ib_callbacks`
- Request logic in `ib_requests` and order logic in `ib_orders`

This modular structure makes it easier to extend or swap out components without breaking everything.

### 2. Multi-Source Data Support
- **Denali/CME feed** for futures, **IBKR feed** for other instruments (or for backup).
- Unified approach to historical data ingestion and real-time updates, so you can develop once and adapt to multiple feeds.

### 3. Research & ML Integration
- Built with Jupyter notebooks in mind for exploration, backtesting, and machine learning.
- Entire codebase in Python, making advanced data science workflows more seamless.

---

## Installation

### 1. Clone this repo:
```bash
git clone https://github.com/YourUsername/StochasticStreet.git
cd StochasticStreet
```

### 2. Install Requirements:
```bash
pip install -r requirements.txt
```
Typical libraries include `ibapi` for Interactive Brokers, plus optional libraries for DTC, data science (`numpy`, `pandas`, `matplotlib`, `scipy`, etc.), and logging.

### 3. Configure Sierra Chart (If Using Denali):
- Enable the DTC server (in Sierra Chart: **Global Settings → Data/Trade Service Settings → DTC Settings**).
- Get your Denali subscription set up in Sierra Chart if you want real-time futures data.

### 4. Set Up TWS/IB Gateway:
- Launch TWS or IB Gateway, enable API access (**Configure → API → Settings**).
- Confirm the host/port matches the settings you will use in `main.py` (`--host`, `--port`).

### 5. Test the Connection:
```bash
python main.py --host 127.0.0.1 --port 7497 --client-id 999 --account DU123456
```
Adjust parameters as needed. If successful, you should see log messages indicating successful connection and data requests.

---

## Usage Examples

### Main Script (`main.py`):
Demonstrates how to set up the IB Connector and make requests:
```bash
python main.py --host 127.0.0.1 --port 7497 --client-id 5 --account DUXXXXXX
```

### Jupyter Notebook (`notebooks/main.ipynb`):
Shows interactive steps for requesting market data, analyzing real-time ticks, and placing a test order (in a paper account).

### Data Processing Modules (`data_processing/`):
- `historical_data.py`: Example code to store downloaded bars/ticks in a time-series database or CSV.
- `realtime_data.py`: Handling streaming data for immediate strategy decisions.

---

## Directory Structure

```plaintext
StochasticStreet/
├─ ib_api/
│  ├─ __init__.py          # Package init: sets up logging, re-exports key classes
│  ├─ ib_callbacks.py      # EWrapper subclass for IB callbacks
│  ├─ ib_connector.py      # EClient subclass for IB connection
│  ├─ ib_requests.py       # High-level request methods (market data, accounts, etc.)
│  ├─ ib_orders.py         # Specialized order/position methods
│  ├─ ib_contract.py       # Helper for creating IBAPI Contract objects
│  └─ logging_config.py    # Central logging config
├─ data_processing/
│  ├─ historical_data.py   # Downloading & formatting historical bars
│  ├─ realtime_data.py     # Low-latency or streaming data handling
│  ├─ timeseries_db.py     # DB interface (Influx, Timescale, etc.)
│  └─ __init__.py
├─ data_storage/
│  ├─ local_storage.py     # Interface to local external drives, etc.
│  └─ __init__.py
├─ notebooks/
│  ├─ main.ipynb           # Example interactive notebook
│  ├─ historical_analysis.ipynb
│  └─ trading_strategy.ipynb
├─ config/
│  └─ settings.py          # API keys, DB credentials, etc.
├─ logs/
│  └─ ib_api.log           # Default log file
├─ requirements.txt
├─ LICENSE (if any)
├─ README.md               # This file
└─ main.py                 # CLI entry point with argparse
```

---

## Project Status & Roadmap

- [x] Basic IBKR connector & callbacks
- [ ] Historical data requests + real-time streaming
- [ ] Denali/CME feed integration via DTC
- [ ] Expand library of built-in indicators & strategy templates
- [ ] Add robust backtesting framework
- [ ] Integrate more advanced ML tools (`PyTorch`, `TensorFlow`) for automated strategy exploration
- [ ] Enhanced GUI or dashboard for real-time monitoring

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Simply:
1. Fork the repo
2. Create a new branch (`feature/your-improvement`)
3. Submit a PR with a clear description of changes

We adhere to standard Python coding practices (PEP8) and rely on logging, type hints, and docstrings for maintainability.

---

## License

StochasticStreet is open-sourced under the GNU AFFERO GENERAL PUBLIC LICENSE. Please review the details to ensure compliance when using this project.

---

## Disclaimer

Trading involves substantial risk and is not suitable for all investors. This project is provided as is, without any guarantees. Always test in a paper trading environment before risking real capital.
"""
