import logging

import pandas as pd

from trading_bots import constants


class PlaceTrailingStopsBotBybitHelper:
    DEFAULT_PRICE_SCALE = 2

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.instruments_info = pybit_client.get_instruments_info(category=constants.BYBIT_LINEAR_CATEGORY)["result"][
            "list"]

    def get_open_positions(self) -> pd.DataFrame:
        response = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        positions = pd.DataFrame(response["result"]["list"])

        logging.debug("Response get_positions: {}".format(response))

        return positions

    def calculate_trailing_stops(self, positions: pd.DataFrame) -> None:
        positions["avgPrice"] = pd.to_numeric(positions["avgPrice"])
        positions["stopLoss"] = pd.to_numeric(positions["stopLoss"])

        positions["priceScale"] = positions.apply(lambda row: self._get_price_scale(row["symbol"]), axis=1)
        positions["isSetStopLoss"] = positions["stopLoss"] > 0
        positions["computeTrailingStop"] = abs(positions["avgPrice"] - positions["stopLoss"])
        positions["computeTrailingStop"] = positions.apply(
            lambda x: round(x["computeTrailingStop"], x["priceScale"]), axis=1)

    def place_trailing_stops(self, positions: pd.DataFrame) -> None:
        for index, position in positions.iterrows():
            if self._is_active_trailing_stop(position):
                logging.info("The Position {}-{} position already has a trailing stop.".format(
                    position["symbol"], position["side"]))
                continue

            if position["isSetStopLoss"] == False:
                logging.error(
                    "The Position {}-{} does not have a hard stop loss set. Job cannot set traling stop loss.".format(
                        position["symbol"], position["side"]))
                continue

            try:
                self.pybit_client.set_trading_stop(
                    category=constants.BYBIT_LINEAR_CATEGORY,
                    symbol=position["symbol"],
                    side=position["side"],
                    trailing_stop=str(position["computeTrailingStop"]),
                    position_idx=position["positionIdx"]
                )
                logging.info("Successfull place trailing stop for position {}-{}".format(
                    position["symbol"], position["side"]))
            except Exception as e:
                logging.exception("Problem with place trailing stop for {}-{} on exchange Bybit".format(
                    position["symbol"], position["side"]))

    def _get_price_scale(self, ticker: str) -> float:
        price_scale = [x["priceScale"] for x in self.instruments_info if x["symbol"] == ticker]
        return int(price_scale[0]) if any(price_scale) else self.DEFAULT_PRICE_SCALE

    @staticmethod
    def _is_active_trailing_stop(position: pd.Series) -> bool:
        return float(position["trailingStop"]) > 0
