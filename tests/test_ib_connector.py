import unittest
from unittest.mock import patch, MagicMock
from stochasticstreet.ib_api.ib_connector import IBConnector, create_ib_connector

class TestIBConnector(unittest.TestCase):

    @patch('stochasticstreet.ib_api.ib_connector.EClient.connect')
    @patch('stochasticstreet.ib_api.ib_connector.threading.Thread.start')
    def test_start_connection_success(self, mock_thread_start, mock_connect):
        connector = IBConnector()
        connector.isConnected = MagicMock(return_value=True)
        connector.start_connection()
        self.assertTrue(connector.connected)

    @patch('stochasticstreet.ib_api.ib_connector.EClient.connect')
    @patch('stochasticstreet.ib_api.ib_connector.threading.Thread.start')
    def test_start_connection_failure(self, mock_thread_start, mock_connect):
        connector = IBConnector()
        connector.isConnected = MagicMock(return_value=False)
        connector.start_connection()
        self.assertFalse(connector.connected)

    @patch('stochasticstreet.ib_api.ib_connector.EClient.disconnect')
    def test_stop_connection(self, mock_disconnect):
        connector = IBConnector()
        connector.connected = True
        connector.stop_connection()
        self.assertFalse(connector.connected)

    def test_is_connected(self):
        connector = IBConnector()
        connector.connected = True
        self.assertTrue(connector.isConnected())
        connector.connected = False
        self.assertFalse(connector.isConnected())

    @patch('stochasticstreet.ib_api.ib_connector.logger.info')
    def test_next_valid_id(self, mock_logger_info):
        connector = IBConnector()
        connector.nextValidId(1)
        mock_logger_info.assert_called_with("Next valid order ID: 1")

    @patch('stochasticstreet.ib_api.ib_connector.logger.error')
    def test_error(self, mock_logger_error):
        connector = IBConnector()
        connector.error(1, 404, "Not Found")
        mock_logger_error.assert_called_with("Error. ReqId: 1, Code: 404, Msg: Not Found")

    @patch('stochasticstreet.ib_api.ib_connector.logger.warning')
    def test_connection_closed(self, mock_logger_warning):
        connector = IBConnector()
        connector.connectionClosed()
        self.assertFalse(connector.connected)
        mock_logger_warning.assert_called_with("Connection to IB API closed.")

    @patch('stochasticstreet.ib_api.ib_connector.IBConnector.start_connection')
    def test_create_ib_connector(self, mock_start_connection):
        connector = create_ib_connector()
        self.assertTrue(isinstance(connector, IBConnector))
        mock_start_connection.assert_called_once()

if __name__ == '__main__':
    unittest.main()