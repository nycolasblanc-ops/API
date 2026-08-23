# src/routers/review.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.review import Review
from src.models.user import User
from src.models.product import Product
from src.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CREATE: Crear una reseña validando existencia de Usuario y Producto
@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    # Validar que el usuario exista
    user_exists = db.query(User).filter(User.id == review_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="El usuario especificado no existe")

    # Validar que el producto exista
    product_exists = db.query(Product).filter(Product.id == review_data.product_id).first()
    if not product_exists:
        raise HTTPException(status_code=404, detail="El producto especificado no existe")

    db_review = Review(
        rate=review_data.rate,
        description=review_data.description,
        user_id=review_data.user_id,
        product_id=review_data.product_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 2. READ ALL: Obtener reseñas generales
@router.get("/", response_model=List[ReviewResponse])
def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Review).offset(skip).limit(limit).all()

# 3. READ BY PRODUCT: Endpoint muy útil para traer las reseñas de un producto específico
@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_reviews_by_product(product_id: UUID, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()

# 4. UPDATE: Modificar puntaje o comentario
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: UUID, review_data: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    db_review.rate = review_data.rate
    db_review.description = review_data.description
    
    db.commit()
    db.refresh(db_review)
    return db_review

# 5. DELETE: Eliminar reseña
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: UUID, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    db.delete(db_review)
    db.commit()
    return None
