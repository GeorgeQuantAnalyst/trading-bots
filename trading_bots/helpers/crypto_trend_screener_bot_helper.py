import logging
import sys

import pandas as pd

from trading_bots import constants
from trading_bots.templates.trend_screener_bot_helper import TrendScreenerBotHelper


class CryptoTrendScreenerBotHelper(TrendScreenerBotHelper):

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.category = constants.BYBIT_LINEAR_CATEGORY

    def get_available_tickers(self) -> list:
        try:
            response = self.pybit_client.get_instruments_info(category=self.category)
        except Exception as e:
            logging.error("Failed call method get_instruments_info on pybit client: {}".format(str(e)))
            sys.exit(-1)

        logging.debug("Response get_instruments_info: {}".format(response))

        return [x["symbol"] for x in
                response["result"]["list"] if "USDT" in x["symbol"]]

    def get_ohlc(self, ticker: str, time_frame: str) -> pd.DataFrame:
        try:
            response = self.pybit_client.get_kline(category=self.category, symbol=ticker, interval=time_frame)
        except Exception as e:
            logging.error("Failed call method get_kline on pybit client: {}".format(str(e)))
            sys.exit(-1)

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

    def create_tw_trends_report(self, swing_weekly_trends: pd.DataFrame,
                                swing_monthly_trends: pd.DataFrame,
                                position_quarterly_trends: pd.DataFrame,
                                reports_folder: str) -> None:
        swing_weekly_trends["ticker"] = "BYBIT:" + swing_weekly_trends["ticker"] + ".P"
        swing_monthly_trends["ticker"] = "BYBIT:" + swing_monthly_trends["ticker"] + ".P"
        position_quarterly_trends["ticker"] = "BYBIT:" + position_quarterly_trends["ticker"] + ".P"

        swing_weekly_trends_report_path = "{}/Crypto swing W trends.txt".format(reports_folder)
        swing_weekly_trends_report = self.create_tw_report_weekly_trends(swing_weekly_trends)
        self.save_tw_report(swing_weekly_trends_report, swing_weekly_trends_report_path)

        swing_monthly_trends_report_path = "{}/Crypto swing M trends.txt".format(reports_folder)
        swing_monthly_trends_report = self.create_tw_report_monthly_trends(swing_monthly_trends)
        self.save_tw_report(swing_monthly_trends_report, swing_monthly_trends_report_path)

        position_quarterly_trends_report_path = "{}/Crypto position 3M trends.txt".format(reports_folder)
        position_quarterly_trends_report = self.create_tw_report_quarterly_trends(position_quarterly_trends)
        self.save_tw_report(position_quarterly_trends_report, position_quarterly_trends_report_path)

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
        report = []

        report.append("###UP-TREND M")
        uptrend_markets_df = trends[trends["Context M"] == "Up-trend"]
        uptrend_markets_sorted_df = uptrend_markets_df.sort_values("Change 90 days, %", ascending=False)
        report.extend(uptrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER UP-TREND M")
        start_rotation_markets_df = trends[trends["Context M"] == "Start rotation after up-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 90 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        report.append("###DOWN-TREND M")
        downtrend_markets_df = trends[trends["Context M"] == "Down-trend"]
        downtrend_markets_sorted_df = downtrend_markets_df.sort_values("Change 90 days, %", ascending=False)
        report.extend(downtrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER DOWN-TREND M")
        start_rotation_markets_df = trends[trends["Context M"] == "Start rotation after down-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 90 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        return ",".join(report)

    @staticmethod
    def create_tw_report_quarterly_trends(trends: pd.DataFrame) -> str:
        report = []

        report.append("###UP-TREND 3M")
        uptrend_markets_df = trends[trends["Context 3M"] == "Up-trend"]
        uptrend_markets_sorted_df = uptrend_markets_df.sort_values("Change 90 days, %", ascending=False)
        report.extend(uptrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER UP-TREND 3M")
        start_rotation_markets_df = trends[trends["Context 3M"] == "Start rotation after up-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 90 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        report.append("###DOWN-TREND 3M")
        downtrend_markets_df = trends[trends["Context 3M"] == "Down-trend"]
        downtrend_markets_sorted_df = downtrend_markets_df.sort_values("Change 90 days, %", ascending=False)
        report.extend(downtrend_markets_sorted_df["ticker"].tolist())

        report.append("###START ROTATION AFTER DOWN-TREND 3M")
        start_rotation_markets_df = trends[trends["Context 3M"] == "Start rotation after down-trend"]
        start_rotation_markets_sorted_df = start_rotation_markets_df.sort_values(
            "Change 90 days, %", ascending=False)
        report.extend(start_rotation_markets_sorted_df["ticker"].tolist())

        return ",".join(report)

    @staticmethod
    def save_tw_report(report: str, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(report)
