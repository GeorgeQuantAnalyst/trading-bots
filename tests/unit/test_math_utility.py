import unittest

import pandas as pd

from trading_bots.trading_math import (
    convert_ohlc,
    calculate_context,
    calculate_break_out_sd_range,
)


class TestTradingMath(unittest.TestCase):

    def test_convert_ohlc(self):
        ohlc_df = pd.read_csv("fixtures/AAPL_OHLC_D.csv")

        # Test the function
        result = convert_ohlc(ohlc_df, 'Q')

        # Verify the result
        expected_result = pd.read_csv("fixtures/APPL_OHLC_3M.csv", parse_dates=["startTime"])
        pd.testing.assert_frame_equal(result, expected_result)

    def test_calculate_context_is_uptrend(self):
        ohlc_df = pd.read_csv("fixtures/AAPL_OHLC_M.csv")

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Up-trend')

    def test_calculate_context_is_start_rotation_after_uptrend(self):
        ohlc_df = pd.read_csv("fixtures/LULU_OHLC_M.csv")

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Start rotation after up-trend')

    def test_calculate_context_is_rotation(self):
        ohlc_df = pd.read_csv("fixtures/SONY_OHLC_M.csv")

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Rotation')

    def test_calculate_context_is_downtrend(self):
        ohlc_df = pd.read_csv("fixtures/MRNA_OHLC_M.csv")

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Down-trend')

    def test_calculate_context_is_start_rotation_after_downtrend(self):
        ohlc_df = pd.read_csv("fixtures/CHPT_OHLC_M.csv")

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Start rotation after down-trend')

    def test_calculate_break_out_sd_range_resistance(self):
        tickers = ["VTYX", "WKHS", "CLSK", "INSG", "RIOT", "GOEV", "BLND", "COIN", "MSTR", "SFIX"]
        expected_breakouts = [2.19, 7.04, 1.55, 2.32, 2.72, 2.87, 1.92, 2.69, 3.31, 3.87]

        for ticker, expected_breakout in zip(tickers, expected_breakouts):
            ohlc_df = pd.read_csv("fixtures/test_breakouts/{}_OHLC_D.csv".format(ticker))
            breakout = round(calculate_break_out_sd_range(ohlc_df), 2)
            print("{} breakout sd range resistance: {}".format(ticker, breakout))
            self.assertEqual(breakout, expected_breakout)

    def test_calculate_break_out_sd_range_no_breakout(self):
        tickers = ["OSCR", "AIZ", "SR", "U", "SBUX", "AYI", "DAWN", "BILL", "COUR", "SKY"]
        expected_breakouts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for ticker, expected_breakout in zip(tickers, expected_breakouts):
            ohlc_df = pd.read_csv("fixtures/test_breakouts/{}_OHLC_D.csv".format(ticker))
            breakout = round(calculate_break_out_sd_range(ohlc_df), 2)
            print("{} breakout sd range no breakout: {}".format(ticker, breakout))
            self.assertEqual(breakout, expected_breakout)

    def test_calculate_break_out_sd_range_support(self):
        tickers = ["TTCF", "PTGX", "TNYA", "REPL", "OM", "AGEN", "SEER", "CMAX", "KPTI", "ANAB"]
        expected_breakouts = [-21.99, 0, -1.02, -1.72, -1.45, -1.64, -1.35, -1.06, -3.96, -1.54]

        for ticker, expected_breakout in zip(tickers, expected_breakouts):
            ohlc_df = pd.read_csv("fixtures/test_breakouts/{}_OHLC_D.csv".format(ticker))
            breakout = round(calculate_break_out_sd_range(ohlc_df), 2)
            print("{} breakout sd range support: {}".format(ticker, breakout))
            self.assertEqual(breakout, expected_breakout)


if __name__ == '__main__':
    unittest.main()
