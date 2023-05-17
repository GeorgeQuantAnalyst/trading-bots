from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper
from trading_bots.templates.trend_screener_bot import TrendScreenerBot

import logging


class CryptoTrendScreenerBot(TrendScreenerBot):

    def __init__(self, config: dict):
        super().__init__(config)
        exchange = None
        self.helper = CryptoTrendScreenerBotHelper(exchange)
        pass

    def run(self):
        logging.info("Start CryptoTrendScreenerBot")

        # TODO: @Lucka migrate crypto-trend-screener-job (https://github.com/GeorgeQuantAnalyst/crypto-trend-screener-job)

        logging.info("Finished CryptoTrendScreenerBot")


