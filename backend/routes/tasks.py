from flask import Blueprint, request, jsonify
from models.db import get_db_connection
from utils.auth_decorator import token_required

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["GET"])
@token_required
def get_tasks(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Only return tasks belonging to the logged-in user
            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC",
                (current_user_id,)
            )
            tasks = cursor.fetchall()
        return jsonify(tasks), 200
    finally:
        conn.close()


@tasks_bp.route("/tasks", methods=["POST"])
@token_required
def create_task(current_user_id):
    data = request.get_json()

    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    description = data.get("description")
    category_id = data.get("category_id")
    priority = data.get("priority", "medium")
    deadline = data.get("deadline")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO tasks (user_id, category_id, title, description, priority, deadline)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (current_user_id, category_id, title, description, priority, deadline)
            )
            new_task_id = cursor.lastrowid
        return jsonify({"message": "Task created", "task_id": new_task_id}), 201
    finally:
        conn.close()


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@token_required
def update_task(current_user_id, task_id):
    data = request.get_json()

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Confirm the task belongs to this user before updating
            cursor.execute(
                "SELECT task_id FROM tasks WHERE task_id = %s AND user_id = %s",
                (task_id, current_user_id)
            )
            if not cursor.fetchone():
                return jsonify({"error": "Task not found"}), 404

            cursor.execute(
                """UPDATE tasks
                   SET title = %s, description = %s, category_id = %s,
                       priority = %s, status = %s, deadline = %s
                   WHERE task_id = %s""",
                (
                    data.get("title"),
                    data.get("description"),
                    data.get("category_id"),
                    data.get("priority", "medium"),
                    data.get("status", "pending"),
                    data.get("deadline"),
                    task_id
                )
            )
        return jsonify({"message": "Task updated"}), 200
    finally:
        conn.close()


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user_id, task_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE task_id = %s AND user_id = %s",
                (task_id, current_user_id)
            )
            if cursor.rowcount == 0:
                return jsonify({"error": "Task not found"}), 404
        return jsonify({"message": "Task deleted"}), 200
    finally:
        conn.close()