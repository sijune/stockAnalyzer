import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('SK하이닉스', '2018-11-02', '2019-12-30')

# 볼린저 밴드 지
df['MA20'] = df['close'].rolling(window=20).mean()
print(df['MA20'])
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + df['stddev']*2
df['lower'] = df['MA20'] - df['stddev']*2
df['PB'] = (df['close']-df['lower']) / (df['upper']-df['lower'])
df['bandwidth'] = (df['upper']-df['lower']) / (df['MA20']) * 100

# 현금 흐름 지표
df['TP'] = (df.high + df.close + df.low) / 3
df['PMF'] = 0
df['NMF'] = 0

for i in range(len(df.close)-1):
    if df.TP.values[i] < df.TP.values[i+1]:
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i + 1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i + 1] = 0
df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
df['MF10'] = 100-100/(1+df.MFR)

# 일중 강도 지표
df['II'] = (2*df.close - df.high - df.low) / (df.high-df.low) * df.volume
df['IIP21'] = df.II.rolling(window=21).sum() / df.volume.rolling(window=21).sum() * 100
df = df.dropna()

print(df)

# 볼린저 밴드표 Plot
plt.figure(figsize=(9, 11))
plt.subplot(3,1,1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving Average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
# for i in range(len(df.close)):
#     if df.PB.values[i] > 0.8 and df.MF10.values[i] > 80:
#         plt.plot(df.index.values[i], df.close.values[i], 'r^')
#     elif df.PB.values[i] < 0.2 and df.MF10.values[i] < 20:
#         plt.plot(df.index.values[i], df.close.values[i], 'bv')
for i in range(len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')
plt.title('Bollinger Band')

# %B Plot
plt.subplot(3,1,2)
plt.plot(df.index, df['PB']*100, color='b', label='%B')
plt.plot(df.index, df.MF10, 'g--', label='MF10')
plt.grid(True)
# for i in range(len(df.close)):
#     if df.PB.values[i] > 0.8 and df.MF10.values[i] > 80:
#         plt.plot(df.index.values[i], 0, 'r^')
#     elif df.PB.values[i] < 0.2 and df.MF10.values[i] < 20:
#         plt.plot(df.index.values[i], 0, 'bv')
plt.legend(loc='best')
plt.title('Bollinger Band %B')

# 밴드폭 Plot
# plt.subplot(3,1,3)
# plt.plot(df.index, df['bandwidth'], color='m', label='bandwidth')
# plt.grid(True)
# plt.legend(loc='best')
# plt.title('Bollinger Band Bandwidth')

# 일중강도율
plt.subplot(3,1,3)
plt.bar(df.index, df.IIP21, color='g', label='IIP21')
plt.grid(True)
for i in range(len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv')
plt.legend(loc='best')
plt.title('II21')

plt.show()