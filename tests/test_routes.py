import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(str(Path(__file__).parent.parent))

from app.modules import create_app
from app.modules.task_manager import TaskManager
from app.modules.task import Task

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_task():
    return {
        "title": "Tarea de prueba",
        "description": "Descripción de prueba",
        "priority": "alta",
        "effort_hours": 5,
        "status": "pendiente",
        "assigned_to": "Usuario prueba"
    }

# Prueba que verifica la obtención de todas las tareas
def test_get_tasks(client, setup_teardown):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Prueba que verifica la obtención de una tarea específica
def test_get_task(client, setup_teardown, test_task):
    # Crear una tarea primero
    response = client.post('/tasks', json=test_task)
    task_id = response.json['id']
    
    # Obtener la tarea creada
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == test_task['title']

# Prueba que verifica la creación de una tarea
def test_create_task(client, setup_teardown, test_task):
    response = client.post('/tasks', json=test_task)
    assert response.status_code == 201
    assert response.json['title'] == test_task['title']
    assert 'id' in response.json

# Prueba que verifica la actualización de una tarea
def test_update_task(client, setup_teardown, test_task):
    # Crear una tarea primero
    response = client.post('/tasks', json=test_task)
    task_id = response.json['id']
    
    # Actualizar la tarea
    update_data = {
        "title": "Título actualizado",
        "status": "en progreso"
    }
    response = client.put(f'/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['title'] == update_data['title']
    assert response.json['status'] == update_data['status']

# Prueba que verifica la eliminación de una tarea
def test_delete_task(client, setup_teardown, test_task):
    # Crear una tarea primero
    response = client.post('/tasks', json=test_task)
    task_id = response.json['id']
    
    # Eliminar la tarea
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    
    # Verificar que la tarea ya no existe
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 404 