from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    email = Column(String(150), nullable=False)
    password = Column(String(64), nullable=False)
    role = Column(String(25), nullable=False, default="user")
    name = Column(String(60), nullable=False)
    surname = Column(String(60), nullable=False)
    street = Column(String(100), nullable=False)
    number = Column(String(8), nullable=False)
    floor = Column(String(2), nullable=True)
    apart = Column(String(3), nullable=True)

    # Clave foránea que apunta a la TABLA 'neighborhoods' y su columna 'id'
    neighborhood_id = Column(UUID(as_uuid=True), ForeignKey("neighborhoods.id"), nullable=False)

    # Relación orientada a objetos que apunta a la CLASE 'Neighborhood'
    neighborhood = relationship("Neighborhood", back_populates="users")

    #Relación inversa: Un producto tiene muchas skus
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")