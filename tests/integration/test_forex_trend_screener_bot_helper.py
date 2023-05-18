import unittest

from alpha_vantage.foreignexchange import ForeignExchange

from trading_bots.helpers.forex_trend_screener_bot_helper import ForexTrendScreenerBotHelper

class ForexTrendScreenerBotHelperTest(unittest.TestCase):

    def setUp(self):
        print("Start setUp")
        api_key = "12345"
        foreign_exchange = ForeignExchange(key=api_key)
        self.helper = ForexTrendScreenerBotHelper(foreign_exchange, "fixtures/tickers.csv")

        print("Finished setUp")

    def test_get_available_tickers(self):
        tickers = self.helper.get_available_tickers()

        print("Tickers: {}".format(tickers))

        self.assertTrue(len(tickers) == 3)
        self.assertIn("EURUSD", tickers)
        self.assertIn("USDJPY", tickers)
        self.assertIn("GBPUSD", tickers)

    def test_get_ohlc(self):
        ohlc = self.helper.get_ohlc(ticker="EURUSD", time_frame="D")
        print("EURUSD daily OHCL: \n {}".format(ohlc))

        missing_values = ohlc.isnull().sum()

        self.assertTrue(ohlc.shape[0] == 100)
        self.assertEqual(ohlc.columns.tolist(), ['startTime', 'open', 'high', 'low', 'close'])
        self.assertEqual(missing_values.sum(), 0)

    def test_load_ohlc_cache(self):
        tickers = self.helper.get_available_tickers()
        cache = self.helper.load_ohlc_cache(tickers)

        print("Cache: {}".format(cache))

        self.assertIn("daily", cache.keys())
        self.assertIn("weekly", cache.keys())
        self.assertIn("monthly", cache.keys())

        self.assertTrue(len(cache["daily"]) == 3)
        self.assertTrue(len(cache["weekly"]) == 3)
        self.assertTrue(len(cache["monthly"]) == 3)

    def test_calculate_percentage_change(self):
        # TODO Lucka
        pass
        ohlc = self.helper.get_ohlc(ticker="EURUSD", time_frame="D")
        ohlc.to_csv("eurusd.csv", index=False)
        # btc_ohlc = pd.read_csv("fixtures/btc_ohlc.csv")
        # eth_ohlc = pd.read_csv("fixtures/eth_ohlc.csv")
        # bnb_ohlc = pd.read_csv("fixtures/bnb_ohlc.csv")
        #
        # self.assertEqual(self.helper.calculate_percentage_change(ohlc=btc_ohlc, days=7), -3.1)
        # self.assertEqual(self.helper.calculate_percentage_change(ohlc=eth_ohlc, days=7), 4.84)
        # self.assertEqual(self.helper.calculate_percentage_change(ohlc=bnb_ohlc, days=7), 0.93)

    def test_calculate_context(self):
        # TODO Lucka
        pass

        # alice_ohlc = pd.read_csv("fixtures/alice_ohlc.csv")
        # ankr_ohlc = pd.read_csv("fixtures/ankr_ohcl.csv")
        # cream_ohlc = pd.read_csv("fixtures/cream_ohlc.csv")
        # inj_ohlc = pd.read_csv("fixtures/inj_ohlc.csv")
        # lina_ohlc = pd.read_csv("fixtures/lina_ohlc.csv")
        #
        # self.assertEqual(self.helper.calculate_context(alice_ohlc), "Rotation")
        # self.assertEqual(self.helper.calculate_context(ankr_ohlc), "Start rotation after down-trend")
        # self.assertEqual(self.helper.calculate_context(cream_ohlc), "Up-trend")
        # self.assertEqual(self.helper.calculate_context(inj_ohlc), "Down-trend")
        # self.assertEqual(self.helper.calculate_context(lina_ohlc), "Start rotation after up-trend")
