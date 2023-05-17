from trading_bots.templates.trend_screener_bot_helper import TrendScreenerBotHelper


class CryptoTrendScreenerBotHelper(TrendScreenerBotHelper):

    def __init__(self, exchange):
        self.exchange = exchange

    def get_available_tickers(self):
        # TODO: @Lucka
        pass

    def get_ohlc(self, ticker, time_frame):
        # TODO: @Lucka
        pass
