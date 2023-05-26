import unittest

from pybit.unified_trading import HTTP

from trading_bots import constants


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

    def tearDown(self) -> None:
        print("Start Tear down")

        print("Cancel all derivatives orders")
        self.pybit_client.cancel_all_orders(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")

        print("Cancel all derivatives positions")
        positions = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")

        for position in positions["result"]["list"]:
            self.pybit_client.place_order(
                category=constants.BYBIT_LINEAR_CATEGORY,
                symbol=position["symbol"],
                orderType="Market",
                side="Sell" if position["side"] == "Buy" else "Buy",
                qty=position["size"],
                positionIdx=position["positionIdx"],
                reduceOnly=True)

        print("Finished Tear down")

    def test_get_available_balance_on_futures_account(self):
        print("Start test_get_available_balance_on_futures_account")

        response = self.pybit_client.get_wallet_balance(
            accountType="CONTRACT",
            coin="USDT"
        )
        print("Response: {}".format(response))

        total_balance = float(response["result"]["list"][0]["coin"][0]["walletBalance"])
        free_balance = float(response["result"]["list"][0]["coin"][0]["availableToWithdraw"])

        print("Total balance: {} USDT, Free balance: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)
        print("Finished test_get_available_balance_on_futures_account")

    def test_is_open_positions(self):
        print("Start test_is_open_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        print(positions)

        self.assertEqual(positions["retCode"], 0)
        self.assertEqual(positions["retMsg"], "OK")
        self.assertEqual(len(positions["result"]["list"]), 2)
        self.assertEqual(positions["result"]["list"][0]["symbol"], "BTCUSDT")
        self.assertEqual(positions["result"]["list"][1]["symbol"], "ETHUSDT")

        print("Finished test_is_open_positions")

    def test_get_last_position_close_date(self):
        print("Start test_get_last_position_close_date")

        print("Get closed trades dates")
        closed_trades_dates = self.pybit_client.get_closed_pnl(category=constants.BYBIT_LINEAR_CATEGORY, limit=2)
        print(closed_trades_dates)

        self.assertEqual(closed_trades_dates["retCode"], 0)
        self.assertEqual(closed_trades_dates["retMsg"], "OK")
        self.assertEqual(len(closed_trades_dates["result"]["list"]), 2)
        self.assertEqual(closed_trades_dates["result"]["list"][0]["symbol"], "ETHUSDT")
        self.assertEqual(closed_trades_dates["result"]["list"][1]["symbol"], "BTCUSDT")

        print("Finished test_get_last_position_close_date")

    def create_small_btc_long_position(self, type_of_order="Market", limit_price=None):
        return self.pybit_client.place_order(
            category=constants.BYBIT_LINEAR_CATEGORY,
            symbol="BTCUSDT",
            orderType=type_of_order,
            side="Buy",
            qty=0.001,
            price=limit_price,
            positionIdx=0
        )

    def create_small_eth_long_position(self, type_of_order="Market", limit_price=None):
        return self.pybit_client.place_order(
            category=constants.BYBIT_LINEAR_CATEGORY,
            symbol="ETHUSDT",
            orderType=type_of_order,
            side="Buy",
            qty=0.01,
            price=limit_price,
            positionIdx=0
        )


if __name__ == '__main__':
    unittest.main()
