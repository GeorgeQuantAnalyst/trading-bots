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
    ohlc_filtered = ohlc.head(4)

    if ohlc_filtered.shape[0] < 4:
        return "N/A"

    # Compute candle color
    ohlc_filtered.loc[ohlc_filtered['close'] < ohlc_filtered['open'], 'candleColor'] = 'Red'
    ohlc_filtered.loc[ohlc_filtered['close'] >= ohlc_filtered['open'], 'candleColor'] = 'Green'

    # Compute context
    if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Green":
        return "Up-trend"

    if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Green" and \
            ohlc_filtered.loc[3]["candleColor"] == "Green":
        return "Start rotation after up-trend"

    if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Red":
        return "Down-trend"

    if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Red" and \
            ohlc_filtered.loc[3]["candleColor"] == "Red":
        return "Start rotation after down-trend"

    return "Rotation"
