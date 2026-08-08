from flask import Blueprint, request, jsonify
from models.db import get_db_connection
from utils.auth_decorator import token_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories", methods=["GET"])
@token_required
def get_categories(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM categories WHERE user_id = %s",
                (current_user_id,)
            )
            categories = cursor.fetchall()
        return jsonify(categories), 200
    finally:
        conn.close()


@categories_bp.route("/categories", methods=["POST"])
@token_required
def create_category(current_user_id):
    data = request.get_json()

    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    color = data.get("color")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO categories (user_id, name, color) VALUES (%s, %s, %s)",
                (current_user_id, name, color)
            )
            new_id = cursor.lastrowid
        return jsonify({"message": "Category created", "category_id": new_id}), 201
    finally:
        conn.close()


@categories_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@token_required
def delete_category(current_user_id, category_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM categories WHERE category_id = %s AND user_id = %s",
                (category_id, current_user_id)
            )
            if cursor.rowcount == 0:
                return jsonify({"error": "Category not found"}), 404
        return jsonify({"message": "Category deleted"}), 200
    finally:
        conn.close()