from ibapi.wrapper import EWrapper
import logging

class LoggingWrapper(EWrapper):
    """
    A wrapper around EWrapper to log every callback method call.
    This helps debug whether the IB API is triggering the callbacks as expected.
    """

    def __getattribute__(self, name):
        """
        Intercept all attribute accesses and log callback method calls.
        """
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                logging.debug(f"Callback: {name} called with args={args}, kwargs={kwargs}")
                return attr(*args, **kwargs)
            return wrapper
        return attr