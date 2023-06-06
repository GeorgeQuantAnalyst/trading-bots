import logging

import pandas as pd

from trading_bots import constants
from trading_bots.templates.trend_screener_bot_helper import TrendScreenerBotHelper


class CryptoTrendScreenerBotHelper(TrendScreenerBotHelper):

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.category = constants.BYBIT_LINEAR_CATEGORY

    def get_available_tickers(self) -> list:
        response = self.pybit_client.get_instruments_info(category=self.category)

        logging.debug("Response get_instruments_info: {}".format(response))

        return [x["symbol"] for x in
                response["result"]["list"] if "USDT" in x["symbol"]]

    def get_ohlc(self, ticker: str, time_frame: str) -> pd.DataFrame:
        response = self.pybit_client.get_kline(category=self.category, symbol=ticker, interval=time_frame)
        ohlc = pd.DataFrame(response["result"]["list"],
                            columns=["startTime", "open", "high", "low", "close", "volume", "turnover"])

        logging.debug("Response get_kline: {}".format(response))

        ohlc["open"] = pd.to_numeric(ohlc["open"])
        ohlc["high"] = pd.to_numeric(ohlc["high"])
        ohlc["low"] = pd.to_numeric(ohlc["low"])
        ohlc["close"] = pd.to_numeric(ohlc["close"])
        ohlc["volume"] = pd.to_numeric(ohlc["volume"])
        ohlc["turnover"] = pd.to_numeric(ohlc["turnover"])
        ohlc["startTime"] = pd.to_numeric(ohlc["startTime"])
        ohlc['startTime'] = pd.to_datetime(ohlc["startTime"], unit='ms')
        return ohlc

    @staticmethod
    def filter_tickers(tickers: list, daily_volume_above_filter: int, ohlc_cache: dict) -> list:
        filtered_tickers = []

        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"].get(ticker)

            if ohlc_daily is not None:
                last_ohlc = ohlc_daily.iloc[0]
                daily_volume_in_usd = last_ohlc["volume"] * last_ohlc["close"]
                if daily_volume_in_usd > daily_volume_above_filter:
                    filtered_tickers.append(ticker)

        return filtered_tickers

    @staticmethod
    def create_tw_report_weekly_trends(trends: pd.DataFrame) -> str:
        report = []

        report.append("###UP-TREND W")
        uptrend_markets_df = trends[trends["Context W"] == "Up-trend"]
        uptrend_markets_sorted_df = uptrend_markets_df.sort_values("Change 30 days, %", ascending=False)
        report.extend(uptrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER UP-TREND W")
        start_rotation_markets_df = trends[trends["Context W"] == "Start rotation after up-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 30 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        report.append("###DOWN-TREND W")
        downtrend_markets_df = trends[trends["Context W"] == "Down-trend"]
        downtrend_markets_sorted_df = downtrend_markets_df.sort_values("Change 30 days, %", ascending=False)
        report.extend(downtrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER DOWN-TREND W")
        start_rotation_markets_df = trends[trends["Context W"] == "Start rotation after down-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 30 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        return ",".join(report)

    @staticmethod
    def create_tw_report_monthly_trends(trends: pd.DataFrame) -> str:
        # TODO: @Lucka
        pass

    @staticmethod
    def create_tw_report_quarterly_trends(trends: pd.DataFrame) -> str:
        # TODO: @Lucka
        pass

    @staticmethod
    def save_tw_report(report: str, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(report)
