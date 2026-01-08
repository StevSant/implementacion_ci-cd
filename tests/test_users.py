"""
Tests para endpoints de usuarios.
"""

import pytest


def test_get_users(client):
    """Test para listar usuarios."""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_user_not_found(client):
    """Test para usuario no encontrado."""
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_create_user(client):
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


def test_get_user_by_id(client):
    """Test para obtener usuario por ID."""
    # Primero crear un usuario
    new_user = {
        "email": "getuser@example.com",
        "name": "Get User",
        "password": "securepassword123",
        "is_active": True,
    }
    create_response = client.post("/users/", json=new_user)
    user_id = create_response.json()["id"]

    # Luego obtenerlo
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "email" in data
    assert "name" in data


def test_create_user_invalid_email(client):
    """Test para creación con email inválido."""
    new_user = {"email": "invalid-email", "name": "Test User", "password": "securepassword123"}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 422


def test_create_user_duplicate_email(client):
    """Test para email duplicado."""
    new_user = {
        "email": "duplicate@example.com",
        "name": "First User",
        "password": "securepassword123",
    }
    client.post("/users/", json=new_user)

    # Intentar crear otro con el mismo email
    response = client.post("/users/", json=new_user)
    assert response.status_code == 400


def test_users_pagination(client):
    """Test de paginación de usuarios."""
    # Crear algunos usuarios
    for i in range(3):
        client.post(
            "/users/",
            json={
                "email": f"user{i}@example.com",
                "name": f"User {i}",
                "password": "securepassword123",
            },
        )

    response = client.get("/users/?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 1


def test_delete_user(client):
    """Test para eliminar usuario."""
    # Crear usuario
    new_user = {
        "email": "delete@example.com",
        "name": "Delete User",
        "password": "securepassword123",
    }
    create_response = client.post("/users/", json=new_user)
    user_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
