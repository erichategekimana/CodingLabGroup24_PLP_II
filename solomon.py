import mysql.connector
import bcrypt
from db import get_connection
from db import create_tables
from datetime import datetime
from effects import type_print, loading_spinner, styled_input

# Add new student record
def add_student_record(instructor_id):
    # Establish database connection and insert record
    try:
        conn = get_connection()
        cursor = conn.cursor()
        from datetime import datetime
        type_print("\n --- Add Student Grade ---")
        is_new = styled_input("Is this a new student? (yes/no): ").strip().lower()

        if is_new == 'yes':
            # Add new student
            type_print("\n--- Add New Student Record ---".upper())
            student_names = styled_input("Student Name: ").strip() # Validate student name input
            if not student_names:
                type_print("Error: Student name cannot be empty.")
                return
            student_email = styled_input("Student Email: ")
            password = styled_input("Student password: ").encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            student_level = styled_input("Student Level: ")

            cursor.execute(''' INSERT INTO students (student_names, student_email, password, student_level, instructor_id)
                        VALUES (%s, %s, %s, %s, %s)''', (student_names, student_email, hashed_password, student_level, instructor_id))
            conn.commit()
            type_print("New Student Added")

        else:
            # Use existing student
            student_email = styled_input("Enter the student email: ").strip()

            # Geting his/her id (in both cases)
        cursor.execute("SELECT student_id, student_names FROM students WHERE student_email = %s", (student_email,))
        result = cursor.fetchone()

        if not result:
            type_print(" Student not found. Please add them first.")
            return
        student_id = result[0] if result else None
        student_names = result[1] if result else None

        # SUBJECT

        subject = styled_input("Subject: ").strip().lower()
        if not subject:
            type_print("Error: Subject cannot be empty.")
            return
        # checking if the subject already exists
        cursor.execute('SELECT subject_id FROM subjects WHERE subject_name = %s AND instructor_id = %s', (subject, instructor_id))

        existing_subject = cursor.fetchone()

        if existing_subject:
            subject_id = existing_subject[0]
        else:
            cursor.execute('INSERT INTO subjects (subject_name, instructor_id) VALUES (%s, %s)',
                           (subject, instructor_id))
            conn.commit()
            subject_id = cursor.lastrowid
            type_print("Subject added.")

        # Add grade
    # Validate score input
        term = styled_input("Enter term (Term 1, Term 2, Term 3): ").strip()
        while True:
            try:
                score = int(styled_input("Score (0-100): "))
                if 0 <= score <= 100:
                    break
                type_print("Error: Score must be between 0 and 100.")
            except ValueError:
                type_print("Error: Please enter a valid number.")
    # Get current date
        #date = datetime.now().strftime("%Y-%m-%d")
        status = "Pass" if score >= 50 else "Fail"
        # Preventing duplicate grade for same subject/term
        cursor.execute(''' SELECT * FROM grades WHERE student_id = %s AND subject_id = %s AND term = %s''', (student_id, subject_id, term))
        if cursor.fetchone():
            type_print("Grade for this subject and term already exists.")
            return

        # INSERT GRADE
        cursor.execute('''
            INSERT INTO grades (student_id, subject_id, instructor_id, term, grade, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (student_id, subject_id, instructor_id, term, score, status))
        conn.commit()
        cursor.close()
        conn.close()
        type_print(f"Added {student_names}'s {subject} score!")
    except mysql.connector.Error as err:
        type_print(f"Error adding student: {err}")

# View all records
def view_records(instructor_id):
    type_print("\n--- View All Records ---".upper())
    # Check if there are any records to view
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT s.student_names, s.student_email, sub.subject_name, g.term, g.grade, g.status FROM students s
                       JOIN grades g ON s.student_id = g.student_id
                       JOIN subjects sub ON g.subject_id = sub.subject_id
                       WHERE g.instructor_id = %s
                       ORDER BY s.student_names, g.term''', (instructor_id,))
        records = cursor.fetchall()



        if not records:
            type_print("\nNo records found.")
            return
# Print all records
        type_print("\n--- All Records ---")
        type_print("\n" + "=" * 110)
        type_print(" Student Grades Overview".center(110))
        type_print("=" * 110)
        type_print(f"{'Student Name': <25} {'Email':<30} {'Subject':<20} {'Term':<10} {'Status':<10}")
        type_print("-" * 110)
        for name, email, subject, term, grade, status in records:
            type_print(f"{name:<25} {email:<30} {subject:<20} {term:<10} {str(grade) + '%':<8} {status:<10}")
        type_print("=" * 110)

    except mysql.connector.Error as err:
        type_print(f"Error viewing records: {err}")
    finally:
        cursor.close()
        conn.close()
# Generate progress report
def progress_report(instructor_id):
    # Check if there are any records to analyze
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Getting student grade data
        cursor.execute('''SELECT s.student_names, sub.subject_name, g.grade FROM students s
                       JOIN grades g ON s.student_id = g.student_id
                       JOIN subjects sub ON g.subject_id = sub.subject_id
                       WHERE g.instructor_id = %s''', (instructor_id,))
        data = cursor.fetchall()

        # Get subject averages
        cursor.execute('''SELECT sub.subject_name, AVG(g.grade)
                       FROM grades g
                       JOIN subjects sub ON g.subject_id = sub.subject_id
                       WHERE g.instructor_id = %s
                       GROUP BY sub.subject_name''', (instructor_id,))
        averages = cursor.fetchall()

# Analyze data and print report
        if not data:
            type_print("\nNo records to analyze.")
            return
# Check if averages are empty
        if not averages:
            type_print("\nNo subject averages available.")
            return
        type_print("\n" + "=" * 110)
        type_print("Progress Report".center(110))
        type_print("\n" + "=" * 110)
        type_print(f"{'Student':<30} {'Subject':<50} {'Score':<10} {'Status':<20}")
        type_print("-" * 110)
        for name, subject, score in data:
            status = "🟢 Excellent" if score >= 70 else "🔴 Needs Help"
            type_print(f"{name:<30} {subject:<40} {str(score) + '%':<10} {status:<20}")

        type_print("\n" + "=" * 110)
        type_print("Subject Averages".center(110))
        type_print("-" * 110)
        for subject, avg in averages:
            type_print(f"{subject:<50}: {avg:.1f}%")
    except mysql.connector.Error as err:
        type_print(f"Error generating progress report: {err}")
    finally:
        cursor.close()
        conn.close()
# Search parent and send message
def search_message_parent(instructor_id):
    type_print("\n--- Send Message to Parent ---")
    student_name = styled_input("Enter Student's Name: ").strip()
    if not student_name:
        type_print("Error: Student name cannot be empty.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get student ID
        cursor.execute("SELECT student_id, parent_id FROM students WHERE student_names = %s", (student_name,))
        student_data = cursor.fetchone()
        if not student_data:
            type_print("Student not found.")
            return

        student_id, parent_id = student_data

        message = styled_input("Enter Message: ").strip()
        if not message:
            type_print("Error: Message cannot be empty.")
            return

        cursor.execute("""
            INSERT INTO messages (
                sender_type, sender_id,
                receiver_type, receiver_id,
                student_id, contents
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            'instructor', instructor_id,
            'parent', parent_id,
            student_id, message
        ))

        conn.commit()
        cursor.close()
        conn.close()

        type_print(f"Message sent to Parent ID {parent_id} for Student '{student_name}'.")

    except mysql.connector.Error as err:
        type_print(f"Error sending message: {err}")

def view_parent_responses():
    # Check if there are any parent responses to view
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM parent_responses ORDER BY date DESC')
        responses = cursor.fetchall()
        cursor.close()
        conn.close()
        # Check if there are any responses
        if not responses:
            type_print("\nNo parent responses yet.")
            return

        type_print("\n--- Parent Responses ---")
        for row in responses:
            type_print(f"{row[1]} responded on {row[3]}: {row[2]}")
    except mysql.connector.Error as err:
        type_print(f"Error viewing parent responses: {err}")
        return
# Teacher dashboard for managing student records and communication
def teacher_dashboard():
    instructor_id = 1
    # Initialize database
    create_tables()
    type_print("\nWelcome to the Teacher Dashboard!")
    # Main loop for dashboard menu
    while True:
        type_print("\n" + "="*35)
        type_print(" TEACHER DASHBOARD - ADMIN MENU")
        type_print("="*35)
        type_print("1. Add New Student Record")
        type_print("2. View All Records")
        type_print("3. Generate Progress Report")
        type_print("4. Search Parent and Send Message")
        type_print("5. View Parent Responses")
        type_print("6. Logout")
        # Get user choice
        choice = styled_input("\nSelect option (1-6): ").strip()
        if choice == "1":
            add_student_record(instructor_id)
        elif choice == "2":
            view_records(instructor_id)
        elif choice == "3":
            progress_report(instructor_id)
        elif choice == "4":
            search_message_parent(instructor_id)
        elif choice == "5":
            view_parent_responses()
        elif choice == "6":
            type_print("Logging out...")
            break
        else:
            type_print("Invalid option. Try again.")
# Main function to initialize database and start dashboard
def main():
    # Ensure the database is initialized before starting the dashboard
    try:
        create_tables()
        teacher_dashboard()
    except Exception as e:
        type_print(f"Application error: {e}")
# Ensure the script runs only if executed directly
if __name__ == "__main__":
    main()