import logging

import pandas as pd

from trading_bots.helpers.equity_trend_screener_bot_helper import EquityTrendScreenerBotHelper
from trading_bots.templates.bot import Bot
from trading_bots.trading_math import convert_ohlc, calculate_context


class EquityTrendScreenerBot(Bot):
    SEPARATOR = "------------------------"

    def __init__(self, config):
        super().__init__(config)
        self.helper = EquityTrendScreenerBotHelper()

    def run(self) -> None:
        logging.info("Start EquityTrendScreenerBot")

        tickers = self.loading_tickers()
        trends = self.find_trends(tickers)
        self.create_tw_trends_report(trends)

        logging.info("Finished EquityTrendScreenerBot")

    def loading_tickers(self) -> dict[str, list]:
        logging.info(self.SEPARATOR)
        logging.info("Loading tickers")
        logging.info(self.SEPARATOR)

        if self.config["mostTradedUsStocks"]["enable"]:
            tickers_most_traded_us_stocks = self.helper.get_tickers(
                self.config["mostTradedUsStocks"]["tickersFilePath"])
        else:
            tickers_most_traded_us_stocks = []

        if self.config["sp500"]["enable"]:
            tickers_sp_500 = self.helper.get_tickers(self.config["sp500"]["tickersFilePath"])
        else:
            tickers_sp_500 = []

        if self.config["russell2k"]["enable"]:
            tickers_russell_2k = self.helper.get_tickers(self.config["russell2k"]["tickersFilePath"])
        else:
            tickers_russell_2k = []

        logging.info("Loaded {} tickers for Most traded US stocks".format(len(tickers_most_traded_us_stocks)))
        logging.info("Loaded {} tickers for index S&P 500".format(len(tickers_sp_500)))
        logging.info("Loaded {} tickers for index Russell 2000".format(len(tickers_russell_2k)))

        return {
            "tickers_most_traded_us_stocks": tickers_most_traded_us_stocks,
            "tickers_sp_500": tickers_sp_500,
            "tickers_russell_2k": tickers_russell_2k
        }

    def find_trends(self, tickers: dict[str, list]) -> dict[str, pd.DataFrame]:
        logging.info(self.SEPARATOR)
        logging.info("Find trends")
        logging.info(self.SEPARATOR)

        logging.info("Find trends in Most traded US stocks tickers")
        most_traded_us_stocks_quarterly_trends = []
        most_traded_us_stocks_yearly_trends = []
        for ticker in tickers["tickers_most_traded_us_stocks"]:
            logging.info("Process {} ticker".format(ticker))
            daily_ohlc = self.helper.get_daily_ohlc(ticker)
            quarterly_ohlc = convert_ohlc(daily_ohlc, "Q")
            yearly_ohlc = convert_ohlc(daily_ohlc, "Y")

            logging.debug("Daily ohlc (last 10 candles): \n {}".format(daily_ohlc))
            logging.debug("Quarterly ohlc (last 10 candles): \n {}".format(quarterly_ohlc))
            logging.debug("Yearly ohlc (last 10 candles): \n {}".format(yearly_ohlc))

            quarterly_context = calculate_context(quarterly_ohlc)
            yearly_context = calculate_context(yearly_ohlc)

            logging.debug("Quarterly context: {}".format(quarterly_context))
            logging.debug("Yearly context: {}".format(yearly_context))

            most_traded_us_stocks_quarterly_trends.append({
                "ticker": ticker,
                "context": quarterly_context
            })

            most_traded_us_stocks_yearly_trends.append({
                "ticker": ticker,
                "context": yearly_context
            })

        logging.info("Find trends in S&P 500 tickers")
        sp_500_quarterly_trends = []
        sp_500_yearly_trends = []
        for ticker in tickers["tickers_sp_500"]:
            logging.info("Process {} ticker".format(ticker))
            daily_ohlc = self.helper.get_daily_ohlc(ticker)
            quarterly_ohlc = convert_ohlc(daily_ohlc, "Q")
            yearly_ohlc = convert_ohlc(daily_ohlc, "Y")

            logging.debug("Daily ohlc (last 10 candles): \n {}".format(daily_ohlc))
            logging.debug("Quarterly ohlc (last 10 candles): \n {}".format(quarterly_ohlc))
            logging.debug("Yearly ohlc (last 10 candles): \n {}".format(yearly_ohlc))

            quarterly_context = calculate_context(quarterly_ohlc)
            yearly_context = calculate_context(yearly_ohlc)

            logging.debug("Quarterly context: {}".format(quarterly_context))
            logging.debug("Yearly context: {}".format(yearly_context))

            sp_500_quarterly_trends.append({
                "ticker": ticker,
                "context": quarterly_context
            })

            sp_500_yearly_trends.append({
                "ticker": ticker,
                "context": yearly_context
            })

        logging.info("Find trends in Russell 2000 tickers")
        russell_2k_quarterly_trends = []
        russell_2k_yearly_trends = []
        for ticker in tickers["tickers_russell_2k"]:
            logging.info("Process {} ticker".format(ticker))
            daily_ohlc = self.helper.get_daily_ohlc(ticker)
            quarterly_ohlc = convert_ohlc(daily_ohlc, "Q")
            yearly_ohlc = convert_ohlc(daily_ohlc, "Y")

            logging.debug("Daily ohlc (last 10 candles): \n {}".format(daily_ohlc))
            logging.debug("Quarterly ohlc (last 10 candles): \n {}".format(quarterly_ohlc))
            logging.debug("Yearly ohlc (last 10 candles): \n {}".format(yearly_ohlc))

            quarterly_context = calculate_context(quarterly_ohlc)
            yearly_context = calculate_context(yearly_ohlc)

            logging.debug("Quarterly context: {}".format(quarterly_context))
            logging.debug("Yearly context: {}".format(yearly_context))

            russell_2k_quarterly_trends.append({
                "ticker": ticker,
                "context": quarterly_context
            })

            russell_2k_yearly_trends.append({
                "ticker": ticker,
                "context": yearly_context
            })

        return {
            "most_traded_us_stocks_quarterly_trends": pd.DataFrame(most_traded_us_stocks_quarterly_trends),
            "most_traded_us_stocks_yearly_trends": pd.DataFrame(most_traded_us_stocks_yearly_trends),
            "sp_500_quarterly_trends": pd.DataFrame(sp_500_quarterly_trends),
            "sp_500_yearly_trends": pd.DataFrame(sp_500_yearly_trends),
            "russell_2k_quarterly_trends": pd.DataFrame(russell_2k_quarterly_trends),
            "russell_2k_yearly_trends": pd.DataFrame(russell_2k_yearly_trends)
        }

    def create_tw_trends_report(self, trends):
        logging.info(self.SEPARATOR)
        logging.info("Create TradingView trends report")
        logging.info(self.SEPARATOR)

        reports_folder = self.config["base"]["reportsFolder"]

        logging.info("Create Most traded US stocks 3M trends")
        most_traded_us_stocks_quarterly_trends = trends["most_traded_us_stocks_quarterly_trends"]
        if not most_traded_us_stocks_quarterly_trends.empty:
            most_traded_us_stocks_quarterly_trends_path = "{}/Most traded US stocks 3M trends.txt".format(reports_folder)
            most_traded_us_stocks_quarterly_trends_report = self.helper.create_tw_report(
                most_traded_us_stocks_quarterly_trends)
            self.helper.save_tw_report(most_traded_us_stocks_quarterly_trends_report,
                                       most_traded_us_stocks_quarterly_trends_path)

        logging.info("Create Most traded US stocks Y trends")
        most_traded_us_stocks_yearly_trends = trends["most_traded_us_stocks_yearly_trends"]
        if not most_traded_us_stocks_yearly_trends.empty:
            most_traded_us_stocks_yearly_trends_path = "{}/Most traded US stocks Y trends.txt".format(reports_folder)
            most_traded_us_stocks_yearly_trends_report = self.helper.create_tw_report(
                most_traded_us_stocks_yearly_trends)
            self.helper.save_tw_report(most_traded_us_stocks_yearly_trends_report,
                                       most_traded_us_stocks_yearly_trends_path)

        logging.info("Create S&P500 3M trends")
        sp_500_quarterly_trends = trends["sp_500_quarterly_trends"]
        if not sp_500_quarterly_trends.empty:
            sp_500_quarterly_trends_path = "{}/S&P 500 3M trends.txt".format(reports_folder)
            sp_500_quarterly_trends_report = self.helper.create_tw_report(sp_500_quarterly_trends)
            self.helper.save_tw_report(sp_500_quarterly_trends_report, sp_500_quarterly_trends_path)

        logging.info("Create S&P500 Y trends")
        sp_500_yearly_trends = trends["sp_500_yearly_trends"]
        if not sp_500_yearly_trends.empty:
            sp_500_yearly_trends_path = "{}/S&P 500 Y trends.txt".format(reports_folder)
            sp_500_yearly_trends_report = self.helper.create_tw_report(sp_500_yearly_trends)
            self.helper.save_tw_report(sp_500_yearly_trends_report, sp_500_yearly_trends_path)

        logging.info("Create Russell 2000 3M trends")
        russell_2k_quarterly_trends = trends["russell_2k_quarterly_trends"]
        if not russell_2k_quarterly_trends.empty:
            if self.helper.count_items_without_rotation(russell_2k_quarterly_trends) > 1000:
                russell_2k_quarterly_trends_path_part1 = "{}/Russell 2000 3M trends part1.txt".format(reports_folder)
                russell_2k_quarterly_trends_path_part2 = "{}/Russell 2000 3M trends part2.txt".format(reports_folder)

                n = russell_2k_quarterly_trends.shape[0]
                russell_2k_quarterly_trends_part1 = russell_2k_quarterly_trends.head(n // 2)
                russell_2k_quarterly_trends_part2 = russell_2k_quarterly_trends.tail(n // 2)

                russell_2k_quarterly_trends_report_part1 = self.helper.create_tw_report(
                    russell_2k_quarterly_trends_part1)
                russell_2k_quarterly_trends_report_part2 = self.helper.create_tw_report(
                    russell_2k_quarterly_trends_part2)

                self.helper.save_tw_report(russell_2k_quarterly_trends_report_part1,
                                           russell_2k_quarterly_trends_path_part1)
                self.helper.save_tw_report(russell_2k_quarterly_trends_report_part2,
                                           russell_2k_quarterly_trends_path_part2)
            else:
                russell_2k_quarterly_trends_path = "{}/Russell 2000 3M trends.txt".format(reports_folder)
                russell_2k_quarterly_trends_report = self.helper.create_tw_report(russell_2k_quarterly_trends)
                self.helper.save_tw_report(russell_2k_quarterly_trends_report, russell_2k_quarterly_trends_path)

        logging.info("Create Russell 2000 Y trends")
        russell_2k_yearly_trends = trends["russell_2k_yearly_trends"]
        if not russell_2k_yearly_trends.empty:
            if self.helper.count_items_without_rotation(russell_2k_yearly_trends) > 1000:
                russell_2k_yearly_trends_path_part1 = "{}/Russell 2000 Y trends part1.txt".format(reports_folder)
                russell_2k_yearly_trends_path_part2 = "{}/Russell 2000 Y trends part2.txt".format(reports_folder)

                n = russell_2k_yearly_trends.shape[0]
                russell_2k_yearly_trends_part1 = russell_2k_yearly_trends.head(n // 2)
                russell_2k_yearly_trends_part2 = russell_2k_yearly_trends.tail(n // 2)

                russell_2k_yearly_trends_report_part1 = self.helper.create_tw_report(russell_2k_yearly_trends_part1)
                russell_2k_yearly_trends_report_part2 = self.helper.create_tw_report(russell_2k_yearly_trends_part2)

                self.helper.save_tw_report(russell_2k_yearly_trends_report_part1, russell_2k_yearly_trends_path_part1)
                self.helper.save_tw_report(russell_2k_yearly_trends_report_part2, russell_2k_yearly_trends_path_part2)
            else:
                russell_2k_yearly_trends_path = "{}/Russell 2000 Y trends.txt".format(reports_folder)
                russell_2k_yearly_trends_report = self.helper.create_tw_report(russell_2k_yearly_trends)
                self.helper.save_tw_report(russell_2k_yearly_trends_report, russell_2k_yearly_trends_path)