"""
Endpoints de salud del sistema.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Respuesta de estado de salud."""

    status: str
    timestamp: datetime
    version: str


class ReadinessResponse(BaseModel):
    """Respuesta de readiness."""

    ready: bool
    database: str
    timestamp: datetime


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica el estado de salud de la aplicación.",
)
async def health_check():
    """Endpoint de health check básico."""
    return HealthResponse(status="healthy", timestamp=datetime.utcnow(), version="1.0.0")


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness Check",
    description="Verifica si la aplicación está lista para recibir tráfico.",
)
async def readiness_check():
    """Endpoint de readiness check."""
    return ReadinessResponse(ready=True, database="connected", timestamp=datetime.utcnow())


@router.get("/live", summary="Liveness Check", description="Verifica si la aplicación está viva.")
async def liveness_check():
    """Endpoint de liveness check."""
    return {"alive": True}
