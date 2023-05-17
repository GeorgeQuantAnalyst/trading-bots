from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper
from trading_bots.templates.trend_screener_bot import TrendScreenerBot

import logging
from datetime import datetime

from pybit.unified_trading import HTTP


class CryptoTrendScreenerBot(TrendScreenerBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.pybit_client = HTTP()
        self.helper = CryptoTrendScreenerBotHelper(self.pybit_client)

    def run(self):
        now = datetime.now().strftime("%Y%m%d")
        excel_path = "report/CryptoTrendScreener_" + now + ".xlsx"

        logging.info("Start CryptoTrendScreenerBot")

        logging.info("Loading data")
        tickers = self.helper.get_available_tickers()
        ohlc_cache = self.helper.load_ohlc_cache(tickers)

        logging.info("Find intraday daily trends")
        intraday_daily_trends = self.find_intraday_daily_trends(tickers, ohlc_cache)

        logging.info("Find swing weekly trends")
        swing_weekly_trends = self.find_swing_weekly_trends(tickers, ohlc_cache)

        logging.info("Find swing monthly trends")
        swing_monthly_trends = self.find_swing_monthly_trends(tickers, ohlc_cache)

        ticker_names_intraday_d = "BYBIT:" + intraday_daily_trends["ticker"] + ".P"
        ticker_names_swing_w = "BYBIT:" + swing_weekly_trends["ticker"] + ".P"
        ticker_names_swing_m = "BYBIT:" + swing_monthly_trends["ticker"] + ".P"

        logging.info("Save result to excel file")
        super().save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends, excel_path, ticker_names_intraday_d, ticker_names_swing_w, ticker_names_swing_m)

        # TODO: @Lucka migrate crypto-trend-screener-job (https://github.com/GeorgeQuantAnalyst/crypto-trend-screener-job)

        logging.info("Finished CryptoTrendScreenerBot")




