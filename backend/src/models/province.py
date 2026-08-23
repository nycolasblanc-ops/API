from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base  # Importación absoluta de la Base común

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, autoincrement= True)
    name = Column(String(100), nullable=False, unique=True)

    # Relación inversa: Una provincia tiene muchas ciudades
    cities = relationship("City", back_populates="province", cascade="all, delete-orphan")