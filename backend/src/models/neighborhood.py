from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

import uuid

class Neighborhood(Base):
    __tablename__ = "neighborhoods"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False,unique=True)
    zip_code = Column(String(8), nullable=False,unique=True)

    # Clave foránea que apunta a la TABLA 'cities' y su columna 'id'
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'cities'
    city = relationship("City", back_populates="neighborhoods")

    # Relación inversa: Un barrio tiene muchos usuarios
    users = relationship("User", back_populates="neighborhood", cascade="all, delete-orphan")