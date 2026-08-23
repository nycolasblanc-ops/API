from pydantic import BaseModel, ConfigDict

# Esquema base con los datos comunes
class ProvinceBase(BaseModel):
    name: str

# Esquema para recibir datos al CREAR una provincia
class ProvinceCreate(ProvinceBase):
    pass  # Hereda name

# Esquema para responder al cliente (LECTURA)
class ProvinceResponse(ProvinceBase):
    id: int

    # Permite a Pydantic leer directamente los objetos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)