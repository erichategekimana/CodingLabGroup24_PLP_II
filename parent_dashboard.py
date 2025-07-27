from connection import conn
from rich.table import Table
from rich.console import Console
import sys

console = Console()

# Send message from parent to instructor


def send_message(parent_id, instructor_id, message):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_type, sender_id, receiver_type, receiver_id, message) VALUES (%s,%s,%s,%s,%s)",
        ('parent', parent_id, 'instructor', instructor_id, message)
    )
    conn.commit()
    cursor.close()
    console.print("✅ Message sent successfully!", style="green")

# Dashboard


def dashboard(parent_id):
    cursor = conn.cursor()
    console.print(
        "\n\n===============[bold underline] 😊 Welcome To Our Dashboard 😊 [/bold underline] ===============",
        style="bold green"
    )

    subject_option = {}

    while True:
        option = console.input("""\nPlease select an option:\n
                 [bold]1. View My Child's Progress Report 📊[/bold] \n
                 [bold]2. Chat with Instructor 💬[/bold]\n
                 [bold]3. Logout 🚪[/bold]\n
                 [bold] Enter your Choice:[/bold]
                   """)

        if option == '1':
            cursor.execute("""
                SELECT s.student_names, s.student_level, sub.subject_name, g.term, g.grade, g.status,
                       i.instructor_name, i.instructor_phone, i.instructor_id
                FROM parents p
                INNER JOIN students s ON p.student_id = s.student_id
                INNER JOIN grades g ON s.student_id = g.student_id
                INNER JOIN subjects sub ON g.subject_id = sub.subject_id
                INNER JOIN instructors i ON s.instructor_id = i.instructor_id
                WHERE p.parent_id = %s
            """, (parent_id,))
            results = cursor.fetchall()

            if not results:
                console.print(
                    "⚠️ No Progress Found for your child!", style="bold red")
            else:
                console.print(
                    "\n📊 [bold underline] Student Progress Dashboard [/bold underline]",
                    style="blue"
                )
                table = Table(title="📚 Child Academic Progress",
                              header_style="bold magenta")
                table.add_column("Student Name", style="cyan")
                table.add_column("Student Level", style="green")
                table.add_column("Subject", style="yellow")
                table.add_column("Term", style="blue")
                table.add_column("Score %", style="magenta")
                table.add_column("Status", style="red")
                table.add_column("Teacher Name", style="white")
                table.add_column("Teacher PhoneNumber", style="white")

                subject_option = {}

                for student_name, student_level, subject_name, term, grade, status, instructor_name, instructor_phone, instructor_id in results:
                    table.add_row(student_name, student_level, subject_name,
                                  term, str(grade), status, instructor_name, instructor_phone)
                    subject_option[subject_name.lower()] = (
                        instructor_name, instructor_id)

                console.print(table)
                print("\n\n")

        elif option == '2':
            if not subject_option:
                console.print(
                    "⚠️ Please view progress report first to get subjects.", style="bold red")
                continue

            console.print("Available Subjects to Chat:")
            for subj in subject_option:
                console.print(f"- {subj.capitalize()}")

            choice = console.input(
                "Enter Subject name or 'back' to go back: ").strip().lower()
            if choice == 'back':
                continue

            if choice not in subject_option:
                console.print("❌ Subject not found.", style="bold red")
                continue

            instructor_name, instructor_id = subject_option[choice]

            console.print(
                f"\n📖 [bold cyan] Chat History with {instructor_name} [/bold cyan]")

            cursor.execute("""
                SELECT sender_type, message, timestamp FROM messages
                WHERE (sender_type = 'parent' AND sender_id = %s AND receiver_type = 'instructor' AND receiver_id = %s)
                   OR (sender_type = 'instructor' AND sender_id = %s AND receiver_type = 'parent' AND receiver_id = %s)
                ORDER BY timestamp ASC
            """, (parent_id, instructor_id, instructor_id, parent_id))
            messages = cursor.fetchall()

            if not messages:
                console.print("💬 No previous messages yet.\n")
            else:
                for sender_type, content, timestamp in messages:
                    sender = "🧑‍🏫 Instructor" if sender_type == 'instructor' else "👪 You"
                    console.print(
                        f"[{timestamp}] [bold] {sender}: [/bold] {content}")

            new_msg = console.input(
                f"Write a new message to {instructor_name} (or type 'cancel'): ").strip()
            if new_msg.lower() != 'cancel' and new_msg:
                send_message(parent_id, instructor_id, new_msg)

        elif option == '3':
            console.print("👋 Logging out. Goodbye!", style="bold green")
            sys.exit()

        else:
            console.print(
                "❌ Invalid choice. Please Enter 1, 2 or 3.", style="bold red")


console.print(
    "\n\n\n[bold green]======================THANK YOU 😊 ====================[/bold green]")
