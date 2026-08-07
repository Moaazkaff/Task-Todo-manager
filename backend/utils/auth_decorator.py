import jwt
from functools import wraps
from flask import request, jsonify
from config import Config

def token_required(f):
    """
    Decorator for protected routes.
    Expects header: Authorization: Bearer <token>
    Decodes the JWT and passes the user_id into the route as `current_user_id`.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Pass the authenticated user's id into the wrapped route function
        return f(current_user_id, *args, **kwargs)

    return decorated