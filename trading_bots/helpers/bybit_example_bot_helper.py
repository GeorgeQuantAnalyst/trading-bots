from statistics import mean

import logging

from trading_bots.constants import BYBIT_LINEAR_CATEGORY


class BybitExampleBotHelper:

    def __init__(self, exchange):
        self.exchange = exchange

    def get_btc_current_price(self):
        response = self.exchange.get_orderbook(
            category=BYBIT_LINEAR_CATEGORY,
            symbol="BTCUSDT"
        )

        logging.debug("Response get_orderbook: {}".format(response))

        result = response["result"]
        bid = float(result["b"][0][0])
        ask = float(result["a"][0][0])

        return mean([bid, ask])
