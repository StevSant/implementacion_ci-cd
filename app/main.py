"""
Punto de entrada principal de la aplicación FastAPI.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .config import settings
from .database import engine
from .models import Base
from .routers import users_router, products_router, health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa la base de datos al arrancar la aplicación."""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    yield


def create_application() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configurar CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, especificar orígenes permitidos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar routers
    application.include_router(health_router)
    application.include_router(users_router)
    application.include_router(products_router)

    return application


app = create_application()


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "Bienvenido a la API de Demostración DevSecOps",
        "docs": "/docs",
        "health": "/health",
    }


def custom_openapi():
    """Personaliza el esquema OpenAPI."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        routes=app.routes,
    )

    # Agregar información de seguridad
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    openapi_schema["tags"] = [
        {"name": "Health", "description": "Endpoints de salud del sistema"},
        {"name": "Users", "description": "Gestión de usuarios"},
        {"name": "Products", "description": "Gestión de productos"},
        {"name": "Root", "description": "Información general de la API"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
