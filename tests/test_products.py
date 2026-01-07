"""
Tests para endpoints de productos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_products():
    """Test para listar productos."""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_product_by_id():
    """Test para obtener producto por ID."""
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "price" in data


def test_get_product_not_found():
    """Test para producto no encontrado."""
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_create_product():
    """Test para crear producto."""
    new_product = {
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "stock": 10,
    }
    response = client.post("/products/", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_product["name"]
    assert "id" in data


def test_create_product_invalid_price():
    """Test para creación con precio negativo."""
    new_product = {"name": "Test Product", "price": -10.00, "stock": 10}
    response = client.post("/products/", json=new_product)
    assert response.status_code == 422


def test_products_filter_by_price():
    """Test de filtro por precio."""
    response = client.get("/products/?min_price=50")
    assert response.status_code == 200
    data = response.json()
    for product in data:
        assert float(product["price"]) >= 50


def test_openapi_docs_available():
    """Test que la documentación OpenAPI está disponible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
