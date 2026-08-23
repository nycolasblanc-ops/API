# src/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import SessionLocal
from src.models.user import User
from src.schemas.auth import LoginRequest, TokenResponse
from src.utils.crypto import Crypto

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # 1. Buscar al usuario por email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # 2. Validar usuario y verificar contraseña
    if not user or not Crypto.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Asignar rol (si tu modelo no tiene la columna aún, puedes usar user.role o harcodearlo para pruebas)
    # Por seguridad, asumimos que tu modelo User tiene un atributo: user.role (ej: "admin" o "usuario")
    user_role = getattr(user, "role", "usuario") 

    # 4. Crear el token JWT
    access_token = Crypto.create_access_token(user_id=user.id, role=user_role)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user_role
    }
