import pandas as pd
from backtesting import Strategy, Backtest, lib
from signals import MACDSignal

# Load the CSV file
data = pd.read_csv("EURJPY.csv")
macd_signal = MACDSignal(data)
signal = macd_signal.run()


class TestStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        current_price = self.data.Close[-1]
        current_spread = self.data.Spread[-1]
        current_entry = self.data.Entry[-1]

        # Convert spread from points to price units (for JPY pairs)
        spread_in_price_units = current_spread * 0.001
        bid_price = current_price - (spread_in_price_units / 2)
        ask_price = current_price + (spread_in_price_units / 2)

        # Manage open trades
        for trade in self.trades:
            current_entry_price = trade.entry_price

            # Adjust SL and TP based on trade direction
            if trade.is_long:
                current_entry_sl = current_entry_price - 3  # SL below entry price
                current_entry_tp = current_entry_price + 1  # TP above entry price
            elif trade.is_short:
                current_entry_sl = current_entry_price + 3  # SL above entry price
                current_entry_tp = current_entry_price - 1  # TP below entry price

            # Check exit conditions
            if trade.is_long:
                if bid_price >= current_entry_tp or bid_price <= current_entry_sl:
                    trade.close()
            elif trade.is_short:
                if ask_price <= current_entry_tp or ask_price >= current_entry_sl:
                    trade.close()

        # Enter new trades only if no trades are open
        if len(self.trades) == 0:
            if current_entry == 1:
                self.buy()  # Market order for long trade
            elif current_entry == -1:
                self.sell()  # Market order for short trade


# Set up and run the backtest
bt = Backtest(signal, TestStrategy, cash=10000)
stats = bt.run()

print(stats)
bt.plot()
