import unittest

from alpha_vantage.foreignexchange import ForeignExchange

from trading_bots.helpers.forex_trend_screener_bot_helper import ForexTrendScreenerBotHelper

import pandas as pd


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
        eurusd_ohlc = pd.read_csv("fixtures/eurusd_ohlc.csv")
        eurcad_ohlc = pd.read_csv("fixtures/eurcad_ohlc.csv")
        nzdchf_ohlc = pd.read_csv("fixtures/nzdchf_ohlc.csv")

        self.assertEqual(self.helper.calculate_percentage_change(ohlc=eurusd_ohlc, days=7), -1.95)
        self.assertEqual(self.helper.calculate_percentage_change(ohlc=eurcad_ohlc, days=7), -1.15)
        self.assertEqual(self.helper.calculate_percentage_change(ohlc=nzdchf_ohlc, days=7), -0.6)

    def test_calculate_context(self):
        # ohlc = self.helper.get_ohlc(ticker="EURNZD", time_frame="W")
        # ohlc.to_csv("fixtures/eurnzd_ohlc_w.csv", index=False)
        eurusd_ohlc = pd.read_csv("fixtures/eurusd_ohlc.csv")
        nzdchf_ohlc = pd.read_csv("fixtures/nzdchf_ohlc.csv")
        chfjpy_ohlc = pd.read_csv("fixtures/chfjpy_ohlc.csv")
        cadchf_ohlc = pd.read_csv("fixtures/cadchf_ohlc_w.csv")
        eurnzd_ohlc = pd.read_csv("fixtures/eurnzd_ohlc_w.csv")

        self.assertEqual(self.helper.calculate_context(eurusd_ohlc), "Down-trend")
        self.assertEqual(self.helper.calculate_context(nzdchf_ohlc), "Rotation")
        self.assertEqual(self.helper.calculate_context(chfjpy_ohlc), "Up-trend")
        self.assertEqual(self.helper.calculate_context(cadchf_ohlc), "Start rotation after up-trend")
        self.assertEqual(self.helper.calculate_context(eurnzd_ohlc), "Start rotation after down-trend")

