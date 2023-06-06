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

        self.daily_volume_in_usd_above_filter_intraday = self.config["base"]["dailyVolumeInUsdAboveFilterIntraday"]
        self.daily_volume_in_usd_above_filter_swing = self.config["base"]["dailyVolumeInUsdAboveFilterSwing"]
        self.daily_volume_in_usd_above_filter_position = self.config["base"]["dailyVolumeInUsdAboveFilterPosition"]

    def run(self) -> None:
        logging.info("Start CryptoTrendScreenerBot")

        logging.info("Loading data")
        tickers = self.helper.get_available_tickers()
        ohlc_cache = self.helper.load_ohlc_cache(tickers)

        tickers_intraday = self.helper.filter_tickers(tickers,
                                                      self.daily_volume_in_usd_above_filter_intraday,
                                                      ohlc_cache)
        tickers_swing = self.helper.filter_tickers(tickers,
                                                   self.daily_volume_in_usd_above_filter_swing,
                                                   ohlc_cache)
        tickers_position = self.helper.filter_tickers(tickers,
                                                      self.daily_volume_in_usd_above_filter_position,
                                                      ohlc_cache)

        logging.debug("Tickers intraday: {}".format(tickers_intraday))
        logging.debug("Tickers swing: {}".format(tickers_swing))
        logging.debug("Tickers position: {}".format(tickers_position))

        logging.info("Find intraday daily trends")
        intraday_daily_trends = self.find_intraday_daily_trends(tickers_intraday, ohlc_cache)

        logging.info("Find swing weekly trends")
        swing_weekly_trends = self.find_swing_weekly_trends(tickers_swing, ohlc_cache)

        logging.info("Find swing monthly trends")
        swing_monthly_trends = self.find_swing_monthly_trends(tickers_swing, ohlc_cache)

        logging.info("Find position quarterly trends")
        position_quarterly_trends = self.find_position_quarterly_trends(tickers_position, ohlc_cache)

        logging.info("Save result to excel file")
        now = datetime.now().strftime("%Y%m%d")
        reports_folder = self.config["base"]["reportsFolder"]
        excel_path = "{}/CryptoTrendScreener_{}.xlsx".format(reports_folder, now)
        self.save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends, excel_path) #TODO add quarterly Lucka

        logging.info("Create TradingView trends report")
        swing_weekly_trends_report_path = "{}/CryptoSwingWeeklyTrends_{}.txt".format(reports_folder, now)
        swing_weekly_trends_report = self.helper.create_tw_report_weekly_trends(swing_weekly_trends)
        self.helper.save_tw_report(swing_weekly_trends_report, swing_weekly_trends_report_path)

        # TODO: @Lucka M, 3M trends for TW report

        logging.info("Finished CryptoTrendScreenerBot")
