"""
Modelo SQLAlchemy de Producto.
"""

from sqlalchemy import Column, Integer, String, Float, Text

from .base import Base


class Product(Base):
    """Modelo de producto en la base de datos."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
