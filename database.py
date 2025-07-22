import mysql.connector

def create_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="school_management"
        )
        cursor = connection.cursor()

        # Instructors table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password TEXT
        )
        """)

        # Students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password TEXT,
            parent_id INT,
            FOREIGN KEY (parent_id) REFERENCES parents(id)
        )
        """)

        # Parents table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password TEXT
        )
        """)

        # Subjects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(100),
            instructor_id INT,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        )
        """)

        # Student_Subjects table (Many-to-Many)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)

        # Grades table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            grade VARCHAR(10),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)

        # Reports table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            overall_comment TEXT,
            term VARCHAR(50),
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
        """)

        # Messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT,
            sender_role ENUM('student', 'instructor', 'parent'),
            receiver_id INT,
            receiver_role ENUM('student', 'instructor', 'parent'),
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        connection.commit()
        print("All tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Run the function to initialize the DB
create_tables()
