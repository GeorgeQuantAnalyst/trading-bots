import logging

import json

from trading_bots import constants


class EarlyReactionBotBybitHelper:

    def __init__(self, pybit_client, before_entry_ids_json_path):
        self.pybit_client = pybit_client
        self.instruments_info = pybit_client.get_instruments_info(category=constants.BYBIT_LINEAR_CATEGORY)["result"][
            "list"]
        self.before_entry_ids_json_path = before_entry_ids_json_path

    def get_pending_orders(self) -> list:
        logging.info("Get pending orders")
        response = self.pybit_client.get_open_orders(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.debug("Response get_open_orders: {}".format(response))

        return response["result"]["list"]

    def get_last_closed_bar(self, ticker: str, interval: int = 1) -> dict:
        response = self.pybit_client.get_kline(
            symbol=ticker,
            category=constants.BYBIT_LINEAR_CATEGORY,
            interval=interval,
            limit=2
        )

        logging.debug("Response get_kline: {}".format(response))

        last_bar = response["result"]["list"][1]

        return {
            "startTime": float(last_bar[0]),
            "openPrice": float(last_bar[1]),
            "highPrice": float(last_bar[2]),
            "lowPrice": float(last_bar[3]),
            "closePrice": float(last_bar[4]),
            "volume": float(last_bar[5]),
            "turnover": float(last_bar[6])
        }

    def cancel_pending_order(self, order_id, symbol):
        logging.info("Cancel pending order with early reaction")
        response = self.pybit_client.cancel_order(category=constants.BYBIT_LINEAR_CATEGORY,
                                                                symbol=symbol, orderId=order_id)
        logging.debug("Response cancel_order: {}".format(response))

    def remove_not_exists_ids(self, before_entry_ids: list, pending_orders: list) -> None:
        ids = []
        not_exists_ids = []

        for order in pending_orders:
            ids.append(order["orderId"])

        for before_entry_id in before_entry_ids:
            if before_entry_id not in ids:
                logging.info("Start removing not existing ids")
                not_exists_ids.append(before_entry_id)

        for not_exists_id in not_exists_ids:
            before_entry_ids.remove(not_exists_id)
            logging.info("Removing not existing id: {}".format(not_exists_id))

    def load_before_entry_ids_list(self):
        with open(self.before_entry_ids_json_path) as f:
            content = f.read()
            if content:
                return json.loads(content)

    def save_before_entry_ids_list(self, before_entry_ids):
        with open(self.before_entry_ids_json_path, 'w') as f:
            json.dump(before_entry_ids, f, indent=4)
