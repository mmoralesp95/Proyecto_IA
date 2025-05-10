import json
import os
from .task import Task

class TaskManager:
    # Ruta del archivo JSON donde se almacenarán las tareas
    TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "tasks.json")

    @staticmethod
    # Carga las tareas desde el archivo JSON. Si el archivo no existe, retorna una lista vacía
    def load_tasks():
        if not os.path.exists(TaskManager.TASKS_FILE):
            return []

        with open(TaskManager.TASKS_FILE, "r") as file:
            data = json.load(file)
            return [Task.from_dict(task) for task in data]

    @staticmethod
    # Guarda las tareas en el archivo JSON
    def save_tasks(tasks):
        with open(TaskManager.TASKS_FILE, "w") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)
