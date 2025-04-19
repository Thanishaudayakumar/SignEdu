from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import bcrypt
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ✅ Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Thanisha@20",  # Replace safely
    database="sign_language_app"
)
cursor = db.cursor(dictionary=True)

# ✅ Signup API
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required!'}), 400

    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
                   (username, email, hashed_password))
    db.commit()

    return jsonify({'message': 'Signup successful!'}), 201

# ✅ Login API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful!', 'token': 'dummy-token'}), 200

# ✅ Serve frontend HTML files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
