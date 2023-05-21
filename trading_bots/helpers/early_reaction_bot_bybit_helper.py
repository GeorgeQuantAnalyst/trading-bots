import pandas as pd

from trading_bots import constants


class EarlyReactionBotBybitHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.instruments_info = pybit_client.get_instruments_info(category=constants.BYBIT_LINEAR_CATEGORY)["result"][
            "list"]

    def get_open_positions(self) -> list:
        response = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        positions = pd.DataFrame(response["result"]["list"])
        return positions

    def check_if_position_has_tp_and_sl(self) -> bool:
        pass

    def get_actual_price(self):
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

    def remove_trades_with_early_reaction(self):
        pass

    def remove_not_existing_ids(self):
        pass
