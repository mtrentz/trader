from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime()
        print('%s, %s' % (dt, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.6f' % self.dataclose[0])



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

#     data = btfeeds.GenericCSVData(
#         dataname='dados/forex/EURUSD_HOURLY.csv',

#         fromdate=datetime.datetime(2021, 2, 14),
#         todate=datetime.datetime(2021, 2, 18),

#         nullvalue=0.0,

#         dtformat=('%Y-%m-%d %H:%M:%S'),

#         datetime=0,
#         open=1,
#         high=2,
#         low=3,
#         close=4,
#         volume=5,
#         openinterest=-1
# )


    df = pd.read_csv('dados\crypto\Binance_ETHUSDT_d.csv')
    df = df[['date', 'open', 'high', 'low', 'close', 'Volume ETH']]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.round(2)
    df = df[::-1]
    data = bt.feeds.PandasData(dataname=df)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())





