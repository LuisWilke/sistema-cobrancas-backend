import pytest
from app import create_app
from database import db
from flask_jwt_extended import decode_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_login_invalido(client):
    resposta = client.post('/api/login', json={
        'email': 'teste@teste.com',
        'senha': '123456'
    })

    assert resposta.status_code == 401
    json_resposta = resposta.get_json()
    assert 'Credenciais inválidas' in json_resposta['erro']