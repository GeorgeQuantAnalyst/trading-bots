import logging
import os
import sys

import pandas as pd
import yfinance as yf


class EquityTrendScreenerBotHelper:

    @staticmethod
    def get_tickers(file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            return df["Ticker"].tolist()
        except Exception as e:
            logging.error("Failed read tickers from file {}: {}".format(file_path, str(e)))
            sys.exit(-1)

    @staticmethod
    def get_daily_ohlc(ticker: str) -> pd.DataFrame:
        try:
            ohlc_raw = yf.Ticker(ticker).history(period="120mo", interval="1d")
            ohlc = ohlc_raw[["Open", "High", "Low", "Close"]][::-1].reset_index()
            ohlc.columns = ['startTime', 'open', 'high', 'low', 'close']
            return ohlc
        except Exception as e:
            logging.error("Failed get_daily_ohlc for ticker {}: {}".format(ticker, str(e)))
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
