import pandas as pd


class MACDSignal:
    def __init__(self, df):
        self.df = self.clean_data(df)

    def clean_data(self, df):
        """Clean and prepare the DataFrame for analysis."""
        column_map = {
            "time": "Time",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "spread": "Spread",
            "tick_volume": "Volume",
        }
        return df.rename(columns=column_map)

    def calculate_ma(self, data, length, ma_type="EMA"):
        if ma_type == "SMA":
            return data.rolling(window=length).mean()
        else:
            return data.ewm(span=length, adjust=False).mean()

    def calculate_macd(self, fast_length=12, slow_length=26, signal_length=9):
        fast_ema = self.calculate_ma(self.df["Close"], fast_length, "EMA")
        slow_ema = self.calculate_ma(self.df["Close"], slow_length, "EMA")
        macd_line = fast_ema - slow_ema
        signal_line = self.calculate_ma(macd_line, signal_length, "EMA")
        histogram = macd_line - signal_line
        return pd.DataFrame(
            {"MACD": macd_line, "Signal": signal_line, "Histogram": histogram}
        )

    def run(
        self,
        fast_length=12,
        slow_length=26,
        signal_length=9,
    ):
        # Calculate MACD indicators
        indicator = self.calculate_macd(fast_length, slow_length, signal_length)
        print(indicator)
        # Create trading signals (1 for buy, -1 for sell, 0 for no action)
        signal = pd.Series(0, index=self.df.index)
        signal[indicator["MACD"] > indicator["Signal"]] = 1
        signal[indicator["MACD"] < indicator["Signal"]] = -1

        # Combine the original price data with the indicators
        result = pd.DataFrame(
            {
                "Open": self.df["Open"],
                "High": self.df["High"],
                "Low": self.df["Low"],
                "Close": self.df["Close"],
                "Volume": self.df["Volume"],
                "Spread": self.df["Spread"],
                "MACD": indicator["MACD"],
                "Signal": signal,
                "Histogram": indicator["Histogram"],
            }
        )

        return result
