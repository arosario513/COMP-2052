#!venv/bin/python
'''Flask App'''

from flask import Flask, jsonify, request
from task import Task

app: Flask = Flask(__name__)

tasks: list[Task] = [
    Task(0, "Eat"),
    Task(1, "Sleep"),
    Task(2, "Work")
]


@app.route("/", methods=["GET"])
def index():
    '''GET /'''
    return jsonify(message="Basic REST API."), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    '''GET /tasks'''
    return jsonify([i.to_dict() for i in tasks]), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_single_task(task_id: int):
    '''GET /tasks/<int:task_id>'''
    for i in tasks:
        if i.task_id == task_id:
            return jsonify(i.to_dict())

    return jsonify(error=f"Task with ID {task_id} doesn't exist."), 400


@app.route("/tasks", methods=["POST"])
def create_task():
    '''POST /tasks'''
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify(error="Incomplete data."), 400

    t_id: int = tasks[-1].task_id + 1 if tasks else 0
    t: Task = Task(t_id, name)
    tasks.append(t)
    return jsonify(message="New task added.", task=t.to_dict()), 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    '''PUT /tasks/<task_id>'''
    data = request.get_json()
    new_name = data.get("name")

    if not new_name:
        return jsonify(error="Incomplete data."), 400

    for i in tasks:
        if i.task_id == task_id:
            old_task = i.to_dict().copy()
            i.name = new_name
            return jsonify(message=f"Updated name for task with ID {task_id}.", old_task=old_task, new_task=i.to_dict()), 200
    return jsonify(error=f"Task with ID {task_id} not found."), 400


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    '''DELETE /tasks/<int:task_id>'''
    for i, j in enumerate(tasks):
        if j.task_id == task_id:
            tasks.pop(i)
            return jsonify(message=f"Task with ID {task_id} deleted."), 200
    return jsonify(error=f"Task with ID {task_id} doesn't exist."), 400


if __name__ == "__main__":
    app.run(debug=True)
