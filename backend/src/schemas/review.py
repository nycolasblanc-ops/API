# src/schemas/review.py
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class ReviewBase(BaseModel):
    rate: int = Field(..., ge=1, le=5, description="La calificación debe ser entre 1 y 5")
    description: str = Field(..., max_length=300)
    user_id: UUID
    product_id: UUID

class ReviewCreate(ReviewBase):
    pass  # Se usa para recibir los datos al crear

class ReviewUpdate(BaseModel):
    rate: int = Field(..., ge=1, le=5)
    description: str = Field(..., max_length=300)

class ReviewResponse(ReviewBase):
    id: UUID

    # Habilita la lectura compatible con los modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
