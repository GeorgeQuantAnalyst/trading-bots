import logging
from datetime import datetime

from alpha_vantage.foreignexchange import ForeignExchange
from trading_bots.templates.trend_screener_bot import TrendScreenerBot
from trading_bots.helpers.forex_trend_screener_bot_helper import ForexTrendScreenerBotHelper


class ForexTrendScreenerBot(TrendScreenerBot):

    def __init__(self, config: dict):
        self.config = config
        self.helper = ForexTrendScreenerBotHelper(ForeignExchange(key=config["alphaVantage"]["apiKey"]),
                                                  config["base"]["tickersFilePath"])
        super().__init__(config, self.helper)

        self.ticker_prefix = "FX_IDC:"

    def run(self) -> None:
        logging.info("Start ForexTrendScreenerBot")

        logging.info("Loading data")
        tickers = self.helper.get_available_tickers()

        ohlc_cache = self.helper.load_ohlc_cache(tickers)

        logging.info("Find intraday daily trends")
        intraday_daily_trends = self.find_intraday_daily_trends(tickers, ohlc_cache)

        logging.info("Find swing weekly trends")
        swing_weekly_trends = self.find_swing_weekly_trends(tickers, ohlc_cache)

        logging.info("Find swing monthly trends")
        swing_monthly_trends = self.find_swing_monthly_trends(tickers, ohlc_cache)

        logging.info("FInd position quarterly trends")
        position_quarterly_trends = self.find_position_quarterly_trends(tickers, ohlc_cache)

        logging.info("Save result to excel file")
        now = datetime.now().strftime("%Y%m%d")
        reports_folder = self.config["base"]["reportsFolder"]
        excel_path = "{}/ForexTrendScreener_{}.xlsx".format(reports_folder, now)
        self.save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends,
                                  position_quarterly_trends, excel_path)

        logging.info("Finished ForexTrendScreenerBot")
