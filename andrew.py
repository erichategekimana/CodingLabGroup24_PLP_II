import os
import mysql.connector
from db import get_connection

def student_dashboard(student_id, student_names, student_email):
    """Display the student dashboard menu and handle user actions."""
    while True:
        print(f"\n--- Welcome, {student_names}! ---")
        print("1. View My Progress")
        print("2. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_my_progress(student_id, student_names, student_email)
        elif choice == "2":
            print("Logging out...\n")
            break
        else:
            print("Invalid Option. Please try again.")

def view_my_progress(student_id, student_names, student_email):
    """Fetch and display a student's academic progress."""
    conn = get_connection()
    #cursor = None
    try:
        """db_password = os.getenv("DB_PASSWORD")
        if not db_password:
            print("Error: Database password not found in environment variables.")
            return"""

        """conn = get_connection()"""


        cursor = conn.cursor()

        """cursor.execute("SELECT student_id, student_names FROM students WHERE student_email = %s", (student_email,))
        result = cursor.fetchone()

        if not result:
            print("Student not found.\n")
            return"""

        cursor.execute("""
            SELECT s.subject_name, g.grade, g.timestamp
            FROM grades g
            JOIN subjects s ON g.subject_id = s.subject_id
            WHERE g.student_id = %s
            ORDER BY g.timestamp DESC
        """, (student_id,))
        records = cursor.fetchall()

        if not records:
            print("No progress records found.\n")
            return

        print("\n--- {student_names}'s Progress ---")
        for subject, grade, timestamp in records:
            advice = "Needs Help" if grade < 50 else "Doing Well"
            print(f"Subject : {subject}")
            print(f"Grade   : {grade} → {advice}")
            print(f"Date    : {timestamp}\n")

    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

"""if __name__ == "__main__":
    print("Welcome to the Student Portal\n")
    student_name = input("Enter your full name: ").strip()
    student_id = input("Enter your student ID: ").strip()

    if not student_id.isdigit():
        print("Invalid student ID. Must be numeric.")
    else:
        student_dashboard(student_name, int(student_id))
def main():
    # Ensure the database is initialized before starting the dashboard
    try:
        student_dashboard()
    except Exception as e:
        print(f"Application error: {e}")
# Ensure the script runs only if executed directly
if __name__ == "__main__":
    main()
"""