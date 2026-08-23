# src/utils/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from src.utils.crypto import SECRET_KEY, ALGORITHM

security = HTTPBearer()

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            # Decodificar y verificar la firma del token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_role: str = payload.get("role")
            
            if user_role not in self.allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos suficientes para realizar esta acción"
                )
                
            return payload # Retorna los datos del token (contiene el id en 'sub')
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="El token ha expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
