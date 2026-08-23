from pydantic import BaseModel, ConfigDict
from uuid import UUID

# Esquema base con los datos comunes
class NeighborhoodBase(BaseModel):
    name: str
    zip_code: str
    city_id: UUID

# Esquema para recibir datos al CREAR un barrio
class NeighborhoodCreate(NeighborhoodBase):
    pass  # Hereda name zip_code y city_id

# Esquema para responder al cliente (LECTURA)
class NeighborhoodResponse(NeighborhoodBase):
    id: UUID

    # Permite a Pydantic leer directamente los objetos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)