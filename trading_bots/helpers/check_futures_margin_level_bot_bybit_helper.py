import logging
from datetime import datetime

from trading_bots import constants


class CheckFuturesMarginLevelBotBybitHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client

    def get_available_balance_on_futures_account(self) -> float:
        response = self.pybit_client.get_wallet_balance(
            accountType="CONTRACT",
            coin="USDT")
        logging.info("Response: {}".format(response))

        total_balance = float(response["result"]["list"][0]["coin"][0]["walletBalance"])
        free_balance = float(response["result"]["list"][0]["coin"][0]["availableToWithdraw"])

        logging.info(
            "Total balance: {} USDT, Available balance to withdraw: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        return total_balance

    def is_open_positions(self) -> bool:
        response = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.info("Response: {}".format(response))
        return len(response["result"]["list"]) > 0

    def was_funding_account_today(self) -> bool:
        #TODO: @Jirka
        return False

    def get_last_position_close_date(self) -> datetime:
        response = self.pybit_client.get_closed_pnl(category=constants.BYBIT_LINEAR_CATEGORY, limit=2)
        logging.info("Response: {}".format(response))
        return response["result"]["list"][0]["createdTime"]

    def funding_futures_account(self, margin_level: float, available_balance: float):
        # TODO: @Jirka
        pass