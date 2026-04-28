from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


import models
import schemas
from database import engine, SessionLocal

# Crear la tabla automaticamente
models.Base.metadata.create_all(bind=engine)    

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
        
        
@app.get("/")
def root():
    return {"message": "API conectada a PostgreSQL"}

# -------------------------
# CLUBES
# -------------------------

# Endpoint para crear un club
@app.post("/clubes", response_model=schemas.ClubResponse)
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


# Endpoint para listar clubes
@app.get("/clubes", response_model=list[schemas.ClubResponse])
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


# Endpoint para listar jugadores por club
@app.get("/clubes/{club_id}/jugadores", response_model=list[schemas.JugadorResponse])
def listar_jugadores_por_club(club_id: int, db: Session = Depends(get_db)):
    return db.query(models.Jugador).filter(models.Jugador.club_id == club_id).all()

# -------------------------
# JUGADORES
# -------------------------


@app.post("/jugadores/", response_model=schemas.JugadorResponse)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    club = db.query(models.Club).filter(models.Club.id == jugador.club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    existe_matricula = db.query(models.Jugador).filter(models.Jugador.matricula == jugador.matricula).first()
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

@app.get("/jugadores/", response_model=List[schemas.JugadorResponse])
def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(models.Jugador).all()

# -------------------------
# TARJETAS COMPLETAS
# -------------------------

@app.post("/tarjetas/", response_model=schemas.TarjetaJugadorResponse)
def crear_tarjeta(tarjeta: schemas.TarjetaJugadorCreate, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == tarjeta.jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if jugador.club_id != tarjeta.club_id:
        raise HTTPException(status_code=400, detail="El jugador no pertenece al club especificado")

    if len(tarjeta.hoyos) != 18:
        raise HTTPException(status_code=400, detail="La tarjeta debe tener exactamente 18 hoyos")

    hoyo_numeros = [h.numero_hoyo for h in tarjeta.hoyos]
    if sorted(hoyo_numeros) != list(range(1, 19)):
        raise HTTPException(status_code=400, detail="Los hoyos deben ir del 1 al 18 sin repetir")

    hoyos_ordenados = sorted(tarjeta.hoyos, key=lambda h: h.numero_hoyo)

    total_ida = sum(h.golpes for h in hoyos_ordenados[:9])
    total_vuelta = sum(h.golpes for h in hoyos_ordenados[9:])
    total_gross = total_ida + total_vuelta
    total_neto = total_gross - tarjeta.handicap_juego

    nueva_tarjeta = models.TarjetaJugador(
        fecha=tarjeta.fecha,
        estado=tarjeta.estado,
        jugador_id=tarjeta.jugador_id,
        club_id=tarjeta.club_id,
        matricula_jugador=jugador.matricula,
        handicap_juego=tarjeta.handicap_juego,
        handicap_index_usado=jugador.handicap_index,
        tee_salida=tarjeta.tee_salida,
        total_ida=total_ida,
        total_vuelta=total_vuelta,
        total_gross=total_gross,
        total_neto=total_neto
    )

    db.add(nueva_tarjeta)
    db.commit()
    db.refresh(nueva_tarjeta)

    for hoyo in hoyos_ordenados:
        nuevo_hoyo = models.TarjetaJugadorHoyo(
            tarjeta_jugador_id=nueva_tarjeta.id,
            numero_hoyo=hoyo.numero_hoyo,
            golpes=hoyo.golpes
        )
        db.add(nuevo_hoyo)

    db.commit()
    db.refresh(nueva_tarjeta)

    return nueva_tarjeta

@app.get("/tarjetas/", response_model=List[schemas.TarjetaJugadorResponse])
def listar_tarjetas(db: Session = Depends(get_db)):
    return db.query(models.TarjetaJugador).all()
