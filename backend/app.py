import hashlib
import sqlite3
from flasgger import Swagger
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import init_db, create_admin, get_connection, user_to_dict
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
#cors 
CORS(app)

# Swagger and JWT setup
swagger = Swagger(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
jwt = JWTManager(app)

# Initialize DB and create default admin
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

@app.route('/api/print-hello', methods=['GET'])
@jwt_required()
def print_hello():
    """
    Returns a hello message for quiz master (JWT protected)
    ---
    tags:
      - Utility
    security:
      - Bearer: []
    responses:
      200:
        description: Returns hello message
      401:
        description: Unauthorized
    """
    current_user_email = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role", "unknown")
    return jsonify({"message": "Hello quiz master!", "email": current_user_email, "role": role}), 200

if __name__ == '__main__':
    app.run(debug=True)
