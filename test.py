import backtrader as bt
from datetime import datetime

# Define a simple moving average strategy
class SMAStrategy(bt.Strategy):
    params = (('sma_period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if self.data.close > self.sma:
            self.buy()
        elif self.data.close < self.sma:
            self.sell()

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add strategy to the cerebro
cerebro.addstrategy(SMAStrategy)

# Load data
data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2020, 1, 1), todate=datetime(2021, 1, 1))
cerebro.adddata(data)

# Set initial cash
cerebro.broker.set_cash(10000)

# Run the backtest
cerebro.run()

# Plot the result
cerebro.plot()
