from flask import Blueprint, jsonify, request
from .task_manager import TaskManager
from .task import Task

# Blueprint para agrupar las rutas relacionadas con tareas
tasks_bp = Blueprint("tasks", __name__)

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
      500:
        description: Error interno del servidor
    """
    try:
        tasks = TaskManager.load_tasks()
        return jsonify([task.to_dict() for task in tasks]), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


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
      400:
        description: Datos inválidos o faltantes
      500:
        description: Error interno del servidor
    """
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No input data provided"}), 400

        required_fields = ["title", "description", "priority", "effort_hours", "status", "assigned_to"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400
        
        # Validación de tipos y formatos
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({"error": "Title must be a non-empty string"}), 400
        if not isinstance(data["description"], str):
            return jsonify({"error": "Description must be a string"}), 400
        if not isinstance(data["priority"], str):
            return jsonify({"error": "Priority must be a string"}), 400
        if not isinstance(data["effort_hours"], int) or data["effort_hours"] < 0:
            return jsonify({"error": "Effort_hours must be a non-negative integer"}), 400
        if not isinstance(data["status"], str):
            return jsonify({"error": "Status must be a string"}), 400
        if not isinstance(data["assigned_to"], str):
            return jsonify({"error": "Assigned_to must be a string"}), 400

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
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


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
      400:
        description: Datos inválidos
      404:
        description: Tarea no encontrada
      500:
        description: Error interno del servidor
    """
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validación de tipos y formatos solo para los campos presentes
        if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
            return jsonify({"error": "Title must be a non-empty string"}), 400
        if "description" in data and not isinstance(data["description"], str):
            return jsonify({"error": "Description must be a string"}), 400
        if "priority" in data and not isinstance(data["priority"], str):
            return jsonify({"error": "Priority must be a string"}), 400
        if "effort_hours" in data and (not isinstance(data["effort_hours"], int) or data["effort_hours"] < 0):
            return jsonify({"error": "Effort_hours must be a non-negative integer"}), 400
        if "status" in data and not isinstance(data["status"], str):
            return jsonify({"error": "Status must be a string"}), 400
        if "assigned_to" in data and not isinstance(data["assigned_to"], str):
            return jsonify({"error": "Assigned_to must be a string"}), 400

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
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


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
    original_count = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]
    if len(tasks) == original_count:
        return jsonify({"error": "Task not found"}), 404
    TaskManager.save_tasks(tasks)
    return jsonify({"message": "Task deleted"}), 200
