from sqlalchemy import Column, UUID, Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

import uuid

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rate = Column(Integer, nullable=False)
    description = Column(String(300),nullable=False)

     # Clave foránea que apunta a la TABLA 'users' y su columna 'id'
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'User'
    user = relationship("User", back_populates="reviews")

     # Clave foránea que apunta a la TABLA 'products' y su columna 'id'
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'Province'
    product = relationship("Product", back_populates="reviews")
    
