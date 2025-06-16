import json
import os
from app.models.taskModel import TaskModel as Task

class TaskManager:
    # Ruta del archivo JSON donde se almacenarán las tareas
    TASKS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json"))
    @staticmethod
    # Carga las tareas desde el archivo JSON. Si el archivo no existe, retorna una lista vacía
    def load_tasks():
        try:
            if not os.path.exists(TaskManager.TASKS_FILE):
                return []
            with open(TaskManager.TASKS_FILE, "r") as file:
                data = json.load(file)
                return [Task.parse_obj(task) for task in data]
        except (json.JSONDecodeError, IOError, FileNotFoundError) as e:
            raise RuntimeError(f"Error loading tasks: {e}")
        except Exception as e:
            # Para cualquier otro error inesperado
            raise RuntimeError(f"Error loading tasks: {e}")

    @staticmethod
    # Guarda las tareas en el archivo JSON
    def save_tasks(tasks):
        try:
            print(f"GUARDANDO EN: {TaskManager.TASKS_FILE}")
            with open(TaskManager.TASKS_FILE, "w") as file:
                json.dump([task.dict() for task in tasks], file, indent=4)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise RuntimeError(f"Error saving tasks: {e}")
        except Exception as e:
            raise RuntimeError(f"Error saving tasks: {e}")