import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='自己数据库的密码', port=3306)
cursor = db.cursor()
cursor.execute("CREATE DATABASE gaokao DEFAULT CHARACTER SET utf8mb4")
db.close()