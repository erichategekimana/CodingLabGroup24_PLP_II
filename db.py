import mysql.connector
from mysql.connector import Error

# create connection between app and database(remote server)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=" mysql-spt-codinglabgroup24-alustudent-6f2b.c.aivencloud.com",
            user="avnadmin",
            password="AVNS_u8Js2pj4YWqsyGRmsBr",
            database="ydefaultdb",
            port=13891 
        )
        return connection
    except Error as e:
        print()
        print(f"Database connection failed: {e}")
        print("Try again later! ")
        print()
        return None