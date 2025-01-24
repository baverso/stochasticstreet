"""
main.py

Entry point for the IB API application. Demonstrates how to use:
- IBConnector (EClient + connection management)
- IBRequests (all your request methods)
- IBCallbacks (custom callbacks)
- IBOrders (optional order-related calls)

Now includes argparse for dynamic configuration of host, port, client ID, and account.
"""

import argparse
import logging
import time

# Relative imports from within the same package directory:
from .ib_connector import IBConnector
from .ib_requests import IBRequests
from .ib_callbacks import IBCallbacks
from .ib_contract import IBContract
from .ib_orders import IBOrders
from .logging_config_json import LoggingConfig

# Additional IB API imports:
from ibapi.execution import ExecutionFilter
from ibapi.scanner import ScannerSubscription
def parse_arguments():
    """Parse command-line arguments for IB connection configuration."""
    parser = argparse.ArgumentParser(description="Python IBAPI Client Example")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Host IP for IB TWS/Gateway (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4002,
                        help="Port for IB TWS/Gateway (default: 7497 for TWS, 4001 for IB Gateway)")
    parser.add_argument("--client-id", type=int, default=1,
                        help="Client ID for the IB connection (default: 1)")
    parser.add_argument("--account", type=str, default="DUXXXXXX",
                        help="Account code to use for account-related requests (default: DUXXXXXX)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # 1. JSON LOGGING SETUP (replacing logging.basicConfig calls)
    LoggingConfig.setup_logging()

    # ------------------------------------------------------------------------------
    # 2. CREATE CALLBACKS + CONNECTOR + START THREAD
    # ------------------------------------------------------------------------------
    callbacks = IBCallbacks()
    ib = IBConnector(callbacks=callbacks)

    logging.info(f"Connecting to IB at {args.host}:{args.port} with client ID {args.client_id}")
    ib.connect(host=args.host, port=args.port, client_id=args.client_id)
    ib.start()

    # Give a brief pause to ensure connection is established
    time.sleep(3)

    # (Optional) If you have a method to check connection status:
    ib.get_connection_status()

    # ------------------------------------------------------------------------------
    # 3. CREATE REQUESTS + ORDERS HELPERS
    # ------------------------------------------------------------------------------
    requests = IBRequests(ib)
    orders = IBOrders(ib)  # if you want to test order-related calls

    # ------------------------------------------------------------------------------
    # 4. CONTRACT EXAMPLES
    # ------------------------------------------------------------------------------
    stock_contract = IBContract.create_contract(
        symbol="AAPL",      # Apple
        sec_type="STK",
        exchange="SMART",
        currency="USD",
        primary_exchange="NASDAQ"
    )

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

    futures_contract = IBContract.create_contract(
        symbol="ES",       # E-mini S&P 500
        sec_type="FUT",
        exchange="CME",
        currency="USD",
        last_trade_date="20250321"
    )

    forex_contract = IBContract.create_contract(
        symbol="EUR",
        sec_type="CASH",
        exchange="IDEALPRO",
        currency="USD"
    )

    commodity_contract = IBContract.create_contract(
        symbol="GC",       # Gold
        sec_type="CMDTY",
        exchange="COMEX",
        currency="USD",
        last_trade_date="20250321"
    )

    test_contract = stock_contract  # We'll primarily use the AAPL stock contract below.

    # ------------------------------------------------------------------------------
    # 5. BASIC REQUESTS
    # ------------------------------------------------------------------------------
    requests.req_current_time()
    time.sleep(2)

    # Request Market Data Type (e.g., delayed data = 3)
    requests.req_market_data_type(3)

    # Request Real-Time Market Data (if you have the subscription)
    requests.req_market_data(req_id=1001, contract=test_contract)
    time.sleep(3)
    requests.cancel_market_data(req_id=1001)

    # Tick-by-tick data
    requests.req_tick_by_tick_data(req_id=1101, contract=test_contract, tick_type="Last", number_of_ticks=0)
    time.sleep(3)
    requests.cancel_tick_by_tick_data(req_id=1101)

    # ------------------------------------------------------------------------------
    # 6. OPTIONS / VOLATILITY CALCULATIONS (Requires appropriate data subscription)
    # ------------------------------------------------------------------------------
    requests.calculate_implied_volatility(req_id=1201, contract=option_contract,
                                          option_price=10.5, under_price=150.0)
    time.sleep(2)
    requests.cancel_calculate_implied_volatility(req_id=1201)

    requests.calculate_option_price(req_id=1202, contract=option_contract,
                                    volatility=0.25, under_price=150.0)
    time.sleep(2)
    requests.cancel_calculate_option_price(req_id=1202)

    # ------------------------------------------------------------------------------
    # 7. ACCOUNT / PORTFOLIO REQUESTS
    # ------------------------------------------------------------------------------
    # Replace with your actual account code if not provided as an arg
    account_code = args.account

    requests.req_account_updates(True, account_code=account_code)
    time.sleep(3)
    requests.req_account_updates(False, account_code=account_code)

    requests.req_account_summary(req_id=1301, group_name="All", tags="NetLiquidation,TotalCashValue")
    time.sleep(3)
    requests.cancel_account_summary(req_id=1301)

    requests.req_positions()
    time.sleep(3)
    requests.cancel_positions()

    requests.req_positions_multi(req_id=1401, account=account_code, model_code="")
    time.sleep(2)
    requests.cancel_positions_multi(req_id=1401)

    requests.req_account_updates_multi(req_id=1501, account=account_code, model_code="", ledger_and_nlv=True)
    time.sleep(2)
    requests.cancel_account_updates_multi(req_id=1501)

    requests.req_pnl(req_id=1601, account=account_code)
    time.sleep(2)
    requests.cancel_pnl(req_id=1601)

    # If you know a valid ConId for a position in your account:
    # (AAPL is often 265598 but it may differ)
    requests.req_pnl_single(req_id=1701, account=account_code, model_code="", con_id=265598)
    time.sleep(2)
    requests.cancel_pnl_single(req_id=1701)

    # Execution filter
    exec_filter = ExecutionFilter()
    requests.req_executions(req_id=1801, execution_filter=exec_filter)
    time.sleep(2)

    # ------------------------------------------------------------------------------
    # 8. CONTRACT DETAILS, MARKET DEPTH, NEWS
    # ------------------------------------------------------------------------------
    requests.req_contract_details(req_id=1901, contract=test_contract)
    time.sleep(2)

    requests.req_mkt_depth_exchanges()
    time.sleep(2)

    requests.req_mkt_depth(req_id=2001, contract=test_contract, num_rows=5)
    time.sleep(3)
    requests.cancel_mkt_depth(req_id=2001)

    requests.req_news_bulletins(all_messages=True)
    time.sleep(2)
    requests.cancel_news_bulletins()

    requests.req_managed_accounts()
    time.sleep(1)

    # (Optional) If you have the correct conId for AAPL in your region
    requests.req_sec_def_opt_params(
        req_id=2101,
        underlying_symbol="AAPL",
        fut_fop_exchange="SMART",
        underlying_sec_type="STK",
        underlying_con_id=265598
    )

    # ------------------------------------------------------------------------------
    # 9. HISTORICAL DATA
    # ------------------------------------------------------------------------------
    requests.request_historical_data(
        req_id=2201,
        contract=test_contract,
        end_date_time="",
        duration_str="1 D",
        bar_size_setting="1 min",
        what_to_show="TRADES",
        use_rth=1,
        format_date=1
    )
    time.sleep(3)
    requests.cancel_historical_data(req_id=2201)

    requests.req_head_timestamp(req_id=2301, contract=test_contract, what_to_show="TRADES", use_rth=1)
    time.sleep(3)
    requests.cancel_head_timestamp(req_id=2301)

    requests.req_histogram_data(req_id=2401, contract=test_contract, use_rth=1, duration_str="1 D")
    time.sleep(3)
    requests.cancel_histogram_data(req_id=2401)

    requests.req_historical_ticks(
        req_id=2501,
        contract=test_contract,
        start_time="20250101 00:00:00",
        end_time="",
        number_of_ticks=10,
        what_to_show="TRADES",
        use_rth=1,
        ignore_size=False
    )
    time.sleep(2)

    # ------------------------------------------------------------------------------
    # 10. SCANNER, REAL-TIME BARS, FUNDAMENTAL DATA
    # ------------------------------------------------------------------------------
    requests.req_scanner_parameters()
    time.sleep(1)

    scan_sub = ScannerSubscription()
    scan_sub.instrument = "STK"
    scan_sub.locationCode = "STK.US.MAJOR"
    scan_sub.scanCode = "TOP_PERC_GAIN"
    requests.req_scanner_subscription(req_id=2601, subscription=scan_sub)
    time.sleep(3)
    requests.cancel_scanner_subscription(req_id=2601)

    requests.req_real_time_bars(req_id=2701, contract=test_contract, bar_size=5, what_to_show="TRADES", use_rth=1)
    time.sleep(5)
    requests.cancel_real_time_bars(req_id=2701)

    requests.req_fundamental_data(req_id=2801, contract=test_contract, report_type="ReportsFinSummary")
    time.sleep(3)
    requests.cancel_fundamental_data(req_id=2801)

    requests.req_news_providers()
    time.sleep(1)

    # Sample News Article request (adjust provider/article ID as valid for your subscription)
    requests.req_news_article(req_id=2901, provider_code="BZ", article_id="Benzinga-20250122-1")

    requests.req_historical_news(
        req_id=3001,
        con_id=265598,  # AAPL typically
        provider_codes="BZ",
        start_time="20250101 00:00:00",
        end_time="",
        total_results=10
    )

    # ------------------------------------------------------------------------------
    # 11. ORDER-RELATED CALLS (Optional Demo)
    # ------------------------------------------------------------------------------
    orders.req_ids(num_ids=10)
    time.sleep(1)
    orders.req_open_orders()
    time.sleep(1)
    orders.req_auto_open_orders(auto_bind=True)
    time.sleep(1)
    orders.req_all_open_orders()
    time.sleep(1)
    # CAUTION: This cancels ALL active orders across all sessions
    orders.req_global_cancel()
    time.sleep(1)
    orders.req_completed_orders(api_only=True)

    # ------------------------------------------------------------------------------
    # 12. CLEANUP / DISCONNECT
    # ------------------------------------------------------------------------------
    logging.info("All requests made. Sleeping briefly to allow callbacks to finish.")
    time.sleep(5)

    logging.info("Disconnecting from IB...")
    ib.disconnect()


if __name__ == "__main__":
    main()