import pytest
from app.api import app
from app.models import User
from app.auth import hash_password

@pytest.fixture #fonction spéciale utilisée par pytest pour préparer un env propre pour le test
def client():
    app.config["TESTING"] = True #active le mode test de Flask
    return app.test_client() # crrée un client de test

def test_login_missing_fields_returns_422(client):
    r = client.post("/api/login", json={})#envoie une requête vide
    assert r.status_code == 422

def test_data_without_token_returns_401(client):
    r = client.get("/api/data")#on appelle ssans token JWT
    assert r.status_code == 401

def test_register_creates_user(client):#on crée un user
    r = client.post("/api/register", json={
        "username": "damien",
        "password": "password123"
    })
    assert r.status_code == 201

def test_register_existing_user_returns_400(client):
    client.post("/api/register", json={
        "username": "damien",
        "password": "password123"
    })
    r = client.post("/api/register", json={
        "username": "damien",
        "password": "password123"
    })
    assert r.status_code == 400

def test_login_wrong_password_returns_401(client):
    client.post("/api/register", json={
        "username": "damien",
        "password": "password123"
    })
    r = client.post("/api/login", json={
        "username": "damien",
        "password": "wrongpass"
    })
    assert r.status_code == 401