"""
Endpoints de usuarios.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Simulación de base de datos en memoria
fake_users_db: List[dict] = [
    {"id": 1, "email": "admin@example.com", "name": "Admin User", "is_active": True},
    {"id": 2, "email": "user@example.com", "name": "Normal User", "is_active": True},
]


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Obtiene la lista de todos los usuarios registrados.",
)
async def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
):
    """Obtiene todos los usuarios con paginación."""
    return fake_users_db[skip : skip + limit]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario",
    description="Obtiene un usuario específico por su ID.",
)
async def get_user(user_id: int):
    """Obtiene un usuario por ID."""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema.",
)
async def create_user(user: UserCreate):
    """Crea un nuevo usuario."""
    new_id = max([u["id"] for u in fake_users_db], default=0) + 1
    new_user = {"id": new_id, "email": user.email, "name": user.name, "is_active": user.is_active}
    fake_users_db.append(new_user)
    return new_user


# ⚠️ VULNERABILIDAD INTENCIONAL: SQL Injection
# Este endpoint simula una vulnerabilidad de SQL Injection para demostración
@router.get(
    "/search/vulnerable",
    response_model=List[UserResponse],
    summary="Búsqueda vulnerable (DEMO)",
    description="⚠️ VULNERABLE: Este endpoint contiene SQL Injection intencional para demostración.",
)
async def search_users_vulnerable(query: str = Query(..., description="Término de búsqueda")):
    """
    ⚠️ ENDPOINT VULNERABLE - Solo para demostración.

    Este endpoint simula una vulnerabilidad de SQL Injection.
    En un sistema real, NUNCA concatenar input del usuario directamente en queries.
    """
    # VULNERABLE: Concatenación directa de input del usuario
    # Esto sería detectado por herramientas SAST como CodeQL o Bandit
    sql_query = f"SELECT * FROM users WHERE name LIKE '%{query}%'"  # noqa: S608

    # Simulación de ejecución (no real, solo para demo)
    import sqlite3

    # VULNERABLE: Ejecución de query sin sanitización
    # conn = sqlite3.connect(":memory:")
    # cursor = conn.execute(sql_query)  # Esto sería muy peligroso

    # Retornamos datos simulados
    return [u for u in fake_users_db if query.lower() in u["name"].lower()]


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema.",
)
async def delete_user(user_id: int):
    """Elimina un usuario por ID."""
    global fake_users_db
    for i, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            fake_users_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
