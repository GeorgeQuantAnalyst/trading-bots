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
        self.daily_volume_in_usd_above_filter_swing = self.config["base"]["dailyVolumeInUsdAboveFilterSwing"]
        self.daily_volume_in_usd_above_filter_position = self.config["base"]["dailyVolumeInUsdAboveFilterPosition"]

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
        bybit_futures_quarterly_trends = []
        bybit_futures_yearly_trends = []
        for ticker in tickers["tickers_pybit_futures"]:
            logging.info("Process {} ticker".format(ticker))

            weekly_ohlc = self.helper.get_ohlc(ticker, "W")
            monthly_ohlc = self.helper.get_ohlc(ticker, "M")
            quarterly_ohlc = convert_ohlc(monthly_ohlc, "Q")
            yearly_ohlc = convert_ohlc(monthly_ohlc, "Y")

            logging.debug("Weekly ohlc (last 10 candles): \n {}".format(weekly_ohlc))
            logging.debug("Monthly ohlc (last 10 candles): \n {}".format(monthly_ohlc))
            logging.debug("Quarterly ohlc (last 10 candles): \n {}".format(quarterly_ohlc))
            logging.debug("Yearly ohlc (last 10 candles): \n {}".format(yearly_ohlc))

            # TODO: @Lucka compute W and M context
            quarterly_context = calculate_context(quarterly_ohlc)
            yearly_context = calculate_context(yearly_ohlc)

            logging.debug("Quarterly context: {}".format(quarterly_context))
            logging.debug("Yearly context: {}".format(yearly_context))

            bybit_futures_quarterly_trends.append({
                "ticker": ticker,
                "context": quarterly_context
            })

            bybit_futures_yearly_trends.append({
                "ticker": ticker,
                "context": yearly_context
            })

        return {
            "bybit_futures_quarterly_trends": pd.DataFrame(bybit_futures_quarterly_trends),
            "bybit_futures_yearly_trends": pd.DataFrame(bybit_futures_yearly_trends)
        }

    def create_tw_trends_report(self, trends):
        logging.info(self.SEPARATOR)
        logging.info("Create TradingView trends report")
        logging.info(self.SEPARATOR)

        reports_folder = self.config["base"]["reportsFolder"]

        # TODO: @Lucka create tw trends report for W and M trends

        logging.info("Create Bybit futures 3M trends")
        bybit_futures_quarterly_trends = trends["bybit_futures_quarterly_trends"]
        bybit_futures_quarterly_trends["ticker"] = "BYBIT:" + bybit_futures_quarterly_trends["ticker"] + ".P"
        bybit_futures_quarterly_trends_path = "{}/Bybit futures 3M trends.txt".format(reports_folder)
        bybit_futures_quarterly_trends_report = self.helper.create_tw_report(bybit_futures_quarterly_trends)
        self.helper.save_tw_report(bybit_futures_quarterly_trends_report, bybit_futures_quarterly_trends_path)

        logging.info("Create Bybit futures Y trends")
        bybit_futures_yearly_trends = trends["bybit_futures_yearly_trends"]
        bybit_futures_yearly_trends["ticker"] = "BYBIT:" + bybit_futures_yearly_trends["ticker"] + ".P"
        bybit_futures_yearly_trends_path = "{}/Bybit futures Y trends.txt".format(reports_folder)
        bybit_futures_yearly_trends_report = self.helper.create_tw_report(bybit_futures_yearly_trends)
        self.helper.save_tw_report(bybit_futures_yearly_trends_report, bybit_futures_yearly_trends_path)
