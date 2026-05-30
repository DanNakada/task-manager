from flask import Flask, jsonify, request
from src.models import Task

app = Flask(__name__)

tasks = []
next_id = 1


def find_task(task_id):
    return next((t for t in tasks if t.id == task_id), None)


def validate_task_data(data, require_title=True):
    if require_title and (not data or "title" not in data):
        return "O campo 'title' é obrigatório"
    if data and "title" in data and len(data["title"].strip()) == 0:
        return "O título não pode ser vazio"
    if data and "status" in data and data["status"] not in ["pending", "done"]:
        return "Status inválido. Use 'pending' ou 'done'"
    return None


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    error = validate_task_data(data, require_title=True)
    if error:
        return jsonify({"error": error}), 400

    task = Task(
        id=next_id,
        title=data["title"].strip(),
        description=data.get("description", ""),
        status=data.get("status", "pending")
    )
    tasks.append(task)
    next_id += 1

    return jsonify(task.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)