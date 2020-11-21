import matplotlib.pyplot as plt
from Investar import Analyzer

#시세 조회
mk = Analyzer.marketDB()
df = mk.get_daily_price('005930', '2017-07-10', '2018-06-30')

plt.figure(figsize=(9, 6))
plt.subplot(2,1,1)
plt.plot(df.index, df['close'], 'c', label='Close')
plt.legend(loc='best')
plt.subplot(2,1,2)
plt.bar(df.index, df['Volume'], clor='g', label='Volume')
plt.legend(loc='best')
plt.show()