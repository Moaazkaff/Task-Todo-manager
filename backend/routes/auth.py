import jwt
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_db_connection
from config import Config

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    # Hash the password — never store plain text passwords
    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if the email is already registered
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already registered"}), 409

            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, password_hash)
            )
        return jsonify({"message": "User registered successfully"}), 201
    finally:
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
    finally:
        conn.close()

    # Check the user exists and the password matches the stored hash
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Build the JWT payload: which user this is, and when it expires
    payload = {
        "user_id": user["user_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token}), 200