import datetime
import backtrader as bt
from strategies.two_ma import TwoMA
import os
import sys


if __name__ == '__main__':
    cerebro = bt.Cerebro(optreturn=False)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.optstrategy(TwoMA, fastperiod=range(14,16), slowperiod=range(50,55))
    #cerebro.optstrategy(SMAcrossover, fast=range(5,55,5), slow=range(60,310,10))
    STARTING_CASH = 1000.0
    cerebro.broker.set_cash(STARTING_CASH)
    #cerebro.broker.set_coc(True)

    #Set data parameters and add to Cerebro
    data = bt.feeds.GenericCSVData(
        dataname='dados/forex/EURUSD_HOURLY.csv',

        fromdate=datetime.datetime(2021, 1, 1),
        todate=datetime.datetime(2021, 6, 16),
        timeframe=bt.TimeFrame.Minutes,
        compression=60,

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


    cerebro.adddata(data)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    #comminfo = DegiroCommission()
    cerebro.broker.setcommission(commission=0.0)

    optimized_runs = cerebro.run()

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.get_value() - STARTING_CASH,2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.fastperiod, 
                strategy.params.slowperiod, PnL, sharpe['sharperatio']])

    # sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
    #                          reverse=True)
    # for line in sort_by_sharpe[:5]:
    #     print(line)
    print(final_results_list)






# if __name__ == '__main__':
#     # Create a cerebro entity
#     cerebro = bt.Cerebro(optreturn=False)

#     # Add a strategy
#     cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
#     cerebro.optstrategy(TwoMA, fastperiod=range(3,5), slowperiod=range(20,22))

#     # Datas are in a subfolder of the samples. Need to find where the script is
#     # because it could have been called from anywhere
#     # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#     # datapath = os.path.join(modpath, 'dados/oracle.txt')

#     # # Create a Data Feed
#     # data = bt.feeds.YahooFinanceCSVData(
#     #     dataname=datapath,
#     #     # Do not pass values before this date
#     #     fromdate=datetime.datetime(1996, 1, 1),
#     #     # Do not pass values before this date
#     #     todate=datetime.datetime(2013, 12, 31),
#     #     # Do not pass values after this date
#     #     reverse=False)


#     #Set data parameters and add to Cerebro
#     data = bt.feeds.GenericCSVData(
#         dataname='dados/forex/EURUSD_HOURLY.csv',

#         fromdate=datetime.datetime(2021, 1, 1),
#         todate=datetime.datetime(2021, 6, 16),
#         timeframe=bt.TimeFrame.Minutes,
#         compression=60,

#         nullvalue=0.0,

#         dtformat=('%Y-%m-%d %H:%M:%S'),
#         #dtformat=('%Y-%m-%d'),

#         datetime=0,
#         open=1,
#         high=2,
#         low=3,
#         close=4,
#         volume=-1,
#         openinterest=-1
#     )

#     # Add the Data Feed to Cerebro
#     cerebro.adddata(data)



#     # Set our desired cash start
#     cerebro.broker.setcash(1000.0)

#     # Add a FixedSize sizer according to the stake
#     cerebro.addsizer(bt.sizers.FixedSize, stake=10)

#     # Set the commission
#     cerebro.broker.setcommission(commission=0.0)

#     # Print out the starting conditions
#     #print('Starting Portfolio Value: %.6f' % cerebro.broker.getvalue())


#     #  # Run over everything
#     # opt_runs = cerebro.run()

#     # # Generate results list
#     # final_results_list = []
#     # for run in opt_runs:
#     #     for strategy in run:
#     #         value = round(strategy.broker.get_value(),2)
#     #         PnL = round(value - 1000.0,2)
#     #         period = strategy.params.period
#     #         final_results_list.append([period,PnL])

#     # #Sort Results List
#     # by_period = sorted(final_results_list, key=lambda x: x[0])
#     # by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

#     # #Print results
#     # print('Results: Ordered by period:')
#     # for result in by_period:
#     #     print('Period: {}, PnL: {}'.format(result[0], result[1]))
#     # print('Results: Ordered by Profit:')
#     # for result in by_PnL:
#     #     print('Period: {}, PnL: {}'.format(result[0], result[1]))

#     # Run over everything
#     #cerebro.run()

#     optimized_runs = cerebro.run()

#     final_results_list = []
#     for run in optimized_runs:
#         for strategy in run:
#             PnL = round(cerebro.broker.get_value() - 1000.0,2)
#             sharpe = bt.analyzers.sharpe_ratio.get_analysis()
#             final_results_list.append([cerebro.params.fastperiod, 
#                 cerebro.params.slowperiod, PnL, sharpe['sharperatio']])

#     sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
#                              reverse=True)
#     for line in sort_by_sharpe[:5]:
#         print(line)

#     # Print out the final result
#     # print('Final Portfolio Value: %.6f' % cerebro.broker.getvalue())

#     # optimized_runs = cerebro.run()

#     # final_results_list = []
#     # for run in optimized_runs:
#     #     for strategy in run:
#     #         PnL = round(strategy.broker.get_value() - 1000,2)
#     #         sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
#     #         final_results_list.append([strategy.params.fastperiod, 
#     #             strategy.params.slowperiod, PnL, sharpe['sharperatio']])

#     # sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
#     #                          reverse=True)
#     # for line in sort_by_sharpe[:5]:
#     #     print(line)


    
#     # # Plot the result
#     # cerebro.plot()