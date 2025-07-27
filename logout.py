from database import connection
import os


def logout():
    cursor = connection.cursor()
    if os.path.exists('session.txt'):
        os.remove('session.txt')
        print("logged out successfully.")
    else:
        print("you are not logged out")
    cursor.close()


logout()
