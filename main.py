import datetime
import backtrader as bt
from strategies.two_ma import TwoMA
import os
import sys

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TwoMA)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'dados/oracle.txt')

    # # Create a Data Feed
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(1996, 1, 1),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2013, 12, 31),
    #     # Do not pass values after this date
    #     reverse=False)


    #Set data parameters and add to Cerebro
    data = bt.feeds.GenericCSVData(
        dataname='dados/forex/EURUSD_HOURLY.csv',

        fromdate=datetime.datetime(2010, 2, 14),
        todate=datetime.datetime(2021, 2, 18),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d %H:%M:%S'),
        #dtformat=('%Y-%m-%d'),

        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=-1,
        openinterest=-1
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.6f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.6f' % cerebro.broker.getvalue())

    
    # Plot the result
    cerebro.plot()