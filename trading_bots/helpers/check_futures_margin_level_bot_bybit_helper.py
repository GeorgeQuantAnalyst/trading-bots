import logging
from datetime import datetime


class CheckFuturesMarginLevelBotBybitHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client

    def get_available_balance_on_futures_account(self) -> float:
        response = None  # TODO: @Lucka
        logging.info("Response: {}".format(response))
        return response["result"]["x"]  # TODO: @Lucka

    def is_open_positions(self) -> bool:
        response = None  # TODO: @Lucka
        logging.info("Response: {}".format(response))
        return len(response["result"]["list"]) > 0  # TODO: @Lucka

    def was_funding_account_today(self) -> bool:
        #TODO: @Jirka
        return False

    def get_last_position_close_date(self) -> datetime:
        response = None  # TODO: @Lucka
        logging.info("Response: {}".format(response))
        return response["result"]["x"]  # TODO: @Lucka

    def funding_futures_account(self, margin_level: float, available_balance: float):
        # TODO: @Jirka
        pass