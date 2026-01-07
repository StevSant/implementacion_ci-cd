"""
Routers de la aplicación.
"""

from .users import router as users_router
from .products import router as products_router
from .health import router as health_router

__all__ = ["users_router", "products_router", "health_router"]
