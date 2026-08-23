# src/routers/province.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.province import Province
from src.schemas.province import ProvinceCreate, ProvinceResponse
from src.utils.dependencies import RoleChecker

router = APIRouter(
    prefix="/provinces",
    tags=["Provinces"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CREATE: Crear una nueva provincia
@router.post("/", response_model=ProvinceResponse, status_code=status.HTTP_201_CREATED)
def create_province(province_data: ProvinceCreate, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):
    db_province = Province(name=province_data.name)
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province

# 2. READ ALL: Obtener todas las provincias
@router.get("/", response_model=List[ProvinceResponse])
def get_provinces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    return db.query(Province).offset(skip).limit(limit).all()

# 3. READ ONE: Obtener una provincia por ID
@router.get("/{province_id}", response_model=ProvinceResponse)
def get_province(province_id: int, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if not db_province:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return db_province

# 4. UPDATE: Actualizar una provincia
@router.put("/{province_id}", response_model=ProvinceResponse)
def update_province(province_id: int, province_data: ProvinceCreate, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if not db_province:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db_province.name = province_data.name
        
    db.commit()
    db.refresh(db_province)
    return db_province

# 5. DELETE: Eliminar una provincia
@router.delete("/{province_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_province(province_id: int, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if not db_province:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db.delete(db_province)
    db.commit()
    return None
