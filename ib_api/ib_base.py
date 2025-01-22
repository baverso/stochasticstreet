# ib_base.py

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class IBBase(EWrapper, EClient):
    """
    Base class combining EWrapper and EClient for all IB API operations.
    Provides the foundation for the connection and callback handling.
    """
    def __init__(self):
        EClient.__init__(self, self)
        EWrapper.__init__(self)
        self.connected = False
        
    def error(self, reqId, errorCode, errorString):
        """Override error handling to log all errors"""
        super().error(reqId, errorCode, errorString)
        print(f"Error {errorCode}: {errorString}")
        
    def connectAck(self):
        """Called on successful connection"""
        super().connectAck()
        self.connected = True