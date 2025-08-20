import backtrader as bt


class BreakRedStrategy(bt.Strategy):
    params = dict(
        lookahead=30  # number of candles to check for R/R exit
    )

    def __init__(self):
        self.order = None
        self.entry_price = None
        self.stop_price = None
        self.target_price = None
        self.entry_bar = None

    def next(self):
        if self.order:
            return  # wait if order is pending

        # If we’re in a trade, manage exit
        if self.position:
            bars_since_entry = len(self) - self.entry_bar

            # stop handled automatically by Backtrader
            # check if RR reached
            if self.data.close[0] >= self.target_price:
                self.close()
                self.log(f"TP hit at {self.data.close[0]}")
            elif bars_since_entry >= self.p.lookahead:
                # close if 30 bars passed and RR was met earlier
                if self.data.close[0] >= self.target_price:
                    self.close()
                    self.log(f"Closed on RR after {bars_since_entry} bars")
                else:
                    self.close()
                    self.log(f"Closed after {bars_since_entry} bars (no RR)")
            return

        # --- ENTRY LOGIC ---
        if len(self.data) < 2:
            return

        prev_close = self.data.close[-1]
        prev_open = self.data.open[-1]
        prev_high = self.data.high[-1]
        prev_low = self.data.low[-1]

        curr_close = self.data.close[0]
        curr_open = self.data.open[0]
        curr_high = self.data.high[0]

        # prev candle red, curr green breaking prev high
        if prev_close < prev_open and curr_close > curr_open and curr_high > prev_high:
            entry_price = prev_high
            stop_price = prev_low
            risk = entry_price - stop_price
            target_price = entry_price + risk

            # place stop-market entry at prev high
            self.order = self.buy(exectype=bt.Order.Stop, price=entry_price)
            self.entry_price = entry_price
            self.stop_price = stop_price
            self.target_price = target_price
            self.entry_bar = len(self)
            self.log(f"Entry setup: buy {entry_price}, stop {stop_price}, target {target_price}")

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED at {order.executed.price}")
                self.entry_bar = len(self)
                # attach stop loss
                self.sell(
                    exectype=bt.Order.Stop,
                    price=self.stop_price,
                    size=order.executed.size
                )
        self.order = None

    def log(self, txt):
        dt = self.datas[0].datetime.datetime(0)
        print(f"{dt}, {txt}")


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # CSV feed
    data = bt.feeds.GenericCSVData(
        dataname="MNQU25_M30_modified.csv",
        timeframe=bt.TimeFrame.Minutes,
        dtformat=('%Y-%m-%d %H:%M:%S'),  # adjust depending on your csv
        compression=1,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.addstrategy(BreakRedStrategy)
    cerebro.run()
    cerebro.plot()
