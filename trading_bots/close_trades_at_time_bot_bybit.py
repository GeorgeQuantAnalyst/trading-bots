import datetime
import logging
import time

from trading_bots.helpers.close_trades_at_time_bot_bybit_helper import CloseTradesAtTimeBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class CloseTradesAtTimeBotBybit(BybitBot):
    _24_HOURS = 86400

    def __init__(self, config):
        super().__init__(config)
        self.helper = CloseTradesAtTimeBotBybitHelper(self.pybit_client)

    def run(self) -> None:
        logging.info("Start CloseTradesAtTimeBotBybit")

        hours = self.config["base"]["hours"]
        minutes = self.config["base"]["minutes"]

        if type(hours) is not int or type(minutes) is not int:
            raise Exception(
                "Config properties hours and minutes must be integer. [hours: {}, minutes: {}]".format(hours, minutes))

        if hours < 0 or minutes < 0:
            raise Exception(
                "Config properties hours and minutes must be greater than zero. [hours: {}, minutes: {}]".format(hours,
                                                                                                                 minutes))

        now = datetime.datetime.now()

        target_time = datetime.datetime(now.year, now.month, now.day, hours, minutes, 0)
        logging.info("Target time is: {}".format(target_time))

        time_diff = (target_time - now).total_seconds()

        # If the target time is before the current time, we add 24 hours for correct calculation
        if time_diff < 0:
            time_diff += self._24_HOURS

        time.sleep(time_diff)

        logging.info("Close all pending orders and open positions")
        self.helper.close_all_open_positions_and_pending_orders()

        logging.info("Finished CloseTradesAtTimeBotBybit")
