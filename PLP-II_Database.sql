/*
this codes creates four tables that are: 1. users, 3. students, 3. progress, 
and 4. messages.
      /\
     /  \
    /  ! \  *tiny change of these codes might result to the fail of entire database!*
   --------
*/

CREATE TABLE students (
  id int(11) primary KEY NOT NULL AUTO_INCREMENT,
  parent_id int(11) DEFAULT NULL,
  instructor_id int(11) DEFAULT NULL,
  student_names varchar(50) NOT NULL,
  student_email varchar(100) NOT NULL UNIQUE,
  password varchar(100) NOT NULL,
  student_level varchar(50) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Foreign Key (parent_id) REFERENCES parents(parent_id) ON DELETE SET NULL ON UPDATE CASCADE,
  Foreign Key (instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE parents (
  parent_id int(11) primary key NOT NULL AUTO_INCREMENT,
  parent_name varchar(100) NOT NULL,
  password varchar(128) NOT NULL,
  parent_email varchar(100) NOT NULL UNIQUE,
  parent_phone varchar(15) DEFAULT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE instructors (
  instructor_id int(11) primary key NOT NULL AUTO_INCREMENT,
  instructor_name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  instructor_email varchar(100) NOT NULL UNIQUE,
  instructor_phone varchar(15) DEFAULT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  specialization varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE subjects (
  subject_id int(11) primary key NOT NULL AUTO_INCREMENT,
  subject_name varchar(100) NOT NULL UNIQUE,
  instructor_id int(11) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Foreign Key (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE messages (
  message_id int(11) primary key NOT NULL AUTO_INCREMENT,
  sender_type ENUM('instructor', 'parent') NOT NULL,
  sender_id int(11) NOT NULL,
  receiver_type ENUM('instructor', 'parent') NOT NULL,
  receiver_id int(11) NOT NULL,
  student_id int(11) NOT NULL,
  contents text NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Foreign Key (sender_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE,
  Foreign Key (receiver_id) REFERENCES parents(parent_id) ON DELETE CASCADE ON UPDATE CASCADE,
  Foreign Key (student_id) REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE Table grades (
  grade_id int(11) primary key NOT NULL AUTO_INCREMENT,
  student_id int(11) NOT NULL,
  subject_id int(11) NOT NULL,
  instructor_id int(11) NOT NULL,
  term ENUM('Term 1', 'Term 2', 'Term 3') NOT NULL,
  grade int(3) NOT NULL,
  status VARCHAR(10) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Foreign Key (student_id) REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE,
  Foreign Key (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
  Foreign Key (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
