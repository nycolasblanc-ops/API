from sqlalchemy import Column, UUID, String, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base  # Importación absoluta de la Base común
import uuid
from ..enums.size import Size

class Sku(Base):
    __tablename__ = "skus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ean = Column(String(20), nullable=True)
    size = Column(Enum(Size),nullable=False)
    color = Column(String(50), nullable=False)
    imageUrl = Column(String(200), nullable=True)
    stock = Column(Integer, nullable= False)

    # Clave foránea que apunta a la TABLA 'products' y su columna 'id'
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'Province'
    product = relationship("Product", back_populates="skus")