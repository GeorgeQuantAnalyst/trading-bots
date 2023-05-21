import logging

import pandas as pd

from trading_bots import constants


class EarlyReactionBotBybitHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.instruments_info = pybit_client.get_instruments_info(category=constants.BYBIT_LINEAR_CATEGORY)["result"][
            "list"]

    def get_pending_orders(self) -> list:
        logging.info("Get pending orders")
        response = self.pybit_client.get_open_orders(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.debug("Pending orders response: {}".format(response))

        return response["result"]["list"]

    # def check_if_position_has_tp_and_sl(self, pending_orders) -> bool:
    #
    #     is_set_stop_loss = pending_orders["isSetStopLoss"] = pending_orders["stopLoss"] > 0
    #     is_set_take_profit = pending_orders["isSetTakeProfit"] = pending_orders["takeProfit"] > 0
    #
    #     if is_set_stop_loss is True & is_set_take_profit is True:
    #         return True

    def get_actual_price(self):
        # print("Start test_get_btc_current_price")
        #
        # response = self.pybit_client.get_orderbook(
        #     category=constants.BYBIT_LINEAR_CATEGORY,
        #     symbol="BTCUSDT"
        # )
        #
        # print("Response: {}".format(response))
        # result = response["result"]
        # bid = float(result["b"][0][0])
        # ask = float(result["a"][0][0])

        # return
        pass

    def get_last_bar(self, ticker: str, interval: int = 1) -> dict:
        response = self.pybit_client.get_kline(
            symbol=ticker,
            category=constants.BYBIT_LINEAR_CATEGORY,
            interval=interval,
            limit=1
        )

        last_bar = response["result"]["list"][0]
        return {
            "startTime": last_bar[0],
            "openPrice": last_bar[1],
            "highPrice": last_bar[2],
            "lowPrice": last_bar[3],
            "closePrice": last_bar[4],
            "volume": last_bar[5],
            "turnover": last_bar[6]
        }

    def get_before_entry_ids(self):
        pass

    def check_early_reaction(self):

        pass

    def cancel_trades_with_early_reaction(self, symbol):
        logging.info("Get pending orders")
        pending_orders = self.pybit_client.get_open_orders(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.debug("Pending response orders: {}".format(pending_orders))

        logging.info("Cancel all pending orders")
        cancel_orders_response = self.pybit_client.cancel_all_orders(category=constants.BYBIT_LINEAR_CATEGORY,
                                                                     symbol=symbol)
        logging.debug("Cancel orders response: {}".format(cancel_orders_response))

    # def remove_not_exists_ids(self):
    #     ids = []
    #     notExistsIds = []
    #
    #     for order in PendingOrders:
    #         ids.append(order["orderId"])
    #     for id in BeforeEntryIds:
    #         if (!ids in id)
    #             notExistsIds.append(id)
    #     for id in notExistsIds:
    #         BeforeEntryIds.Remove(id)
