import logging
import sys

from trading_bots import constants


class CloseTradesAtTimeBotBybitHelper:

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client

    def close_all_pending_orders_and_open_positions(self) -> None:
        logging.info("Get positions")
        try:
            response = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY,
                                                       settleCoin="USDT")
        except Exception as e:
            logging.error("Failed call method get_positions on pybit client: {}".format(str(e)))
            sys.exit(-1)

        logging.debug("Response get_positions: {}".format(response))

        logging.info("Cancel all open positions")
        for position in response["result"]["list"]:
            try:
                self.pybit_client.place_order(
                    category=constants.BYBIT_LINEAR_CATEGORY,
                    symbol=position["symbol"],
                    orderType="Market",
                    side="Sell" if position["side"] == "Buy" else "Buy",
                    qty=position["size"],
                    positionIdx=position["positionIdx"],
                    reduceOnly=True)
            except Exception as e:
                logging.error("Failed call method place_order on pybit client: {}".format(str(e)))
                sys.exit(-1)

        logging.info("Cancel all orders")
        try:
            self.pybit_client.cancel_all_orders(
                category="linear",
                settleCoin="USDT",
            )
        except Exception as e:
            logging.error("Failed call method cancel_all_orders on pybit client: {}".format(str(e)))
            sys.exit(-1)
