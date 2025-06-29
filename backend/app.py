import hashlib
import sqlite3
from flask import abort
from functools import wraps
from flask_cors import CORS
from flasgger import Swagger
from datetime import timedelta
from flask import Flask, request, jsonify
from models import init_db, create_admin, get_connection, user_to_dict, subject_to_dict, chapter_to_dict, quiz_to_dict, score_to_dict
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt)

# Initialize Flask app
app = Flask(__name__)

# Swagger JWT lock setup
app.config['SWAGGER'] = {
    'title': 'Your API',
    'uiversion': 3,
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    },
    'security': [{'Bearer': []}]
}
# CORS
CORS(app)

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
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
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
      400:
        description: Email already exists
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob = data.get('dob')
    role = 'user'

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
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
    user = cursor.fetchone()

    if user:
        user_dict = user_to_dict(user)

        # Create token: identity must be a string
        access_token = create_access_token(
            identity=user_dict['email'],
            additional_claims={"role": user_dict['role']},
            expires_delta=timedelta(hours=1)
        )

        # Optional: Store token in DB
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

        return jsonify({"message": "Login successful", "user": user_dict, "access_token": access_token}), 200
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
    parameters:
      - name: body    
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:  
        description: Subject added successfully
      400:
        description: Name and description are required or subject name already exists
    security:
      - Bearer: []
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
        return jsonify({'message': 'Subject added successfully'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Subject name already exists'}), 400

    finally:
        conn.close()

@app.route('/api/get_subjects', methods=['GET'])
@admin_required
def get_subjects():
    """
    Get list of all subjects (Admin only)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: List of subjects
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subjects')
    subjects = cursor.fetchall()
    conn.close()

    subject_list = [subject_to_dict(subject) for subject in subjects]

    return jsonify({"subjects": subject_list}), 200

@app.route('/api/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    """Update an existing subject (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Subject updated successfully
      400:
        description: Name and description are required
      404:
        description: Subject not found
    security:
      - Bearer: []
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE subjects SET name = ?, description = ? WHERE id = ?', (name, description, subject_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Subject updated successfully"}), 200


@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    """Delete a subject (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: subject_id
        in: path
        required: true
        type: integer
    responses:   
      200:
        description: Subject deleted successfully
      404:    
        description: Subject not found
    security:
      - Bearer: []
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Subject deleted successfully"}), 200 


@app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
@admin_required
def get_chapters_by_subject(subject_id):
    """Get all chapters for a specific subject (Admin only)
    ---
    tags:
      - Admin
    parameters:   
      - name: subject_id
        in: path
        required: true
        type: integer
    responses:  
      200:
        description: List of chapters for the subject
      404:
        description: Subject not found
    security:
      - Bearer: []
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
    subject = cursor.fetchone()

    if not subject:
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
    """Add a new chapter to a subject (admin only)
    ---
    tags:
      - Admin
    parameters:   
      - name: subject_id
        in: path  
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema: 
          type: object
          properties:
            name:
              type: string  
            description:
              type: string
    responses:
      201:
        description: Chapter added successfully
      400:
        description: Chapter name is required or subject not found
    security:
      - Bearer: []
    """
    data = request.json
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
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Chapter updated successfully
      404:
        description: Chapter not found
    security:
      - Bearer: []
    """
    data = request.json
    name = data.get('name')
    description = data.get('description')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM chapters WHERE id = ?', (chapter_id,))
    if not cursor.fetchone():
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
    Delete a chapter (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: chapter_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Chapter deleted
      404:
        description: Chapter not found
    security:
      - Bearer: []
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
        type: integer
    responses:  
      200:
        description: List of quizzes for the chapter
      404:
        description: Chapter not found
    security:
      - Bearer: []
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Validate if chapter exists
    cursor.execute('SELECT name FROM chapters WHERE id = ?', (chapter_id,))
    chapter = cursor.fetchone()

    if not chapter:
        conn.close()
        return jsonify({'error': 'Chapter not found'}), 404

    chapter_name = chapter[0]

    # Fetch all quizzes for the chapter
    cursor.execute('''
        SELECT id, quiz_name, date_of_quiz, time_duration 
        FROM quiz 
        WHERE chapter_id = ?
    ''', (chapter_id,))
    quizzes = cursor.fetchall()
    conn.close()

    # Format and return response
    return jsonify({
        'chapter_name': chapter_name,
        'quizzes': [
            {
                'id': q[0],
                'quiz_name': q[1],
                'date_of_quiz': q[2],
                'time_duration': q[3]
            } for q in quizzes
        ]
    }), 200

@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@admin_required
def add_quiz(chapter_id):
    """
    Add a new quiz to a chapter (admin only)
    ---
    tags:
      - Admin
    parameters:   
      - name: chapter_id  
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
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
      400:
        description: All fields are required
      409:
        description: Quiz with same name exists
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










#--------------------------------------------------GET ALL USERS ENDPOINT---------------------------------------------------
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
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch only users with role='user'
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
      404:
        description: User not found
      403:
        description: Admin access required
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    # Delete user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"}), 200






if __name__ == '__main__':
    app.run(debug=True)
