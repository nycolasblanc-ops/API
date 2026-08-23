# src/routers/product.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.product import Product
from src.models.sku import Sku
from src.schemas.product import ProductCreate, ProductResponse, SkuCreate, SkuResponse
from src.utils.dependencies import RoleChecker

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory (Products & Skus)"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🛡️ Permisos preconfigurados
admin_only = RoleChecker(["admin"])
any_user = RoleChecker(["usuario", "admin"])


# =============================================================================
# ENDPOINTS DE PRODUCTOS
# =============================================================================

# 1. CREAR PRODUCTO (Solo Admin)
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    db_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 2. OBTENER TODOS LOS PRODUCTOS (Cualquier usuario autenticado)
@router.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(any_user)):
    # SQLAlchemy traerá automáticamente las SKUs asociadas gracias al response_model
    return db.query(Product).offset(skip).limit(limit).all()

# 3. ELIMINAR PRODUCTO (Solo Admin - Borra SKUs en cascada por tu configuración del modelo)
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_product)
    db.commit()
    return None


# =============================================================================
# ENDPOINTS DE SKUS (VARIANTES)
# =============================================================================

# 4. CREAR SKU / VARIANTE (Solo Admin)
@router.post("/skus", response_model=SkuResponse, status_code=status.HTTP_201_CREATED)
def create_sku(sku_data: SkuCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    # Verificar si el producto padre realmente existe
    product_exists = db.query(Product).filter(Product.id == sku_data.product_id).first()
    if not product_exists:
        raise HTTPException(status_code=404, detail="El producto padre especificado no existe")
    
    # Verificar que el código SKU no esté duplicado en el sistema
    sku_ean_exists = db.query(Sku).filter(Sku.ean == sku_data.ean).first()
    if sku_ean_exists:
        raise HTTPException(status_code=400, detail="El código SKU ya está registrado en el sistema")

    db_sku = Sku(
        ean=sku_data.ean,
        stock=sku_data.stock,
        size=sku_data.size,
        color=sku_data.color,
        product_id=sku_data.product_id
    )
    db.add(db_sku)
    db.commit()
    db.refresh(db_sku)
    return db_sku

# 5. ACTUALIZAR STOCK DE UN SKU (Solo Admin)
@router.patch("/skus/{sku_id}/stock", response_model=SkuResponse)
def update_sku_stock(sku_id: UUID, new_stock: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
        
    db_sku = db.query(Sku).filter(Sku.id == sku_id).first()
    if not db_sku:
        raise HTTPException(status_code=404, detail="Variante SKU no encontrada")
    
    db_sku.stock = new_stock
    db.commit()
    db.refresh(db_sku)
    return db_sku
