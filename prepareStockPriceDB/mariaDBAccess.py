import pymysql
import passwdMaria

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR', user='root', passwd=passwdMaria.mariaDBPasswd, autocommit=True)

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()

print(result)

connection.close()