import mysql.connector
from effects import loading_spinner, type_print

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql-spt-codinglabgroup24-alustudent-6f2b.c.aivencloud.com",
            user="avnadmin",
            password="",
            database="new_spt_database",
            port = 13891
        )
        return connection
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None

def create_tables():
    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        connection.commit()
        loading_spinner("Analysing")
        type_print("Database is connected successfully.")
    except mysql.connector.Error as err:
        print("Error during table creation:", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Call this only when needed
create_tables()
