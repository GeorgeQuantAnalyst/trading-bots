import logging
from trading_bots.helpers.early_reaction_bot_bybit_helper import EarlyReactionBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class EarlyReactionBotBybit(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = EarlyReactionBotBybitHelper(self.pybit_client)
        self.before_entry_ids = self.helper.load_before_entry_ids_list()
        logging.debug("Before entry ids: {}".format(self.before_entry_ids))

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

            last_closed_bar = self.helper.get_last_closed_bar(symbol)

            if take_profit == 0 or stop_loss == 0:
                logging.warning("Order {} does not have bracked orders (profit target and stop loss), "
                                "continue to next order.".format(order_id))
                continue

            before_entry_price = entry_price + ((entry_price - stop_loss) * percentage_before_entry)
            logging.info("Before entry price: {}".format(before_entry_price))

            logging.info("Last closed bar: {}".format(last_closed_bar))

            if order_id not in self.before_entry_ids:
                if (order_side == "Buy" and before_entry_price >= last_closed_bar["lowPrice"]) or (
                        order_side == "Sell" and before_entry_price <= last_closed_bar["highPrice"]):
                    logging.info("Price arrived before entry: [Order Id: {}, Before Entry Price: {}, "
                                 "Last Bar Low: {}, last Bar High: {}]".format(order_id, before_entry_price,
                                                                               last_closed_bar["lowPrice"],
                                                                               last_closed_bar["highPrice"]))
                    self.before_entry_ids.append(order_id)
            else:
                if (order_side == "Buy" and take_profit <= last_closed_bar["highPrice"]) or (
                        order_side == "Sell" and take_profit >= last_closed_bar["lowPrice"]):
                    logging.info(
                        "Price arrived to TakeProfit before reaching EntryPrice and make EarlyReaction, "
                        "pending order will be canceled.: [Order Id: {}, Take Profit: {}, Last Bar Low: {}, "
                        "Last Bar High: {}]"
                        .format(order_id, take_profit, last_closed_bar["lowPrice"], last_closed_bar["highPrice"]))

                    self.helper.cancel_pending_order(order_id, symbol)
                    self.before_entry_ids.remove(order_id)

        self.helper.remove_not_exists_ids(self.before_entry_ids, pending_orders)
        self.helper.save_before_entry_ids_list(self.before_entry_ids)
        logging.info("Finished EarlyReactionBotBybit")
