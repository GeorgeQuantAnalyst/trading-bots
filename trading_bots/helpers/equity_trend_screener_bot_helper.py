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
            ticker = ticker.replace(".", "-")
            # Download ohlc data without splits and dividend [auto_adjust=False]
            ohlc_raw = yf.Ticker(ticker).history(period="120mo", interval="1d", auto_adjust=False)
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
    def create_tw_breakouts_report(breakouts: pd.DataFrame) -> str:
        report = []

        report.append("###BREAKOUTS ABOVE 5SD")
        breakouts_above_five_sd_df = breakouts[breakouts["breakout from SD range"] > 5]
        breakouts_above_five_sd_df.sort_values("breakout from SD range", ascending=False, inplace=True)
        report.extend(breakouts_above_five_sd_df["ticker"].tolist())

        report.append("###BREAKOUTS BETWEEN 3SD AND 5SD")
        breakouts_between_three_and_five_sd_df = breakouts[
            (breakouts["breakout from SD range"] > 3) & (breakouts["breakout from SD range"] < 5)]
        breakouts_between_three_and_five_sd_df.sort_values("breakout from SD range", ascending=False, inplace=True)
        report.extend(breakouts_between_three_and_five_sd_df["ticker"].tolist())

        report.append("###BREAKOUTS BETWEEN 1SD AND 3SD")
        breakouts_between_one_and_three_sd_df = breakouts[
            (breakouts["breakout from SD range"] > 1) & (breakouts["breakout from SD range"] < 3)]
        breakouts_between_one_and_three_sd_df.sort_values("breakout from SD range", ascending=False, inplace=True)
        report.extend(breakouts_between_one_and_three_sd_df["ticker"].tolist())

        report.append("###BREAKOUTS BELOW -5SD")
        breakouts_below_minus_five_sd_df = breakouts[breakouts["breakout from SD range"] < -5]
        breakouts_below_minus_five_sd_df.sort_values("breakout from SD range", inplace=True)
        report.extend(breakouts_below_minus_five_sd_df["ticker"].tolist())

        report.append("###BREAKOUTS BETWEEN -3SD AND -5SD")
        breakouts_between_minus_three_and_minus_five_sd_df = breakouts[
            (breakouts["breakout from SD range"] < -3) & (breakouts["breakout from SD range"] > -5)]
        breakouts_between_minus_three_and_minus_five_sd_df.sort_values("breakout from SD range", inplace=True)
        report.extend(breakouts_between_minus_three_and_minus_five_sd_df["ticker"].tolist())

        report.append("###BREAKOUTS BETWEEN -1SD AND -3SD")
        breakouts_between_minus_one_and_minus_three_sd_df = breakouts[
            (breakouts["breakout from SD range"] < -1) & (breakouts["breakout from SD range"] > -3)]
        breakouts_between_minus_one_and_minus_three_sd_df.sort_values("breakout from SD range", inplace=True)
        report.extend(breakouts_between_minus_one_and_minus_three_sd_df["ticker"].tolist())

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

    @staticmethod
    def count_items_without_rotation(trends: pd.DataFrame) -> int:
        trends_without_rotations = trends[~(trends["context"] == "Rotation") | (trends["context"] == "N/A")]
        return trends_without_rotations.shape[0]
