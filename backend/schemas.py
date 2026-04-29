from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class ClubCreate(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    federacion: Optional[str] = None


class ClubResponse(BaseModel):
    id: int
    nombre: str
    ubicacion: Optional[str] = None
    federacion: Optional[str] = None

    class Config:
        from_attributes = True


class JugadorCreate(BaseModel):
    nombre: str
    apellido: str
    matricula: str
    handicap_index: Optional[float] = Field(None, ge=-10, le=54)
    club_id: int


class JugadorResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    matricula: str
    handicap_index: Optional[float] = Field(None, ge=-10, le=54)
    club_id: int

    class Config:
        from_attributes = True


class HoyoCreate(BaseModel):
    numero_hoyo: int = Field(..., ge=1, le=18)
    golpes: int = Field(..., ge=1)


class HoyoResponse(BaseModel):
    id: int
    tarjeta_jugador_id: int
    numero_hoyo: int
    golpes: int

    class Config:
        from_attributes = True


class TarjetaJugadorCreate(BaseModel):
    fecha: date
    estado: str = "manual"
    jugador_id: int
    club_id: int
    handicap_juego: int
    tee_salida: str
    hoyos: List[HoyoCreate]


class TarjetaJugadorResponse(BaseModel):
    id: int
    fecha: date
    estado: str
    jugador_id: int
    club_id: int
    matricula_jugador: str
    handicap_index_usado: Optional[float] = None
    handicap_juego: int
    tee_salida: str
    total_ida: int
    total_vuelta: int
    total_gross: int
    total_neto: int

    class Config:
        from_attributes = True


class TarjetaDetalleResponse(BaseModel):
    id: int
    fecha: date
    estado: str
    jugador_id: int
    club_id: int
    matricula_jugador: str
    handicap_index_usado: Optional[float] = None
    handicap_juego: int
    tee_salida: str
    total_ida: int
    total_vuelta: int
    total_gross: int
    total_neto: int
    hoyos: List[HoyoCreate]