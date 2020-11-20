import pymysql, urllib, calendar, time, json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from threading import Timer
import pandas as pd
from datetime import datetime
import passwdMaria

class DBUpdater:
    def __init__(self):
        # 1. 마리아 db연결 
        # 2. 종목코드 딕셔너리 생성
        self.conn = pymysql.connect(host='localhost', db='INVESTAR', user='root', passwd=passwdMaria.mariaDBPasswd, charset='utf8') #회사명이 한글일 수 있으므로 인코딩방식 설정

        with self.conn.cursor() as curs:
            sql = """
                CREATE TABLE IF NOT EXISTS company_info (
                    code VARCHAR(20),
                    company VARCHAR(40),
                    last_update DATE,
                    PRIMARY KEY (CODE)
                )
            """
            curs.execute(sql)
            sql = """
                CREATE TABLE if NOT EXISTS daily_price (
                    CODE VARCHAR(20),
                    DATE DATE,
                    OPEN BIGINT(20),
                    high BIGINT(20),
                    low  BIGINT(20),
                    close BIGINT(20),
                    diff BIGINT(20),
                    volume BIGINT(20),
                    PRIMARY KEY (CODE, DATE)
                )
            """
            curs.execute(sql)
        self.conn.commit()

        self.codes = dict()
        self.update_comp_info() # 메서드를 호출해 company_info를 업데이트 한다.

    def __del__(self):
        self.conn.close()

    def read_krx_code(self):
        # krx로부터 상장기업을 데이터프레임(krx)로 반환
        krx = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드':'code', '회사명':'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        # 종목코드 -> company_info에 업데이트 & 딕셔너리 저장
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn) # read_sql을 이용해 데이터를 불러온다.
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO company_info VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print('===end===')

    def read_naver(self, code, company, pages_to_fetch):
        # 네이버로부터 주식시세 -> DataFrame
        try:
            #1. 일자별 시세 마지막 페이지 값 구하기
            url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"
            with urlopen(url) as doc:
                html = BeautifulSoup(doc, 'lxml')
                pgrr = html.find('td', class_='pgRR')
                if pgrr is None:
                    return None
                last_page = pgrr.a['href'].split('=')[-1]
            df = pd.DataFrame()
            pages = min(int(last_page), pages_to_fetch) # 매개변수 or 마지막 페이지 중 작은 값

            for page in range(1, pages+1):
                pg_url = '{}&page={}'.format(url, page)
                df = df.append(pd.read_html(pg_url, header=0)[0]) #header: 가져온 테이블 중 첫 행을 데이터프레임 칼럼으로 설정
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.format(tmnow, company, code, page, pages), end="\r")
            df = df.rename(columns={'날짜':'date', '종가':'close', '전일비':'diff', '시가':'open', '고가':'high', '저가':'low', '거래량':'volume'})
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
            df = df[['date',  'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print('Exception : ', str(e))
            return None
        return df

    def replace_into_db(self, df, num, code, company):
        # 읽은 주식시세를 테이블에 저장
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO daily_price VALUES ('{code}', '{r.date}', '{r.open}', '{r.high}', '{r.low}', '{r.close}', '{r.diff}', '{r.volume}')"
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_price [OK]'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), num+1, company, code, len(df))) # len(df)는 일시 갯수(상장날짜 ~ 오늘)
    
    def update_daily_price(self, pages_to_fetch):
        # 위 두개 메서드를 이어준다.
        for idx, code in enumerate(self.codes):
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code])
    def execute_daily(self):
        # 실행 즉시 or 매일 오후 5시에 테이블 업데이트
        self.update_comp_info()
        try:
            with open('config.json', 'r') as in_file: # 한 페이지만 불러온다.
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError:
            with open('config.json', 'w') as out_file: # 파일이 없으면 첫 세팅을 100으로 한다.
                pages_to_fetch = 100
                config = {'pages_to_fetch':1}
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch)

        # 매일 오후 5시 업데이트
        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        if tmnow.month ==12 and tmnow.day == lastday: # 12월 31일인경우
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1, hour=17, minute=0, second=0) # 다음날 설정
        elif tmnow.day == lastday: # 그냥 매월 마지막일인 경우
            tmnext = tmnow.replace( month=tmnow.month+1, day=1, hour=17, minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0, second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds

        t = Timer(secs, self.execute_daily) #secs마다 호출
        print("Waiting for next update ({}) ... ".format(tmnext.strftime('%Y-%m-%d %H-%M')))

        t.start()

if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
    # dbu.update_comp_info()