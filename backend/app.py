import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "application": "AWS Security Hardening Demo",
        "status": "running"
    })

@app.get("/health")
def health():
    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            connect_timeout=3
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return jsonify({
            "status": "UP",
            "database": "connected"
        }), 200

    except Exception:
        app.logger.exception("Health check failed")
        return jsonify({"status": "DOWN"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
