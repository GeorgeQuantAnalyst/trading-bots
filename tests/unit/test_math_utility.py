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

# TODO: repair me please @Lucka
class TestTradingMath(unittest.TestCase):

    def test_convert_ohlc(self):
        ohlc_df = pd.read_csv("fixtures/AAPL_OHLC_D.csv")

        # Test the function
        result = convert_ohlc(ohlc_df, 'Q')

        # Verify the result
        expected_result = pd.read_csv("fixtures/APPL_OHLC_3M.csv", parse_dates=["startTime"])
        pd.testing.assert_frame_equal(result, expected_result)

    def test_calculate_context(self):
        ohlc_data = {
            'startTime': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'open': [100, 150, 200, 250, 300],
            'high': [120, 160, 210, 260, 310],
            'low': [80, 140, 190, 240, 290],
            'close': [110, 155, 205, 255, 305],
            'candleColor': ['Green', 'Green', 'Green', 'Green', 'Green']
        }
        ohlc_df = pd.DataFrame(ohlc_data)

        # Test the function
        result = calculate_context(ohlc_df)

        # Verify the result
        self.assertEqual(result, 'Up-trend')

    def test_is_up_trend(self):
        ohlc_data = {
            'startTime': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
            'open': [100, 150, 200, 250],
            'high': [120, 160, 210, 260],
            'low': [80, 140, 190, 240],
            'close': [110, 155, 205, 255],
            'candleColor': ['Green', 'Green', 'Green', 'Green']
        }
        ohlc_df = pd.DataFrame(ohlc_data)

        # Test the function
        result = is_up_trend(ohlc_df)

        # Verify the result
        self.assertTrue(result)

    # Add more test cases for the remaining functions...


if __name__ == '__main__':
    unittest.main()
