from flask import Flask, jsonify, request

app = Flask(__name__)

# Data dummy untuk menyimpan to-do list
todos = [
    {"id": 1, "task": "Belajar Flask", "done": False},
    {"id": 2, "task": "Mengerjakan PR", "done": False},
]

# Endpoint untuk mendapatkan semua to-do
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# Endpoint untuk mendapatkan to-do berdasarkan ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "To-do tidak ditemukan"}), 404
    return jsonify(todo)

# Endpoint untuk menambahkan to-do baru
@app.route('/todos', methods=['POST'])
def add_todo():
    new_todo = request.get_json()
    if not new_todo or "task" not in new_todo:
        return jsonify({"error": "Data tidak valid"}), 400
    new_todo["id"] = todos[-1]["id"] + 1 if todos else 1
    new_todo["done"] = False
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Endpoint untuk memperbarui to-do berdasarkan ID
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    updated_todo = request.get_json()
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "To-do tidak ditemukan"}), 404
    if not updated_todo or "task" not in updated_todo:
        return jsonify({"error": "Data tidak valid"}), 400
    todo.update(updated_todo)
    return jsonify(todo)

# Endpoint untuk menghapus to-do berdasarkan ID
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"result": "To-do dihapus"})

if __name__ == '__main__':
    app.run(debug=True)
