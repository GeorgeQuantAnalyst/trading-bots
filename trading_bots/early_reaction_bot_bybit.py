import logging
from trading_bots.helpers.early_reaction_bot_bybit_helper import EarlyReactionBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class EarlyReactionBotBybit(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = EarlyReactionBotBybitHelper(self.pybit_client)
        self.before_entry_ids = []

    def run(self):
        logging.info("Start EarlyReactionBotBybit")

        pending_orders = self.helper.get_pending_orders()
        logging.info("Count pending orders: {}".format(len(pending_orders)))
        logging.debug("Pending orders: {}".format(pending_orders))

        for order in pending_orders:
            logging.info("Process order {}".format(order["orderId"]))

            take_profit = float(order["takeProfit"])
            stop_loss = float(order["stopLoss"])
            entry_price = float(order["price"])
            percentage_before_entry = self.config["base"]["percentageBeforeEntry"]
            symbol = order["symbol"]
            order_side = order["side"]
            order_id = order["orderId"]

            if take_profit == 0 or stop_loss == 0:
                logging.warning("Order {} does not have bracked orders (profit target and stop loss), "
                                "continue to next order.".format(order_id))

            before_entry_price = entry_price + ((entry_price - stop_loss) * percentage_before_entry)
            logging.info("Before entry price: {}".format(before_entry_price))

            last_bar = self.helper.get_last_bar(symbol)
            logging.info("Last bar: {}".format(last_bar))

            if order_id not in self.before_entry_ids:
                if (order_side == "Buy" and before_entry_price >= last_bar["lowPrice"]) or (
                        order_side == "Sell" and before_entry_price <= last_bar["highPrice"]):
                    logging.info("Price arrived before entry: [Order Id: {}, Before Entry Price: {},"
                                 "Last Bar Low: {}, last Bar High: {}]".format(order_id, before_entry_price,
                                                                               last_bar["lowPrice"],
                                                                               last_bar["highPrice"]))
                    self.before_entry_ids.append(order_id)
            else:
                if (order_side == "Buy" and take_profit <= last_bar["highPrice"]) or (
                        order_side == "Sell" and take_profit >= last_bar["lowPrice"]):
                    logging.info(
                        "Price arrived to TakeProfit price early after arrived BeforeEntryPrice,"
                        "pending order will be cancel. : [Order Id: {}, Take Profit: {}, Last Bar Low: {},"
                        "Last Bar High: {}]"
                        .format(order_id, take_profit, last_bar["lowPrice"], last_bar["highPrice"]))

                    self.helper.cancel_trades_with_early_reaction(symbol)

                    self.before_entry_ids.remove(order_id)

                logging.info("Finished EarlyReactionBotBybit")
