import mysql.connector
from mysql.connector import Error

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="amir",
        passwd="password",
        auth_plugin='mysql_native_password',
    )

    my_cursor = mydb.cursor()

    my_cursor.execute("CREATE DATABASE IF NOT EXISTS flask_tutorial")

    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        print(db)
except Error as e:
    print("Error while connecting to MySQL", e)