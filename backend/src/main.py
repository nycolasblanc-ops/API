# main.py o src/main.py
from fastapi import FastAPI
from src.routers.province import router as province_router
from src.routers.city import router as city_router
from src.routers.neighborhood import router as neighborhood_router
from src.routers.review import router as review_router
from src.routers.user import router as user_router
from src.routers.auth import router as auth_router
from src.routers.product import router as inventory_router



app = FastAPI(title="Nico API Backend")

# Registrar las rutas de los CRUD
app.include_router(province_router)
app.include_router(city_router)
app.include_router(neighborhood_router)
app.include_router(review_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(inventory_router)

@app.get("/")
def read_root():
    return {"message": "¡API corriendo exitosamente!"}
