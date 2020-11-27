from Investar import Analyzer
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

mk = Analyzer.MarketDB()
df = mk.get_daily_price("엔씨소프트", "2017-01-01", "2020-05-01")

# 1. 시장 조류: 장기차트 분석
ema60 = df.close.ewm(span=60).mean()  # 12주 지수이평선
ema130 = df.close.ewm(span=130).mean()  # 26주 지수이평선

macd = ema60 - ema130 # macd
signal = macd.ewm(span=45).mean()
macdhist = macd - signal # macd  히스토그램

df=df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
print(df)
ohlc = df[['number', 'OPEN', 'high', 'low', 'close']]
print(ohlc)

ndays_high = df.high.rolling(window=14, min_periods=1).max()
ndays_low = df.low.rolling(window=14, min_periods=1).min()
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
slow_d = fast_k.rolling(window=3).mean()
df = df.assign(fast_k = fast_k, slow_d = slow_d).dropna()



plt.figure(figsize=(9, 7))
p1 = plt.subplot(3, 1, 1)
plt.title("Triple Trading")
plt.grid(True)

candlestick_ohlc(p1, ohlc.values, width=6, colorup='red', colordown= 'blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
for i in range(1, len(df.close)):
    # 좀 더 확실한 신호를 위해 %K가 아닌 %D를 사용
    if df.ema130.values[i-1] < df.ema130.values[i] and df.slow_d.values[i-1]>=20 and df.slow_d.values[i] < 20:
        plt.plot(df.number.values[i], 250000, 'r^')
    elif df.ema130.values[i-1] > df.ema130.values[i] and df.slow_d.values[i-1]<=80 and df.slow_d.values[i] > 80:
        plt.plot(df.number.values[i], 250000, 'bv')

plt.legend(loc='best')

p1 = plt.subplot(3, 1, 2)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='macd-hist')
plt.plot(df.number, df['macd'], color='b', label='macd')
plt.plot(df.number, df['signal'], 'g--', label='macd-signal')
plt.legend(loc='best')

p1 = plt.subplot(3, 1, 3)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100])
plt.legend(loc='best')
plt.show()

