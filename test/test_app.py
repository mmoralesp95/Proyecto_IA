from app import app

def test_root():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hola" in response.data 
