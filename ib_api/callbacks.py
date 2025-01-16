import json
import logging
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import ContractDetails

# Initialize a logger
logger = logging.getLogger("TradeAppLogger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("trade_app.log")
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

PrintInLine = True  # Global flag for optional inline printing

class TradeApp(EWrapper, EClient):
    def __init__(self, json_indent=2):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.json_indent = json_indent  # Control JSON indentation
        self.reqId_to_symbol = {}  # Map reqId to symbols for easier tracking

    def log_and_print(self, log_msg):
        """Helper method to log and optionally print JSON-formatted messages."""
        logger.info(json.dumps(log_msg, indent=self.json_indent))
        if PrintInLine:
            print(json.dumps(log_msg, indent=self.json_indent))

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        log_msg = {
            "type": "AccountSummary",
            "details": {
                "reqId": reqId,
                "account": account,
                "tag": tag,
                "value": value,
                "currency": currency
            }
        }
        self.log_and_print(log_msg)

    def accountSummaryEnd(self, reqId: int):
        log_msg = {
            "type": "AccountSummaryEnd",
            "details": {"reqId": reqId}
        }
        self.log_and_print(log_msg)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        log_msg = {
            "type": "ContractDetails",
            "details": {
                "reqId": reqId,
                "symbol": contractDetails.contract.symbol,
                "exchange": contractDetails.contract.exchange,
                "currency": contractDetails.contract.currency,
                "lastTradeDateOrContractMonth": contractDetails.contract.lastTradeDateOrContractMonth,
                "multiplier": contractDetails.contract.multiplier,
                "tradingHours": contractDetails.tradingHours,
                "liquidHours": contractDetails.liquidHours,
                "priceMagnifier": contractDetails.priceMagnifier
            }
        }
        self.log_and_print(log_msg)

    def contractDetailsEnd(self, reqId: int):
        log_msg = {
            "type": "ContractDetailsEnd",
            "details": {"reqId": reqId}
        }
        self.log_and_print(log_msg)

    def tickPrice(self, reqId: int, tickType: int, price: float, attrib):
        log_msg = {
            "type": "TickPrice",
            "details": {
                "reqId": reqId,
                "symbol": self.reqId_to_symbol.get(reqId, "Unknown"),
                "price": price,
                "tickType": tickType,
                "attrib": attrib.__dict__  # Assuming attrib is an object with attributes
            }
        }
        self.log_and_print(log_msg)

    def tickSize(self, reqId: int, tickType: int, size: int):
        log_msg = {
            "type": "TickSize",
            "details": {
                "reqId": reqId,
                "tickType": tickType,
                "size": size
            }
        }
        self.log_and_print(log_msg)

    def tickSnapshotEnd(self, reqId: int):
        log_msg = {
            "type": "TickSnapshotEnd",
            "details": {"reqId": reqId}
        }
        self.log_and_print(log_msg)