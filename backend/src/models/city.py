from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
import uuid

class City(Base):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)

    # Clave foránea que apunta a la TABLA 'provinces' y su columna 'id'
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'Province'
    province = relationship("Province", back_populates="cities")

    # Relación inversa: Una ciudad tiene muchos barrios
    neighborhoods = relationship("Neighborhood", back_populates="city", cascade="all, delete-orphan")