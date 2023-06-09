import logging

from trading_bots.helpers.place_trailing_stops_bot_bybit_helper import PlaceTrailingStopsBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class PlaceTrailingStopsBotBybit(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = PlaceTrailingStopsBotBybitHelper(self.pybit_client)

    def run(self) -> None:
        logging.info("Start PlaceTrailingStopsBotBybit")

        open_positions = self.helper.get_open_positions()
        logging.info(f"Count open positions: {open_positions.shape[0]}")
        logging.debug(f"Open positions: {open_positions.to_json()}")

        if not open_positions.empty:
            logging.info("Place trailing stops")
            self.helper.calculate_trailing_stops(open_positions)
            logging.debug(f"Prepared open positions: {open_positions.to_json()}")
            self.helper.place_trailing_stops(open_positions)

        logging.info("Finished PlaceTrailingStopsBotBybit")
