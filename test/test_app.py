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
class MockCompletions:
    def create(self, *args, **kwargs):
        return fake_openai_response()
    def parse(self, *args, **kwargs):
        return fake_openai_response()

class MockChat:
    completions = MockCompletions()

class MockBeta:
    chat = MockChat()

class MockAzureOpenAI:
    def __init__(self, *args, **kwargs):
        self.chat = MockChat()
        self.beta = MockBeta()

with patch("openai.AzureOpenAI", MockAzureOpenAI):
    from run import app
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    with app.app_context():
        from app.db import Base, engine
        Base.metadata.create_all(bind=engine)

def test_root():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hola" in response.data

def test_user_stories_list():
    tester = app.test_client()
    response = tester.get('/user-stories')
    assert response.status_code == 200
    assert b"Historias de Usuario" in response.data

def test_add_user_story():
    tester = app.test_client()
    response = tester.post('/user-stories', data={'prompt': 'Como usuario quiero...'}, follow_redirects=True)
    print(response.data)  # Para ver el error real si falla
    assert response.status_code == 200
    assert b"Historia de usuario creada correctamente" in response.data

def test_add_user_story_empty_prompt():
    tester = app.test_client()
    response = tester.post('/user-stories', data={'prompt': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b"error" in response.data.lower() or b"prompt" in response.data.lower()

def test_404():
    tester = app.test_client()
    response = tester.get('/no-existe')
    assert response.status_code == 404