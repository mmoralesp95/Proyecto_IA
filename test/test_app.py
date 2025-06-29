import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ["AZURE_OPENAI_KEY"] = "dummy"
os.environ["AZURE_OPENAI_ENDPOINT"] = "dummy"
os.environ["AZURE_OPENAI_API_VERSION"] = "dummy"
os.environ["AZURE_OPENAI_DEPLOYMENT"] = "dummy"

with patch("openai.AzureOpenAI", MagicMock()):
    from run import app

def test_root():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hola" in response.data