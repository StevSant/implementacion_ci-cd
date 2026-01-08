"""
Esquemas Pydantic de la aplicación.
"""

from .user import UserCreate, UserResponse
from .product import ProductCreate, ProductResponse

__all__ = ["UserCreate", "UserResponse", "ProductCreate", "ProductResponse"]
