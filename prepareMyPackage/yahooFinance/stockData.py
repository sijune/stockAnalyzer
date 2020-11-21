from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
yf.pdr_override() # pandas data reader를 재정의

sec = pdr.get_data_yahoo('005930.KS', start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')

# print(sec.head(10))
# tmp_msft = msft.drop(columns='Volume')
# print(tmp_msft.tail())

# print(sec.index)

# print(sec.columns)

plt.plot(sec.index, sec.Close, 'b', label='Samsung')
plt.plot(msft.index, msft.Close, 'r--', label='MS')
plt.legend(loc='best')
plt.show()