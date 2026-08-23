# src/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from typing import Optional

# Base común para los datos del usuario
class UserBase(BaseModel):
    email: EmailStr
    role: str
    name: str
    surname: str
    street: str
    number: str
    floor: Optional[str] = None
    apart: Optional[str] = None
    neighborhood_id: UUID

# Esquema para el REGISTRO (Aquí sí viaja la contraseña en texto plano)
class UserCreate(UserBase):
    password: str

# Esquema para la RESPUESTA (Ocultamos la contraseña por seguridad)
class UserResponse(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
