import logging
import csv
import sys

import pandas as pd

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper
from trading_bots.templates.bot import Bot


class EquityLevelTraderBotCapital(Bot):

    def __init__(self, config: dict):
        self.helper = EquityLevelTraderBotCapitalHelper(config)
        self.trades_csv_path = config["base"]["ordersCsvPath"]

    def run(self):
        logging.info("Start EquityLevelTraderCapital")

        if not self.helper.is_open_exchange():
            logging.info("The American stock exchange is currently not open, the bot will not continue working.")
            sys.exit(0)

        if not self.helper.is_open_positions():
            logging.info(
                "the application will not check the orders for entry, because there is an open trade on the exchange.")

        logging.info("Loading orders from database")
        orders = self.helper.load_orders(self.trades_csv_path)
        logging.debug(f"Loaded orders: \n {orders}")

        logging.info("Start process orders")
        for order in orders:
            logging.info(f"Process order with id: {order['id']}")
            ticker = order["ticker"]

            if order["active"]:
                logging.info(f"Skip active order: [OrderId: {order['id']}]")
                continue

            if order['early_reaction']:
                logging.info(f"Skip early reaction order: [OrderId: {order['id']}]")
                continue

            if self.helper.was_yesterday_earnings(ticker):
                logging.info(f"Skip ticker {ticker}, because yesterday was earnings. [OrderId: {order['id']}]")
                continue

            if self.helper.is_earnings_next_days(ticker, 10):
                logging.info(
                    f"Skip ticker {ticker}, because equity has earning in next 10 days. [OrderId: {order['id']}]")
                continue

            if self.helper.has_price_reached_entry(order):
                self.helper.place_trade(order)

        logging.info("Finished EquityLevelTraderCapital")
