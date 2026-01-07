"""
Configuración de la aplicación.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    APP_NAME: str = "Vulnerability Management Demo API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = """
    API de demostración para integración de gestión de vulnerabilidades en CI/CD.

    ## Funcionalidades

    * **Users**: Gestión básica de usuarios
    * **Products**: Gestión de productos
    * **Health**: Endpoints de salud del sistema

    ## Seguridad

    Esta aplicación contiene vulnerabilidades intencionales para demostración:
    - SQL Injection en endpoint de búsqueda
    - Dependencias vulnerables
    """
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./demo.db"

    class Config:
        env_file = ".env"


settings = Settings()
