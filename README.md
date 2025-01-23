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

Explanation
	1.	Denali/CME Data Feed
	•	Supplies futures market data (real-time & historical) to Sierra Chart.
	•	Typically requires a subscription through Sierra Chart.
	2.	Virtual Machine (VM) (or local Windows instance if preferred)
	•	Runs Sierra Chart to receive Denali data.
	•	Exposes a DTC server, allowing external processes to subscribe to streaming market data.
	3.	Local Environment (Host OS)
	•	Your Python code requests real-time quotes/market depth via DTC.
	•	For order execution and account data, it connects to Interactive Brokers API (TWS or Gateway).
	4.	Interactive Brokers
	•	The “live” brokerage interface for order routing.
	•	Hosted on your machine at 127.0.0.1:7497 (TWS) or 127.0.0.1:4001 (IB Gateway).
	5.	Data & Order Flow
	•	Data: Denali/CME → Sierra Chart → DTC → Python
	•	Orders: Python → IBKR API → Exchanges

For many Windows users, Sierra Chart can run directly on the host OS without a VM. The above diagram simply illustrates one recommended approach to isolating the charting software if desired.