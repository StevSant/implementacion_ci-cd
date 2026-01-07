"""
Tests para endpoints de health.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test del endpoint de health check."""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_readiness_check():
    """Test del endpoint de readiness."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True
    assert data["database"] == "connected"


def test_liveness_check():
    """Test del endpoint de liveness."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["alive"] is True


def test_root_endpoint():
    """Test del endpoint raíz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
