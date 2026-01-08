"""
Esquemas Pydantic de Usuario.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Esquema para crear un usuario."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6)
    is_active: bool = True


class UserResponse(BaseModel):
    """Esquema de respuesta de usuario (sin datos sensibles)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    is_active: bool
