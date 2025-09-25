# CodingLabGroup24_PLP_II

# Student Progress Tracker

A CLI based application for tracking student progress, designed for schools. The app allows instructors, parents, and students to manage, monitor, and communicate about student performance efficiently.

---

## Features

- **User Roles**
  - **Instructors**: Manage subjects, assign grades, communicate with parents.
  - **Parents**: Track child’s performance, send messages to instructors.
  - **Students**: View grades and progress (if needed, can be extended).

- **Student Management**
  - Maintain student records including level, email, and assigned instructors/parents.
  
- **Grade Tracking**
  - Record grades per subject, per term.
  - Store status for each grade (e.g., Passed/Failed).

- **Messaging System**
  - Secure messaging between parents and instructors.
  - Messages linked to students for context.

- **Subjects Management**
  - Instructors can manage subjects they teach.
  
---

## Database Schema

The app uses **MySQL** with the following tables:

1. **students**
   - Tracks students and links to parents and instructors.
   - Fields: `id`, `parent_id`, `instructor_id`, `student_names`, `student_email`, `password`, `student_level`, `timestamp`.

2. **parents**
   - Tracks parent information.
   - Fields: `parent_id`, `parent_name`, `parent_email`, `password`, `parent_phone`, `timestamp`.

3. **instructors**
   - Tracks instructor information.
   - Fields: `instructor_id`, `instructor_name`, `instructor_email`, `password`, `instructor_phone`, `specialization`, `timestamp`.

4. **subjects**
   - Stores subjects taught by instructors.
   - Fields: `subject_id`, `subject_name`, `instructor_id`, `timestamp`.

5. **messages**
   - Stores messages between parents and instructors, linked to students.
   - Fields: `message_id`, `sender_type`, `sender_id`, `receiver_type`, `receiver_id`, `student_id`, `contents`, `timestamp`.

6. **grades**
   - Tracks student grades per subject and term.
   - Fields: `grade_id`, `student_id`, `subject_id`, `instructor_id`, `term`, `grade`, `status`, `timestamp`.

**Relationships:**  
- Students → Parents & Instructors (`SET NULL` on delete)  
- Subjects → Instructors (`CASCADE` on delete)  
- Messages → Students, Instructors, Parents (`CASCADE` on delete)  
- Grades → Students, Subjects, Instructors (`CASCADE` on delete)

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/erichategekimana/CodingLabGroup24_PLP_II







