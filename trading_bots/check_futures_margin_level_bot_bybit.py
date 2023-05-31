import logging
from datetime import datetime

from trading_bots.helpers.check_futures_margin_level_bot_bybit_helper import CheckFuturesMarginLevelBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class CheckFuturesMarginLevelBotBybit(BybitBot):
    ONE_MINUTE_SECONDS = 60

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = CheckFuturesMarginLevelBotBybitHelper(self.pybit_client, config["base"]["fundingDatesJsonPath"])
        self.margin_level = config["base"]["marginLevel"]
        self.funding_interval_in_minutes = config["base"]["fundingIntervalInMinutes"]

    def run(self):
        logging.info("Start CheckFuturesMarginLevelBotBybit")

        available_balance = self.helper.get_available_balance_on_futures_account()

        if available_balance < self.margin_level:
            msg = "Available balance on futures account is under margin level. [availableBalance: {}, marginLevel: {}]"
            logging.info(msg.format(available_balance, self.margin_level))
            self.funding_futures_account(available_balance)
        else:
            msg = "Available balance on futures account is OK. [availableBalance: {}, marginLevel: {}]"
            logging.info(msg.format(available_balance, self.margin_level))

        logging.info("Finished CheckFuturesMarginLevelBotBybit")

    def funding_futures_account(self, available_balance: float) -> None:
        if self.helper.is_open_positions():
            logging.info(
                "Actually is open position[s] on futures account, Funding will only take place after the open positions was closed.")
            return

        if self.helper.was_funding_account_today():
            logging.warning(
                "The futures account has already been funded, max allowed funding is only one time per day.")
            return

        last_trade_close_date = self.helper.get_last_position_close_date()
        logging.info("LastTradeCloseDate: {}".format(last_trade_close_date))
        minutes_after_last_trade = (datetime.now() - last_trade_close_date).seconds / self.ONE_MINUTE_SECONDS
        if minutes_after_last_trade < self.funding_interval_in_minutes:
            msg = "The futures account was funding after defined funding interval. [fundingIntervalInMinutes: {}, minutesAfterLastTrade: {}]"
            logging.info(msg.format(self.funding_interval_in_minutes, round(minutes_after_last_trade, 2)))
            return

        logging.info("Funding futures account to margin level")
        self.helper.funding_futures_account(self.margin_level, available_balance)
