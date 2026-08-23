from src.database.database import engine, Base
# Importar el paquete 'models' gatilla la lectura de todos tus archivos individuales
import src.models

def init_db():
    print("Detectando modelos y creando tablas en PostgreSQL...")
    # SQLalchemy creará las tablas respetando el orden de las Foreign Keys automáticamente
    Base.metadata.create_all(bind=engine)
    print("¡Estructura de base de datos creada con éxito!")

if __name__ == "__main__":
    init_db()
