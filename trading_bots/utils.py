import yaml

from trading_bots.bybit_example_bot import BybitExampleBot
from trading_bots.templates.bot import Bot


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            return parsed_yaml
        except yaml.YAMLError as exc:
            print(exc)


def create_bot(bot_name: str, config: dict) -> Bot:
    match bot_name:
        case "BybitExampleBot":
            return BybitExampleBot(config)
        case _:
            raise ValueError("Not supported bot_name: {}".format(bot_name))
