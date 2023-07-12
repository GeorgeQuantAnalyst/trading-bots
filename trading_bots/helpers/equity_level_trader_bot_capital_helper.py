import csv
import datetime
from datetime import time


class EquityLevelTraderBotCapitalHelper:

    def __init__(self, config: dict):
        self.capital_client = None

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
    def was_earnings_yesterday(ticker) -> bool:
        now = datetime.datetime.now().date()
        # TODO: Lucka
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
