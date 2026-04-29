from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/jugadores",
    tags=["Jugadores"]
)


@router.post("/", response_model=schemas.JugadorResponse)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    club = db.query(models.Club).filter(models.Club.id == jugador.club_id).first()

    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    existe_matricula = (
        db.query(models.Jugador)
        .filter(models.Jugador.matricula == jugador.matricula)
        .first()
    )

    if existe_matricula:
        raise HTTPException(status_code=400, detail="Ya existe un jugador con esa matrícula")

    nuevo = models.Jugador(
        nombre=jugador.nombre,
        apellido=jugador.apellido,
        matricula=jugador.matricula,
        handicap_index=jugador.handicap_index,
        club_id=jugador.club_id
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=list[schemas.JugadorResponse])
def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(models.Jugador).all()


@router.get("/club/{club_id}", response_model=list[schemas.JugadorResponse])
def listar_jugadores_por_club(club_id: int, db: Session = Depends(get_db)):
    return db.query(models.Jugador).filter(models.Jugador.club_id == club_id).all()