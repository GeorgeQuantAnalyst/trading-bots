import logging

from pybit.unified_trading import HTTP

from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper
from trading_bots.templates.trend_screener_bot import TrendScreenerBot


class CryptoTrendScreenerBot(TrendScreenerBot):

    def __init__(self, config: dict):
        self.pybit_client = HTTP()
        self.helper = CryptoTrendScreenerBotHelper(self.pybit_client)
        super().__init__(config, self.helper)

        self.daily_volume_in_usd_above_filter_swing = self.config["base"]["dailyVolumeInUsdAboveFilterSwing"]
        self.daily_volume_in_usd_above_filter_position = self.config["base"]["dailyVolumeInUsdAboveFilterPosition"]

    def run(self) -> None:
        logging.info("Start CryptoTrendScreenerBot")

        logging.info("Loading data")
        logging.info("Loading tickers")
        tickers = self.helper.get_available_tickers()
        logging.info("Loading OHLC cache")
        ohlc_cache = self.helper.load_ohlc_cache(tickers)

        tickers_swing = self.helper.filter_tickers(tickers,
                                                   self.daily_volume_in_usd_above_filter_swing,
                                                   ohlc_cache)
        tickers_position = self.helper.filter_tickers(tickers,
                                                      self.daily_volume_in_usd_above_filter_position,
                                                      ohlc_cache)

        logging.debug("Swing filter - above {} daily volume in usd is {} tickers.".format(
            self.daily_volume_in_usd_above_filter_swing, len(tickers_swing)))
        logging.debug("Position filter - above {} daily volume in usd is {} tickers.".format(
            self.daily_volume_in_usd_above_filter_position, len(tickers_position)))

        logging.info("Find swing weekly trends")
        swing_weekly_trends = self.find_swing_weekly_trends(tickers_swing, ohlc_cache)

        logging.info("Find swing monthly trends")
        swing_monthly_trends = self.find_swing_monthly_trends(tickers_swing, ohlc_cache)

        logging.info("Find position quarterly trends")
        position_quarterly_trends = self.find_position_quarterly_trends(tickers_position, ohlc_cache)

        logging.info("Create TradingView trends report")
        reports_folder = self.config["base"]["reportsFolder"]
        self.helper.create_tw_trends_report(swing_weekly_trends, swing_monthly_trends, position_quarterly_trends,
                                            reports_folder)

        logging.info("Finished CryptoTrendScreenerBot")
