"""
ib_requests.py

Contains classes or methods for sending requests to the IB API
(e.g., requesting market data, historical data, orders, etc.).
By putting requests in a dedicated class, we keep them separate
from connection logic and callback logic.
"""

import logging
from ibapi.contract import Contract


class IBRequests:
    """
    A helper class for sending IB API requests through an active
    IBConnector instance.
    """

    def __init__(self, ib_connector):
        """
        :param ib_connector: An instance of IBConnector (EClient).
        """
        self.ib = ib_connector
        self.logger = logging.getLogger(self.__class__.__name__)

    def req_current_time(self):
        """
        Request the current server time from IB. The response is returned asynchronously
        and handled via the `currentTime` callback.

        This can be used to verify the server connection and ensure synchronization.

        Example:
            requests.req_current_time()

        Callback:
            IBCallbacks.currentTime
        """
        self.logger.info("Requesting current server time...")
        self.ib.reqCurrentTime()

    def req_market_data(self, req_id, contract, generic_tick_list="", snapshot=False, regulatory_snapshot=False):
        """
        Request real-time market data for a specific contract.

        Args:
            req_id (int): A unique identifier for the request. Example: 1001.
            contract (Contract): An IBAPI Contract object representing the instrument to query.
                Example:
                    Contract attributes for AAPL (Apple Inc.):
                    - symbol="AAPL"
                    - secType="STK"
                    - exchange="SMART"
                    - currency="USD"
            generic_tick_list (str, optional): Comma-separated list of specific tick types. Default is "".
                Examples:
                    - "233" for RTVolume
                    - "236" for Auction values
                    - "258" for Mark Price
            snapshot (bool, optional): If True, retrieves a single snapshot of data. Default is False (streaming data).
            regulatory_snapshot (bool, optional): If True, includes additional regulatory data in the snapshot.
                Default is False.

        Returns:
            None. Data is returned asynchronously via the `tickPrice`, `tickSize`, and other market data callbacks.

        Example:
            # Create a Contract for AAPL
            from ibapi.contract import Contract
            contract = Contract()
            contract.symbol = "AAPL"
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"

            # Request real-time market data
            requests.req_market_data(req_id=1001, contract=contract)

        Callback:
            IBCallbacks.tickPrice
            IBCallbacks.tickSize
        """
        self.logger.info(f"Requesting market data: ReqId={req_id}, Contract={contract.symbol}.")
        self.ib.reqMktData(req_id, contract, generic_tick_list, snapshot, regulatory_snapshot, [])

    def cancel_market_data(self, req_id):
        """
        Cancel an active market data subscription.

        Args:
            req_id (int): The unique identifier of the subscription to cancel.

        Example:
            # Cancel the subscription with request ID 1001
            requests.cancel_market_data(req_id=1001)

        Returns:
            None. Cancellation is acknowledged asynchronously.

        Callback:
            IBCallbacks.cancelMktData
        """
        self.logger.info(f"Cancelling market data: ReqId={req_id}.")
        self.ib.cancelMktData(req_id)

    def req_market_data_type(self, market_data_type):
        """
        Request a specific market data type.

        Args:
            market_data_type (int): The type of market data to request:
                - 1: Real-time streaming data (default)
                - 2: Frozen data
                - 3: Delayed data
                - 4: Delayed frozen data

        Example:
            # Request delayed market data
            requests.req_market_data_type(3)

        Returns:
            None.

        Callback:
            Affects all subsequent market data requests (e.g., `tickPrice`, `tickSize`).
        """
        self.logger.info(f"Requesting market data type: {market_data_type}.")
        self.ib.reqMarketDataType(market_data_type)

    def req_tick_by_tick_data(self, req_id, contract, tick_type, number_of_ticks, ignore_size=False):
        """
        Request tick-by-tick market data for a specified contract.

        Args:
            req_id (int): Unique identifier for the request.
            contract (Contract): The IBAPI Contract object representing the instrument.
            tick_type (str): Type of tick data to request:
                - "Last": Last traded price
                - "AllLast": Last traded price (including exchanges)
                - "BidAsk": Bid/Ask updates
                - "MidPoint": Midpoint updates
            number_of_ticks (int): Number of ticks to return. Use 0 for continuous updates.
            ignore_size (bool, optional): Whether to ignore the tick size. Default is False.

        Example:
            # Request tick-by-tick data for AAPL
            requests.req_tick_by_tick_data(
                req_id=1001, contract=contract, tick_type="Last", number_of_ticks=0
            )

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.tickByTickAllLast
            IBCallbacks.tickByTickBidAsk
            IBCallbacks.tickByTickMidPoint
        """
        self.logger.info(f"Requesting tick-by-tick data: ReqId={req_id}, TickType={tick_type}.")
        self.ib.reqTickByTickData(req_id, contract, tick_type, number_of_ticks, ignore_size)

    def cancel_tick_by_tick_data(self, req_id):
        """
        Cancel an active tick-by-tick market data request.

        Args:
            req_id (int): Unique identifier of the tick-by-tick data subscription to cancel.

        Example:
            # Cancel tick-by-tick data subscription
            requests.cancel_tick_by_tick_data(req_id=1001)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling tick-by-tick data: ReqId={req_id}.")
        self.ib.cancelTickByTickData(req_id)

    def calculate_implied_volatility(self, req_id, contract, option_price, under_price):
        """
        Request implied volatility for an options contract.

        Args:
            req_id (int): Unique identifier for the request.
            contract (Contract): The IBAPI Contract object for the option.
            option_price (float): The price of the option.
            under_price (float): The price of the underlying instrument.

        Example:
            # Request implied volatility for an AAPL option
            requests.calculate_implied_volatility(
                req_id=1002, contract=contract, option_price=10.5, under_price=150.0
            )

        Returns:
            None. The result is returned asynchronously.

        Callback:
            IBCallbacks.tickOptionComputation
        """
        self.logger.info(f"Requesting implied volatility: ReqId={req_id}.")
        self.ib.calculateImpliedVolatility(req_id, contract, option_price, under_price, [])

    def cancel_calculate_implied_volatility(self, req_id):
        """
        Cancel an active implied volatility calculation request.

        Args:
            req_id (int): Unique identifier of the implied volatility calculation request to cancel.

        Example:
            # Cancel implied volatility calculation
            requests.cancel_calculate_implied_volatility(req_id=1002)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling implied volatility calculation: ReqId={req_id}.")
        self.ib.cancelCalculateImpliedVolatility(req_id)

    def calculate_option_price(self, req_id, contract, volatility, under_price):
        """
        Request option price calculation for a specific volatility.

        Args:
            req_id (int): Unique identifier for the request.
            contract (Contract): The IBAPI Contract object for the option.
            volatility (float): The volatility value to use for the calculation.
            under_price (float): The price of the underlying instrument.

        Example:
            # Request option price for an AAPL option
            requests.calculate_option_price(
                req_id=1003, contract=contract, volatility=0.2, under_price=150.0
            )

        Returns:
            None. The result is returned asynchronously.

        Callback:
            IBCallbacks.tickOptionComputation
        """
        self.logger.info(f"Requesting option price calculation: ReqId={req_id}.")
        self.ib.calculateOptionPrice(req_id, contract, volatility, under_price, [])

    def cancel_calculate_option_price(self, req_id):
        """
        Cancel an active option price calculation request.

        Args:
            req_id (int): Unique identifier of the option price calculation request to cancel.

        Example:
            # Cancel option price calculation
            requests.cancel_calculate_option_price(req_id=1003)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling option price calculation: ReqId={req_id}.")
        self.ib.cancelCalculateOptionPrice(req_id)

    def req_account_updates(self, subscribe, account_code):
        """
        Request real-time account updates.

        Args:
            subscribe (bool): Whether to subscribe (True) or unsubscribe (False) to account updates.
            account_code (str): The account identifier.

        Example:
            # Subscribe to account updates for a specific account
            requests.req_account_updates(subscribe=True, account_code="DU123456")

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.updateAccountValue
            IBCallbacks.updatePortfolio
            IBCallbacks.accountDownloadEnd
        """
        self.logger.info(f"Requesting account updates: Subscribe={subscribe}, Account={account_code}.")
        self.ib.reqAccountUpdates(subscribe, account_code)

    def req_account_summary(self, req_id, group_name, tags):
        """
        Request an account summary for one or more accounts.

        Args:
            req_id (int): Unique identifier for the request.
            group_name (str): The group of accounts to query. Common values:
                - "All": All accounts.
                - Specific advisor account group name.
            tags (str): Comma-separated list of tags to request. Common tags include:
                - "NetLiquidation"
                - "TotalCashValue"
                - "BuyingPower"

        Example:
            # Request account summary for all accounts
            requests.req_account_summary(req_id=1004, group_name="All", tags="NetLiquidation,TotalCashValue")

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.accountSummary
            IBCallbacks.accountSummaryEnd
        """
        self.logger.info(f"Requesting account summary: ReqId={req_id}, GroupName={group_name}, Tags={tags}.")
        self.ib.reqAccountSummary(req_id, group_name, tags)

    def cancel_account_summary(self, req_id):
        """
        Cancel an active account summary request.

        Args:
            req_id (int): Unique identifier of the account summary request to cancel.

        Example:
            # Cancel account summary request
            requests.cancel_account_summary(req_id=1004)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling account summary: ReqId={req_id}.")
        self.ib.cancelAccountSummary(req_id)

    def req_positions(self):
        """
        Request real-time position updates for all accounts.

        Example:
            # Request position updates
            requests.req_positions()

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.position
            IBCallbacks.positionEnd
        """
        self.logger.info("Requesting real-time positions for all accounts.")
        self.ib.reqPositions()

    def cancel_positions(self):
        """
        Cancel real-time position updates for all accounts.

        Example:
            # Cancel position updates
            requests.cancel_positions()

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info("Cancelling real-time positions for all accounts.")
        self.ib.cancelPositions()

    def req_positions_multi(self, req_id, account, model_code):
        """
        Request positions for a specific account and model code.

        Args:
            req_id (int): Unique identifier for the request.
            account (str): The account identifier.
            model_code (str): The model code (if applicable) to filter positions.

        Example:
            # Request positions for a specific account and model code
            requests.req_positions_multi(req_id=2001, account="DU123456", model_code="model1")

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.positionMulti
            IBCallbacks.positionMultiEnd
        """
        self.logger.info(
            f"Requesting multi-account positions: ReqId={req_id}, Account={account}, ModelCode={model_code}.")
        self.ib.reqPositionsMulti(req_id, account, model_code)

    def cancel_positions_multi(self, req_id):
        """
        Cancel a specific multi-account position request.

        Args:
            req_id (int): Unique identifier of the multi-account position request to cancel.

        Example:
            # Cancel positions for a specific request
            requests.cancel_positions_multi(req_id=2001)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling multi-account positions: ReqId={req_id}.")
        self.ib.cancelPositionsMulti(req_id)

    def req_account_updates_multi(self, req_id, account, model_code, ledger_and_nlv):
        """
        Request account updates for a specific account and model code.

        Args:
            req_id (int): Unique identifier for the request.
            account (str): The account identifier.
            model_code (str): The model code (if applicable) to filter updates.
            ledger_and_nlv (bool): Whether to include ledger and net liquidation value (True/False).

        Example:
            # Request account updates for a specific account and model code
            requests.req_account_updates_multi(req_id=3001, account="DU123456", model_code="model1", ledger_and_nlv=True)

        Returns:
            None. Data is returned asynchronously.

        Callback:
            IBCallbacks.accountUpdateMulti
            IBCallbacks.accountUpdateMultiEnd
        """
        self.logger.info(
            f"Requesting multi-account updates: ReqId={req_id}, Account={account}, ModelCode={model_code}.")
        self.ib.reqAccountUpdatesMulti(req_id, account, model_code, ledger_and_nlv)

    def cancel_account_updates_multi(self, req_id):
        """
        Cancel a specific multi-account updates request.

        Args:
            req_id (int): Unique identifier of the multi-account updates request to cancel.

        Example:
            # Cancel account updates for a specific request
            requests.cancel_account_updates_multi(req_id=3001)

        Returns:
            None.

        Callback:
            Acknowledged silently by IB.
        """
        self.logger.info(f"Cancelling multi-account updates: ReqId={req_id}.")
        self.ib.cancelAccountUpdatesMulti(req_id)

    def req_pnl(self, req_id, account, model_code=None):
        """
        Requests real-time profit and loss updates for an account.

        Args:
            req_id (int): Unique request identifier.
            account (str): The account code for which PnL updates are requested.
            model_code (str, optional): The model code within the account. Defaults to None.

        Callback:
            - `pnl()`: Delivers PnL updates.
        """
        self.logger.info(f"Requesting PnL updates for ReqId={req_id}, Account={account}, ModelCode={model_code}.")
        self.ib.reqPnL(req_id, account, model_code or "")

    def cancel_pnl(self, req_id):
        """
        Cancels the PnL updates for a previously issued request.

        Args:
            req_id (int): The request identifier to cancel.

        Callback:
            - None (Stops the pnl() callback).
        """
        self.logger.info(f"Cancelling PnL updates for ReqId={req_id}.")
        self.ib.cancelPnL(req_id)

    def req_pnl_single(self, req_id, account, model_code, con_id):
        """
        Requests real-time profit and loss updates for a single position.

        Args:
            req_id (int): Unique request identifier.
            account (str): The account code.
            model_code (str): The model code within the account.
            con_id (int): The contract identifier (ConId) for the position.

        Callback:
            - `pnlSingle()`: Delivers PnL updates for the specified position.
        """
        self.logger.info(f"Requesting single PnL for ReqId={req_id}, Account={account}, ConId={con_id}.")
        self.ib.reqPnLSingle(req_id, account, model_code, con_id)

    def cancel_pnl_single(self, req_id):
        """
        Cancels the PnL updates for a previously issued single position request.

        Args:
            req_id (int): The request identifier to cancel.

        Callback:
            - None (Stops the pnlSingle() callback).
        """
        self.logger.info(f"Cancelling single PnL updates for ReqId={req_id}.")
        self.ib.cancelPnLSingle(req_id)

    def req_executions(self, req_id, execution_filter):
        """
        Requests trade execution reports based on specified filters.

        Args:
            req_id (int): Unique request identifier.
            execution_filter (ExecutionFilter): A filter object specifying trade criteria.

        Callback:
            - `execDetails()`: Delivers execution details for trades matching the filter.
            - `execDetailsEnd()`: Marks the end of execution report data.
        """
        self.logger.info(f"Requesting executions for ReqId={req_id}, Filter={execution_filter}.")
        self.ib.reqExecutions(req_id, execution_filter)

    def req_contract_details(self, req_id, contract):
        """
        Requests contract details for a specific contract.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): An IBAPI Contract object specifying the financial instrument.

        Callback:
            - `contractDetails()`: Provides the contract details.
            - `contractDetailsEnd()`: Marks the end of contract details data.
        """
        self.logger.info(f"Requesting contract details for ReqId={req_id}, Contract={contract.symbol}.")
        self.ib.reqContractDetails(req_id, contract)

    def req_mkt_depth_exchanges(self):
        """
        Requests market depth exchanges.

        Callback:
            - `mktDepthExchanges()`: Provides the list of exchanges offering market depth data.
        """
        self.logger.info("Requesting market depth exchanges.")
        self.ib.reqMktDepthExchanges()

    def req_mkt_depth(self, req_id, contract, num_rows):
        """
        Requests market depth data for a specific contract.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): An IBAPI Contract object.
            num_rows (int): The number of market depth rows to retrieve.

        Callback:
            - `updateMktDepth()`: Provides updates for market depth data.
            - `updateMktDepthL2()`: Provides level 2 market depth updates.
        """
        self.logger.info(f"Requesting market depth for ReqId={req_id}, Contract={contract.symbol}.")
        self.ib.reqMktDepth(req_id, contract, num_rows, False, [])

    def cancel_mkt_depth(self, req_id):
        """
        Cancels market depth data for a specific request.

        Args:
            req_id (int): The request identifier to cancel.

        Callback:
            - None (Stops updateMktDepth and updateMktDepthL2 callbacks).
        """
        self.logger.info(f"Cancelling market depth for ReqId={req_id}.")
        self.ib.cancelMktDepth(req_id, False)

    def req_news_bulletins(self, all_messages):
        """
        Requests news bulletins from IB.

        Args:
            all_messages (bool): If True, all active bulletins are delivered; otherwise, only new bulletins are delivered.

        Callback:
            - `updateNewsBulletin()`: Delivers news bulletins.
        """
        self.logger.info("Requesting news bulletins.")
        self.ib.reqNewsBulletins(all_messages)

    def cancel_news_bulletins(self):
        """
        Cancels news bulletin subscriptions.

        Callback:
            - None (Stops the updateNewsBulletin callback).
        """
        self.logger.info("Cancelling news bulletins.")
        self.ib.cancelNewsBulletins()

    def req_managed_accounts(self):
        """
        Requests a list of managed accounts associated with the user.

        Callback:
            - `managedAccounts()`: Delivers the list of managed accounts.
        """
        self.logger.info("Requesting managed accounts.")
        self.ib.reqManagedAccts()

    def req_sec_def_opt_params(self, req_id, underlying_symbol, fut_fop_exchange, underlying_sec_type,
                               underlying_con_id):
        """
        Requests security definition option parameters for a given contract.

        Args:
            req_id (int): Unique request identifier.
            underlying_symbol (str): The underlying security symbol.
            fut_fop_exchange (str): The exchange for the future or option.
            underlying_sec_type (str): The security type of the underlying (e.g., "STK", "FUT").
            underlying_con_id (int): The contract ID of the underlying security.

        Callback:
            - `securityDefinitionOptionParameter()`: Delivers option parameters.
            - `securityDefinitionOptionParameterEnd()`: Marks the end of option parameter data.
        """
        self.logger.info(f"Requesting security definition option parameters for ReqId={req_id}.")
        self.ib.reqSecDefOptParams(req_id, underlying_symbol, fut_fop_exchange, underlying_sec_type,
                                   underlying_con_id)
    def request_historical_data(self, req_id: int, contract: Contract, end_date_time: str, duration_str: str,
                                bar_size_setting: str, what_to_show: str, use_rth: int, format_date: int):
        """
        Request historical data from IB for a given contract.
        The data is returned via the `historicalData` callback.

        Args:
            req_id (int):
                A unique identifier for the request.
                Example: 1001

            contract (Contract):
                An IBAPI Contract object representing the financial instrument for which historical data is requested.
                Example: A Contract object for "AAPL" (Apple Inc.) or ES futures.

            end_date_time (str):
                The request's end date and time in the format 'YYYYMMDD HH:MM:SS' (in the local time zone).
                This defines the most recent point in time for the data requested.
                Example: '20250122 23:59:59'

            duration_str (str):
                The duration of the data request, specifying how much historical data is retrieved.
                Valid examples:
                - '1 D' (1 day)
                - '1 W' (1 week)
                - '1 M' (1 month)
                - '3 Y' (3 years)

            bar_size_setting (str):
                The size of the bars (candlesticks) in the returned data.
                Examples:
                - '1 min' (1-minute bars)
                - '5 mins' (5-minute bars)
                - '1 day' (daily bars)
                - '1 hour' (hourly bars)

            what_to_show (str):
                Specifies the type of data to retrieve. Common values include:
                - 'TRADES': Trade prices.
                - 'MIDPOINT': The midpoint of the bid and ask.
                - 'BID': Bid prices.
                - 'ASK': Ask prices.
                - 'BID_ASK': Both bid and ask data.
                - 'HISTORICAL_VOLATILITY': Historical volatility data.
                - 'OPTION_IMPLIED_VOLATILITY': Option implied volatility data.

            use_rth (int):
                Whether to use regular trading hours (RTH) only:
                - 1: Yes, retrieve data from regular trading hours only.
                - 0: No, include all available hours (e.g., pre-market and after-hours).

            format_date (int):
                Specifies the format of the returned dates:
                - 1: Date and time in the format 'YYYYMMDD HH:MM:SS'.
                - 2: Epoch time (number of seconds since January 1, 1970).

        Returns:
            None. The data is retrieved asynchronously and delivered via the `historicalData` callback.

        Example Usage:
            # Create a Contract for Apple Inc.
            contract = Contract()
            contract.symbol = "AAPL"
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"

            # Request 1 week of 1-hour bars for Apple Inc., showing trade prices
            self.request_historical_data(
                req_id=1001,
                contract=contract,
                end_date_time='20250122 23:59:59',
                duration_str='1 W',
                bar_size_setting='1 hour',
                what_to_show='TRADES',
                use_rth=1,
                format_date=1
            )
                Callback:
            - historicalData() (from IBCallbacks)
        """
        self.logger.info(f"Requesting historical data for ReqId={req_id}, Symbol={contract.symbol}.")
        self.ib.reqHistoricalData(
            req_id,
            contract,
            end_date_time,
            duration_str,
            bar_size_setting,
            what_to_show,
            use_rth,
            format_date,
            False,  # False for historical data only (not streaming updates)
            []
        )

    def cancel_historical_data(self, req_id):
        """
        Cancels a historical data request.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling historical data: ReqId={req_id}")
        self.ib.cancelHistoricalData(req_id)

    def req_head_timestamp(self, req_id, contract, what_to_show, use_rth):
        """
        Requests the earliest timestamp available for a contract.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): The contract to query.
            what_to_show (str): Type of data ('TRADES', 'MIDPOINT', etc.).
            use_rth (int): 1 to use regular trading hours, 0 otherwise.

        Callback:
            - headTimestamp()
        """
        self.logger.info(f"Requesting head timestamp: ReqId={req_id}, Symbol={contract.symbol}")
        self.ib.reqHeadTimeStamp(req_id, contract, what_to_show, use_rth, 0)

    def cancel_head_timestamp(self, req_id):
        """
        Cancels a head timestamp request.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling head timestamp: ReqId={req_id}")
        self.ib.cancelHeadTimeStamp(req_id)

    def req_histogram_data(self, req_id, contract, use_rth, duration_str):
        """
        Requests histogram data for a contract.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): The contract to query.
            use_rth (int): 1 to use regular trading hours, 0 otherwise.
            duration_str (str): Duration of the data request (e.g., '1 D').

        Callback:
            - histogramData()
        """
        self.logger.info(f"Requesting histogram data: ReqId={req_id}, Symbol={contract.symbol}")
        self.ib.reqHistogramData(req_id, contract, use_rth, duration_str)

    def cancel_histogram_data(self, req_id):
        """
        Cancels a histogram data request.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling histogram data: ReqId={req_id}")
        self.ib.cancelHistogramData(req_id)

    def req_historical_ticks(self, req_id, contract, start_time, end_time, number_of_ticks, what_to_show, use_rth,
                             ignore_size):
        """
        Requests historical tick data for a contract.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): The contract to query.
            start_time (str): Start time for the data (format: 'YYYYMMDD HH:MM:SS').
            end_time (str): End time for the data (format: 'YYYYMMDD HH:MM:SS').
            number_of_ticks (int): Maximum number of ticks to return.
            what_to_show (str): Type of data ('TRADES', 'BID_ASK', etc.).
            use_rth (int): 1 to use regular trading hours, 0 otherwise.
            ignore_size (bool): True to ignore size, False otherwise.

        Callback:
            - historicalTicks()
        """
        self.logger.info(f"Requesting historical ticks: ReqId={req_id}, Symbol={contract.symbol}")
        self.ib.reqHistoricalTicks(req_id, contract, start_time, end_time, number_of_ticks, what_to_show, use_rth,
                                   ignore_size, [])

    def req_scanner_parameters(self):
        """
        Requests scanner parameters in XML format.

        Callback:
            - scannerParameters()
        """
        self.logger.info("Requesting scanner parameters")
        self.ib.reqScannerParameters()

    def req_scanner_subscription(self, req_id, subscription):
        """
        Requests a scanner subscription.

        Args:
            req_id (int): Unique request identifier.
            subscription (ScannerSubscription): Subscription criteria.

        Callback:
            - scannerData()
        """
        self.logger.info(f"Requesting scanner subscription: ReqId={req_id}")
        self.ib.reqScannerSubscription(req_id, subscription, [], [])

    def cancel_scanner_subscription(self, req_id):
        """
        Cancels a scanner subscription.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling scanner subscription: ReqId={req_id}")
        self.ib.cancelScannerSubscription(req_id)

    def req_real_time_bars(self, req_id, contract, bar_size, what_to_show, use_rth):
        """
        Requests real-time bar data.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): The contract to query.
            bar_size (int): The bar size in seconds (e.g., 5).
            what_to_show (str): Type of data ('TRADES', 'BID', etc.).
            use_rth (int): 1 to use regular trading hours, 0 otherwise.

        Callback:
            - realtimeBar()
        """
        self.logger.info(f"Requesting real-time bars: ReqId={req_id}, Symbol={contract.symbol}")
        self.ib.reqRealTimeBars(req_id, contract, bar_size, what_to_show, use_rth, [])

    def cancel_real_time_bars(self, req_id):
        """
        Cancels a real-time bar data request.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling real-time bars: ReqId={req_id}")
        self.ib.cancelRealTimeBars(req_id)

    def req_fundamental_data(self, req_id, contract, report_type):
        """
        Requests fundamental data for a stock.

        Args:
            req_id (int): Unique request identifier.
            contract (Contract): The contract to query.
            report_type (str): Report type (e.g., 'ReportsFinSummary').

        Callback:
            - fundamentalData()
        """
        self.logger.info(f"Requesting fundamental data: ReqId={req_id}, Symbol={contract.symbol}")
        self.ib.reqFundamentalData(req_id, contract, report_type, [])

    def cancel_fundamental_data(self, req_id):
        """
        Cancels a fundamental data request.

        Args:
            req_id (int): The request ID to cancel.
        """
        self.logger.info(f"Cancelling fundamental data: ReqId={req_id}")
        self.ib.cancelFundamentalData(req_id)

    def req_news_providers(self):
        """
        Requests available news providers.

        Callback:
            - newsProviders()
        """
        self.logger.info("Requesting news providers")
        self.ib.reqNewsProviders()

    def req_news_article(self, req_id, provider_code, article_id):
        """
        Requests a specific news article.

        Args:
            req_id (int): Unique request identifier.
            provider_code (str): News provider code.
            article_id (str): ID of the news article.

        Callback:
            - newsArticle()
        """
        self.logger.info(f"Requesting news article: ReqId={req_id}, Provider={provider_code}, ArticleId={article_id}")
        self.ib.reqNewsArticle(req_id, provider_code, article_id, [])

    def req_historical_news(self, req_id, con_id, provider_codes, start_time, end_time, total_results):
        """
        Requests historical news.

        Args:
            req_id (int): Unique request identifier.
            con_id (int): Contract ID for the news request.
            provider_codes (str): Comma-separated provider codes.
            start_time (str): Start time for the news (format: 'YYYYMMDD HH:MM:SS').
            end_time (str): End time for the news (format: 'YYYYMMDD HH:MM:SS').
            total_results (int): Maximum number of results to return.

        Callback:
            - historicalNews()
        """
        self.logger.info(f"Requesting historical news: ReqId={req_id}, ConId={con_id}")
        self.ib.reqHistoricalNews(req_id, con_id, provider_codes, start_time, end_time, total_results, [])