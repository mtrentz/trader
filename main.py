import datetime
import backtrader as bt
from strategies.two_ma import TwoMA
from strategies.rsi import RSI
from strategies.bollinger_bands import BollingerBands
from strategies.buy_and_hold import BuyAndHold
import pandas as pd
import os
import sys

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    #cerebro.addstrategy(RSI, period=14)
    cerebro.addstrategy(BuyAndHold)
    #cerebro.addstrategy(TwoMA)
    #cerebro.addstrategy(BollingerBands, BBandsperiod=115, Fator=3)

    # # Create a Data Feed
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'dados/oracle.txt')
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2010, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2013, 12, 31),
        # Do not pass values after this date
        reverse=False)


    # # DADOS DO METATRADER
    # data = bt.feeds.GenericCSVData(
    #     dataname='dados/forex/EURUSD_HOURLY.csv',

    #     fromdate=datetime.datetime(2021, 1, 1),
    #     todate=datetime.datetime(2021, 6, 16),
    #     timeframe=bt.TimeFrame.Minutes,
    #     compression=60,

    #     nullvalue=0.0,

    #     dtformat=('%Y-%m-%d %H:%M:%S'),
    #     #dtformat=('%Y-%m-%d'),

    #     datetime=0,
    #     open=1,
    #     high=2,
    #     low=3,
    #     close=4,
    #     volume=-1,
    #     openinterest=-1
    # )

    # # # DADOS DE CRYPTO BINANCE DAILY
    # df = pd.read_csv('dados\crypto\Binance_ETHUSDT_d.csv')
    # df = df[['date', 'open', 'high', 'low', 'close', 'Volume ETH']]
    # df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    # df['datetime'] = pd.to_datetime(df['datetime'])
    # df = df.set_index('datetime')
    # df = df.round(2)
    # df = df[::-1]
    # data = bt.feeds.PandasData(dataname=df)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)

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