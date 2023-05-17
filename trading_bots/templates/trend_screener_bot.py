from datetime import datetime

import pandas as pd

from trading_bots.templates.bot import Bot


class TrendScreenerBot(Bot):

    def find_intraday_daily_trends(self, tickers, ohlc_cache):
        intraday_daily_trends = []

        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]

            intraday_daily_trends.append({
                "ticker": ticker,
                "Change 7 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=7),
                "Context D": self.helper.calculate_context(ohlc_daily)
            })

        return pd.DataFrame(intraday_daily_trends)

    def find_swing_weekly_trends(self, tickers, ohlc_cache):
        swing_weekly_trends = []
        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]
            ohlc_weekly = ohlc_cache["weekly"][ticker]

            swing_weekly_trends.append({
                "ticker": ticker,
                "Change 30 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=30),
                "Context W": self.helper.calculate_context(ohlc_weekly)
            })
        return pd.DataFrame(swing_weekly_trends)

    def find_swing_monthly_trends(self, tickers, ohlc_cache):
        swing_monthly_trends = []
        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]
            ohlc_monthly = ohlc_cache["monthly"][ticker]

            swing_monthly_trends.append({
                "ticker": ticker,
                "Change 90 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=90),
                "Context M": self.helper.calculate_context(ohlc_monthly)
            })
        return pd.DataFrame(swing_monthly_trends)

    @staticmethod
    def save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends, excel_path: str):
        now = datetime.now().strftime("%Y%m%d")
        writer = pd.ExcelWriter(excel_path, engine="openpyxl")

        intraday_daily_trends["ticker"] = "BYBIT:" + intraday_daily_trends["ticker"] + ".P"
        swing_weekly_trends["ticker"] = "BYBIT:" + swing_weekly_trends["ticker"] + ".P"
        swing_monthly_trends["ticker"] = "BYBIT:" + swing_monthly_trends["ticker"] + ".P"

        intraday_daily_trends.to_excel(writer, sheet_name="Intraday D trends", index=False)
        swing_weekly_trends.to_excel(writer, sheet_name="Swing W trends", index=False)
        swing_monthly_trends.to_excel(writer, sheet_name="Swing M trends", index=False)

        writer.close()
