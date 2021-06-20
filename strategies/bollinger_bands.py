import backtrader as bt

# Create a Stratey
class BollingerBands(bt.Strategy):
    params = (
        ('BBandsperiod', 115),
        ('Fator', 3)        
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.comprado = None
        self.vendido = None

        self.bband = bt.indicators.BollingerBands(self.datas[0], period=self.params.BBandsperiod, 
                                                                devfactor=self.params.Fator)
                

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

        # FULL COPIADO
        # CRIA LINHAS BLUE E RED
        # if self.dataclose < self.bband.lines.bot and not self.position:
        # 	self.redline = True

        # if self.dataclose > self.bband.lines.top and self.position:
        # 	self.blueline = True

        # #AVALIA POSSIBILIDADE DE ENTRAR
        # if self.dataclose > self.bband.lines.mid and not self.position and self.redline:
        #     print("AAAAAAAAAAAAAAAAAAAAAAAA")     	
        # 	# BUY, BUY, BUY!!! (with all possible default parameters)
        #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #     # Keep track of the created order to avoid a 2nd order
        #     self.order = self.buy()
            

        # if self.dataclose > self.bband.lines.top and not self.position:
        #     # BUY, BUY, BUY!!! (with all possible default parameters)
        #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #     # Keep track of the created order to avoid a 2nd order
        #     self.order = self.buy()

        # if self.dataclose < self.bband.lines.mid and self.position and self.blueline:
        #     # SELL, SELL, SELL!!! (with all possible default parameters)
        #     self.log('SELL CREATE, %.2f' % self.dataclose[0])
        #     self.blueline = False
        #     self.redline = False
        #     # Keep track of the created order to avoid a 2nd order
        #     self.order = self.sell()

        #MINHA TENTATIVA
        #AVALIA POSSIBILIDADE DE ENTRAR
        if self.dataclose >= self.bband.lines.top and not self.position:        	
        	# BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()
            self.vendido = True

        if self.dataclose <= self.bband.lines.bot and not self.position:
            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()
            self.comprado = True

        if self.dataclose <= self.bband.lines.mid and self.position and self.vendido:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])            
            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()
            self.vendido = False

        if self.dataclose >= self.bband.lines.mid and self.position and self.comprado:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])            
            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()
            self.comprado = False
