import json
import pymysql
def to_mysql(i,x):
    """
    信息写入mysql
    """
    table=i
    keys =', '.join(x.keys())
    values = ', '.join(['%s'] * len(x))

    db = pymysql.connect(host='localhost', user='root', password='928587987', port=3306, db='gaokao')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(x.values())):
            print("Successful")
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()

def to_json(i,x):
    json_name_true=i
    with open(json_name_true,'a')as file:
        file.write(json.dumps(x,indent=1,ensure_ascii=False))