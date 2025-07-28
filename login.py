# login.py
import bcrypt
from db import get_connection
from effects import type_print, loading_spinner, styled_input

def verify_login(role):
    loading_spinner("Initialising✍🏿")
    conn = get_connection()
    welcome = styled_input("Press Enter to continue:")
    if welcome == '':
        print("==========================================================================="
              "\nWELCOME TO OUR STUDENT PROGRESS TRACKER APP😁"
              "\n==========================================================================="
              "\nLOGIN TO CONTINUE TO OUR APP✍"
              "\n===========================================================================")
    if not conn:
        type_print("Database connection failed.")
        return
    loading_spinner("Loading👉🏿")
    cursor = conn.cursor()
    email = styled_input("Enter your email: ").strip()
    password = styled_input("Enter your password: ").encode("utf-8")

    try:
        if role == "student":
            cursor.execute("SELECT student_id, student_names, student_email, password FROM students WHERE student_email = %s", (email,))
        elif role == "teacher":
            cursor.execute("SELECT instructor_id, instructor_name, instructor_email, password FROM instructors WHERE instructor_email = %s", (email,))
        elif role == "parent":
            cursor.execute("SELECT parent_id, parent_name, parent_email, password FROM parents WHERE parent_email = %s", (email,))
        else:
            type_print("❌Invalid role❌.")
            return

        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[3].encode('utf-8')):
            loading_spinner("Checking😁")
            with open("session.txt", "w") as f:
                f.write(f"{role.capitalize()} name: {user[1]}")
            type_print(f"😁{role.capitalize()} logged in successfully!😁")
            print("==========================================================================="
                  "\n🙏🏿THANK YOU FOR REGISTERING TO OUR STUDENT PROGRESS TRACKER APP🙏🏿"
                  "\n===========================================================================")
            if role == "teacher":
                from solomon import teacher_dashboard
                teacher_dashboard(user[0], user[1])
            elif role == "student":
                from andrew import student_dashboard
                student_dashboard(user[0], user[1], user[2])
            elif role == "parent":
                from ange import dashboard
                dashboard(user[0])
            #main()
        else:
            type_print("❌Incorrect email or password❌.")

    except Exception as e:
        type_print(f"❌Login failed:, {e} ❌")

    finally:
        cursor.close()
        conn.close()

def login():
    loading_spinner("Initialising😁")
    role = styled_input("Are you a Teacher, Student or Parent?\n(Choose one role): ").lower().strip()

    if role in ["student", "teacher", "parent"]:
        verify_login(role)
    else:
        type_print("❌Invalid role. Please choose either Student, Teacher, or Parent❌.")

if __name__ == "__main__":
    login()
