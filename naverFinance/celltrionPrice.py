import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from matplotlib import pyplot as plt
import mplfinance as mpf

# 종목코드 가져오기
krx_list = pd.read_html('C:/Users/SijuneLee/Desktop/practice/naverFinance/상장법인목록.xlsx')
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]

df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by='종목코드')
# print(df)

# 네이버에서 크롤링하기
#1. 일자별 시세 마지막 페이지 값 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    last_page = pgrr.a['href'].split('=')[-1]
    print(last_page)

#2. 일자별 시세 구하기
df2 = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    print(page)
    page_url = '{}&page={}'.format(sise_url, page)
    df2 = df2.append(pd.read_html(page_url, header=0)[0])


#3. 종가 기준으로 그래프 출력
df2 = df2.dropna()
df2 = df2.iloc[0:30] # 30개만 가져오겠다.
df2 = df2.sort_values(by='날짜')

#plt.title('Celltrion Chart')
#plt.xticks(rotation=45)
#plt.plot(df2['날짜'], df2['종가'], 'co--')
#plt.grid(color='gray', linestyle='--')
#plt.show()

#4. 캔들 차트 출력
df3 = df2.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df3 = df3.sort_values(by='Date')
df3.index = pd.to_datetime(df3.Date)
df3 = df3[['Open', 'High', 'Low', 'Close', 'Volume']]

#mpf.plot(df3, title='Celltrion Candle Chart', type='candle') # 한 줄로 캔들차트 출력할 수 있다.
kwargs = dict(title='Celltrion Candle Chart', type='candle', mav=(2,4,6), volume=True, ylabel='ohlc candles')
#mav는 이평선
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df3, **kwargs, style=s)