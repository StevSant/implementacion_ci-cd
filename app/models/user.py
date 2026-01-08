"""
Modelo SQLAlchemy de Usuario.
"""

from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class User(Base):
    """Modelo de usuario en la base de datos."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
