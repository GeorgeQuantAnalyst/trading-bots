import logging

from trading_bots.helpers.bybit_example_bot_helper import BybitExampleBotHelper
from trading_bots.templates.bybit_bot import BybitBot


class BybitExampleBot(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)

        self.helper = BybitExampleBotHelper(self.pybit_client)

    def run(self) -> None:
        logging.info("Start BybitExampleBot")

        logging.info("Get BTCUSDT current price from exchange")
        btc_current_price = self.helper.get_btc_current_price()
        logging.info(f"Btc current price is: {btc_current_price} USD")

        logging.info("Finished BybitExampleBot")
