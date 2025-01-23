import pandas as pd


def ema(data, period):
    """
    Calculate EMA using pandas' ewm method
    """
    return data.ewm(span=period, adjust=False).mean()


def macd(data, short_period, long_period, signal_period):
    short_ema = ema(data, short_period)
    long_ema = ema(data, long_period)

    # Calculate MACD line
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    return pd.DataFrame(
        {"macd": macd_line, "signal": signal_line, "histogram": macd_histogram}
    )
