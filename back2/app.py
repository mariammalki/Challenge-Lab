from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "database": os.environ.get("DB_NAME", "mydb"),
    "user": os.environ.get("DB_USER", "myuser"),
    "password": os.environ.get("DB_PASSWORD", "pass1234"),
    "port": int(os.environ.get("DB_PORT", 5432))
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/users/count', methods=['GET'])
def count_users():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM users")
                count = cur.fetchone()[0]
        return jsonify({"total_users": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Back2 (Users Count API) is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
