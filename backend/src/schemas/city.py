from pydantic import BaseModel, ConfigDict
from uuid import UUID

# Esquema base con los datos comunes
class CityBase(BaseModel):
    name: str
    province_id: int

# Esquema para recibir datos al CREAR una ciudad
class CityCreate(CityBase):
    pass  # Hereda name y province_id

# Esquema para responder al cliente (LECTURA)
class CityResponse(CityBase):
    id: UUID

    # Permite a Pydantic leer directamente los objetos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)