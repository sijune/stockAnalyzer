import pymysql
import pandas as pd
from datetime import datetime
from datetime import timedelta
import re
import passwdDB

class MarketDB:
    # 해당 클래스에서는 codes변수와 get_daily_price 메소드를 사용한다.

    def __init__(self):
        # DB연결 및 종목코드 딕셔너리 생성
        self.conn = pymysql.connect(host='localhost', user='root', password=passwdDB.DBPasswd, db='INVESTAR', charset='utf8')
        self.codes={}
        self.get_comp_info()

    def __del__(self):
        # DB해제
        self.conn.close()

    def get_comp_info(self):
        #company_info 에서 데이터 읽어와 딕셔너리에 저장
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]

    def get_daily_price(self, code, start_date=None, end_date=None):
        # 종목별 시세를 데이터프레임 형태로 반환

        #기본값 설정
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print("start_date is initialized to '{}'".format(start_date))
        else:
            start_lst = re.split('\D+', start_date) # 숫자가 아닌 문자열
            if start_lst[0] == '':
               start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError : start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError : start_month({start_month:d}) is wrong.")
                return 
            if start_day < 1 or start_day > 31:
                print(f"ValueError : start_day({start_day:d}) is wrong.")
                return 
            start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}"

        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            print("end_date is initialized to '{}'".format(end_date))
        else:
            end_lst = re.split('\D+', end_date) # 숫자가 아닌 문자열
            if end_lst[0] == '':
               end_lst = end_lst[1:]
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1900 or end_year > 2200:
                print(f"ValueError : end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError : end_month({end_month:d}) is wrong.")
                return 
            if end_day < 1 or end_day > 31:
                print(f"ValueError : end_day({end_day:d}) is wrong.")
                return 
            end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}"
        
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())
        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print("ValueError: Code({}) doesn't exist.".format(code))

        # 실제 메서드 내용
        sql = f"SELECT * FROM daily_price WHERE code = '{code}' AND date >= '{start_date}' AND date <= '{end_date}'"
        df=pd.read_sql(sql, self.conn)
        df.index = df['DATE']
        return df

