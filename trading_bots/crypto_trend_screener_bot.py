import logging

import pandas as pd
from pybit.unified_trading import HTTP

from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper
from trading_bots.templates.bot import Bot
from trading_bots.trading_math import convert_ohlc, calculate_context


class CryptoTrendScreenerBot(Bot):
    SEPARATOR = "------------------------"

    def __init__(self, config: dict):
        super().__init__(config)
        self.pybit_client = HTTP()
        self.helper = CryptoTrendScreenerBotHelper(self.pybit_client)

    def run(self) -> None:
        logging.info("Start CryptoTrendScreenerBot")

        tickers = self.loading_tickers()
        trends = self.find_trends(tickers)
        self.create_tw_trends_report(trends)

        logging.info("Finished CryptoTrendScreenerBot")

    def loading_tickers(self) -> dict[str, list]:
        logging.info(self.SEPARATOR)
        logging.info("Loading tickers")
        logging.info(self.SEPARATOR)

        tickers_pybit_futures = self.helper.get_pybit_futures_tickers()

        return {
            "tickers_pybit_futures": tickers_pybit_futures
        }

    def find_trends(self, tickers: dict[str, list]) -> dict[str, pd.DataFrame]:
        logging.info(self.SEPARATOR)
        logging.info("Find trends")
        logging.info(self.SEPARATOR)

        logging.info("Find trends in Bybit futures tickers")
        bybit_futures_weekly_trends = []
        bybit_futures_monthly_trends = []
        bybit_futures_quarterly_trends = []
        bybit_futures_yearly_trends = []

        for ticker in tickers["tickers_pybit_futures"]:
            logging.info(f"Process {ticker} ticker")

            weekly_ohlc = self.helper.get_ohlc(ticker, "W")
            monthly_ohlc = self.helper.get_ohlc(ticker, "M")
            quarterly_ohlc = convert_ohlc(monthly_ohlc, "Q")
            yearly_ohlc = convert_ohlc(monthly_ohlc, "Y")

            logging.debug(f"Weekly ohlc (last 10 candles): \n {weekly_ohlc}")
            logging.debug(f"Monthly ohlc (last 10 candles): \n {monthly_ohlc}")
            logging.debug(f"Quarterly ohlc (last 10 candles): \n {quarterly_ohlc}")
            logging.debug(f"Yearly ohlc (last 10 candles): \n {yearly_ohlc}")

            weekly_context = calculate_context(weekly_ohlc)
            monthly_context = calculate_context(monthly_ohlc)
            quarterly_context = calculate_context(quarterly_ohlc)
            yearly_context = calculate_context(yearly_ohlc)

            logging.debug(f"Weekly context: {weekly_context}")
            logging.debug(f"Monthly context: {monthly_context}")
            logging.debug(f"Quarterly context: {quarterly_context}")
            logging.debug(f"Yearly context: {yearly_context}")

            bybit_futures_weekly_trends.append({
                "ticker": ticker,
                "context": weekly_context
            })

            bybit_futures_monthly_trends.append({
                "ticker": ticker,
                "context": monthly_context
            })

            bybit_futures_quarterly_trends.append({
                "ticker": ticker,
                "context": quarterly_context
            })

            bybit_futures_yearly_trends.append({
                "ticker": ticker,
                "context": yearly_context
            })

        return {
            "bybit_futures_weekly_trends": pd.DataFrame(bybit_futures_weekly_trends),
            "bybit_futures_monthly_trends": pd.DataFrame(bybit_futures_monthly_trends),
            "bybit_futures_quarterly_trends": pd.DataFrame(bybit_futures_quarterly_trends),
            "bybit_futures_yearly_trends": pd.DataFrame(bybit_futures_yearly_trends)
        }

    def create_tw_trends_report(self, trends):
        logging.info(self.SEPARATOR)
        logging.info("Create TradingView trends report")
        logging.info(self.SEPARATOR)

        self.create_and_save_bybit_futures_trend_reports(trends, "weekly", "W")
        self.create_and_save_bybit_futures_trend_reports(trends, "monthly", "M")
        self.create_and_save_bybit_futures_trend_reports(trends, "quarterly", "3M")
        self.create_and_save_bybit_futures_trend_reports(trends, "yearly", "Y")

    def create_and_save_bybit_futures_trend_reports(self, trends, name_of_timeframe, time_frame):
        reports_folder = self.config["base"]["reportsFolder"]
        trends_timeframe_id = "bybit_futures_{}_trends".format(name_of_timeframe)

        logging.info(f"Create Bybit futures {time_frame} trends")
        bybit_futures_trends = trends[trends_timeframe_id]
        bybit_futures_trends["ticker"] = "BYBIT:" + bybit_futures_trends["ticker"] + ".P"
        bybit_futures_trends_path = "{}/Bybit futures {} trends.txt".format(reports_folder, time_frame)
        bybit_futures_trends_report = self.helper.create_tw_report(bybit_futures_trends)
        self.helper.save_tw_report(bybit_futures_trends_report, bybit_futures_trends_path)
