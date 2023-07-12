import unittest
from unittest.mock import patch

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper
import datetime


class TestEquityLevelTraderBotCapitalHelper(unittest.TestCase):
    def setUp(self):
        config = {}
        config["alphavantageApiKey"] = {"apiKey": "demo"}
        config["capitalApi"] = {}

        self.helper = EquityLevelTraderBotCapitalHelper(config)

    @patch('requests.get')
    def test_was_yesterday_the_last_earnings_is_true(self, mock_get):
        ticker = 'MSFT'
        now = datetime.datetime.now().date()
        yesterday = now - datetime.timedelta(days=1)

        response_data = {
            "quarterlyEarnings": [
                {"reportedDate": yesterday.strftime('%Y-%m-%d')}
            ],
            "annualEarnings": []
        }
        mock_get.return_value.json.return_value = response_data

        result = self.helper.was_yesterday_earnings(ticker)

        self.assertTrue(result)

        expected_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=demo"
        mock_get.assert_called_once_with(expected_url)

        # TODO: je treba opravit

    def test_is_earnings_next_days(self):
        pass

    if __name__ == '__main__':
        unittest.main()