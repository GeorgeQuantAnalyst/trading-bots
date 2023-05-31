import logging
import time

import pandas as pd

from trading_bots.templates.trend_screener_bot_helper import TrendScreenerBotHelper


class ForexTrendScreenerBotHelper(TrendScreenerBotHelper):
    API_CALL_LIMIT_EXCEPTION_MSG = "Our standard API call frequency is 5 calls per minute and 500 calls per day."
    API_CALL_LIMIT_WARNING_MSG = "The request per minute limit has just been exceeded, the application will wait a minute before retrying the data download."
    API_CALL_LIMIT_SLEEP_INTERVAL_SECONDS = 60

    def __init__(self, foreign_exchange, tickers_csv_path):
        self.foreign_exchange = foreign_exchange
        self.tickers_csv_path = tickers_csv_path

    def get_available_tickers(self) -> list:
        df = pd.read_csv(self.tickers_csv_path)
        return df["Ticker"].tolist()

    def get_ohlc(self, ticker: str, time_frame: str) -> pd.DataFrame:
        try:
            from_symbol = ticker[0:3]
            to_symbol = ticker[3:6]

            data = []
            match time_frame:
                case "D":
                    data, meta_data = self.foreign_exchange.get_currency_exchange_daily(from_symbol=from_symbol,
                                                                                        to_symbol=to_symbol)
                case "W":
                    data, meta_data = self.foreign_exchange.get_currency_exchange_weekly(from_symbol=from_symbol,
                                                                                         to_symbol=to_symbol)
                case "M":
                    data, meta_data = self.foreign_exchange.get_currency_exchange_monthly(from_symbol=from_symbol,
                                                                                          to_symbol=to_symbol)
            df = pd.DataFrame.from_dict(data, orient='index', dtype=float)
            df = df.reset_index()
            df.columns = ['startTime', 'open', 'high', 'low', 'close']
            return df
        except ValueError as e:
            if self.API_CALL_LIMIT_EXCEPTION_MSG in str(e):
                logging.warning(self.API_CALL_LIMIT_WARNING_MSG)
                time.sleep(self.API_CALL_LIMIT_SLEEP_INTERVAL_SECONDS)
                return self.get_ohlc(ticker, time_frame)
            raise e
