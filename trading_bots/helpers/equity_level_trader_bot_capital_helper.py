import csv
import datetime
import logging
from datetime import time

import requests


class EquityLevelTraderBotCapitalHelper:

    def __init__(self, config: dict):
        self.capital_client = None
        self.api_key = config["alphavantageApiKey"]["apiKey"]

    @staticmethod
    def load_orders(file_path):
        result = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                result.append(row)
        return result

    def is_open_exchange(self) -> bool:
        now = datetime.datetime.now()
        return self._is_work_day(now) and self._is_time_between_range(now.time(), time(15, 30), time(22, 00))

    def is_open_positions(self) -> bool:
        # TODO: @Lucka
        return False

    @staticmethod
    def place_trade(order: dict):
        # TODO: @Lucka
        pass

    @staticmethod
    def is_price_arrive_to_order(order: dict):
        # TODO: Jirka

        return False
    @staticmethod
    def was_yesterday_the_last_earnings(self, ticker) -> bool:
        now = datetime.datetime.now().date()
        yesterday = now - datetime.timedelta(days=1)

        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()

        earnings_types = ["quarterlyEarnings", "annualEarnings"]
        for earnings_type in earnings_types:
            earnings = data.get(earnings_type, [])
            if earnings and datetime.datetime.strptime(earnings[0]["reportedDate"], "%Y-%m-%d").date() == yesterday:
                logging.debug(f"The last earnings result ({earnings_type}) was yesterday: {yesterday}")
                return True
            else:
                return False

    @staticmethod
    def is_earnings_next_days(ticker: str, count_days: int = 10) -> bool:
        now = datetime.datetime.now().date()
        # TODO: Lucka
        return False

    @staticmethod
    def _is_work_day(date):
        return date.weekday() < 5

    @staticmethod
    def _is_time_between_range(actual_time: datetime.time, start_time: datetime.time, end_time: datetime.time) -> bool:
        return start_time <= actual_time <= end_time
