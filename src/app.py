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

@app.route("/tasks", methods=["GET"])
def list_tasks():
    status_filter = request.args.get("status")
    result = tasks

    if status_filter:
        if status_filter not in ["pending", "done"]:
            return jsonify({"error": "Status inválido. Use 'pending' ou 'done'"}), 400
        result = [t for t in tasks if t.status == status_filter]

    return jsonify([t.to_dict() for t in result]), 200


@app.route("/tasks/", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return jsonify(task.to_dict()), 200

@app.route("/tasks/", methods=["PUT"])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    data = request.get_json()
    error = validate_task_data(data, require_title=False)
    if error:
        return jsonify({"error": error}), 400

    task.update(data)
    return jsonify(task.to_dict()), 200

@app.route("/tasks/", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    tasks = [t for t in tasks if t.id != task_id]
    return jsonify({"message": "Tarefa removida com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)