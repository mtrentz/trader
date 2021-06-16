import backtrader as bt

# Create a Stratey
class TwoMA(bt.Strategy):
    params = (
        ('fastperiod', 15),
        ('slowperiod', 50),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        #print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.slow_sma = bt.indicators.SMA(
            self.dataclose, period=self.params.slowperiod)
        self.fast_sma = bt.indicators.SMA(
            self.dataclose, period=self.params.fastperiod)
        self.crossover = bt.indicators.CrossOver(
            self.fast_sma, self.slow_sma)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.6f, Cost: %.6f, Comm %.6f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.6f, Cost: %.6f, Comm %.6f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.6f, NET %.6f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.6f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            if self.crossover > 0:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.6f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()



        else:

            if self.crossover < 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.6f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                #self.order = self.close()