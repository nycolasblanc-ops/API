import bcrypt
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Configuración de la cadena de conexión a PostgreSQL
# Formato: postgresql://usuario:contraseña@servidor:puerto/nombre_base_datos
DB_USER = "postgres"
DB_PASS = "Billyq@69"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nicoApiDb"

# 💡 ESCAPA LA CONTRASEÑA AQUÍ (Esto convertirá el '@' en '%40')
DB_PASS_ESCAPED = urllib.parse.quote_plus(DB_PASS)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS_ESCAPED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# 2. Crear el motor de conexión y la sesión
engine = create_engine(DATABASE_URL, echo=True) # echo=True te mostrará los CREATE TABLE en consola
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. La Base que ya deben estar heredando tus modelos
Base = declarative_base()


# =====================================================================
# REQUISITO IMPORTANTE:
# Para que SQLAlchemy cree tus tablas, debe "conocer" tus modelos antes.
# Asegúrate de importarlos aquí si están en otros archivos, por ejemplo:
# from models import User, Neighborhood, City, Province, Product, Sku, Reviews
# =====================================================================
#from src.models import User, Neighborhood, City, Province, Product, Sku, Reviews

def init_db():
    """
    Función para crear todas las tablas en PostgreSQL. 
    Se ejecuta una sola vez al inicio del proyecto.
    """
    print("Creando tablas en PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")


# =====================================================================
# LOGICA DE USUARIOS CON BCRYPT Y SQLALCHEMY
# =====================================================================

# Asumiendo que tu modelo 'User' importado tiene estos campos:
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True)
#     password_hash = Column(String)

def register_user(email: str, plain_password: str, **extra_fields):
    """Cifra la contraseña e inserta el nuevo usuario en PostgreSQL"""
    db = SessionLocal()
    try:
        # Cifrar password con bcrypt
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        password_str = hashed_bytes.decode('utf-8')
        
        # Crear instancia del modelo User (asumiendo que está importado)
        new_user = User(email=email, password_hash=password_str, **extra_fields)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def authenticate_user(email: str, plain_password: str) -> bool:
    """Busca al usuario y verifica si su contraseña coincide"""
    db = SessionLocal()
    try:
        # Buscar usuario por email (asumiendo que está importado)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False # El usuario no existe
            
        # Verificar la contraseña usando los strings guardados
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            user.password_hash.encode('utf-8')
        )
    finally:
        db.close()

# Ejecución de prueba/inicialización
if __name__ == "__main__":
    # 1. Crea las tablas físicamente en tu base de datos PostgreSQL vacía
    init_db()
