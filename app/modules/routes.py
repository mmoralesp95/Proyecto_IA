from flask import Blueprint, jsonify, request
from .task_manager import TaskManager
from .task import Task

# Blueprint para agrupar las rutas relacionadas con tareas
tasks_bp = Blueprint("tasks", __name__)

# Obtiene todas las tareas del sistema
@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Obtener todas las tareas
    ---
    responses:
      200:
        description: Lista de tareas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
    """
    tasks = TaskManager.load_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200

# Obtiene una tarea específica por su ID
@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """
    Obtener una tarea por ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID de la tarea
    responses:
      200:
        description: Tarea encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
      404:
        description: Tarea no encontrada
    """
    tasks = TaskManager.load_tasks()
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict()), 200
    return jsonify({"error": "Task not found"}), 404

# Crea una nueva tarea en el sistema
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    """
    Crear una nueva tarea
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            priority:
              type: string
            effort_hours:
              type: integer
            status:
              type: string
            assigned_to:
              type: string
    responses:
      201:
        description: Tarea creada
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
    """
    data = request.get_json()
    tasks = TaskManager.load_tasks()
    if tasks:
        new_id = max(task.id for task in tasks) + 1
    else:
        new_id = 1

    new_task = Task(
        id=new_id,
        title=data["title"],
        description=data["description"],
        priority=data["priority"],
        effort_hours=data["effort_hours"],
        status=data["status"],
        assigned_to=data["assigned_to"]
    )

    tasks.append(new_task)
    TaskManager.save_tasks(tasks)
    return jsonify(new_task.to_dict()), 201

# Actualiza una tarea existente por su ID
@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Actualizar una tarea existente
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID de la tarea
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            priority:
              type: string
            effort_hours:
              type: integer
            status:
              type: string
            assigned_to:
              type: string
    responses:
      200:
        description: Tarea actualizada
      404:
        description: Tarea no encontrada
    """
    data = request.get_json()
    tasks = TaskManager.load_tasks()

    for task in tasks:
        if task.id == task_id:
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.priority = data.get("priority", task.priority)
            task.effort_hours = data.get("effort_hours", task.effort_hours)
            task.status = data.get("status", task.status)
            task.assigned_to = data.get("assigned_to", task.assigned_to)

            TaskManager.save_tasks(tasks)
            return jsonify(task.to_dict()), 200

    return jsonify({"error": "Task not found"}), 404

# Elimina una tarea por su ID
@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Eliminar una tarea por ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID de la tarea
    responses:
      200:
        description: Tarea eliminada
      404:
        description: Tarea no encontrada
    """
    tasks = TaskManager.load_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    TaskManager.save_tasks(tasks)
    return jsonify({"message": "Task deleted"}), 200
