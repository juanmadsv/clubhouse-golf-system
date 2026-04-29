from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/clubes",
    tags=["Clubes"]
)


@router.post("/", response_model=schemas.ClubResponse)
def crear_club(club: schemas.ClubCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Club).filter(models.Club.nombre == club.nombre).first()

    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un club con ese nombre")

    nuevo = models.Club(
        nombre=club.nombre,
        ubicacion=club.ubicacion,
        federacion=club.federacion
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return schemas.ClubResponse(
        id=nuevo.id,
        nombre=nuevo.nombre,
        ubicacion=nuevo.ubicacion,
        federacion=nuevo.federacion if nuevo.federacion else "Federación no especificada"
    )


@router.get("/", response_model=list[schemas.ClubResponse])
def listar_clubes(db: Session = Depends(get_db)):
    clubes = db.query(models.Club).all()

    return [
        schemas.ClubResponse(
            id=c.id,
            nombre=c.nombre,
            ubicacion=c.ubicacion,
            federacion=c.federacion if c.federacion else "Federación no especificada"
        )
        for c in clubes
    ]