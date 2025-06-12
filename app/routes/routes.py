from flask import Blueprint, jsonify, request
from app.services.task_manager import TaskManager
from app.models.task import Task
from app.services import client, deployment_name

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
      404:
        description: Archivo de tareas no encontrado
      500:
        description: Error interno del servidor
    """
    try:
        tasks = TaskManager.load_tasks()
        return jsonify([task.to_dict() for task in tasks]), 200
    except FileNotFoundError:
        return jsonify({"error": "Tasks file not found"}), 404
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
      500:
        description: Error interno del servidor
    """
    try:
      tasks = TaskManager.load_tasks()
      for task in tasks:
          if task.id == task_id:
              return jsonify(task.to_dict()), 200
      return jsonify({"error": "Task not found"}), 404
    except FileNotFoundError:
        return jsonify({"error": "Tasks file not found"}), 404
    except Exception as e:  
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


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

@tasks_bp.route("/ai/tasks/describe", methods=["POST"])
def describe_tasks():
    """
    Generar una descripción breve de una tarea usando IA
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
      200:
        description: Descripción generada
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
      400:
        description: Datos inválidos o faltantes
      500:
        description: Error interno del servidor
    """
    if not client or not deployment_name:
        return jsonify({"error": "AI service not configured"}), 500
    try:
    
      data = request.get_json()
      if data is None:
              return jsonify({"error": "No input data provided"}), 400
      title = data.get("title", '')

      response = client.chat.completions.create(
          model=deployment_name,
          messages=[
              {"role": "system", "content": "Eres experto generando descripciones técnicas breves."},
              {"role": "user", "content": f"Describe brevemente la tarea '{title}'"}
          ]
      )

      description = response.choices[0].message.content.strip()


      return jsonify({
          "title": data["title"],
          "description": description
      }), 200
    except ValueError:
        return jsonify({"error": "Invalid input data"}), 400

    except Exception as e:
      return jsonify({"error": "Internal server error", "details": str(e)}), 500

@tasks_bp.route("/ai/tasks/categorize", methods=["POST"])
def categorize_tasks():
    """
    Categorizar una tarea usando IA
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
      200:
        description: Categoría generada
        schema:
          type: object
          properties:
            category:
              type: string
      400:
        description: Datos inválidos o faltantes
      500:
        description: Error interno del servidor
    """
    if not client or not deployment_name:
        return jsonify({"error": "AI service not configured"}), 500
    
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No input data provided"}), 400
        
        title = data.get("title", '')
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Eres experto categorizando tareas.Las categorías pueden ser: Frontend, Backend, Testing, Infra, etc."},
                {"role": "user", "content": f"Categoriza la tarea en una palabra cuyo titulo es '{title} cuyo descripción es '{data.get('description', '')}'"}  
            ]
        )

        category = response.choices[0].message.content.strip()

        return jsonify({
            "category": category
        }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid input data"}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@tasks_bp.route("/ai/tasks/estimate", methods=["POST"])
def estimate_task():
    """
    Estimar el esfuerzo de una tarea usando IA
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
            status:
              type: string
            assigned_to:
              type: string
            
    responses:
      200:
        description: Estimación generada
        schema:
          type: object
          properties:
            effort_hours:
              type: integer
      400:
        description: Datos inválidos o faltantes
      500:
        description: Error interno del servidor
    """
    if not client or not deployment_name:
        return jsonify({"error": "AI service not configured"}), 500
    
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No input data provided"}), 400
        
        title = data.get("title", '')
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Eres experto estimando el esfuerzo de tareas."},
                {"role": "user", "content": f"Responde solo con un numero entero estimando el esfuerzo en un numero en horas para la tarea '{title}' cuyo descripción es '{data.get('description', '')}' y catergoría '{data.get('category', '')}'"}
            ]
        )

        effort_hours = response.choices[0].message.content.strip()

        print(f"Effort hours response: {effort_hours}")  # Debugging line

        try:
            effort_hours = int(effort_hours)
        except ValueError:
            return jsonify({"error": "Invalid effort_hours value"}), 400

        return jsonify({
            "effort_hours": effort_hours
        }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid input data"}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500    

@tasks_bp.route("/ai/tasks/audit", methods=["POST"])
def audit_task():
    """
    Auditar una tarea con IA: análisis y mitigación de riesgos.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
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
            category:
              type: string
    responses:
      200:
        description: Tarea auditada con análisis y mitigación de riesgos
        schema:
          type: object
          properties:
            id:
              type: integer
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
            category:
              type: string
            risk_analysis:
              type: string
            risk_mitigation:
              type: string
      400:
        description: Datos inválidos o faltantes
      500:
        description: Error interno del servidor
    """
    if not client or not deployment_name:
        return jsonify({"error": "AI service not configured"}), 500

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No input data provided"}), 400

        # Validación básica de campos requeridos
        required_fields = ["title", "description", "priority", "effort_hours", "status", "assigned_to", "category"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400

        # 1. Petición al LLM para análisis de riesgos
        risk_analysis_prompt = (
            f"Analiza los riesgos potenciales de la siguiente tarea:\n"
            f"Título: {data['title']}\n"
            f"Descripción: {data['description']}\n"
            f"Prioridad: {data['priority']}\n"
            f"Esfuerzo estimado: {data['effort_hours']} horas\n"
            f"Estado: {data['status']}\n"
            f"Asignado a: {data['assigned_to']}\n"
            f"Categoría: {data['category']}\n"
            f"Enumera los riesgos más relevantes."
        )
        risk_analysis_response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Eres un experto en gestión de proyectos y análisis de riesgos."},
                {"role": "user", "content": risk_analysis_prompt}
            ]
        )
        risk_analysis = risk_analysis_response.choices[0].message.content.strip()

        # 2. Petición al LLM para mitigación de riesgos
        risk_mitigation_prompt = (
            f"Para la tarea:\n"
            f"Título: {data['title']}\n"
            f"Descripción: {data['description']}\n"
            f"Prioridad: {data['priority']}\n"
            f"Esfuerzo estimado: {data['effort_hours']} horas\n"
            f"Estado: {data['status']}\n"
            f"Asignado a: {data['assigned_to']}\n"
            f"Categoría: {data['category']}\n"
            f"Riesgos identificados: {risk_analysis}\n"
            f"Proporciona un plan de mitigación para estos riesgos."
        )
        risk_mitigation_response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Eres un experto en gestión de proyectos y mitigación de riesgos."},
                {"role": "user", "content": risk_mitigation_prompt}
            ]
        )
        risk_mitigation = risk_mitigation_response.choices[0].message.content.strip()

        # Devuelve la tarea con los nuevos campos
        audited_task = {
            "id": data.get("id"),
            "title": data["title"],
            "description": data["description"],
            "priority": data["priority"],
            "effort_hours": data["effort_hours"],
            "status": data["status"],
            "assigned_to": data["assigned_to"],
            "category": data["category"],
            "risk_analysis": risk_analysis,
            "risk_mitigation": risk_mitigation
        }

        return jsonify(audited_task), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500