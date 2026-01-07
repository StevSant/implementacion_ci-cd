"""
Modelos de usuario.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Modelo base de usuario."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """Modelo para crear usuario."""

    password: str = Field(..., min_length=6)


class User(UserBase):
    """Modelo de usuario completo."""

    id: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Respuesta de usuario (sin datos sensibles)."""

    id: int
    email: EmailStr
    name: str
    is_active: bool
