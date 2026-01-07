"""
Tests para endpoints de usuarios.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_users():
    """Test para listar usuarios."""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_user_by_id():
    """Test para obtener usuario por ID."""
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "email" in data
    assert "name" in data


def test_get_user_not_found():
    """Test para usuario no encontrado."""
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_create_user():
    """Test para crear usuario."""
    new_user = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword123",
        "is_active": True,
    }
    response = client.post("/users/", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == new_user["email"]
    assert data["name"] == new_user["name"]
    assert "id" in data


def test_create_user_invalid_email():
    """Test para creación con email inválido."""
    new_user = {"email": "invalid-email", "name": "Test User", "password": "securepassword123"}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 422


def test_users_pagination():
    """Test de paginación de usuarios."""
    response = client.get("/users/?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 1
