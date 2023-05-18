import logging.config
import sys

from trading_bots.__version__ import __version__
from trading_bots.constants import __logo__
from trading_bots.utils import load_config, create_bot


bot_names = ["BybitExampleBot", "CryptoTrendScreenerBot"]

if __name__ == "__main__":
    bot_name = sys.argv[1]

    if bot_name not in bot_names:
        raise ValueError("Not supported bot with name: {}".format(bot_name))

    logger_config_file_path = "config/{}Logger.conf".format(bot_name)
    config_file_path = "config/{}Config.yaml".format(bot_name)

    logging.config.fileConfig(fname=logger_config_file_path, disable_existing_loggers=False)
    logging.info(__logo__.format(bot_name=bot_name, app_version=__version__))

    try:
        config = load_config(config_file_path)
        bot = create_bot(bot_name, config)
        bot.run()
    except:
        logging.exception("Error in app: ")
