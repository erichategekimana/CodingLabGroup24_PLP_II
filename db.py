import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql-spt-codinglabgroup24-alustudent-6f2b.c.aivencloud.com",
            user="avnadmin",
            password="AVNS_XMaaOLpAaCmHNErSMiD",
            database="new_spt_database",
            port = 13891
        )
        return connection
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None

def create_tables():
    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Instructors table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id INT AUTO_INCREMENT PRIMARY KEY,
            instructor_name VARCHAR(100),
            password VARCHAR(255),
            instructor_email VARCHAR(100) UNIQUE,
            instructor_phone VARCHAR(20),
            specialization VARCHAR(100),
            timestamp DATETIME
        )
        """)

        # Parents table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parents (
            parent_id INT AUTO_INCREMENT PRIMARY KEY,
            parent_name VARCHAR(100),
            password VARCHAR(255),
            parent_email VARCHAR(100) UNIQUE,
            parent_phone VARCHAR(20),
            timestamp DATETIME
        )
        """)

        # Students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            parent_id INT,
            instructor_id INT,
            student_names VARCHAR(100),
            student_email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            student_level VARCHAR(50),
            timestamp DATETIME,
            FOREIGN KEY (parent_id) REFERENCES parents(parent_id),
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
        )
        """)

        # Subjects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(100),
            instructor_id INT,
            timestamp DATETIME,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
        )
        """)


        # Grades table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            instructor_id INT,
            term VARCHAR(20),
            grade FLOAT,
            status VARCHAR(20),
            timestamp DATETIME,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
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
            message_id INT AUTO_INCREMENT PRIMARY KEY,
            sender_type VARCHAR(20),
            sender_id INT,
            receiver_type VARCHAR(20),
            receiver_id INT,
            student_id INT,
            contents TEXT,
            timestamp DATETIME,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
        """)

        connection.commit()
        print("All tables created successfully.")
    except mysql.connector.Error as err:
        print("Error during table creation:", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Call this only when needed
create_tables()
