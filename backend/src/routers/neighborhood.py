# src/routers/neighborhood.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.neighborhood import Neighborhood
from src.schemas.neighborhood import NeighborhoodCreate, NeighborhoodResponse
from src.utils.dependencies import RoleChecker

router = APIRouter(
    prefix="/neighborhoods",
    tags=["Neighborhoods"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. CREATE: Crear un nuevo barrio
@router.post("/", response_model=NeighborhoodResponse, status_code=status.HTTP_201_CREATED)
def create_neighborhood(neighborhood_data: NeighborhoodCreate, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):
    db_neighborhood = Neighborhood(name=neighborhood_data.name, zip_code=neighborhood_data.zip_code, city_id=neighborhood_data.city_id)
    db.add(db_neighborhood)
    db.commit()
    db.refresh(db_neighborhood)
    return db_neighborhood

# 2. READ ALL: Obtener todas los barrios
@router.get("/", response_model=List[NeighborhoodResponse])
def get_neighborhoods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    return db.query(Neighborhood).offset(skip).limit(limit).all()

# 3. READ ONE: Obtener un barrio por ID
@router.get("/{neighborhood_id}", response_model=NeighborhoodResponse)
def get_neighborhood(neighborhood_id: UUID, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["user", "admin"]))):
    db_neighborhood = db.query(Neighborhood).filter(Neighborhood.id == neighborhood_id).first()
    if not db_neighborhood:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return db_neighborhood

# 4. UPDATE: Actualizar un barrio
@router.put("/{neighborhood_id}", response_model=NeighborhoodResponse)
def update_neighborhood(neighborhood_id: UUID, neighborhood_data: NeighborhoodCreate, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_neighborhood = db.query(Neighborhood).filter(Neighborhood.id == neighborhood_id).first()
    if not db_neighborhood:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db_neighborhood.name = neighborhood_data.name
    db_neighborhood.city_id = neighborhood_data.city_id
    
    db.commit()
    db.refresh(db_neighborhood)
    return db_neighborhood

# 5. DELETE: Eliminar un barrio
@router.delete("/{neighborhood_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_neighborhood(neighborhood_id: UUID, db: Session = Depends(get_db),  current_user = Depends(RoleChecker(["admin"]))):
    db_neighborhood = db.query(Neighborhood).filter(Neighborhood.id == neighborhood_id).first()
    if not db_neighborhood:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db.delete(db_neighborhood)
    db.commit()
    return None
