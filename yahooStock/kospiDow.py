import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats

yf.pdr_override()

dow = pdr.get_data_yahoo('TLT', '2002-07-30')
kospi = pdr.get_data_yahoo('^KS11', '2002-07-30')

# 변동률 비교
#dow = dow.Close / dow.Close.loc['2000-01-04'] * 100
#kospi = kospi.Close / kospi.Close.loc['2000-01-04'] * 100

# plt.figure(figsize=(9, 7))
# plt.plot(dow.index, dow, 'r--', label='Dow')
# plt.plot(kospi.index, kospi, 'b', label='KOSPI')
# plt.grid(True)
# plt.legend(loc='best')
# plt.show()


# 산점도
df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI':kospi['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')
print(df)
print(df.corr()) # 상관계수 출력

# plt.figure(figsize=(9, 7))
# plt.scatter(df['DOW'], df['KOSPI'], marker='.')
# plt.xlabel('DOW')
# plt.ylabel('KOSPI')
# plt.show()


# 회귀분석
regr = stats.linregress(df['DOW'], df['KOSPI']) #상관계수, 회귀함수 추출 가능
regr_line = f'KOSPI = {regr.slope:.2f} * DOW + {regr.intercept:.2f}'
print(regr_line)

plt.figure(figsize=(9, 7))
plt.plot(df.DOW, df.KOSPI, '.')
plt.plot(df.DOW, regr.slope * df.DOW + regr.intercept, 'r')
plt.legend(['DOW x KOSPI', regr_line])
plt.xlabel('DOW')
plt.ylabel('KOSPI')
plt.show()