import logging
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

        if False and not self.helper.is_open_exchange():
            logging.info("The American stock exchange is currently not open, the bot will not continue working.")
            sys.exit(0)

        orders = self.helper.load_orders(self.trades_csv_path)
        self.check_early_reaction(orders)
        self.place_trade(orders)
        self.save_orders(orders)

        logging.info("Finished EquityLevelTraderCapital")

    def check_early_reaction(self, orders):
        logging.info("Start check early reaction step")

        logging.info("Start process orders")
        for order in orders:
            logging.info(f"Proces order with id: {order['id']}")
            if order["active"]:
                logging.info(f"Skip active order: [OrderId: {order['id']}]")
                continue

            if order['early_reaction']:
                logging.info(f"Skip early reaction order: [OrderId: {order['id']}]")
                continue

            if order["before_entry"]:
                logging.info(f"Check price reach profit target: [OrderId: {order['id']}]")
                if self.helper.check_price_reach_profit_target(order):
                    logging.info("Price reach profit target, order will be mark as early reaction")
                    order["early_reaction"] = True
                continue

            if self.helper.check_price_reach_before_entry_price(order):
                logging.info("Price reach before entry price, set attribute before_entry")
                order["before_entry"] = True

        logging.info("Finished check early reaction step")

    def place_trade(self, orders):
        logging.info("Start place trade step")

        if self.helper.is_open_positions():
            logging.info(
                "The application will not check the orders for entry, because there is an open trade on the exchange.")
            return

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
                logging.info("Price reach entry, order will be place on exchange.")
                self.helper.place_trade(order)
                order["active"] = True

        logging.info("Finished place trade step")

    def save_orders(self, orders):
        logging.info("Save orders to csv file")
        pd.DataFrame(orders).to_csv(self.trades_csv_path, index=False)
