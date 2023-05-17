from trading_bots.templates.bot import Bot
from pybit.unified_trading import HTTP


class BybitBot(Bot):

    def __init__(self, config: dict):
        self.exchange = HTTP(testnet=config["bybitApi"]["testnet"],
                             api_key=config["bybitApi"]["apiKey"],
                             api_secret=config["bybitApi"]["secretKey"])
        super().__init__(config)
