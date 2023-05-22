import logging

import pandas as pd

from trading_bots import constants


class EarlyReactionBotBybitHelper:
    BEFORE_ENTRY_IDS_JSON_PATH = "before_entry_ids.json"

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.instruments_info = pybit_client.get_instruments_info(category=constants.BYBIT_LINEAR_CATEGORY)["result"][
            "list"]

    def get_pending_orders(self) -> list:
        logging.info("Get pending orders")
        response = self.pybit_client.get_open_orders(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.debug("Pending orders response: {}".format(response))

        return response["result"]["list"]

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

    def cancel_pending_orders(self, symbol):
        logging.info("Cancel all pending orders")
        cancel_orders_response = self.pybit_client.cancel_all_orders(category=constants.BYBIT_LINEAR_CATEGORY,
                                                                     symbol=symbol)
        logging.debug("Cancel orders response: {}".format(cancel_orders_response))

    def remove_not_exists_ids(self, before_entry_ids: list) -> None:
        ids = []
        not_exists_ids = []

        for order in self.get_pending_orders():
            ids.append(order["orderId"])

        for before_entry_id in before_entry_ids:
            if before_entry_id not in ids:
                not_exists_ids.append(before_entry_id)

        for not_exists_id in not_exists_ids:
            before_entry_ids.remove(not_exists_id)

    def load_before_entry_ids_list(self):
        # TODO: Lucka https://stackoverflow.com/questions/49221429/how-to-load-a-list-from-a-json-file#49221604
        # with open('movies.txt') as f:
        #     content = f.read()
        #     if content:
        #         movies = json.loads(content)
        pass

    def save_before_entry_ids_list(self, before_entry_ids):
        # TODO: Lucka https://stackoverflow.com/questions/59327547/write-a-json-file-from-list#59328005
        # with open('data.json', 'w') as f:
        #     json.dump(data, f, indent=4)
        pass
