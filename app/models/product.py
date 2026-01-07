"""
Modelos de producto.
"""

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    """Modelo base de producto."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Modelo para crear producto."""

    pass


class Product(ProductBase):
    """Modelo de producto completo."""

    id: int

    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    """Respuesta de producto."""

    id: int
