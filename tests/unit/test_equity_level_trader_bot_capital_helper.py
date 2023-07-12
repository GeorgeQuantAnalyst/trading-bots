import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper
from datetime import datetime, date, timedelta


class TestEquityLevelTraderBotCapitalHelper(unittest.TestCase):
    def setUp(self):
        config = {}
        config["alphavantageApiKey"] = {"apiKey": "demo"}
        config["capitalApi"] = {}

        self.helper = EquityLevelTraderBotCapitalHelper(config)

    @patch('requests.get')
    def test_was_yesterday_the_last_earnings_is_true(self, mock_get):
        ticker = 'MSFT'
        now = datetime.now().date()
        yesterday = now - timedelta(days=1)

        response_data = {
            "quarterlyEarnings": [
                {"reportedDate": yesterday.strftime("%Y-%m-%d")}
            ],
            "annualEarnings": [
                {"fiscalDateEnding": yesterday.strftime("%Y-%m-%d")}
            ]
        }
        mock_get.return_value.json.return_value = response_data

        result = self.helper.was_yesterday_earnings(ticker)

        self.assertTrue(result)

        expected_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=demo"
        mock_get.assert_called_once_with(expected_url)

    @patch('requests.get')
    def test_was_yesterday_the_last_earnings_is_false(self, mock_get):
        ticker = 'MSFT'
        now = datetime.now().date()
        two_days_before = now - timedelta(days=2)

        response_data = {
            "quarterlyEarnings": [
                {"reportedDate": two_days_before.strftime("%Y-%m-%d")}
            ],
            "annualEarnings": [
                {"fiscalDateEnding": two_days_before.strftime("%Y-%m-%d")}
            ]
        }
        mock_get.return_value.json.return_value = response_data

        result = self.helper.was_yesterday_earnings(ticker)

        self.assertFalse(result)

        expected_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=demo"
        mock_get.assert_called_once_with(expected_url)

    @patch("requests.get")
    def test_is_earnings_next_days_is_true(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "reportDate\n2023-07-10\n2023-07-15\n2023-07-20"
        mock_get.return_value = mock_response

        result = self.helper.is_earnings_next_days("MSFT")

        self.assertTrue(result)

        expected_url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=MSFT&horizon=12month&apikey=demo"
        mock_get.assert_called_once_with(expected_url)

    @patch("requests.get")
    def test_is_earnings_next_days_is_false(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "reportDate\n2023-07-30\n2023-10-30\n2023-12-20"
        mock_get.return_value = mock_response

        result = self.helper.is_earnings_next_days("MSFT")

        self.assertFalse(result)

        expected_url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=MSFT&horizon=12month&apikey=demo"
        mock_get.assert_called_once_with(expected_url)

    if __name__ == '__main__':
        unittest.main()