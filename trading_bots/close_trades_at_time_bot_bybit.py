import logging

from trading_bots.helpers.close_trades_at_time_bot_bybit_helper import CloseTradesAtTimeBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class CloseTradesAtTimeBotBybit(BybitBot):

    def __init__(self, config):
        super().__init__(config)
        self.helper = CloseTradesAtTimeBotBybitHelper(self.pybit_client)

    def run(self) -> None:
        logging.info("Start CloseTradesAtTimeBotBybit")

        logging.info("Close all pending orders and open positions")
        self.helper.close_all_open_positions_and_pending_orders()

        logging.info("Finished CloseTradesAtTimeBotBybit")
