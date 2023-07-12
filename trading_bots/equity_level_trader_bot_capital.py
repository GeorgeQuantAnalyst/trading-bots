import logging
import csv
import sys

import pandas as pd

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper
from trading_bots.templates.bot import Bot


class EquityLevelTraderBotCapital(Bot):

    def __init__(self, config: dict):
        self.exchange = None  # TODO: init client
        self.helper = EquityLevelTraderBotCapitalHelper(config)
        self.trades_csv_path = config["base"]["ordersCsvPath"]

    def run(self):
        logging.info("Start EquityLevelTraderCapital")

        if not self.helper.is_open_exchange():
            logging.info("The American stock exchange is currently not open, the bot will not continue working.")
            sys.exit(0)

        if not self.helper.is_open_positions():
            logging.info("the application will not check the orders for entry, because there is an open trade on the exchange.")

        logging.info("Loading orders from database")
        orders = self.helper.load_orders(self.trades_csv_path)
        logging.debug(f"Loaded orders: \n {orders}")

        for order in orders:
            logging.info(f"Process order with id: {order['id']}")

            if order["active"]:
                logging.info(f"Skip active order: [OrderId: {order['id']}]")
                continue

            if order['early_reaction']:
                logging.info(f"Skip early reaction order: [OrderId: {order['id']}]")
                continue

            if self.helper.is_price_arrive_to_order(order):
                self.helper.place_trade(order)

        # for index, order in orders.iterrows():
        #     order["active"] = True
        #
        #     logging.info(f"Orders: {order}")
        #
        # orders_filtered = orders[(orders["ticker"].notnull())
        #                          & (orders["entry_price"].notnull())
        #                          & (orders["stop_loss"].notnull())
        #                          & ~(orders["early_reaction"])
        #                          & ~(orders["active"])]
        #
        # logging.debug(f"Orders filtered: \n {orders_filtered}")

        # for index, order in orders.iterrows():
        #     logging.info(f"Start process order: {order['id']}")
        #
        #     if self.helper.check_early_reaction(order):
        #         logging.info("Early reaction")
        #         order["early_reaction"] = True
        #         continue
        #
        #     if self.helper.is_price_arrive_to_order(order):
        #         logging.info("Price arrive on entry price order")
        #
        #         if self.helper.is_earnings_next_days(ticker=order["ticker"], count_days=10):
        #             logging.warning(
        #                 "The trade will not be opened because the announcement of the result is approaching in the next 10 days.")
        #             continue
        #
        #         if self.helper.was_earnings_yesterday(ticker=order["tikcer"]):
        #             logging.warning(
        #                 "The trade will not be opened because the announcement of the result was yesterday.")
        #             continue
        #
        #         if self.helper.is_open_positions():
        #             logging.warning("The trade will not be opened because already open positions")
        #
        #         logging.info("Start place trade on exchange")
        #         self.helper.place_trade(order)
        #     logging.info(f"Finished process order: {order['id']}")
        #
        logging.info("Save orders to database")
        pd.DataFrame(orders).to_csv(self.trades_csv_path, index=False)

        logging.info("Finished EquityLevelTraderCapital")
