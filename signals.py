import pandas as pd
from indicators import macd  # Import the macd function


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
        # Use the imported macd function
        return macd(self.df["Close"], fast_length, slow_length, signal_length)

    def run(
        self,
        fast_length=12,
        slow_length=26,
        signal_length=9,
    ):
        # Calculate MACD indicators
        indicator = self.calculate_macd(fast_length, slow_length, signal_length)
        print(indicator)
        # Create trading entries (1 for buy, -1 for sell, 0 for no action)
        entry = pd.Series(0, index=self.df.index)
        entry[indicator["macd"] > indicator["signal"]] = 1
        entry[indicator["macd"] < indicator["signal"]] = -1

        # Combine the original price data with the indicators
        result = pd.DataFrame(
            {
                "Open": self.df["Open"],
                "High": self.df["High"],
                "Low": self.df["Low"],
                "Close": self.df["Close"],
                "Volume": self.df["Volume"],
                "Spread": self.df["Spread"],
                "MACD": indicator["macd"],
                "Entry": entry,
                "Histogram": indicator["histogram"],
            }
        )

        return result
