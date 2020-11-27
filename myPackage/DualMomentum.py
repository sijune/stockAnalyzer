import pymysql
from Investar import passwdDB
import pandas as pd

class DualMomentum:
    def __init__(self):
        # 종목코드를 위한 객체생
        self.mk = Analyzer.MarketDB()

    def get_rltv_momentum(self, start_date, end_date, stock_count):
        # 상대적으로 수익률이 좋은 종목 n개 추출
        connection = pymysql.connect(host='localhost', port='3306', db='INVESTAR', user='root', passwd=passwdDB.DBPasswd, charset='utf8')
        cursor = connection.cursor()

        # 매개변수로 들어온 값에 가장 가까운 시작날짜와 마지막 날짜 재계산
        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print("end_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        # rows에 차곡차곡 쌓는다
        rows=[]
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for i, code in enumerate(self.mk.codes):
            sql = f"select close from daily_price where code= '{code}' and date= '{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])

            sql = f"select close from daily_price where code= '{code}' and date= '{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])

            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])기

        df = pd.DataFrame(rows, columns = columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False) # 내림차순 정렬
        df = df.head(stock_count) # 상위 원하는 갯수만큼 기업 출
        df.index = pd.Index(range(stock_count))

        connection.close()
        print(df)
        print(f"\nRelative momentum ({start_date} ~ {end_date}) : {df['returns'].mean():.2f}% \n" )

        return df

    def get_abs_momentumn(self, rltv_momentum, start_date, end_date):
        stockList = list(rltv_momentum['code'])
        connection = pymysql.connect(host='localhost', port='3306', db='INVESTAR', user='root',
                                     passwd=passwdDB.DBPasswd, charset='utf8')
        cursor = connection.cursor()

        # 매개변수로 들어온 값에 가장 가까운 시작날짜와 마지막 날짜 재계산
        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print("end_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        # rows에 차곡차곡 쌓는다
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for i, code in enumerate(stockList):
            sql = f"select close from daily_price where code= '{code}' and date= '{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])

            sql = f"select close from daily_price where code= '{code}' and date= '{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])

            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])
            기

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)  # 내림차순 정렬
        df = df.head(stock_count)  # 상위 원하는 갯수만큼 기업 출
        df.index = pd.Index(range(stock_count))

        connection.close()
        print(df)
        print(f"\nAbsolute momentum ({start_date} ~ {end_date}) : {df['returns'].mean():.2f}% \n")
        return

