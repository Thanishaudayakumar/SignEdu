from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# 🔹 MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change if using remote DB
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Thanisha@20'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sign_language_app'

mysql = MySQL(app)

# 🔹 User Signup Endpoint
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        fullname = data['fullname']
        username = data['username']
        email = data['email']
        password = data['password']

        # 🔹 Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)", 
                    (fullname, username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Make accessible over network
