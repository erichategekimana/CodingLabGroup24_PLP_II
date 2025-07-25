# signup.py
import bcrypt
from db import get_connection
from effects import type_print, loading_spinner, styled_input
from login import login


def signup():
    loading_spinner("Initialising")
    welcome = input("Press Enter to continue:")
    if welcome == '':
        type_print("==========================================================================="
            "\nWELCOME TO OUR STUDENT PROGRESS TRACKER APP😁"
            "\n==========================================================================="
            "\nSIGNUP TO CONTINUE TO OUR APP✍"
            "\n===========================================================================", delay=0.019)
    conn = get_connection()
    if not conn:
        print("Database connection failed.")
        return

    cursor = conn.cursor()
    role = styled_input("Are you signing up as a Teacher, Student or Parent? ").strip().lower()
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").encode("utf-8")
    #phone = input("Enter your phone number: ").strip()

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    try:
        if role == "parent":
            phone = input("Enter your phone number: ").strip()
            cursor.execute("""
                INSERT INTO parents (parent_name, password, parent_email, parent_phone)
                VALUES (%s, %s, %s, %s)
            """, (name, hashed_password, email, phone))

        elif role == "teacher":
            phone = input("Enter your phone number: ").strip()
            specialization = input("Enter your specialization: ").strip()
            cursor.execute("""
                INSERT INTO instructors (instructor_name, password, instructor_email, instructor_phone, specialization)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, hashed_password, email, phone, specialization))

        elif role == "student":
            parent_email = input("Enter your parent's email: ").strip()
            instructor_email = input("Enter your instructor's email: ").strip()

            # Get Parent_id
            cursor.execute("SELECT parent_id FROM parents WHERE parent_email = %s", (parent_email,))
            parent_result = cursor.fetchone()
            """if not parent_result:
                print("😔Parent email not found😔.")
                return"""
            parent_id = parent_result[0] if parent_result else None

            # Get Instructor_id
            cursor.execute("SELECT instructor_id FROM instructors WHERE instructor_email = %s", (instructor_email,))
            instructor_result = cursor.fetchone()
            """if not instructor_result:
                print("😔Instructor email not found😔.")
                return"""
            instructor_id = instructor_result[0] if instructor_result else None
            student_level = input("Enter your level/class: ").strip()

            cursor.execute("""
                INSERT INTO students (student_names, student_email, password, parent_id, instructor_id, student_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, hashed_password, parent_id, instructor_id, student_level))
        else:
            print("❌Invalid role. Please enter student, teacher or parent❌.")
            return

        conn.commit()
        print(f"{role.capitalize()} signed up successfully!")
        print("==========================================================================="
              "\n🙏🏿THANK YOU FOR REGISTERING TO OUR STUDENT PROGRESS TRACKER APP🙏🏿"
              "\n===========================================================================")
        choose = input("Do you want to proceed to log in? yes/no😁: ").lower().strip()
        if choose == 'yes':
            login()
        else:
            return

    except Exception as e:
        print("Signup failed:", e)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    signup()
