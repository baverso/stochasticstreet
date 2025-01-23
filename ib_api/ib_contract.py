"""
ib_contract.py

This module provides a user-friendly wrapper for creating Interactive Brokers (IB) Contract objects.
"""

from ibapi.contract import Contract

class IBContract:
    @staticmethod
    def create_contract(symbol, sec_type, exchange, currency, primary_exchange=None, last_trade_date=None, strike=None,
                        right=None, multiplier=None, local_symbol=None, trading_class=None):
        """
        Create an IB Contract object.

        Args:
            symbol (str):
                The ticker symbol of the financial instrument.
                Example: "AAPL" for Apple Inc., "GOOGL" for Alphabet Inc., "ES" for S&P 500 Futures.

            sec_type (str):
                The type of security. Possible values include:
                - "STK": Stocks
                - "OPT": Options
                - "FUT": Futures
                - "CFD": Contracts for Difference
                - "BOND": Bonds
                - "FOREX": Currency pairs
                - "CMDTY": Commodities

            exchange (str):
                The exchange where the instrument is traded. Common exchanges include:
                - "SMART": IBKR's smart routing system
                - "NASDAQ": NASDAQ Stock Market
                - "NYSE": New York Stock Exchange
                - "CBOE": Chicago Board Options Exchange
                - "LSE": London Stock Exchange
                - "EUREX": European Futures and Options Exchange
                - "HKEX": Hong Kong Stock Exchange
                - "CME": Chicago Mercantile Exchange (futures)
                - "ICE": Intercontinental Exchange (commodities and futures)
                - "SGX": Singapore Exchange

            currency (str):
                The currency in which the instrument is denominated. Examples:
                - "USD": US Dollars
                - "EUR": Euros
                - "GBP": British Pounds
                - "JPY": Japanese Yen

            primary_exchange (str, optional):
                The primary exchange for the instrument. This is particularly useful for stocks listed on multiple exchanges.
                Example: "NASDAQ" for AAPL, "NYSE" for IBM.

            last_trade_date (str, optional):
                The expiration date for options or futures contracts. Format: "YYYYMMDD".
                Example: "20250321" for March 21, 2025.

            strike (float, optional):
                The strike price for options contracts.
                Example: 150.0 for a call or put option with a strike price of $150.

            right (str, optional):
                The right type for options:
                - "C": Call option
                - "P": Put option

            multiplier (str, optional):
                The contract multiplier. Common values:
                - "100" for equity options (representing 100 shares per contract).
                - "50" or "25" for certain index options.

            local_symbol (str, optional):
                The local symbol for the contract, which may vary based on the exchange.
                Example: "ESU5" for the S&P 500 Futures September contract.

            trading_class (str, optional):
                The trading class of the contract, which identifies specific product types.
                Example: "SPY" for SPDR S&P 500 ETF options.

        Returns:
            Contract: An IB Contract object.

        Example:
            Create a stock contract for Apple Inc.:
                contract = create_contract(
                    symbol="AAPL",
                    sec_type="STK",
                    exchange="SMART",
                    currency="USD",
                    primary_exchange="NASDAQ"
                )

            Create an options contract for Apple Inc.:
                contract = create_contract(
                    symbol="AAPL",
                    sec_type="OPT",
                    exchange="SMART",
                    currency="USD",
                    last_trade_date="20250321",
                    strike=150.0,
                    right="C",
                    multiplier="100"
                )
        """
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.currency = currency

        if primary_exchange:
            contract.primaryExchange = primary_exchange
        if last_trade_date:
            contract.lastTradeDateOrContractMonth = last_trade_date
        if strike:
            contract.strike = strike
        if right:
            contract.right = right
        if multiplier:
            contract.multiplier = multiplier
        if local_symbol:
            contract.localSymbol = local_symbol
        if trading_class:
            contract.tradingClass = trading_class

        return contract