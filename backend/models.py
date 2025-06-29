# backend/models.py
import sqlite3
import hashlib

DB_NAME = 'quiz.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Enable foreign key constraint
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT,
            qualification TEXT,
            dob TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Subjects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Chapters Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        )
    ''')

    # Quiz Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            quiz_name TEXT NOT NULL UNIQUE,
            date_of_quiz TEXT NOT NULL,
            time_duration TEXT NOT NULL,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
        )
    ''')

    # Question Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question_statement TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT,
            option4 TEXT,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
        )
    ''')

    # Score Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            date_attempt TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def create_admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@gmail.com',))
    existing = cursor.fetchone()

    if not existing:
        hashed_password = hashlib.sha256('123456'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (email, password, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin@gmail.com', hashed_password, 'ADMIN', 'admin'))
        conn.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    conn.close()

def user_to_dict(user_row, include_scores=False):
    user = dict(user_row)
    
    # Normalize fields (like date format)
    if user.get("dob"):
        user["dob"] = user["dob"]  # already ISO string in DB
    
    # Optionally add scores
    if include_scores:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM score WHERE user_id = ?', (user['id'],))
        scores = cursor.fetchall()
        user['scores'] = [dict(score) for score in scores]
        conn.close()

    return user

def subject_to_dict(subject_row):
    return {
        "id": subject_row["id"],
        "name": subject_row["name"],
        "description": subject_row["description"]
    }




