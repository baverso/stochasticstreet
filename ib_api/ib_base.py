# ib_base.py

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class IBBase(EWrapper, EClient):
    """
    Base class combining EWrapper and EClient for all IB API operations.
    This is used to streamline the initialization of the IBConnector class.
    """
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)