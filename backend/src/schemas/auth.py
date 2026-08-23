# src/schemas/auth.py
from pydantic import BaseModel, EmailStr

# Datos que envía el usuario para loguearse
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Respuesta con el token generado
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
