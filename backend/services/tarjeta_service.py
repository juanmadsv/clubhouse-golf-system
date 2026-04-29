from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def crear_tarjeta_completa(tarjeta: schemas.TarjetaJugadorCreate, db: Session):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == tarjeta.jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if jugador.club_id != tarjeta.club_id:
        raise HTTPException(
            status_code=400,
            detail="El jugador no pertenece al club especificado"
        )

    if len(tarjeta.hoyos) != 18:
        raise HTTPException(
            status_code=400,
            detail="La tarjeta debe tener exactamente 18 hoyos"
        )

    numeros_hoyo = [h.numero_hoyo for h in tarjeta.hoyos]

    if sorted(numeros_hoyo) != list(range(1, 19)):
        raise HTTPException(
            status_code=400,
            detail="Los hoyos deben ir del 1 al 18 sin repetir"
        )

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
        handicap_index_usado=jugador.handicap_index,
        handicap_juego=tarjeta.handicap_juego,
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


def obtener_detalle_tarjeta(tarjeta_id: int, db: Session):
    tarjeta = (
        db.query(models.TarjetaJugador)
        .filter(models.TarjetaJugador.id == tarjeta_id)
        .first()
    )

    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    hoyos = (
        db.query(models.TarjetaJugadorHoyo)
        .filter(models.TarjetaJugadorHoyo.tarjeta_jugador_id == tarjeta_id)
        .order_by(models.TarjetaJugadorHoyo.numero_hoyo)
        .all()
    )

    return {
        "id": tarjeta.id,
        "fecha": tarjeta.fecha,
        "estado": tarjeta.estado,
        "jugador_id": tarjeta.jugador_id,
        "club_id": tarjeta.club_id,
        "matricula_jugador": tarjeta.matricula_jugador,
        "handicap_index_usado": tarjeta.handicap_index_usado,
        "handicap_juego": tarjeta.handicap_juego,
        "tee_salida": tarjeta.tee_salida,
        "total_ida": tarjeta.total_ida,
        "total_vuelta": tarjeta.total_vuelta,
        "total_gross": tarjeta.total_gross,
        "total_neto": tarjeta.total_neto,
        "hoyos": [
            {
                "numero_hoyo": h.numero_hoyo,
                "golpes": h.golpes
            }
            for h in hoyos
        ]
    }