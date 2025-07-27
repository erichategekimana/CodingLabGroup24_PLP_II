import bcrypt
from connection import conn


def register():
    cursor = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ").encode('utf-8')
    email = input("Enter your email: ")
    type_user = input("Enter if you are (user or parent): ").lower().strip()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    if type_user == 'user':
        parent_name = input("Enter your parent name: ")

        # Check if the parent already exists
        cursor.execute(
            "SELECT parent_id FROM parents WHERE name = %s", (parent_name,))
        parent = cursor.fetchone()
        parent_id = parent[0] if parent else None

        # Register the student (with or without parent_id)
        query = "INSERT INTO users (parent_id, name, password, email) VALUES (%s, %s, %s, %s)"
        values = (parent_id, username, hashed, email)
        cursor.execute(query, values)
        conn.commit()
        print("Student registered successfully.")

        # If parent is found, update their student_id now
        if parent:
            # Get the new student user_id
            cursor.execute(
                "SELECT user_id FROM users WHERE name = %s", (username,))
            student = cursor.fetchone()
            if student:
                student_id = student[0]
                cursor.execute(
                    "UPDATE parents SET student_id = %s WHERE parent_id = %s", (student_id, parent_id))
                conn.commit()
                print("Parent record updated with student's ID.")

        else:
            print("Note: Parent not found. Parent can be linked later after registering.")

    elif type_user == 'parent':
        student_name = input("Enter your child's username: ")

        # Register the parent first (without student_id)
        query = "INSERT INTO parents (student_id, name, password, email) VALUES (%s, %s, %s, %s)"
        values = (None, username, hashed, email)
        cursor.execute(query, values)
        conn.commit()

        # Get the new parent_id
        cursor.execute(
            "SELECT parent_id FROM parents WHERE name = %s", (username,))
        parent = cursor.fetchone()

        # Check if the student exists
        cursor.execute(
            "SELECT user_id FROM users WHERE name = %s", (student_name,))
        student = cursor.fetchone()

        if student and parent:
            student_id = student[0]
            parent_id = parent[0]

            # Update parent's student_id
            cursor.execute(
                "UPDATE parents SET student_id = %s WHERE parent_id = %s", (student_id, parent_id))

            # Also update student's parent_id
            cursor.execute(
                "UPDATE users SET parent_id = %s WHERE user_id = %s", (parent_id, student_id))
            conn.commit()

            print("Parent registered and linked to student successfully.")
        else:
            print(
                "Parent registered. Student not found. Link will be added later when the student registers.")

    else:
        print("Invalid user type. Please enter 'user' or 'parent'.")

    cursor.close()


# Run the function
register()
