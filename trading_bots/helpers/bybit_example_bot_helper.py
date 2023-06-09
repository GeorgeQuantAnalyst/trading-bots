from statistics import mean

import logging
import sys

from trading_bots.constants import BYBIT_LINEAR_CATEGORY


class BybitExampleBotHelper:

    def __init__(self, exchange):
        self.exchange = exchange

    def get_btc_current_price(self) -> float:
        try:
            response = self.exchange.get_orderbook(
                category=BYBIT_LINEAR_CATEGORY,
                symbol="BTCUSDT"
            )
        except Exception as e:
            logging.error("Failed call method get_orderbook on exchange api: {}".format(str(e)))
            sys.exit(-1)

        logging.debug("Response get_orderbook: {}".format(response))

        result = response["result"]
        bid = float(result["b"][0][0])
        ask = float(result["a"][0][0])

        return mean([bid, ask])
