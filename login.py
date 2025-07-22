# login.py
import bcrypt
from database import connection

def verify_login(role, table, id_label):
    cursor = connection.cursor()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").encode("utf-8")

    query = f"SELECT * FROM {table} WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user:
        hashed_password = user[3].encode("utf-8")
        if bcrypt.checkpw(password, hashed_password):
            with open("session.txt", "w") as file:
                file.write(f"{id_label} id: {user[0]}")
            print(f"{role.capitalize()} logged in successfully!")
            from dashboard import dashboard
            dashboard()
        else:
            print("Incorrect password.")
    else:
        print(f"No {role} account found with that email.")

    cursor.close()

def login():
    role = input("Are you a Teacher, Student or Parent?\n(Choose one role): ").lower().strip()

    if role == "student":
        verify_login(role, "student", "Student")
    elif role == "teacher":
        verify_login(role, "instructors", "Teacher")
    elif role == "parent":
        verify_login(role, "parents", "Parent")
    else:
        print("Invalid role. Please choose either Student, Teacher, or Parent.")

if __name__ == "__main__":
    login()
