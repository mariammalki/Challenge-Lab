from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Config PostgreSQL depuis variables d'environnement
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db-service"),  # Nom du service PostgreSQL
    "database": os.environ.get("DB_NAME", "mydb"),
    "user": os.environ.get("DB_USER", "myuser"),
    "password": os.environ.get("DB_PASSWORD", "pass1234"),
    "port": int(os.environ.get("DB_PORT", 5432))
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        return jsonify({"message": "User added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email FROM users ORDER BY id")
                rows = [{"id": r[0], "name": r[1], "email": r[2]} for r in cur.fetchall()]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Back1 (Users API) is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
