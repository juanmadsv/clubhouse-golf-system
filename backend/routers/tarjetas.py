from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from services.tarjeta_service import crear_tarjeta_completa, obtener_detalle_tarjeta

router = APIRouter(
    prefix="/tarjetas",
    tags=["Tarjetas"]
)


@router.post("/", response_model=schemas.TarjetaJugadorResponse)
def crear_tarjeta(tarjeta: schemas.TarjetaJugadorCreate, db: Session = Depends(get_db)):
    return crear_tarjeta_completa(tarjeta, db)


@router.get("/", response_model=list[schemas.TarjetaJugadorResponse])
def listar_tarjetas(db: Session = Depends(get_db)):
    return db.query(models.TarjetaJugador).all()


@router.get("/{tarjeta_id}", response_model=schemas.TarjetaDetalleResponse)
def obtener_tarjeta(tarjeta_id: int, db: Session = Depends(get_db)):
    return obtener_detalle_tarjeta(tarjeta_id, db)


@router.get("/jugador/{jugador_id}", response_model=list[schemas.TarjetaJugadorResponse])
def listar_tarjetas_por_jugador(jugador_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.TarjetaJugador)
        .filter(models.TarjetaJugador.jugador_id == jugador_id)
        .all()
    )


@router.get("/club/{club_id}", response_model=list[schemas.TarjetaJugadorResponse])
def listar_tarjetas_por_club(club_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.TarjetaJugador)
        .filter(models.TarjetaJugador.club_id == club_id)
        .all()
    )