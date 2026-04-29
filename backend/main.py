from fastapi import FastAPI

import models
from database import engine
from routers import clubes, jugadores, tarjetas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clubhouse System API",
    description="API para gestión de clubes, jugadores y tarjetas de golf",
    version="0.1.0"
)

app.include_router(clubes.router)
app.include_router(jugadores.router)
app.include_router(tarjetas.router)


@app.get("/")
def root():
    return {"message": "Clubhouse System API funcionando"}