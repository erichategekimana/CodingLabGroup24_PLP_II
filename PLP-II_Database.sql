/*
this codes creates four tables that are: 1. users, 3. students, 3. progress, 
and 4. messages.
      /\
     /  \
    /  ! \  *tiny change of these codes might result to the fail of entire database!*
   -------- 

*/

CREATE Table users (
    id int PRIMARY KEY AUTO_INCREMENT, -- id that will keep track user
    user_name VARCHAR(150) not null,   -- full name
    password VARCHAR(64) not NULL,
    role ENUM(' teacher', 'student', 'parent') NOT NULL, -- this will allow only specified values
                                                    -- ^and categorize users into those three category
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- <auto add timestamp
);

CREATE Table students (
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int NOT NULL, -- user id(from login(users) table)
    parent_id int NOT NULL, -- also from login info(parent category)
    student_names VARCHAR(150) NOT NULL,
    study_level VARCHAR(2) NOT NULL, -- eg: "P6" for primary 6 or S3 or seconary 3, ...
    year VARCHAR(4) NOT NULL,  -- eg: 2022, 2025, ...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- create relationship(connection) between tables!  
    Foreign Key (user_id) REFERENCES users(id) on DELETE CASCADE,
    foreign key (parent_id) REFERENCES users(id)
);

CREATE TABLE progress (
    id int PRIMARY KEY AUTO_INCREMENT,
    student_id int NOT NULL,
    subject VARCHAR(100) NOT NULL,
    term ENUM('Term 1', 'Term 2', 'Term 3') NOT NULL, -- only specified key words are allowed
    grades int NOT NULL,
    teacher_comment varchar(200), -- it can be null(optional)
    teacher_id int,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- create relationship(connection) between tables!
    Foreign Key (student_id) REFERENCES students(id) ON DELETE CASCADE,
    Foreign Key (teacher_id) REFERENCES users(id)
);


/*
message table should hold sender, receiver, msg text and timestamp.
*/
CREATE Table messages(
    id int PRIMARY KEY AUTO_INCREMENT,
    sender_id int NOT NULL,
    receiver_id int NOT NULL,
    student_id int NOT null,
    text_body VARCHAR(250) NOT NULL,
    done_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Foreign Key (sender_id) REFERENCES users(id) on delete cascade,
    Foreign Key (receiver_id) REFERENCES users(id) on delete cascade,
    Foreign Key (student_id) REFERENCES students(id) on delete CASCADE
);