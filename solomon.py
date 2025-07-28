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
        print("\n--- All Records ---")
        print("\n" + "=" * 110)
        print(" Student Grades Overview".center(110))
        print("=" * 110)
        print(f"{'Student Name': <25} {'Email':<30} {'Subject':<20} {'Term':<10} {'Grades':<8} {'Status':<10}")
        print("-" * 110)
        for name, email, subject, term, grade, status in records:
            print(f"{name:<25} {email:<30} {subject:<20} {term:<10} {str(grade) + '%':<8} {status:<10}")
        print("=" * 110)

    except mysql.connector.Error as err:
        print(f"Error viewing records: {err}")
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
        print("\n" + "=" * 110)
        print("Progress Report".center(110))
        print("\n" + "=" * 110)
        print(f"{'Student':<30} {'Subject':<40} {'Score':<10} {'Status':<20}")
        print("-" * 110)
        for name, subject, score in data:
            status = "🟢 Excellent" if score >= 70 else "🔴 Needs Help"
            print(f"{name:<30} {subject:<40} {str(score) + '%':<10} {status:<20}")

        print("\n" + "=" * 110)
        print("Subject Averages".center(110))
        print("-" * 110)
        for subject, avg in averages:
            print(f"{subject:<50}: {avg:.1f}%")
    except mysql.connector.Error as err:
        print(f"Error generating progress report: {err}")
    finally:
        cursor.close()
        conn.close()
# Search parent and send message
from db import get_connection
from effects import styled_input, type_print
import mysql.connector
from rich import print as console_print
from rich.console import Console

console = Console()


def search_message_parent(instructor_id):
    type_print("\n--- Send Message to Parent ---")
    student_name = styled_input("Enter Student's Name: ").strip()
    if not student_name:
        type_print("Error: Student name cannot be empty.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get student ID and parent ID
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


def view_parent_instructor_messages(parent_id, instructor_id, instructor_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sender_type, contents, timestamp FROM messages
            WHERE (sender_type = 'parent' AND sender_id = %s AND receiver_type = 'instructor' AND receiver_id = %s)
               OR (sender_type = 'instructor' AND sender_id = %s AND receiver_type = 'parent' AND receiver_id = %s)
            ORDER BY timestamp ASC
        """, (parent_id, instructor_id, instructor_id, parent_id))
        messages = cursor.fetchall()

        if not messages:
            console.print("💬 No previous messages yet.\n")
        else:
            console.print("\n[bold green]--- Message History ---[/bold green]")
            for sender_type, contents, timestamp in messages:
                sender = "🧑‍🏫 Instructor" if sender_type == 'instructor' else "👪 Parent"
                console.print(f"[{timestamp}] [bold]{sender}:[/bold] {contents}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        type_print(f"Error retrieving messages: {err}")


def send_message_from_parent(parent_id, instructor_id, student_id, instructor_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        message = styled_input(f"Write a new message to {instructor_name} (or type 'cancel'): ").strip()
        if message.lower() == 'cancel' or not message:
            type_print("Message canceled or empty.")
            return

        cursor.execute("""
            INSERT INTO messages (
                sender_type, sender_id,
                receiver_type, receiver_id,
                student_id, contents
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            'parent', parent_id,
            'instructor', instructor_id,
            student_id, message
        ))

        conn.commit()
        cursor.close()
        conn.close()
        type_print("Message sent to instructor.")

    except mysql.connector.Error as err:
        type_print(f"Error sending message: {err}")


def view_parent_responses(instructor_id):
    type_print("\n--- View Parent Responses ---")

    #instructor_id = 1  # You can replace this with dynamic ID in future
    parent_email = styled_input("Enter Parent Email: ").strip()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get parent and student details
        cursor.execute("""
            SELECT p.parent_id, s.student_id, s.student_names
            FROM parents p
            JOIN students s ON p.student_id = s.student_id
            WHERE p.parent_email = %s
        """, (parent_email,))
        result = cursor.fetchone()

        if not result:
            type_print("Parent or linked student not found.")
            return

        parent_id, student_id, student_name = result
        instructor_name = "Instructor"  # You can replace with dynamic name

        view_parent_instructor_messages(parent_id, instructor_id, instructor_name)

        send = styled_input("Do you want to reply to this parent? (yes/no): ").strip().lower()
        if send == "yes":
            send_message_from_parent(parent_id, instructor_id, student_id, instructor_name)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        type_print(f"Error handling parent messages: {err}")

def login_instructor():
    type_print("\n--- Instructor Login ---")
    email = styled_input("Email: ")
    password = styled_input("Password: ").encode("utf-8")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT instructor_id, instructor_password, instructor_name FROM instructors WHERE instructor_email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            instructor_id, hashed_pw, instructor_name = result
            if bcrypt.checkpw(password, hashed_pw.encode('utf-8')):
                type_print(f"\nWelcome back, {instructor_name}!")
                return instructor_id, instructor_name
            else:
                type_print("❌ Incorrect password.")
        else:
            type_print("❌ Instructor not found.")

    except mysql.connector.Error as err:
        type_print(f"Login error: {err}")

    return None, None


# Teacher dashboard for managing student records and communication
def teacher_dashboard(instructor_id, instructor_name):
    #instructor_id = 1
    # Initialize database
    create_tables()
    type_print("\nWelcome to the Teacher Dashboard!")
    # Main loop for dashboard menu
    while True:
        type_print("\n" + "="*35)
        type_print(" TEACHER DASHBOARD - ADMIN MENU")
        print("="*35)
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
            view_parent_responses(instructor_id)
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