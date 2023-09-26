import pymysql.cursors
import time
from datetime import datetime

# Connect to the database
connection = pymysql.connect(host='192.168.2.50',
                            port=3309,
                            user='root',
                            password='123456',
                            database='ef_migrations_test',
                            cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO t_test(p1,p2,p3,p4,p5) values('1',2,STR_TO_DATE('"+datetime.now().strftime("%Y-%m-%d%H:%M:%S")+"','%Y-%m-%d'),'文本',12.45781)"
        cursor.execute(sql )

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM t_test"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)