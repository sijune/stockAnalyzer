import pymysql
import passwdDB

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR', user='root', passwd=passwdDB.DBPasswd, autocommit=True)

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()

print(result)

connection.close()