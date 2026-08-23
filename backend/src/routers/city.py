# src/routers/city.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.city import City
from src.schemas.city import CityCreate, CityResponse
from src.utils.dependencies import RoleChecker

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CREATE: Crear una nueva ciudad
@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city_data: CityCreate, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):
    db_city = City(name=city_data.name, province_id=city_data.province_id)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

# 2. READ ALL: Obtener todas las ciudades
@router.get("/", response_model=List[CityResponse])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    return db.query(City).offset(skip).limit(limit).all()

# 3. READ ONE: Obtener una ciudad por ID
@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: UUID, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return db_city

# 4. UPDATE: Actualizar una ciudad
@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: UUID, city_data: CityCreate, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db_city.name = city_data.name
    db_city.province_id = city_data.province_id
    
    db.commit()
    db.refresh(db_city)
    return db_city

# 5. DELETE: Eliminar una ciudad
@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: UUID, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db.delete(db_city)
    db.commit()
    return None
