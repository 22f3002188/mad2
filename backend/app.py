import sqlite3
from flask import Flask, request, jsonify
from flasgger import Swagger
from models import init_db, create_admin, get_connection, user_to_dict
import hashlib

app = Flask(__name__)
swagger = Swagger(app)  # 👈 Add this line to enable Swagger

init_db()
create_admin()

@app.route('/')
def index():
    return jsonify({"message": "Backend running!"})

@app.route('/api/signup', methods=['POST'])
def signup():
    """
    Register a new user
    ---
    tags:
      - User
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
      - User
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
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user_to_dict(user)})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
