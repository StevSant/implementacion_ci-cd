"""
Fixtures compartidos para tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Cliente de prueba para la API."""
    return TestClient(app)
