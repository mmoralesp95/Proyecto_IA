import pytest
import os
from app.task_manager import TaskManager

# Ruta del archivo de pruebas
TEST_TASKS_FILE = "test_tasks.json"

@pytest.fixture
def setup_teardown():
    # Configuración inicial
    original_file = TaskManager.TASKS_FILE
    TaskManager.TASKS_FILE = TEST_TASKS_FILE
    
    # Limpiar el archivo de pruebas si existe
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)
    
    yield
    
    # Limpieza después de las pruebas
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)
    TaskManager.TASKS_FILE = original_file 