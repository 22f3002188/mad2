import hashlib
import sqlite3
import calendar
from typing import Counter
from flask import abort
from functools import wraps
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from celery_app import make_celery
from models import init_db, create_admin, get_connection, question_to_dict, user_to_dict, subject_to_dict, chapter_to_dict, quiz_to_dict, score_to_dict
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt)

# Initialize Flask app
app = Flask(__name__)
celery = make_celery(app)

from flask_caching import Cache

# Redis cache config
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'  # or 'redis' if using docker-compose
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

cache = Cache(app)


app.config['SWAGGER'] = {
    'title': 'Quiz Nation API',
    'uiversion': 3,
    'specs_route': '/apidocs/',  # Optional: Customize Swagger UI route
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    }
}
# CORS
CORS(app, supports_credentials=True)

# Swagger and JWT setup
swagger = Swagger(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
jwt = JWTManager(app)

# Initialize DB and create default admin
init_db()
create_admin()

#---------------------------------------ADMIN REQUIRED DECORATOR-------------------------------------------------------------------
# Define a decorator to check if the user is an admin
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()  # email
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (identity,))
        user = cursor.fetchone()
        conn.close()

        if not user or user["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return wrapper

#--------------------------------------------------SIGNUP AND LOGIN ENDPOINTS---------------------------------------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    """
    Register a new user
    ---
    tags:
      - Registration
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
              - full_name
              - qualification
              - dob
            properties:
              email:
                type: string
              password:
                type: string
              full_name:
                type: string
              qualification:
                type: string
              dob:
                type: string
                format: date
    responses:
      201:
        description: User registered
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                user_id:
                  type: integer
      400:
        description: Email already exists
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob = data.get('dob')
    role = 'user'

    if not all([email, password, full_name, qualification, dob]):
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password, full_name, qualification, dob, role)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, hashed_password, full_name, qualification, dob, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        return jsonify({"message": "User registered", "user_id": user_id}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400


@app.route('/api/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Registration
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
              password:
                type: string
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                access_token:
                  type: string
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                    full_name:
                      type: string
                    email:
                      type: string
                    role:
                      type: string
      401:
        description: Invalid credentials
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
    user = cursor.fetchone()

    if user:
        user_dict = user_to_dict(user)

        access_token = create_access_token(
            identity=user_dict['email'],
            additional_claims={"role": user_dict['role']},
            expires_delta=timedelta(hours=1)
        )

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                token TEXT
            )
        ''')
        cursor.execute('INSERT INTO user_tokens (email, token) VALUES (?, ?)', (user_dict['email'], access_token))
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user_dict['id'],
                "full_name": user_dict['full_name'],
                "email": user_dict['email'],
                "role": user_dict['role']
            }
        }), 200
    else:
        conn.close()
        return jsonify({"error": "Invalid email or password"}), 401


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout
    ---
    tags:
      - Registration
    security:
      - Bearer: []
    responses:
      200:
        description: Logout successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    jti = get_jwt()['jti']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revoked_tokens (
            jti TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('INSERT INTO revoked_tokens (jti) VALUES (?)', (jti,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Logout successful"}), 200


#--------------------------------------------------SUBJECTS ENDPOINTS---------------------------------------------------

@app.route('/api/subjects', methods=['POST'])
@admin_required
def add_subject():
    """
    Add a new subject (admin only)
    ---
    tags:
      - Admin
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - description
            properties:
              name:
                type: string
              description:
                type: string
    security:
      - Bearer: []
    responses:
      200:
        description: Subject added successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Validation error or duplicate subject
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO subjects (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        cache.delete("all_subjects") 
        return jsonify({'message': 'Subject added successfully'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Subject name already exists'}), 400

    finally:
        conn.close()


@app.route('/api/get_subjects', methods=['GET'])
@cache.cached(timeout=300, key_prefix="all_subjects")
@admin_required
def get_subjects():
    print("/api/get_subjects route called")
    """
    Get list of all subjects (Admin only)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: List of subjects returned successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                subjects:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      description:
                        type: string
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    try:
        print("Cache MISS — fetching subjects from DB")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subjects')
        subjects = cursor.fetchall()
        conn.close()

        subject_list = [subject_to_dict(subject) for subject in subjects]

        return jsonify({"subjects": subject_list}), 200

    except Exception as e:
        print("Error fetching subjects:", e)
        return jsonify({"error": "Internal server error"}), 500



@app.route('/api/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    """
    Update an existing subject (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - description
            properties:
              name:
                type: string
              description:
                type: string
    security:
      - Bearer: []
    responses:
      200:
        description: Subject updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Name or description missing
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE subjects SET name = ?, description = ? WHERE id = ?',
        (name, description, subject_id)
    )
    conn.commit()
    conn.close()
    cache.delete("all_subjects") 

    return jsonify({"message": "Subject updated successfully"}), 200


@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    """
    Delete a subject (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: Subject deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Subject not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM subjects WHERE id = ?", (subject_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Subject not found"}), 404

    cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    conn.commit()
    conn.close()
    cache.delete("all_subjects") 
    return jsonify({"message": "Subject deleted successfully"}), 200




#--------------------------------------------------CHAPTERS ENDPOINTS---------------------------------------------------
# === Get All Chapters by Subject ===
@app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
@admin_required
def get_chapters_by_subject(subject_id):
    """
    Get all chapters for a specific subject (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: List of chapters for the subject
        content:
          application/json:
            schema:
              type: object
              properties:
                subject_name:
                  type: string
                chapters:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      description:
                        type: string
      404:
        description: Subject not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
    subject = cursor.fetchone()

    if not subject:
        conn.close()
        return jsonify({'error': 'Subject not found'}), 404

    subject_name = subject[0]

    cursor.execute('SELECT id, name, description FROM chapters WHERE subject_id = ?', (subject_id,))
    chapters = cursor.fetchall()
    conn.close()

    return jsonify({
        'subject_name': subject_name,
        'chapters': [
            {'id': c[0], 'name': c[1], 'description': c[2]} for c in chapters
        ]
    }), 200


@app.route('/api/subjects/<int:subject_id>/chapters', methods=['POST'])
@admin_required
def add_chapter(subject_id):
    """
    Add a new chapter to a subject (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
              description:
                type: string
    security:
      - Bearer: []
    responses:
      201:
        description: Chapter added successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Chapter name is required or subject not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Chapter name is required'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chapters (name, description, subject_id) VALUES (?, ?, ?)',
                   (name, description, subject_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Chapter added successfully'}), 201


@app.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
@admin_required
def edit_chapter(chapter_id):
    """
    Edit a chapter (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - description
            properties:
              name:
                type: string
              description:
                type: string
    security:
      - Bearer: []
    responses:
      200:
        description: Chapter updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Chapter not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM chapters WHERE id = ?', (chapter_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Chapter not found'}), 404

    cursor.execute('UPDATE chapters SET name = ?, description = ? WHERE id = ?',
                   (name, description, chapter_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Chapter updated successfully'}), 200


@app.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    """
    Delete a chapter (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: Chapter deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Chapter not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
    chapter = cursor.fetchone()
    if not chapter:
        conn.close()
        return jsonify({"error": "Chapter not found"}), 404

    cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Chapter deleted"}), 200




# ---------------------------------------------quiz--------------------------------------
@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@admin_required
def get_quizzes_by_chapter(chapter_id):
    """
    Get all quizzes for a specific chapter (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: List of quizzes for the chapter
        content:
          application/json:
            schema:
              type: object
              properties:
                chapter_name:
                  type: string
                quizzes:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      quiz_name:
                        type: string
                      date_of_quiz:
                        type: string
                      time_duration:
                        type: string
      404:
        description: Chapter not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    security:
      - Bearer: []
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM chapters WHERE id = ?', (chapter_id,))
    chapter = cursor.fetchone()

    if not chapter:
        conn.close()
        return jsonify({'error': 'Chapter not found'}), 404

    chapter_name = chapter['name'] if isinstance(chapter, dict) else chapter[0]
    cursor.execute('SELECT id, quiz_name, date_of_quiz, time_duration FROM quiz WHERE chapter_id = ?', (chapter_id,))
    quizzes = cursor.fetchall()
    conn.close()

    return jsonify({
        'chapter_name': chapter_name,
        'quizzes': [
            {'id': q[0], 'quiz_name': q[1], 'date_of_quiz': q[2], 'time_duration': q[3]}
            for q in quizzes
        ]
    }), 200


@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@admin_required
def add_quiz(chapter_id):
    """
    Add a new quiz to a chapter (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - quiz_name
              - date_of_quiz
              - time_duration
            properties:
              quiz_name:
                type: string
              date_of_quiz:
                type: string
                format: date
              time_duration:
                type: string
    responses:
      201:
        description: Quiz added successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: All fields are required
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      409:
        description: Quiz with same name exists
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    security:
      - Bearer: []
    """
    data = request.get_json()
    quiz_name = data.get('quiz_name')
    date_of_quiz = data.get('date_of_quiz')
    time_duration = data.get('time_duration')

    if not all([quiz_name, date_of_quiz, time_duration]):
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO quiz (chapter_id, quiz_name, date_of_quiz, time_duration)
            VALUES (?, ?, ?, ?)
        ''', (chapter_id, quiz_name, date_of_quiz, time_duration))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Quiz with same name exists'}), 409
    finally:
        conn.close()

    return jsonify({'message': 'Quiz added successfully'}), 201


@app.route('/api/chapters/<int:chapter_id>/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(chapter_id, quiz_id):
    """
    Update quiz details (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - quiz_name
              - date_of_quiz
              - time_duration
            properties:
              quiz_name:
                type: string
              date_of_quiz:
                type: string
                format: date
              time_duration:
                type: string
    responses:
      200:
        description: Quiz updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      404:
        description: Quiz not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    security:
      - Bearer: []
    """
    data = request.get_json()
    quiz_name = data.get('quiz_name')
    date_of_quiz = data.get('date_of_quiz')
    time_duration = data.get('time_duration')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM quiz WHERE id = ? AND chapter_id = ?', (quiz_id, chapter_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404

    cursor.execute('''
        UPDATE quiz 
        SET quiz_name = ?, date_of_quiz = ?, time_duration = ?
        WHERE id = ? AND chapter_id = ?
    ''', (quiz_name, date_of_quiz, time_duration, quiz_id, chapter_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Quiz updated successfully'}), 200


@app.route('/api/chapters/<int:chapter_id>/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(chapter_id, quiz_id):
    """
    Delete a quiz from a chapter (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        schema:
          type: integer
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Quiz deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Quiz not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    security:
      - Bearer: []
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM quiz WHERE id = ? AND chapter_id = ?", (quiz_id, chapter_id))
    quiz = cursor.fetchone()
    if not quiz:
        conn.close()
        return jsonify({"error": "Quiz not found"}), 404

    cursor.execute("DELETE FROM quiz WHERE id = ? AND chapter_id = ?", (quiz_id, chapter_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Quiz deleted successfully'}), 200




# -----------------------------------------questions------------------

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def get_questions_by_quiz(quiz_id):
    """
    Get all questions for a specific quiz (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: List of questions
        content:
          application/json:
            schema:
              type: object
              properties:
                questions:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      question_statement:
                        type: string
                      option1:
                        type: string
                      option2:
                        type: string
                      option3:
                        type: string
                      option4:
                        type: string
                      correct_answer:
                        type: string
      404:
        description: Quiz not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM quiz WHERE id = ?", (quiz_id,))
    quiz = cursor.fetchone()
    if not quiz:
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404

    cursor.execute('''
        SELECT id, question_statement, option1, option2, option3, option4, correct_answer
        FROM question WHERE quiz_id = ?
    ''', (quiz_id,))
    questions = cursor.fetchall()
    conn.close()

    return jsonify({
        'questions': [
            {
                'id': q[0],
                'question_statement': q[1],
                'option1': q[2],
                'option2': q[3],
                'option3': q[4],
                'option4': q[5],
                'correct_answer': q[6]
            } for q in questions
        ]
    }), 200


@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def add_question(quiz_id):
    """
    Add a question to a quiz (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - question_statement
              - option1
              - option2
              - option3
              - option4
              - correct_answer
            properties:
              question_statement:
                type: string
              option1:
                type: string
              option2:
                type: string
              option3:
                type: string
              option4:
                type: string
              correct_answer:
                type: string
    security:
      - Bearer: []
    responses:
      201:
        description: Question added successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                question_id:
                  type: integer
      400:
        description: Missing required fields
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      404:
        description: Quiz not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM quiz WHERE id = ?", (quiz_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404

    cursor.execute("""
        INSERT INTO question (quiz_id, question_statement, option1, option2, option3, option4, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        quiz_id,
        data['question_statement'],
        data['option1'],
        data['option2'],
        data['option3'],
        data['option4'],
        data['correct_answer']
    ))
    conn.commit()
    question_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Question added successfully', 'question_id': question_id}), 201


@app.route('/api/quizzes/<int:quiz_id>/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(quiz_id, question_id):
    """
    Update a question in a quiz (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
      - name: question_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              question_statement:
                type: string
              option1:
                type: string
              option2:
                type: string
              option3:
                type: string
              option4:
                type: string
              correct_answer:
                type: string
    security:
      - Bearer: []
    responses:
      200:
        description: Question updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Question not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM question WHERE id = ? AND quiz_id = ?", (question_id, quiz_id))
    question = cursor.fetchone()
    if not question:
        conn.close()
        return jsonify({"error": "Question not found"}), 404

    cursor.execute("""
        UPDATE question
        SET question_statement = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct_answer = ?
        WHERE id = ? AND quiz_id = ?
    """, (
        data.get('question_statement'),
        data.get('option1'),
        data.get('option2'),
        data.get('option3'),
        data.get('option4'),
        data.get('correct_answer'),
        question_id,
        quiz_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Question updated successfully"}), 200


@app.route('/api/quizzes/<int:quiz_id>/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(quiz_id, question_id):
    """
    Delete a specific question by ID (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
      - name: question_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: Question deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Question not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM question WHERE id = ? AND quiz_id = ?", (question_id, quiz_id))
    question = cursor.fetchone()

    if not question:
        conn.close()
        return jsonify({'error': 'Question not found'}), 404

    cursor.execute("DELETE FROM question WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Question deleted successfully'}), 200





#--------------------------------------------------GET ALL USERS ENDPOINT admin---------------------------------------------------

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """
    Get list of all registered users (Admin only)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      full_name:
                        type: string
                      email:
                        type: string
                      role:
                        type: string
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'user'")
    users = cursor.fetchall()
    conn.close()

    user_list = [user_to_dict(user) for user in users]
    return jsonify({"users": user_list}), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    Delete a user by ID (Admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: User deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User deleted successfully
      404:
        description: User not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: User not found
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200


@app.route('/api/admin/summary', methods=['GET'])
@jwt_required()
def admin_summary_api():
    """
    Get summary statistics for admin dashboard
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: Summary statistics
        content:
          application/json:
            schema:
              type: object
              properties:
                chart_data:
                  type: object
                  properties:
                    labels:
                      type: array
                      items:
                        type: string
                    scores:
                      type: array
                      items:
                        type: number
                    scorers:
                      type: array
                      items:
                        type: string
                attempt_chart_data:
                  type: object
                  properties:
                    labels:
                      type: array
                      items:
                        type: string
                    attempts:
                      type: array
                      items:
                        type: integer
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT sub.name AS subject_name, u.full_name AS top_scorer, MAX(s.score) AS max_score
        FROM score s
        JOIN quiz q ON s.quiz_id = q.id
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        JOIN users u ON s.user_email = u.email
        GROUP BY sub.id, u.email
    ''')
    rows = cursor.fetchall()

    top_scorer_dict = {}
    for row in rows:
        subject = row['subject_name']
        scorer = row['top_scorer']
        score = row['max_score']
        if subject not in top_scorer_dict or score > top_scorer_dict[subject]['max_score']:
            top_scorer_dict[subject] = {'top_scorer': scorer, 'max_score': score}

    chart_data = {
        'labels': list(top_scorer_dict.keys()),
        'scores': [v['max_score'] for v in top_scorer_dict.values()],
        'scorers': [v['top_scorer'] for v in top_scorer_dict.values()]
    }

    cursor.execute('''
        SELECT sub.name AS subject_name, COUNT(s.id) AS attempt_count
        FROM score s
        JOIN quiz q ON s.quiz_id = q.id
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        GROUP BY sub.id
    ''')
    attempts = cursor.fetchall()
    conn.close()

    attempt_chart_data = {
        'labels': [row['subject_name'] for row in attempts],
        'attempts': [row['attempt_count'] for row in attempts]
    }

    return jsonify({
        'chart_data': chart_data,
        'attempt_chart_data': attempt_chart_data
    }), 200

@app.route('/api/search', methods=['GET'])
@admin_required
def api_search():
    """
    Search users, subjects, chapters, quizzes by query (admin only)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - name: q
        in: query
        required: true
        description: Search query string
        schema:
          type: string
    responses:
      200:
        description: Search results
      400:
        description: Missing query
      403:
        description: Admin access required
    """
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    like_query = f"%{query}%"

    # Users by email
    cursor.execute("SELECT * FROM users WHERE email LIKE ?", (like_query,))
    users = cursor.fetchall()

    # Subjects by name
    cursor.execute("SELECT * FROM subjects WHERE name LIKE ?", (like_query,))
    subjects = cursor.fetchall()

    # Chapters by name
    cursor.execute("SELECT * FROM chapters WHERE name LIKE ?", (like_query,))
    chapters = cursor.fetchall()

    # Quizzes by quiz_name
    cursor.execute("SELECT * FROM quiz WHERE quiz_name LIKE ?", (like_query,))
    quizzes = cursor.fetchall()

    conn.close()

    results = {
        "users": [user_to_dict(u) for u in users],
        "subjects": [subject_to_dict(s) for s in subjects],
        "chapters": [chapter_to_dict(c) for c in chapters],
        "quizzes": [quiz_to_dict(q) for q in quizzes],
    }

    return jsonify(results), 200


# -------------------------------------------users dashboard-----------------------------
@app.route('/api/user/quizzes', methods=['GET'])
@jwt_required()
def get_user_quizzes():
    """
    Get all quizzes with chapter and subject info for logged-in user
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: List of quizzes with chapter and subject info
        content:
          application/json:
            schema:
              type: object
              properties:
                quizzes:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      quiz_name:
                        type: string
                      date_of_quiz:
                        type: string
                        format: date
                      time_duration:
                        type: string
                      chapter:
                        type: string
                      subject:
                        type: string
      500:
        description: Internal server error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT q.id, q.quiz_name, q.date_of_quiz, q.time_duration,
                   c.name AS chapter, s.name AS subject
            FROM quiz q
            JOIN chapters c ON q.chapter_id = c.id
            JOIN subjects s ON c.subject_id = s.id
            ORDER BY q.date_of_quiz DESC
        ''')
        quizzes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"quizzes": quizzes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/quiz/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz_details(quiz_id):
    """
    Get details of a specific quiz including questions and chapter info
    ---
    tags:
      - User
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - Bearer: []
    responses:
      200:
        description: Quiz details with questions and chapter info
        content:
          application/json:
            schema:
              type: object
              properties:
                quiz:
                  type: object
                  properties:
                    id:
                      type: integer
                    quiz_name:
                      type: string
                    date_of_quiz:
                      type: string
                      format: date
                    time_duration:
                      type: string
                    chapter:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                    subject:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                questions:
                  type: array
                  items:
                    type: object
      404:
        description: Quiz not found
      500:
        description: Internal server error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT q.id, q.quiz_name, q.date_of_quiz, q.time_duration,
                   c.id as chapter_id, c.name AS chapter_name, s.id as subject_id, s.name AS subject_name
            FROM quiz q
            JOIN chapters c ON q.chapter_id = c.id
            JOIN subjects s ON c.subject_id = s.id
            WHERE q.id = ?
        ''', (quiz_id,))
        quiz_row = cursor.fetchone()
        if not quiz_row:
            return jsonify({"error": "Quiz not found"}), 404

        quiz = {
            "id": quiz_row["id"],
            "quiz_name": quiz_row["quiz_name"],
            "date_of_quiz": quiz_row["date_of_quiz"],
            "time_duration": quiz_row["time_duration"],
            "chapter": {
                "id": quiz_row["chapter_id"],
                "name": quiz_row["chapter_name"]
            },
            "subject": {
                "id": quiz_row["subject_id"],
                "name": quiz_row["subject_name"]
            }
        }

        cursor.execute('SELECT * FROM question WHERE quiz_id = ?', (quiz_id,))
        questions = [question_to_dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"quiz": quiz, "questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/quiz/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    """
    Submit answers for a quiz and calculate score
    ---
    tags:
      - User
    parameters:
      - name: quiz_id
        in: path
        required: true
        schema:
          type: integer
        description: ID of the quiz
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              answers:
                type: object
                additionalProperties:
                  type: string
            example:
              answers:
                "1": "option1"
                "2": "option3"
    security:
      - Bearer: []
    responses:
      200:
        description: Quiz submitted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                score:
                  type: number
              example:
                message: "Quiz submitted"
                score: 80.0
      400:
        description: Answers not provided or invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
              example:
                error: "Answers not provided"
      404:
        description: Quiz or questions not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
              example:
                error: "Quiz or questions not found"
      500:
        description: Internal server error
    """
    try:
        user_email = get_jwt_identity()
        data = request.get_json()

        if not data or "answers" not in data:
            return jsonify({"error": "Answers not provided"}), 400

        answers = data["answers"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, correct_answer FROM question WHERE quiz_id = ?', (quiz_id,))
        questions = cursor.fetchall()

        if not questions:
            return jsonify({"error": "Quiz or questions not found"}), 404

        total_questions = len(questions)
        correct_count = sum(1 for q in questions if answers.get(str(q["id"])) == q["correct_answer"])

        score = (correct_count / total_questions) * 100
        date_attempt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO score (user_email, quiz_id, date_attempt, score)
            VALUES (?, ?, ?, ?)
        ''', (user_email, quiz_id, date_attempt, score))
        conn.commit()
        conn.close()

        return jsonify({"message": "Quiz submitted", "score": score}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    """
    Get all scores for the logged-in user
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: List of scores with quiz and chapter info
        content:
          application/json:
            schema:
              type: object
              properties:
                scores:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      score:
                        type: number
                        format: float
                      date_attempt:
                        type: string
                        format: date-time
                      quiz_name:
                        type: string
                      chapter:
                        type: string
                      subject:
                        type: string
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Database connection failed"
    """
    try:
        user_email = get_jwt_identity()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT s.id, s.score, s.date_attempt, q.quiz_name, c.name AS chapter, sub.name AS subject
            FROM score s
            JOIN quiz q ON s.quiz_id = q.id
            JOIN chapters c ON q.chapter_id = c.id
            JOIN subjects sub ON c.subject_id = sub.id
            WHERE s.user_email = ?
            ORDER BY s.date_attempt DESC
        ''', (user_email,))
        scores = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({"scores": scores}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/quizzes_charts', methods=['GET'])
@jwt_required()
def api_quizzes_charts():
    """
    Get charts data for quizzes by subject and user attempts by month
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: Chart data for quizzes by subject and user attempts by month
        content:
          application/json:
            schema:
              type: object
              properties:
                subject_chart_data:
                  type: object
                  properties:
                    labels:
                      type: array
                      items:
                        type: string
                    quizzes:
                      type: array
                      items:
                        type: integer
                month_chart_data:
                  type: object
                  properties:
                    labels:
                      type: array
                      items:
                        type: string
                    attempts:
                      type: array
                      items:
                        type: integer

    """
    try:
        user_email = get_jwt_identity()
        conn = get_connection()
        cursor = conn.cursor()

        # Subject-wise quiz count
        cursor.execute("""
            SELECT s.name AS subject
            FROM quiz q
            JOIN chapters c ON q.chapter_id = c.id
            JOIN subjects s ON c.subject_id = s.id
        """)
        quizzes = cursor.fetchall()
        subject_counts = Counter(row["subject"] for row in quizzes)
        subject_chart_data = {
            "labels": list(subject_counts.keys()),
            "quizzes": list(subject_counts.values()),
        }

        # Month-wise attempt count
        cursor.execute("SELECT date_attempt FROM score WHERE user_email = ?", (user_email,))
        attempts = cursor.fetchall()

        month_counts = Counter()
        for row in attempts:
            try:
                dt = datetime.strptime(row["date_attempt"], "%Y-%m-%d %H:%M:%S")
                month_counts[dt.month] += 1
            except:
                continue

        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        month_chart_data = {
            "labels": [month_labels[m - 1] for m in sorted(month_counts)],
            "attempts": [month_counts[m] for m in sorted(month_counts)],
        }

        conn.close()
        return jsonify(subject_chart_data=subject_chart_data, month_chart_data=month_chart_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == '__main__':
    app.run(debug=True)
