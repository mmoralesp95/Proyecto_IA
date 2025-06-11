import pytest
import os
import sys
from pathlib import Path
import tempfile

# Asegura que 'app' esté en el path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.task_manager import TaskManager
from app.models.task import Task


@pytest.fixture(autouse=True)
def patch_task_file():
    # Crea un archivo temporal para cada test
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        test_file = tmp.name
    original_file = TaskManager.TASKS_FILE
    TaskManager.TASKS_FILE = test_file
    yield
    # Limpia después
    if os.path.exists(test_file):
        os.remove(test_file)
    TaskManager.TASKS_FILE = original_file

def test_load_tasks_returns_empty_when_file_missing():
    # Elimina el archivo temporal para simular que no existe
    if os.path.exists(TaskManager.TASKS_FILE):
        os.remove(TaskManager.TASKS_FILE)
    tasks = TaskManager.load_tasks()
    assert tasks == []

def test_save_and_load_single_task():
    task = Task(
        id=1,
        title="Test",
        description="Descripción",
        priority="alta",
        effort_hours=2,
        status="pendiente",
        assigned_to="Tester"
    )
    TaskManager.save_tasks([task])
    assert os.path.exists(TaskManager.TASKS_FILE)
    loaded_tasks = TaskManager.load_tasks()
    assert len(loaded_tasks) == 1
    loaded = loaded_tasks[0]
    assert isinstance(loaded, Task)
    assert loaded.title == "Test"
    assert loaded.description == "Descripción"
    assert loaded.priority == "alta"
    assert loaded.effort_hours == 2
    assert loaded.status == "pendiente"
    assert loaded.assigned_to == "Tester"

def test_save_and_load_multiple_tasks():
    tasks = [
        Task(id=1, title="T1", description="D1", priority="alta", effort_hours=1, status="pendiente", assigned_to="A"),
        Task(id=2, title="T2", description="D2", priority="media", effort_hours=2, status="en progreso", assigned_to="B"),
    ]
    TaskManager.save_tasks(tasks)
    loaded_tasks = TaskManager.load_tasks()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "T1"
    assert loaded_tasks[1].title == "T2"

def test_load_tasks_with_invalid_file():
    with open(TaskManager.TASKS_FILE, "w") as f:
        f.write("no es json")
    with pytest.raises(RuntimeError):
        TaskManager.load_tasks()