import unittest
import pandas as pd
from trading_bots.trading_math import (
    convert_ohlc,
    calculate_context,
    is_up_trend,
    is_down_trend,
    is_start_rotation_after_up_trend,
    is_start_rotation_after_down_trend,
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


if __name__ == '__main__':
    unittest.main()
