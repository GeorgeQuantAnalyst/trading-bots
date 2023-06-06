from abc import ABC, abstractmethod
import pandas as pd


class TrendScreenerBotHelper(ABC):

    @abstractmethod
    def get_available_tickers(self):
        pass

    @abstractmethod
    def get_ohlc(self, ticker: str, time_frame: str) -> pd.DataFrame:
        pass

    def load_ohlc_cache(self, tickers: list) -> dict:
        ohlc_cache = {
            "daily": {},
            "weekly": {},
            "monthly": {},
            "quarterly": {}
        }

        for ticker in tickers:
            ohlc_daily = self.get_ohlc(ticker, "D")
            ohlc_weekly = self.convert_daily_ohlc_to_weekly_ohlc(ohlc_daily)
            ohlc_monthly = self.get_ohlc(ticker, "M")
            ohlc_quarterly = self.convert_monthly_ohlc_to_quarterly_ohlc(ohlc_monthly)

            ohlc_cache["daily"][ticker] = ohlc_daily
            ohlc_cache["weekly"][ticker] = ohlc_weekly
            ohlc_cache["monthly"][ticker] = ohlc_monthly
            ohlc_cache["quarterly"][ticker] = ohlc_quarterly

        return ohlc_cache

    @staticmethod
    def calculate_percentage_change(ohlc: pd.DataFrame, days: int) -> float:
        count_days = ohlc.shape[0] - 1

        actual_price = ohlc.loc[0]["close"]
        old_price = ohlc.loc[days]["open"] if days < count_days else ohlc.loc[count_days]["open"]

        return round(((actual_price - old_price) / old_price) * 100, 2)

    @staticmethod
    def calculate_context(ohlc: pd.DataFrame) -> str:
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

    @staticmethod
    def convert_daily_ohlc_to_weekly_ohlc(ohlc: pd.DataFrame) -> pd.DataFrame:
        df = ohlc.copy()
        df['startTime'] = pd.to_datetime(df['startTime'])
        df.set_index('startTime', inplace=True)

        weekly_df = df.resample('W').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        weekly_df = weekly_df[::-1].reset_index()
        weekly_df.columns = ['startTime', 'open', 'high', 'low', 'close']

        return weekly_df

    @staticmethod
    def convert_daily_ohlc_to_monthly_ohlc(ohlc: pd.DataFrame) -> pd.DataFrame:
        df = ohlc.copy()
        df['startTime'] = pd.to_datetime(df['startTime'])
        df.set_index('startTime', inplace=True)

        monthly_df = df.resample('M').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        monthly_df = monthly_df[::-1].reset_index()
        monthly_df.columns = ['startTime', 'open', 'high', 'low', 'close']

        return monthly_df

    @staticmethod
    def convert_monthly_ohlc_to_quarterly_ohlc(ohlc: pd.DataFrame) -> pd.DataFrame:
        df = ohlc.copy()
        df['startTime'] = pd.to_datetime(df['startTime'])
        df.set_index('startTime', inplace=True)

        quarterly_df = df.resample('3M').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        quarterly_df = quarterly_df[::-1].reset_index()
        quarterly_df.columns = ['startTime', 'open', 'high', 'low', 'close']

        return quarterly_df
