"""
Endpoints de productos.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from decimal import Decimal
from ..models.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

# Simulación de base de datos en memoria
fake_products_db: List[dict] = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "Laptop gaming",
        "price": Decimal("999.99"),
        "stock": 10,
    },
    {
        "id": 2,
        "name": "Mouse",
        "description": "Mouse ergonómico",
        "price": Decimal("29.99"),
        "stock": 50,
    },
    {
        "id": 3,
        "name": "Teclado",
        "description": "Teclado mecánico",
        "price": Decimal("79.99"),
        "stock": 30,
    },
]


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Listar productos",
    description="Obtiene la lista de todos los productos disponibles.",
)
async def get_products(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    min_price: Optional[Decimal] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[Decimal] = Query(None, ge=0, description="Precio máximo"),
):
    """Obtiene todos los productos con filtros opcionales."""
    products = fake_products_db[skip : skip + limit]

    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    return products


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto",
    description="Obtiene un producto específico por su ID.",
)
async def get_product(product_id: int):
    """Obtiene un producto por ID."""
    for product in fake_products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
    summary="Crear producto",
    description="Crea un nuevo producto en el inventario.",
)
async def create_product(product: ProductCreate):
    """Crea un nuevo producto."""
    new_id = max([p["id"] for p in fake_products_db], default=0) + 1
    new_product = {
        "id": new_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
    }
    fake_products_db.append(new_product)
    return new_product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto",
    description="Actualiza un producto existente.",
)
async def update_product(product_id: int, product: ProductCreate):
    """Actualiza un producto existente."""
    for i, p in enumerate(fake_products_db):
        if p["id"] == product_id:
            updated = {
                "id": product_id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
            }
            fake_products_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.delete(
    "/{product_id}",
    status_code=204,
    summary="Eliminar producto",
    description="Elimina un producto del inventario.",
)
async def delete_product(product_id: int):
    """Elimina un producto por ID."""
    global fake_products_db
    for i, product in enumerate(fake_products_db):
        if product["id"] == product_id:
            fake_products_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# ⚠️ VULNERABILIDAD INTENCIONAL: Deserialización insegura
@router.post(
    "/import/vulnerable",
    summary="Importar datos (DEMO VULNERABLE)",
    description="⚠️ VULNERABLE: Este endpoint usa pickle para demostración de vulnerabilidades.",
)
async def import_products_vulnerable(data: str):
    """
    ⚠️ ENDPOINT VULNERABLE - Solo para demostración.

    Este endpoint simula una vulnerabilidad de deserialización insegura.
    NUNCA usar pickle con datos no confiables en producción.
    """
    import pickle
    import base64

    try:
        # VULNERABLE: Deserialización de datos no confiables
        # Esto sería detectado por Bandit (B301)
        decoded = base64.b64decode(data)
        # products = pickle.loads(decoded)  # Comentado pero detectado por SAST
        return {"message": "Importación simulada (no ejecutada por seguridad)"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en importación: {str(e)}")
