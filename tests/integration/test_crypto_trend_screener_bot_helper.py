import unittest

import pandas as pd
import timeout_decorator

from pybit.unified_trading import HTTP
from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper


class CryptoTrendScreenerBotHelperTest(unittest.TestCase):

    def setUp(self):
        print("Start setUp")

        pybit_client = HTTP()
        self.helper = CryptoTrendScreenerBotHelper(pybit_client)

        print("Finished setUp")

    def test_get_available_tickers(self):
        tickers = self.helper.get_available_tickers()

        print("Tickers: {}".format(tickers))

        self.assertTrue(len(tickers) > 200)
        self.assertIn("BTCUSDT", tickers)
        self.assertIn("ETHUSDT", tickers)

    def test_get_ohlc(self):
        ohlc = self.helper.get_ohlc(ticker="BTCUSDT", time_frame="D")
        print("BTCUSDT daily OHCL: \n {}".format(ohlc))

        missing_values = ohlc.isnull().sum()

        self.assertTrue(ohlc.shape[0] == 200)
        self.assertEqual(ohlc.columns.tolist(), ['startTime', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        self.assertEqual(missing_values.sum(), 0)

    @timeout_decorator.timeout(180)  # 3 minutes timeout
    def test_load_ohlc_cache(self):
        tickers = self.helper.get_available_tickers()
        cache = self.helper.load_ohlc_cache(tickers)

        print("Cache: {}".format(cache))

        self.assertIn("daily", cache.keys())
        self.assertIn("weekly", cache.keys())
        self.assertIn("monthly", cache.keys())

        self.assertTrue(len(cache["daily"]) > 200)
        self.assertTrue(len(cache["weekly"]) > 200)
        self.assertTrue(len(cache["monthly"]) > 200)

    def test_calculate_percentage_change(self):
        btc_ohlc = pd.read_csv("tests/integration/fixtures/btc_ohlc.csv")
        eth_ohlc = pd.read_csv("tests/integration/fixtures/eth_ohlc.csv")
        bnb_ohlc = pd.read_csv("tests/integration/fixtures/bnb_ohlc.csv")

        self.assertEqual(self.helper.calculate_percentage_change(ohlc=btc_ohlc, days=7), -3.1)
        self.assertEqual(self.helper.calculate_percentage_change(ohlc=eth_ohlc, days=7), 4.84)
        self.assertEqual(self.helper.calculate_percentage_change(ohlc=bnb_ohlc, days=7), 0.93)

    def test_calculate_context(self):
        alice_ohlc = pd.read_csv("tests/integration/fixtures/alice_ohlc.csv")
        ankr_ohlc = pd.read_csv("tests/integration/fixtures/ankr_ohcl.csv")
        cream_ohlc = pd.read_csv("tests/integration/fixtures/cream_ohlc.csv")
        inj_ohlc = pd.read_csv("tests/integration/fixtures/inj_ohlc.csv")
        lina_ohlc = pd.read_csv("tests/integration/fixtures/lina_ohlc.csv")

        self.assertEqual(self.helper.calculate_context(alice_ohlc), "Rotation")
        self.assertEqual(self.helper.calculate_context(ankr_ohlc), "Start rotation after down-trend")
        self.assertEqual(self.helper.calculate_context(cream_ohlc), "Up-trend")
        self.assertEqual(self.helper.calculate_context(inj_ohlc), "Down-trend")
        self.assertEqual(self.helper.calculate_context(lina_ohlc), "Start rotation after up-trend")


