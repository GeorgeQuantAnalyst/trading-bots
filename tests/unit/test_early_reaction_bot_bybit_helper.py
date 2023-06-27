import json
import unittest
import os
from unittest.mock import MagicMock, patch

from trading_bots import constants
from trading_bots.helpers.early_reaction_bot_bybit_helper import EarlyReactionBotBybitHelper


class TestEarlyReactionBotBybitHelper(unittest.TestCase):

    def setUp(self):
        # Initialize the EarlyReactionBotBybitHelper object for testing
        self.pybit_client = MagicMock()
        self.before_entry_ids_json_path = "fixtures/before_entry_ids.json"

        with open(self.before_entry_ids_json_path, "w") as file:
            file.write("[]")

        self.helper = EarlyReactionBotBybitHelper(self.pybit_client, self.before_entry_ids_json_path)

    def tearDown(self):
        # Delete the test file after each test
        try:
            os.remove(self.before_entry_ids_json_path)
        except FileNotFoundError:
            pass

    def test_get_pending_orders(self):
        # Create a mock response from the pybit_client for the get_open_orders call
        response = {
            "result": {
                "list": [
                    {"orderId": "12345", "symbol": "BTCUSDT"},
                    {"orderId": "67890", "symbol": "ETHUSDT"}
                ]
            }
        }
        self.pybit_client.get_open_orders.return_value = response

        # Test the method
        result = self.helper.get_pending_orders()

        # Verify that the pybit_client method was called
        self.pybit_client.get_open_orders.assert_called_once_with(
            category=constants.BYBIT_LINEAR_CATEGORY,
            settleCoin="USDT"
        )

        # Verify the result
        expected_result = [
            {"orderId": "12345", "symbol": "BTCUSDT"},
            {"orderId": "67890", "symbol": "ETHUSDT"}
        ]
        self.assertEqual(result, expected_result)

    def test_get_last_closed_bar(self):
        # Create a mock response from the pybit_client for the get_kline call
        response = {
            "result": {
                "list": [
                    [1625827200000, "32000", "33000", "31000", "31500", "1000", "30000000"],
                    [1625913600000, "31500", "32500", "31000", "32000", "2000", "60000000"]
                ]
            }
        }
        self.pybit_client.get_kline.return_value = response

        # Test the method
        result = self.helper.get_last_closed_bar("BTCUSDT", interval=1)

        # Verify that the pybit_client method was called
        self.pybit_client.get_kline.assert_called_once_with(
            symbol="BTCUSDT",
            category=constants.BYBIT_LINEAR_CATEGORY,
            interval=1,
            limit=2
        )

        # Verify the result
        expected_result = {
            "startTime": 1625913600000.0,
            "openPrice": 31500.0,
            "highPrice": 32500.0,
            "lowPrice": 31000.0,
            "closePrice": 32000.0,
            "volume": 2000.0,
            "turnover": 60000000.0
        }
        self.assertEqual(result, expected_result)

    def test_cancel_pending_order(self):
        order_id = "12345"
        symbol = "BTCUSDT"

        # Test the method
        self.helper.cancel_pending_order(order_id, symbol)

        # Verify that the pybit_client method was called
        self.pybit_client.cancel_order.assert_called_once_with(
            category=constants.BYBIT_LINEAR_CATEGORY,
            symbol="BTCUSDT",
            orderId="12345"
        )

    def test_remove_not_exists_ids(self):
        before_entry_ids = ["12345", "67890", "98765"]
        pending_orders = [
            {"orderId": "12345", "symbol": "BTCUSDT"},
            {"orderId": "23456", "symbol": "ETHUSDT"},
            {"orderId": "78901", "symbol": "XRPUSDT"}
        ]

        # Test the method
        self.helper.remove_not_exists_ids(before_entry_ids, pending_orders)

        # Verify the result
        expected_before_entry_ids = ["12345"]
        self.assertEqual(before_entry_ids, expected_before_entry_ids)

    def test_load_before_entry_ids_list(self):
        # Create a test file with mock content
        mock_content = '["12345", "67890", "98765"]'
        with open(self.before_entry_ids_json_path, "w") as f:
            f.write(mock_content)

        # Test the method
        result = self.helper.load_before_entry_ids_list()

        # Verify the result
        expected_result = ["12345", "67890", "98765"]
        self.assertEqual(result, expected_result)

    def test_save_before_entry_ids_list(self):
        before_entry_ids = ["12345", "67890", "98765"]

        # Test the method
        self.helper.save_before_entry_ids_list(before_entry_ids)

        # Read the content of the test file
        with open(self.before_entry_ids_json_path) as f:
            result_content = json.load(f)

        # Verify the content of the file
        expected_content = ['12345', '67890', '98765']
        self.assertEqual(result_content, expected_content)


if __name__ == '__main__':
    unittest.main()
