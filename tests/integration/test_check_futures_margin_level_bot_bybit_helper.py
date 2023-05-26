import datetime
import unittest

from pybit.unified_trading import HTTP

from trading_bots.helpers.check_futures_margin_level_bot_bybit_helper import CheckFuturesMarginLevelBotBybitHelper


class CheckFuturesMarginLevelBotBybitHelperTest(unittest.TestCase):

    def setUp(self) -> None:
        print("Start SetUp")

        api_key = ""
        secret_key = ""

        print("Init pybit client client")
        self.pybit_client = HTTP(
            testnet=True,
            api_key=api_key,
            api_secret=secret_key
        )
        print("Finished SetUp")

        self.helper = CheckFuturesMarginLevelBotBybitHelper(self.pybit_client, "../../trading_bots/data/funding_dates.json")

    def test_get_available_balance_on_futures_account(self):
        available_balance = self.helper.get_available_balance_on_futures_account()
        self.assertTrue(isinstance(available_balance, float))
        self.assertTrue(available_balance >= 0)

    def test_is_open_positions(self):
        self.assertFalse(self.helper.is_open_positions())

    def test_get_last_position_close_date(self):
        close_date = self.helper.get_last_position_close_date()
        self.assertTrue(isinstance(close_date, datetime.datetime))


if __name__ == '__main__':
    unittest.main()
