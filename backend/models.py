from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from database import Base


class Club(Base):
    __tablename__ = "clubes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    ubicacion = Column(String, nullable=True)
    federacion = Column(String, nullable=False)

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    apellido = Column(String, index=True, nullable=False)
    matricula = Column(String, unique=True, index=True, nullable=False)

    # Handicap Index del jugador (AAG o carga manual)
    handicap_index = Column(Float, nullable=True)

    club_id = Column(Integer, ForeignKey("clubes.id"), nullable=False)


class TarjetaJugador(Base):
    __tablename__ = "tarjetas_jugador"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    estado = Column(String, default="manual", nullable=False)

    jugador_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubes.id"), nullable=False)

    # Datos históricos guardados en la tarjeta
    matricula_jugador = Column(String, nullable=False)
    handicap_juego = Column(Integer, nullable=False)
    handicap_index_usado = Column(Float, nullable=True)
    tee_salida = Column(String, nullable=False)

    total_ida = Column(Integer, nullable=False)
    total_vuelta = Column(Integer, nullable=False)
    total_gross = Column(Integer, nullable=False)
    total_neto = Column(Integer, nullable=False)


class TarjetaJugadorHoyo(Base):
    __tablename__ = "tarjeta_jugador_hoyos"

    id = Column(Integer, primary_key=True, index=True)
    tarjeta_jugador_id = Column(Integer, ForeignKey("tarjetas_jugador.id"), nullable=False)
    numero_hoyo = Column(Integer, nullable=False)
    golpes = Column(Integer, nullable=False)