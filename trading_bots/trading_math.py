import pandas as pd


def convert_ohlc(ohlc: pd.DataFrame, time_frame: str) -> pd.DataFrame:
    df = ohlc.copy()
    df['startTime'] = pd.to_datetime(df['startTime'])
    df.set_index('startTime', inplace=True)

    convert_ohlc_df = df.resample(time_frame).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
    convert_ohlc_df = convert_ohlc_df[::-1].reset_index()
    convert_ohlc_df.columns = ['startTime', 'open', 'high', 'low', 'close']

    return convert_ohlc_df


def calculate_context(ohlc: pd.DataFrame) -> str:
    ohlc_filtered = ohlc.head(5)
    if ohlc_filtered.shape[0] < 5:
        return "N/A"

    # Compute candle color
    ohlc_filtered.loc[ohlc_filtered['close'] < ohlc_filtered['open'], 'candleColor'] = 'Red'
    ohlc_filtered.loc[ohlc_filtered['close'] >= ohlc_filtered['open'], 'candleColor'] = 'Green'

    # Compute context
    if is_up_trend(ohlc_filtered):
        return "Up-trend"
    if is_start_rotation_after_up_trend(ohlc_filtered):
        return "Start rotation after up-trend"
    if is_down_trend(ohlc_filtered):
        return "Down-trend"
    if is_start_rotation_after_down_trend(ohlc_filtered):
        return "Start rotation after down-trend"

    return "Rotation"


def is_up_trend(ohlc: pd.DataFrame) -> bool:
    if ohlc.shape[0] < 4:
        return False

    two_green_candles = ohlc.loc[1]["candleColor"] == "Green" and ohlc.loc[2]["candleColor"] == "Green"
    higher_lows = ohlc.loc[0]["low"] > ohlc.loc[1]["low"] > ohlc.loc[2]["low"]
    break_high = ohlc.loc[0]["close"] > ohlc.loc[3]["high"]

    return two_green_candles and higher_lows and break_high


def is_down_trend(ohlc: pd.DataFrame) -> bool:
    if ohlc.shape[0] < 4:
        return False

    two_red_candles = ohlc.loc[1]["candleColor"] == "Red" and ohlc.loc[2]["candleColor"] == "Red"
    lower_highs = ohlc.loc[0]["high"] < ohlc.loc[1]["high"] < ohlc.loc[2]["high"]
    break_low = ohlc.loc[0]["close"] < ohlc.loc[3]["low"]

    return two_red_candles and lower_highs and break_low


def is_start_rotation_after_up_trend(ohlc: pd.DataFrame) -> bool:
    if ohlc.loc[1]["candleColor"] == "Red":
        ohlc = ohlc[1:].reset_index(drop=True)
        two_green_candles = ohlc.loc[1]["candleColor"] == "Green" and ohlc.loc[2]["candleColor"] == "Green"
        break_high = ohlc.loc[0]["close"] > ohlc.loc[3]["high"]
        return two_green_candles and break_high
    else:
        return False


def is_start_rotation_after_down_trend(ohlc: pd.DataFrame) -> bool:
    if ohlc.loc[1]["candleColor"] == "Green":
        ohlc = ohlc[1:].reset_index(drop=True)
        two_red_candles = ohlc.loc[1]["candleColor"] == "Red" and ohlc.loc[2]["candleColor"] == "Red"
        break_low = ohlc.loc[0]["close"] < ohlc.loc[3]["low"]
        return two_red_candles and break_low
    else:
        return False
