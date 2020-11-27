from datetime import datetime
import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)
        print('aaa')


    def nofity_order(self, order):
        self.log("sss")
        # 주문의 변화가 있을 때마다 자동으로 실행
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            self.log("333")
            if order.isbuy():
                self.log(f'BUY : 주가 {order.executed.price:,.0f}, 수량 {order.executed.size:,.0f}, 수수료 {order.executed.comm:,.0f}, 자산 {cerebro.broker.get_value():,0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f'SELL : 주가 {order.executed.price:,.0f}, 수량 {order.executed.size:,.0f}, 수수료 {order.executed.comm:,.0f}, 자산 {cerebro.broker.get_value():,0f}')

            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log("ORDER CANCELED")
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self): # 지정된 기간동안 순차적으로 호출되는 함수
        if not self.position: # not in the market
            if self.rsi < 30:
                self.order = self.buy()

        else:
            if self.rsi > 70:
                self.order = self.sell()

    def log(self, txt, dt=None):
        print("$$$")
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

cerebro = bt.Cerebro() # 백트레이더의 핵심클래스, 데이터취합 및 테스트 수행 후 결과 출력
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS', fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
print(type(data.close))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print(f'Initial Portfolio Value : {cerebro.broker.get_value(): ,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value : {cerebro.broker.get_value():,.0f} KRW')
cerebro.plot(style='candlestick')

