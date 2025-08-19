# mi_estrategia.py
import backtrader as bt
import backtrader.feeds as btfeeds

class MiEstrategia(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def next(self):
        self.log(f'Close, {self.dataclose[0]}')
        if self.position.size == 0:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('COMPRA CREADA')
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('VENTA CREADA')
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'COMPRA EJECUTADA, Precio: {order.executed.price:.2f}, Costo: {order.executed.value:.2f}, Comisión: {order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'VENTA EJECUTADA, Precio: {order.executed.price:.2f}, Costo: {order.executed.value:.2f}, Comisión: {order.executed.comm:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Orden Cancelada/Rechazada/Margen')
        self.order = None

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MiEstrategia)
    
    # Descarga de datos de ejemplo
    data = btfeeds.YahooFinanceCSVData(
        dataname='oracle.csv',
        fromdate=bt.datetime.datetime(2000, 1, 1),
        todate=bt.datetime.datetime(2000, 12, 31)
    )
    
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    
    print('Capital Inicial: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Capital Final: %.2f' % cerebro.broker.getvalue())
    
    # Para guardar el gráfico en un archivo en lugar de mostrarlo
    cerebro.plot(style='candlestick', iplot=False, savefig=True, figfilename='resultado_backtest.png')