# signup.py
import bcrypt
import sys
from database import connection

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def get_common_inputs():
    username = input("Enter your Full Name: ").strip()
    email = input("Enter your Email: ").strip()
    password = input("Enter your Password: ").strip()
    return username, email, password

def signup():
    cursor = connection.cursor()
    choice = input("Are you a Teacher, Student or Parent?\n(Choose one role): ").lower().strip()

    if choice == "student":
        username, email, password = get_common_inputs()
        hashed = hash_password(password)
        classroom = input("Enter your classroom (e.g. Primary 6, Senior 3): ").strip()
        query = "INSERT INTO student (name, email, password, classroom) VALUES (%s, %s, %s, %s)"
        values = (username, email, hashed, classroom)
        cursor.execute(query, values)
        connection.commit()
        print("Student account created successfully!")

    elif choice == "teacher":
        username, email, password = get_common_inputs()
        hashed = hash_password(password)
        subject = input("Enter your subject specialty (e.g. Science, BEL): ").strip()
        query = "INSERT INTO instructors (name, email, password, subject) VALUES (%s, %s, %s, %s)"
        values = (username, email, hashed, subject)
        cursor.execute(query, values)
        connection.commit()
        print("Teacher account created successfully!")

    elif choice == "parent":
        username, email, password = get_common_inputs()
        hashed = hash_password(password)
        phone_number = input("Enter your phone number: ").strip()
        query = "INSERT INTO parents (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
        values = (username, email, hashed, phone_number)
        cursor.execute(query, values)
        connection.commit()
        print("Parent account created successfully!")

        proceed = input("Do you want to proceed to log in? (yes/no): ").lower().strip()
        if proceed == 'yes':
            from login import login
            login()
        else:
            print("Exiting. Have a nice day!")
            sys.exit()

    else:
        print(f"'{choice}' is not a valid role. Please enter either Student, Teacher or Parent.")

    cursor.close()

if __name__ == "__main__":
    signup()
