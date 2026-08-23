import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID

SECRET_KEY = "tu_clave_secreta_super_segura_y_larga"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # El token durará 2 horas

class Crypto:
    @staticmethod
    def hash_password(password: str) -> str:
        # Recibe una contraseña en texto plano, genera un salt aleatorio
        # y devuelve el hash en formato string listo para guardar en la base de datos.
        
        # Convertir la cadena de texto a bytes
        password_bytes = password.encode('utf-8')
        
        # Generar el salt y el hash
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        
        # Decodificar a string para guardarlo fácilmente (e.g., VARCHAR en BD)
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Compara una contraseña en texto plano con el hash guardado.
        # Devuelve True si coinciden, de lo contrario False.
        
        # Convertir ambos strings a bytes para la comparación
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # bcrypt extrae el salt automáticamente del hash guardado
        return bcrypt.checkpw(plain_bytes, hashed_bytes) 

    @staticmethod
    def create_access_token(user_id: UUID, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # El 'payload' es la información pública que viaja dentro del token
        payload = {
            "sub": str(user_id),       # ID del usuario como string
            "role": role,              # Rol del usuario (admin / usuario)
            "exp": expire              # Fecha de expiración
        }
        
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt