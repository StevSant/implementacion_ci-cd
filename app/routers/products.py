"""
Endpoints de productos.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Listar productos",
    description="Obtiene la lista de todos los productos disponibles.",
)
def get_products(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    db: Session = Depends(get_db),
):
    """Obtiene todos los productos con filtros opcionales."""
    query = db.query(Product)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto",
    description="Obtiene un producto específico por su ID.",
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtiene un producto por ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
    summary="Crear producto",
    description="Crea un nuevo producto en el inventario.",
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Crea un nuevo producto."""
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto",
    description="Actualiza un producto existente.",
)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    """Actualiza un producto existente."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete(
    "/{product_id}",
    status_code=204,
    summary="Eliminar producto",
    description="Elimina un producto del inventario.",
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Elimina un producto por ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(product)
    db.commit()
    return None


# ⚠️ VULNERABILIDAD INTENCIONAL: Deserialización insegura
@router.post(
    "/import/vulnerable",
    summary="Importar datos (DEMO VULNERABLE)",
    description="⚠️ VULNERABLE: Este endpoint usa pickle para demostración de vulnerabilidades.",
)
def import_products_vulnerable(data: str):
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
