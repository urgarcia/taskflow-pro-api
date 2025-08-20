from flask import Blueprint, request, jsonify, abort, g
from app.services.task_service import TaskService
from app.services.jwt_service import jwt_required

tasks_bp = Blueprint('tasks', __name__)
task_service = TaskService()

# GET /tasks: Obtener todas las tareas
@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required
def get_tasks():
    # Los datos del usuario están en g.current_user
    tasks = task_service.list_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200

# GET /tasks/<id>: Obtener una tarea específica por ID
@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@jwt_required
def get_task(id):
    task = task_service.get_task(id)
    if not task:
        abort(404, description='Task not found')
    return jsonify(task.to_dict()), 200

# POST /tasks: Crear una nueva tarea
@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description='Title is required')
    task = task_service.create_task(data['title'], data.get('description', ''))
    return jsonify(task.to_dict()), 201

# PUT /tasks/<id>: Actualizar una tarea existente
@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required
def update_task(id):
    data = request.get_json()
    updated = task_service.update_task(id, data)
    if not updated:
        abort(404, description='Task not found')
    return jsonify(updated.to_dict()), 200

# DELETE /tasks/<id>: Eliminar una tarea
@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required
def delete_task(id):
    deleted = task_service.delete_task(id)
    if not deleted:
        abort(404, description='Task not found')
    return '', 204