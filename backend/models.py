# backend/models.py

import sqlite3
import hashlib

DB_NAME = 'quiz.db'

def get_connection():
    """
    Return a new SQLite connection with foreign-key support enabled.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """
    Create all tables with ON DELETE CASCADE where appropriate.
    """
    conn = get_connection()
    cursor = conn.cursor()

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

    # Chapters (cascade when subject is deleted)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            FOREIGN KEY (subject_id)
              REFERENCES subjects(id)
              ON DELETE CASCADE
        )
    ''')

    # Quiz (cascade when chapter is deleted)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            quiz_name TEXT NOT NULL UNIQUE,
            date_of_quiz TEXT NOT NULL,
            time_duration TEXT NOT NULL,
            FOREIGN KEY (chapter_id)
              REFERENCES chapters(id)
              ON DELETE CASCADE
        )
    ''')

    # Question (cascade when quiz is deleted)
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
            FOREIGN KEY (quiz_id)
              REFERENCES quiz(id)
              ON DELETE CASCADE
        )
    ''')

    # Score (cascade when user OR quiz is deleted)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            quiz_id INTEGER NOT NULL,
            date_attempt TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY (user_email)
              REFERENCES users(email)
              ON DELETE CASCADE,
            FOREIGN KEY (quiz_id)
              REFERENCES quiz(id)
              ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def create_admin():
    """
    Ensure an admin user always exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE email = ?', ('admin@gmail.com',))
    if not cursor.fetchone():
        hashed = hashlib.sha256('123456'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO users (email, password, full_name, role) VALUES (?, ?, ?, ?)',
            ('admin@gmail.com', hashed, 'ADMIN', 'admin')
        )
        conn.commit()
    conn.close()

# -- converters to dicts for your API responses --

def user_to_dict(user_row, include_scores=False):
    user = dict(user_row)
    if include_scores:
        c = get_connection().cursor()
        c.execute('SELECT * FROM score WHERE user_email = ?', (user['email'],))
        user['scores'] = [dict(r) for r in c.fetchall()]
        c.connection.close()
    return user

def subject_to_dict(r):
    return {"id": r["id"], "name": r["name"], "description": r["description"]}

def chapter_to_dict(r):
    return {"id": r["id"], "name": r["name"], "description": r["description"], "subject_id": r["subject_id"]}

def quiz_to_dict(r):
    return {
        "id": r["id"],
        "chapter_id": r["chapter_id"],
        "quiz_name": r["quiz_name"],
        "date_of_quiz": r["date_of_quiz"],
        "time_duration": r["time_duration"]
    }

def question_to_dict(r):
    return {
        "id": r["id"],
        "quiz_id": r["quiz_id"],
        "question_statement": r["question_statement"],
        "option1": r["option1"],
        "option2": r["option2"],
        "option3": r["option3"],
        "option4": r["option4"],
        "correct_answer": r["correct_answer"]
    }

def score_to_dict(r):
    return {
        "id": r["id"],
        "user_email": r["user_email"],
        "quiz_id": r["quiz_id"],
        "date_attempt": r["date_attempt"],
        "score": r["score"]
    }
