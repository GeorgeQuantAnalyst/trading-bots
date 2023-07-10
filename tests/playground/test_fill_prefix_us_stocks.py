import unittest

import pandas as pd


class FillPrefixUsStocks(unittest.TestCase):
    BASE_PATH = "fixtures/test_fill_prefix_us_stocks"
    PREFIX_MAPPING = {
        "nyse": "NYSE",
        "nasdaq": "NASDAQ",
        "amex": "AMEX"
    }

    def setUp(self) -> None:
        self.exchanges = {
            "nyse": pd.read_csv(f"{self.BASE_PATH}/nyse_stocks.csv")["Ticker"].tolist(),
            "nasdaq": pd.read_csv(f"{self.BASE_PATH}/nasdaq_stocks.csv")["Ticker"].tolist(),
            "amex": pd.read_csv(f"{self.BASE_PATH}/amex_stocks.csv")["Ticker"].tolist()
        }

    def test_fill_prefix(self):
        input_files = [
            f"{self.BASE_PATH}/most_traded_us_stocks.csv",
            f"{self.BASE_PATH}/S&P_500.csv",
            f"{self.BASE_PATH}/russell_2000.csv"

        ]
        output_files = [
            "most_traded_us_stocks_with_prefix.csv",
            "S&P_500_with_prefix.csv",
            "russell_2000_with_prefix.csv"
        ]

        for input_file, output_file in zip(input_files, output_files):
            tickers = pd.read_csv(input_file)["Ticker"].tolist()

            result = self._add_prefix_to_tickers(tickers, self.exchanges)
            result_df = pd.DataFrame(result, columns=["Ticker"])
            result_df.to_csv(output_file, index=False)

            expected_df = pd.read_csv(f"{output_file}")
            self.assertTrue(result_df.equals(expected_df))

    def _add_prefix_to_tickers(self, tickers, exchanges):
        result = []
        for ticker in tickers:
            prefix = "XXX"

            for exchange, exchange_tickers in exchanges.items():
                if ticker in exchange_tickers:
                    prefix = self.PREFIX_MAPPING[exchange]
                    break

            result.append("{}:{}".format(prefix, ticker))

        return result


if __name__ == '__main__':
    unittest.main()
