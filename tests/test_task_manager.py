import pytest
import os
import json
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(str(Path(__file__).parent.parent))

from app.modules.task_manager import TaskManager
from app.modules.task import Task

# Ruta del archivo de pruebas
TEST_TASKS_FILE = "test_tasks.json"

# Prueba que verifica la carga de tareas cuando el archivo no existe
def test_load_tasks_file_not_exists(setup_teardown):
    tasks = TaskManager.load_tasks()
    assert tasks == []

# Prueba que verifica la carga de tareas cuando el archivo existe
def test_load_tasks_file_exists(setup_teardown):
    # Crear datos de prueba
    test_tasks = [
        {
            "id": 1,
            "title": "Tarea 1",
            "description": "Descripción 1",
            "priority": "alta",
            "effort_hours": 5,
            "status": "pendiente",
            "assigned_to": "Usuario 1"
        }
    ]
    
    # Guardar datos de prueba
    with open(TaskManager.TASKS_FILE, "w") as file:
        json.dump(test_tasks, file)
    
    # Cargar y verificar
    tasks = TaskManager.load_tasks()
    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert tasks[0].title == "Tarea 1"

# Prueba que verifica el guardado de tareas
def test_save_tasks(setup_teardown):
    # Crear tarea de prueba
    task = Task(
        id=1,
        title="Tarea de prueba",
        description="Descripción de prueba",
        priority="media",
        effort_hours=3,
        status="en progreso",
        assigned_to="Usuario prueba"
    )
    
    # Guardar tarea
    TaskManager.save_tasks([task])
    
    # Verificar que el archivo existe y contiene los datos correctos
    assert os.path.exists(TaskManager.TASKS_FILE)
    with open(TaskManager.TASKS_FILE, "r") as file:
        saved_data = json.load(file)
        assert len(saved_data) == 1
        assert saved_data[0]["title"] == "Tarea de prueba" 