import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='blogapp'
    )
    print("Connection successful")
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if connection:
        connection.close()
