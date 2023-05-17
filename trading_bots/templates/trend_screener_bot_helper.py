from abc import ABC, abstractmethod


class TrendScreenerBotHelper(ABC):

    @abstractmethod
    def get_available_tickers(self):
        pass

    @abstractmethod
    def get_ohlc(self, ticker, time_frame):
        pass

    def load_ohlc_cache(self, tickers):
        ohlc_cache = {
            "daily": {},
            "weekly": {},
            "monthly": {}
        }

        for ticker in tickers:
            ohlc_daily = self.get_ohlc(ticker, "D")
            ohlc_weekly = self.get_ohlc(ticker, "W")
            ohlc_monthly = self.get_ohlc(ticker, "M")

            ohlc_cache["daily"][ticker] = ohlc_daily
            ohlc_cache["weekly"][ticker] = ohlc_weekly
            ohlc_cache["monthly"][ticker] = ohlc_monthly

        return ohlc_cache

    @staticmethod
    def calculate_percentage_change(ohlc, days):
        count_days = ohlc.shape[0] - 1

        actual_price = ohlc.loc[0]["close"]
        old_price = ohlc.loc[days]["open"] if days < count_days else ohlc.loc[count_days]["open"]

        return round(((actual_price - old_price) / old_price) * 100, 2)

    @staticmethod
    def calculate_context(ohlc):
        ohlc_filtered = ohlc.head(4)

        if ohlc_filtered.shape[0] < 4:
            return "N/A"

        # Compute candle color
        ohlc_filtered.loc[ohlc_filtered['close'] < ohlc_filtered['open'], 'candleColor'] = 'Red'
        ohlc_filtered.loc[ohlc_filtered['close'] >= ohlc_filtered['open'], 'candleColor'] = 'Green'

        # Compute context
        if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Green":
            return "Up-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Green" and \
                ohlc_filtered.loc[3]["candleColor"] == "Green":
            return "Start rotation after up-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Red":
            return "Down-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Red" and \
                ohlc_filtered.loc[3]["candleColor"] == "Red":
            return "Start rotation after down-trend"

        return "Rotation"
