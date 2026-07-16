from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory "database" — just a list of dicts
tasks = [
    {"id": 1, "title": "Learn CI/CD", "done": False},
    {"id": 2, "title": "Build a REST API", "done": False},
]
next_id = 3


def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


# CREATE
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="Missing 'title' field")

    task = {"id": next_id, "title": data["title"], "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


# READ (all)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# READ (one)
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)
    if task is None:
        abort(404, description="Task not found")
    return jsonify(task), 200


# UPDATE
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = find_task(task_id)
    if task is None:
        abort(404, description="Task not found")

    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task), 200


# DELETE
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = find_task(task_id)
    if task is None:
        abort(404, description="Task not found")

    tasks = [t for t in tasks if t["id"] != task_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)