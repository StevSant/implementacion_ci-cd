"""
Esquemas Pydantic de Producto.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductCreate(BaseModel):
    """Esquema para crear un producto."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    stock: int = Field(default=0, ge=0)


class ProductResponse(BaseModel):
    """Esquema de respuesta de producto."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
