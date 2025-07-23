import bcrypt
from db import connection


def register():
    cursor = connection.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ").encode('utf-8')
    email = input("Enter your Email: ")
    type_user = input("Enter if you are (user or parent): ").lower().strip()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    if type_user == 'user':
        parent_name = input("Enter your parent name: ")
        # Find parent_id from parents table
        cursor.execute(
            "SELECT parent_id FROM parents WHERE name = %s", (parent_name,))
        parent = cursor.fetchone()
        if parent:
            parent_id = parent[0]
            query = "INSERT INTO users (parent_id, name, password, email) VALUES (%s, %s, %s, %s)"
            values = (parent_id, username, hashed, email)
            cursor.execute(query, values)
            connection.commit()
            print("Student registered successfully.")
        else:
            print("Parent not found. Please ask your parent to register first.")
    elif type_user == 'parent':
        student_name = input("Enter your child's username: ")
        # Find user_id from users table
        cursor.execute(
            "SELECT user_id FROM users WHERE name = %s", (student_name,))
        student = cursor.fetchone()
        if student:
            student_id = student[0]
            query = "INSERT INTO parents (student_id, name, password, email) VALUES (%s, %s, %s, %s)"
            values = (student_id, username, hashed, email)
            cursor.execute(query, values)
            connection.commit()
            print("Parent registered successfully.")
        else:
            print("Student not found. Please ask your child to register first.")
    else:
        print("Invalid user type. Please enter 'user' or 'parent'.")

    cursor.close()


register()
