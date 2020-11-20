from Investar import Analyzer

mk = Analyzer.MarketDB()
stockList = mk.get_daily_price('삼성전자', '2019-09-30', '2019.10.4')
print(stockList)