from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
yf.pdr_override() # pandas data reader를 재정의

sec = pdr.get_data_yahoo('005930.KS', start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')

sec_dpc = (sec['Close']/sec['Close'].shift(1) - 1)*100
sec_dpc.iloc[0] = 0
sec_dpc_cs = sec_dpc.cumsum()
print(sec_dpc.head())

msft_dpc = (msft['Close']/msft['Close'].shift(1) - 1)*100
msft_dpc.iloc[0] = 0
msft_dpc_cs = msft_dpc.cumsum()

plt.plot(sec_dpc_cs.index, sec_dpc_cs, 'b', label='Samsung')
plt.plot(msft_dpc_cs.index, msft_dpc_cs, 'r--', label='MS')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()