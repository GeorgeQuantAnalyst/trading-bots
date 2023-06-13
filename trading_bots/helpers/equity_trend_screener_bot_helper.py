import logging
import os
import sys
import time

import pandas as pd


class EquityTrendScreenerBotHelper:
    API_CALL_LIMIT_EXCEPTION_MSG = "Our standard API call frequency is 5 calls per minute and 500 calls per day."
    API_CALL_LIMIT_WARNING_MSG = "The request per minute limit has just been exceeded, the application will wait a minute before retrying the data download."
    API_CALL_LIMIT_SLEEP_INTERVAL_SECONDS = 60

    def __init__(self, config: dict, exchange):
        self.config = config
        self.exchange = exchange

    @staticmethod
    def get_tickers(file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            return df["Ticker"].tolist()
        except Exception as e:
            logging.error("Failed read tickers from file {}: {}".format(file_path, str(e)))
            sys.exit(-1)

    def get_daily_adjusted_ohlc(self, ticker: str) -> pd.DataFrame:
        try:
            data, meta_data = self.exchange.get_daily_adjusted(symbol=ticker, outputsize="full")
            data = data.reset_index()
            data.columns = ['startTime', 'open', 'high', 'low', 'close', "adjusted close", "volume", "dividend amount",
                            "split coefficient"]

            # fix issue: https://github.com/RomelTorres/alpha_vantage/issues/115
            data["open"] = data["adjusted close"]
            data["high"] = data["adjusted close"]
            data["low"] = data["adjusted close"]
            data["close"] = data["adjusted close"]

            return data
        except ValueError as e:
            if self.API_CALL_LIMIT_EXCEPTION_MSG in str(e):
                logging.warning(self.API_CALL_LIMIT_WARNING_MSG)
                time.sleep(self.API_CALL_LIMIT_SLEEP_INTERVAL_SECONDS)
                return self.get_daily_adjusted_ohlc(ticker)
            else:
                logging.error("Failed call method get_daily_adjusted on AlphaVantage client: {}".format(str(e)))
                sys.exit(-1)

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
