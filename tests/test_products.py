"""
Tests para endpoints de productos.
"""

import pytest


def test_get_products(client):
    """Test para listar productos."""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_product_not_found(client):
    """Test para producto no encontrado."""
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_create_product(client):
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


def test_get_product_by_id(client):
    """Test para obtener producto por ID."""
    # Primero crear un producto
    new_product = {
        "name": "Get Product",
        "description": "A product to get",
        "price": 50.00,
        "stock": 5,
    }
    create_response = client.post("/products/", json=new_product)
    product_id = create_response.json()["id"]

    # Luego obtenerlo
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert "name" in data
    assert "price" in data


def test_create_product_invalid_price(client):
    """Test para creación con precio negativo."""
    new_product = {"name": "Test Product", "price": -10.00, "stock": 10}
    response = client.post("/products/", json=new_product)
    assert response.status_code == 422


def test_update_product(client):
    """Test para actualizar producto."""
    # Crear producto
    new_product = {
        "name": "Original Product",
        "description": "Original description",
        "price": 100.00,
        "stock": 10,
    }
    create_response = client.post("/products/", json=new_product)
    product_id = create_response.json()["id"]

    # Actualizar
    updated_product = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 150.00,
        "stock": 20,
    }
    response = client.put(f"/products/{product_id}", json=updated_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]
    assert data["price"] == updated_product["price"]


def test_delete_product(client):
    """Test para eliminar producto."""
    # Crear producto
    new_product = {
        "name": "Delete Product",
        "price": 25.00,
        "stock": 5,
    }
    create_response = client.post("/products/", json=new_product)
    product_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_products_filter_by_price(client):
    """Test de filtro por precio."""
    # Crear productos con diferentes precios
    client.post("/products/", json={"name": "Cheap", "price": 10.00, "stock": 1})
    client.post("/products/", json={"name": "Expensive", "price": 100.00, "stock": 1})

    response = client.get("/products/?min_price=50")
    assert response.status_code == 200
    data = response.json()
    for product in data:
        assert float(product["price"]) >= 50


def test_openapi_docs_available(client):
    """Test que la documentación OpenAPI está disponible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
