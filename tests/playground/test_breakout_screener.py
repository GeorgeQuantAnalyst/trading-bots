import unittest

import pandas as pd

from trading_bots.helpers.equity_trend_screener_bot_helper import EquityTrendScreenerBotHelper


class BreakOutScreenerTest(unittest.TestCase):

    @staticmethod
    def calculate_break_out_sd_range(ohlc: pd.DataFrame, threshold: int = 1):
        data = ohlc.sort_index(ascending=False)

        data["range"] = data["high"] - data["low"]
        data["5-day range support"] = data["low"].rolling(window=5).mean()
        data["5-day range resistance"] = data["high"].rolling(window=5).mean()
        data["5-day range"] = data["range"].rolling(window=5).mean()
        data["5-day range SD"] = data["range"].rolling(window=5).std()
        data["breakout resistance SDx"] = (data["close"] - data["5-day range resistance"]) / data["5-day range SD"]
        data["breakout support SDx"] = (data["close"] - data["5-day range support"]) / data["5-day range SD"]

        data["breakout support"] = data["close"] < data["5-day range support"] - (
                data["5-day range SD"] * threshold)

        data["breakout resistance"] = data["close"] > data["5-day range resistance"] + (
                data["5-day range SD"] * threshold)

        if data.tail(3)["breakout resistance"].any():
            return data.tail(3)["breakout resistance SDx"].max()

        if data.tail(3)["breakout support"].any():
            return data.tail(3)["breakout support SDx"].min()

        return 0

    def test_find_break_out_from_trading_range(self):
        tickers = ["AAPL", "SFIX", "CIFR", "ADBE", "MSFT", "ABNB", "KMX", "ISRG", "TECH", "XXII", "ENOB", "TYRA",
                   "TTCF",
                   "AVAH", "NG", "XPOF"]
        helper = EquityTrendScreenerBotHelper()

        breakouts = []
        for ticker in tickers:
            ohlc = helper.get_daily_ohlc(ticker)
            break_out_range_sd = self.calculate_break_out_sd_range(ohlc)

            breakouts.append({
                "ticker": ticker,
                "breakout SD range": break_out_range_sd
            })

        breakouts_df = pd.DataFrame(breakouts)
        breakouts_df.sort_values(by="breakout SD range", ascending=False, inplace=True)
        print(breakouts_df)


if __name__ == '__main__':
    unittest.main()
