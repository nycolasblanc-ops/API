# src/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.database.database import SessionLocal
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.utils.crypto import Crypto  # 💡 Importamos tu helper

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. REGISTER / CREATE: Crear usuario cifrando la contraseña
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Validar si el email ya está registrado
    email_exists = db.query(User).filter(User.email == user_data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya se encuentra registrado"
        )

    # 💡 CIFRAMOS LA CONTRASEÑA USANDO TU HELPER
    hashed_password = Crypto.hash_password(user_data.password)

    # Creamos la instancia del modelo mapeando los campos
    db_user = User(
        email=user_data.email,
        password=hashed_password,  # 💡 Guardamos el hash seguro en la BD
        role=user_data.role,
        name=user_data.name,
        surname=user_data.surname,
        street=user_data.street,
        number=user_data.number,
        floor=user_data.floor,
        apart=user_data.apart,
        neighborhood_id=user_data.neighborhood_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 2. READ ALL: Obtener todos los usuarios (retorna la lista sin contraseñas)
@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

# 3. READ ONE: Obtener un único usuario por su ID UUID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user
