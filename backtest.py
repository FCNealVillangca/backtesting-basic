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
        current_signal = self.data.Signal[-1]

        bid_price = current_price - (current_spread * 0.001 / 2)
        ask_price = current_price + (current_spread * 0.001 / 2)

        if len(self.trades) != 0:
            current_entry_price = self.trades[0].entry_price
            current_entry_sl = current_entry_price - 3
            current_entry_tp = current_entry_price + 1

            if self.trades[0].is_long:
                if bid_price >= current_entry_tp:
                    self.trades[0].close()
                elif bid_price <= current_entry_sl:
                    self.trades[0].close()
            elif self.trades[0].is_short:
                if ask_price <= current_entry_tp:
                    self.trades[0].close()
                elif ask_price >= current_entry_sl:
                    self.trades[0].close()
        if current_signal == 1:
            self.buy(limit=ask_price)
        elif current_signal == -1:
            self.sell(limit=bid_price)


# Set up and run the backtest
bt = Backtest(signal, TestStrategy, cash=10000, commission=0.002)
stats = bt.run()

print(stats)
bt.plot()
