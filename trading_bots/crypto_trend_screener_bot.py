import logging
from datetime import datetime

from pybit.unified_trading import HTTP

from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper
from trading_bots.templates.trend_screener_bot import TrendScreenerBot


class CryptoTrendScreenerBot(TrendScreenerBot):

    def __init__(self, config: dict):
        self.pybit_client = HTTP()
        self.helper = CryptoTrendScreenerBotHelper(self.pybit_client)

        super().__init__(config, self.helper)

        self.ticker_prefix = "BYBIT:"
        self.ticker_suffix = ".P"

    def run(self):
        now = datetime.now().strftime("%Y%m%d")
        reports_folder = self.config["base"]["reportsFolder"]
        excel_path = "{}/CryptoTrendScreener_{}.xlsx".format(reports_folder, now)

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

        logging.info("Save result to excel file")

        self.save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends, excel_path)

        logging.info("Finished CryptoTrendScreenerBot")
