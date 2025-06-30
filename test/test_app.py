import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Variables de entorno dummy
os.environ["AZURE_OPENAI_KEY"] = "dummy"
os.environ["AZURE_OPENAI_ENDPOINT"] = "dummy"
os.environ["AZURE_OPENAI_API_VERSION"] = "dummy"
os.environ["AZURE_OPENAI_DEPLOYMENT"] = "dummy"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Mock de la respuesta de OpenAI
# Esta función simula la respuesta de OpenAI para evitar llamadas reales a la API
def fake_openai_response(*args, **kwargs):
    class Parsed:
        def __init__(self):
            self.project = "Proyecto Demo"
            self.role = "Usuario"
            self.goal = "Hacer algo"
            self.reason = "Para lograr un objetivo"
            self.description = "Descripción de la historia"
            self.priority = "alta"
            self.story_points = 5
            self.effort_hours = 8

    class Message:
        def __init__(self):
            self.parsed = Parsed()

    class FakeChoice:
        def __getitem__(self, key):
            return self
        @property
        def message(self):
            return Message()
    class FakeResponse:
        choices = [FakeChoice()]
    return FakeResponse()

# Mock de AzureOpenAI SOLO para la clase, usando clases normales
# esto es necesario porque la clase AzureOpenAI no se puede instanciar directamente
# y no tiene un método beta como se esperaba en el código original.
class MockCompletions:
    def create(self, *args, **kwargs):
        return fake_openai_response()
    def parse(self, *args, **kwargs):
        return fake_openai_response()
# Mock de las clases anidadas para simular la estructura de AzureOpenAI
class MockChat: 
    completions = MockCompletions()
# MockBeta para simular la estructura de AzureOpenAI
class MockBeta:
    chat = MockChat()
# MockAzureOpenAI para simular la clase AzureOpenAI
class MockAzureOpenAI:
    def __init__(self, *args, **kwargs):
        self.chat = MockChat()
        self.beta = MockBeta()
# Mock para reemplazar la clase AzureOpenAI en el código
# Esto es necesario porque la clase AzureOpenAI no se puede instanciar directamente
with patch("openai.AzureOpenAI", MockAzureOpenAI):
    from run import app
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    with app.app_context():
        from app.db import Base, engine
        Base.metadata.create_all(bind=engine)


def test_root():
    """Test la ruta raíz"""
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hola" in response.data

def test_user_stories_list():
    """ Test para la lista de historias de usuario """
    tester = app.test_client()
    response = tester.get('/user-stories')
    assert response.status_code == 200
    assert b"Historias de Usuario" in response.data

def test_add_user_story():
    """ Test para agregar una historia de usuario """
    tester = app.test_client()
    response = tester.post('/user-stories', data={'prompt': 'Como usuario quiero...'}, follow_redirects=True)
    print(response.data)  # Para ver el error real si falla
    assert response.status_code == 200
    assert b"Historia de usuario creada correctamente" in response.data

def test_add_user_story_empty_prompt():
    """ Test para agregar una historia de usuario con un prompt vacío """
    tester = app.test_client()
    response = tester.post('/user-stories', data={'prompt': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b"error" in response.data.lower() or b"prompt" in response.data.lower()

def test_404():
    """ Test para una ruta no existente """
    tester = app.test_client()
    response = tester.get('/no-existe')
    assert response.status_code == 404

def test_delete_user_story():
    """Test para eliminar una historia de usuario"""
    tester = app.test_client()
    # Primero crea una historia de usuario
    tester.post('/user-stories', data={'prompt': 'Como usuario quiero...'}, follow_redirects=True)
    # Elimina la historia de usuario con id 1 (ajusta si tu modelo usa otro id)
    response = tester.post('/user-stories/1/delete', follow_redirects=True)
    assert response.status_code == 200
    # Busca un mensaje de éxito o que ya no esté la historia
    assert b"elimin" in response.data.lower() or b"no hay historias" in response.data.lower()

def test_view_tasks_for_user_story():
    """Test para ver tareas de una historia de usuario"""
    tester = app.test_client()
    tester.post('/user-stories', data={'prompt': 'Como usuario quiero...'}, follow_redirects=True)
    response = tester.get('/user-stories/1/tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b"Tareas" in response.data or b"tarea" in response.data.lower()

def test_add_task_to_user_story():
    """Test para agregar una tarea a una historia de usuario"""
    tester = app.test_client()
    tester.post('/user-stories', data={'prompt': 'Como usuario quiero...'}, follow_redirects=True)
    data = {
        'title': 'Nueva tarea',
        'description': 'Descripción de la tarea'
    }
    response = tester.post('/user-stories/1/tasks', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"tarea" in response.data.lower()