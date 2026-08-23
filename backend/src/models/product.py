from sqlalchemy import Column, UUID, FLOAT, String
from sqlalchemy.orm import relationship
from src.database.database import Base

import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(60),nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(FLOAT(asdecimal=True), nullable=False)

    # Relación inversa: Un producto tiene muchas skus
    skus = relationship("Sku", back_populates="product", cascade="all, delete-orphan")

    # Relación inversa: Un producto tiene muchas skus
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")