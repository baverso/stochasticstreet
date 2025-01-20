from stochasticstreet.ib_api import IBBase

class TestApp(IBBase):
    """
    TestApp combines EWrapper and EClient to manage the connection to the IB API.
    """
    def __init__(self, host="127.0.0.1", port=7497, client_id=1):
        """
        Initializes the TestApp.

        Args:
            host (str): Hostname of the IB Gateway or TWS.
            port (int): Port number of the IB Gateway or TWS.
            client_id (int): A unique client ID for this session.
        """
        super().__init__()
        self.host = host
        self.port = port
        self.client_id = client_id

    def start(self):
        """
        Connects to the IB Gateway or TWS and starts the event loop.
        """
        self.connect(self.host, self.port, self.client_id)  # Use IBBase's connect method
        self.run()  # Use IBBase's run method


if __name__ == "__main__":
    app = TestApp(host="127.0.0.1", port=4002, client_id=1)

    try:
        app.start()
    except KeyboardInterrupt:
        print("Disconnected from IB API.")