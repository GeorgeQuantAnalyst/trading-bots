import logging

import pandas as pd

from trading_bots import constants
from trading_bots.templates.trend_screener_bot_helper import TrendScreenerBotHelper


class CryptoTrendScreenerBotHelper(TrendScreenerBotHelper):

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client
        self.category = constants.BYBIT_LINEAR_CATEGORY

    def get_available_tickers(self) -> list:
        response = self.pybit_client.get_instruments_info(category=self.category)

        logging.debug("Response get_instruments_info: {}".format(response))

        return [x["symbol"] for x in
                response["result"]["list"] if "USDT" in x["symbol"]]

    def get_ohlc(self, ticker: str, time_frame: str) -> pd.DataFrame:
        response = self.pybit_client.get_kline(category=self.category, symbol=ticker, interval=time_frame)
        ohlc = pd.DataFrame(response["result"]["list"],
                            columns=["startTime", "open", "high", "low", "close", "volume", "turnover"])

        logging.debug("Response get_kline: {}".format(response))

        ohlc["open"] = pd.to_numeric(ohlc["open"])
        ohlc["high"] = pd.to_numeric(ohlc["high"])
        ohlc["low"] = pd.to_numeric(ohlc["low"])
        ohlc["close"] = pd.to_numeric(ohlc["close"])
        ohlc["volume"] = pd.to_numeric(ohlc["volume"])
        ohlc["turnover"] = pd.to_numeric(ohlc["turnover"])
        ohlc["startTime"] = pd.to_numeric(ohlc["startTime"])
        ohlc['startTime'] = pd.to_datetime(ohlc["startTime"], unit='ms')
        return ohlc
