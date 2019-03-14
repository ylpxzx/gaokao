import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='自己数据库的密码', port=3306, db='gaokao')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS school_data(id VARCHAR(255) NOT NULL,school_img VARCHAR(255) NOT NULL, school_type VARCHAR(255) NOT NULL, school_subjection VARCHAR(255) NOT NULL, school_nature VARCHAR(255) NOT NULL,school_url VARCHAR(255) NOT NULL,next_url VARCHAR(255) NOT NULL,local_name VARCHAR(255) NOT NULL,PRIMARY KEY (id))'
#sql = 'CREATE TABLE IF NOT EXISTS school_fenshu_data (id VARCHAR(255) NOT NULL,year VARCHAR(255) NOT NULL, low VARCHAR(255) NOT NULL, high VARCHAR(255) NOT NULL, ave VARCHAR(255) NOT NULL,num VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL)'
cursor.execute(sql)
db.close()