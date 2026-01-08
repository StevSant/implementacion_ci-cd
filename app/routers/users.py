"""
Endpoints de usuarios.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Obtiene la lista de todos los usuarios registrados.",
)
def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    db: Session = Depends(get_db),
):
    """Obtiene todos los usuarios con paginación."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario",
    description="Obtiene un usuario específico por su ID.",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema.",
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    db_user = User(
        email=user.email,
        name=user.name,
        password=user.password,  # En producción, hashear la contraseña
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return None


# ⚠️ VULNERABILIDAD INTENCIONAL: SQL Injection
@router.get(
    "/search/vulnerable",
    response_model=List[UserResponse],
    summary="Búsqueda vulnerable (DEMO)",
    description="⚠️ VULNERABLE: Este endpoint contiene SQL Injection intencional para demostración.",
)
def search_users_vulnerable(
    query: str = Query(..., description="Término de búsqueda"),
    db: Session = Depends(get_db),
):
    """
    ⚠️ ENDPOINT VULNERABLE - Solo para demostración.

    Este endpoint simula una vulnerabilidad de SQL Injection.
    En un sistema real, NUNCA concatenar input del usuario directamente en queries.
    """
    # VULNERABLE: Concatenación directa de input del usuario
    sql_query = f"SELECT * FROM users WHERE name LIKE '%{query}%'"  # noqa: S608

    # Forma segura (comentada para demostración):
    # users = db.query(User).filter(User.name.ilike(f"%{query}%")).all()

    # Usamos la forma segura para el resultado real
    users = db.query(User).filter(User.name.ilike(f"%{query}%")).all()
    return users
