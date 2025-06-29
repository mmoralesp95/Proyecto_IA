import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with patch("app.routes.routes.AzureOpenAI"):
    from run import app

def test_root():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hola" in response.data