from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)

VALID_STATUSES = {"todo", "in_progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


def current_user_id():
    return int(get_jwt_identity())


def current_user_is_admin():
    return get_jwt().get("role") == "admin"


def parse_task_payload(data, partial=False):
    errors = {}
    values = {}

    if not partial or "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            errors["title"] = "title is required."
        else:
            values["title"] = title

    if "description" in data:
        values["description"] = data.get("description")

    if "status" in data:
        status = data.get("status")
        if status not in VALID_STATUSES:
            errors["status"] = f"status must be one of: {', '.join(sorted(VALID_STATUSES))}."
        else:
            values["status"] = status

    if "priority" in data:
        priority = data.get("priority")
        if priority not in VALID_PRIORITIES:
            errors["priority"] = f"priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}."
        else:
            values["priority"] = priority

    if "due_date" in data:
        raw_due_date = data.get("due_date")
        if raw_due_date in (None, ""):
            values["due_date"] = None
        else:
            try:
                values["due_date"] = date.fromisoformat(raw_due_date)
            except ValueError:
                errors["due_date"] = "due_date must use YYYY-MM-DD format."

    return values, errors


def get_accessible_task_or_404(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return None, (jsonify({"error": "Task not found."}), 404)

    if not current_user_is_admin() and task.owner_id != current_user_id():
        return None, (jsonify({"error": "You do not have access to this task."}), 403)

    return task, None


@tasks_bp.get("")
@jwt_required()
def list_tasks():
    query = Task.query
    if not current_user_is_admin():
        query = query.filter_by(owner_id=current_user_id())

    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({"tasks": [task.to_dict() for task in tasks]})


@tasks_bp.post("")
@jwt_required()
def create_task():
    data = request.get_json(silent=True) or {}
    values, errors = parse_task_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    task = Task(owner_id=current_user_id(), **values)
    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 201


@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    task, error = get_accessible_task_or_404(task_id)
    if error:
        return error
    return jsonify({"task": task.to_dict()})


@tasks_bp.patch("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    task, error = get_accessible_task_or_404(task_id)
    if error:
        return error

    data = request.get_json(silent=True) or {}
    values, errors = parse_task_payload(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field, value in values.items():
        setattr(task, field, value)

    db.session.commit()
    return jsonify({"task": task.to_dict()})


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    task, error = get_accessible_task_or_404(task_id)
    if error:
        return error

    db.session.delete(task)
    db.session.commit()
    return "", 204
