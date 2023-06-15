import logging
import os
import sys

import pandas as pd

from trading_bots import constants


class CryptoTrendScreenerBotHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.category = constants.BYBIT_LINEAR_CATEGORY

    def get_pybit_futures_tickers(self) -> list:
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

    @staticmethod
    def create_tw_report(trends: pd.DataFrame) -> str:
        report = []

        report.append("###UP-TREND")
        uptrend_markets_df = trends[trends["context"] == "Up-trend"]
        report.extend(uptrend_markets_df["ticker"].tolist())

        report.append("###START ROTATION AFTER UP-TREND")
        start_rotation_markets_df = trends[trends["context"] == "Start rotation after up-trend"]
        report.extend(start_rotation_markets_df["ticker"].tolist())

        report.append("###DOWN-TREND")
        downtrend_markets_df = trends[trends["context"] == "Down-trend"]
        report.extend(downtrend_markets_df["ticker"].tolist())

        report.append("###START ROTATION AFTER DOWN-TREND")
        start_rotation_markets_df = trends[trends["context"] == "Start rotation after down-trend"]
        report.extend(start_rotation_markets_df["ticker"].tolist())

        return ",".join(report)

    @staticmethod
    def save_tw_report(report: str, file_path: str) -> None:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(report)
        except Exception as e:
            logging.error("Failed save tw report: {}".format(str(e)))
            sys.exit(-1)
