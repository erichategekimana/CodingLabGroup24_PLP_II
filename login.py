# login.py
import bcrypt
from db import get_connection

def verify_login(role):
    conn = get_connection()
    welcome = input("Press Enter to continue:")
    if welcome == '':
        print("==========================================================================="
              "\nWELCOME TO OUR STUDENT PROGRESS TRACKER APP😁"
              "\n==========================================================================="
              "\nLOGIN TO CONTINUE TO OUR APP✍"
              "\n===========================================================================")
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").encode("utf-8")

    try:
        if role == "student":
            cursor.execute("SELECT student_id, student_names, student_email, password FROM students WHERE student_email = %s", (email,))
        elif role == "teacher":
            cursor.execute("SELECT instructor_id, instructor_name, instructor_email, password FROM instructors WHERE instructor_email = %s", (email,))
        elif role == "parent":
            cursor.execute("SELECT parent_id, parent_name, parent_email, password FROM parents WHERE parent_email = %s", (email,))
        else:
            print("❌Invalid role❌.")
            return

        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[3].encode('utf-8')):
            with open("session.txt", "w") as f:
                f.write(f"{role.capitalize()} ID: {user[0]}")
            print(f"😁{role.capitalize()} logged in successfully!😁")
            print("==========================================================================="
                  "\n🙏🏿THANK YOU FOR REGISTERING TO OUR STUDENT PROGRESS TRACKER APP🙏🏿"
                  "\n===========================================================================")
            from Teacher import main
            main()
        else:
            print("❌Incorrect email or password❌.")

    except Exception as e:
        print("❌Login failed:", e,"❌")

    finally:
        cursor.close()
        conn.close()

def login():
    role = input("Are you a Teacher, Student or Parent?\n(Choose one role): ").lower().strip()

    if role in ["student", "teacher", "parent"]:
        verify_login(role)
    else:
        print("❌Invalid role. Please choose either Student, Teacher, or Parent❌.")

if __name__ == "__main__":
    login()
