# src/schemas/product.py
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import List, Optional
from src.enums.size import Size
from enum import Enum

# --- SCHEMAS PARA SKU ---
class SkuBase(BaseModel):
    ean: Optional[str] = Field(None, max_length=20)
    size: str
    color: str
    stock: int
    imageUrl: Optional[str] = Field(None, max_length=200)
    product_id: UUID

class SkuCreate(SkuBase):
    pass

class SkuResponse(SkuBase):
    id: UUID
    product_id: UUID
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS PARA PRODUCTO ---
class ProductBase(BaseModel):
    name: str = Field(..., max_length=60)
    description: Optional[str] = Field(None, max_length=200)
    price: float = Field(..., ge=0.0)

class ProductCreate(ProductBase):
    pass  # Datos básicos para registrar el producto base

class ProductResponse(ProductBase):
    id: UUID
    skus: List[SkuResponse] = []  # 💡 Incluye sus variantes automáticamente en las consultas

    model_config = ConfigDict(from_attributes=True)
