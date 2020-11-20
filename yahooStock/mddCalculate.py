from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
yf.pdr_override() # pandas data reader를 재정의

kospi = pdr.get_data_yahoo('^KS11', '2004-01-04')

window = 252
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()
# 윈도우 크기 만큼 못 미칠 경우 min_periods 지정한 개수만 만족하면 연산 수행
drawdown = kospi['Adj Close']/peak - 1.0
max_dd = drawdown.rolling(window, min_periods=1).min()

plt.figure(figsize=(9, 7))
plt.subplot(211)
kospi['Close'].plot(label='KOSPI', grid=True, legend=True)
plt.subplot(212)
drawdown.plot(c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(c='red', label='KOSPI MDD', grid=True, legend=True)
plt.show()

kospi_dpc = (kospi['Close']/kospi['Close'].shift(1) - 1)*100
kospi_dpc.iloc[0] = 0
print(kospi_dpc['2008-10-24'])