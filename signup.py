# Connecting to the database and importing needed libraries
import bcrypt
import re
from db import get_connection
from effects import type_print, loading_spinner, styled_input
from login import login

# Function to handle Dashboard functionality
# Signup function to register new users
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def get_valid_email():
    while True:
        email = styled_input("Enter your email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
        else:
            return email

def get_valid_child_email():
    while True:
        email = styled_input("Enter your child's email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
        else:
            return email

def get_valid_instructor_email():
    while True:
        email = styled_input("Enter your instructor's email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
        else:
            return email

def get_valid_parent_email():
    while True:
        email = styled_input("Enter your parent's email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
        else:
            return email

def get_non_empty_input(prompt):
    while True:
        val = styled_input(prompt).strip()
        if not val:
            print("Input cannot be empty. Please try again.")
        else:
            return val

def signup():
    loading_spinner("Initialising")
    welcome = input("Press Enter to continue:")
    if welcome == '':
        print("=" * 70)
        print( "WELCOME TO OUR STUDENT PROGRESS APPLICATION TRACKER".center(70))
        print("*" * 70)
        print("SIGNUP TO CONTINUE TO STUDENT PROGRESS TRACKER DASHBOARD".center(70))
        print("=" * 70)
    conn = get_connection()
    if not conn:
        type_print("Database connection failed.")
        return

    cursor = conn.cursor()
    loading_spinner("Loading")
    role = get_non_empty_input("Are you signing up as a Teacher, Student or Parent? ").strip().lower()
    name = get_non_empty_input("Enter your full name: ")
    email = get_valid_email()
    password = get_non_empty_input("Enter your password: ").encode("utf-8")
    #phone = input("Enter your phone number: ").strip()

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    # Role-based signup logic

    try:
        # Parent signup
        if role == "parent":
            phone = get_non_empty_input("Enter your phone number: ").strip()
            cursor.execute("""
                INSERT INTO parents (parent_name, password, parent_email, parent_phone)
                VALUES (%s, %s, %s, %s)
            """, (name, hashed_password, email, phone))

            conn.commit()

            #fetch parent_id of the newly inserted parent
            cursor.execute("SELECT parent_id FROM parents WHERE parent_email = %s", (email,))
            new_parent_id = cursor.fetchone()[0]
            child_email = get_valid_child_email()

            cursor.execute("""UPDATE students SET parent_id = %s
                           WHERE student_email = %s AND parent_id IS NULL""", (new_parent_id, child_email))

            cursor.execute("SELECT student_id FROM students WHERE student_email = %s", (child_email,))
            student_id = cursor.fetchone()

            if student_id:
                cursor.execute("""UPDATE parents SET student_id = %s
                               WHERE parent_id = %s""", (student_id[0], new_parent_id))
                conn.commit()
            else:
                print("No Student found with that email. Cannot update the parent.")

        # Teacher signup
        elif role == "teacher":
            phone = get_non_empty_input("Enter your phone number: ").strip()
            specialization = get_non_empty_input("Enter your specialization: ").strip()
            cursor.execute("""
                INSERT INTO instructors (instructor_name, password, instructor_email, instructor_phone, specialization)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, hashed_password, email, phone, specialization))

            conn.commit()

            #getting instructor_id
            cursor.execute("SELECT instructor_id FROM instructors WHERE instructor_email = %s", (email,))
            new_instructor_id = cursor.fetchone()[0]

            #ask teacher what class they're teaching
            level = get_non_empty_input("What class/level are you teaching? ").strip()

            #update the students with this class have NULL instructor
            cursor.execute("""UPDATE students SET instructor_id = %s
                           WHERE student_level = %s AND instructor_id IS NULL""", (new_instructor_id, level))

        # Student signup
        # This is where we get the parent_id and instructor_id
        elif role == "student":
            parent_email = get_valid_parent_email()
            instructor_email = get_valid_instructor_email()

            # Get Parent_id
            cursor.execute("SELECT parent_id FROM parents WHERE parent_email = %s", (parent_email,))
            parent_result = cursor.fetchone()
            """if not parent_result:
                print("Parent email not found.")
                return"""
            parent_id = parent_result[0] if parent_result else None

            # Get Instructor_id
            cursor.execute("SELECT instructor_id FROM instructors WHERE instructor_email = %s", (instructor_email,))
            instructor_result = cursor.fetchone()
            """if not instructor_result:
                print("Instructor email not found.")
                return"""
            instructor_id = instructor_result[0] if instructor_result else None
            student_level = get_non_empty_input("Enter your level/class: ").strip()

            cursor.execute("""
                INSERT INTO students (student_names, student_email, password, parent_id, instructor_id, student_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, hashed_password, parent_id, instructor_id, student_level))
        else:
            type_print("Invalid role. Please enter student, teacher or parent.")
            return

        conn.commit()
        loading_spinner("Please Wait")
        type_print(f"{role.capitalize()} signed up successfully!")
        print("=" * 75)
        print("THANK YOU FOR LOGGING INTO OUR STUDENT PROGRESS APPLICATION TRACKER".center(75))
        print("=" * 75)
        choose = styled_input("Do you want to proceed to log in? yes/no: ").lower().strip()
        if choose == 'yes':
            loading_spinner("Alright")
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
