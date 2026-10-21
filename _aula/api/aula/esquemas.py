"""api/aula/esquemas.py — lo que entra y sale de la API (Pydantic 2); las claves de examen no tienen esquema de salida
para estudiantes: no hay forma de serializarlas por descuido.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_CORREO = re.compile(r"^[^@\s]{1,64}@[^@\s]+\.[^@\s]{2,}$")
_IDENT = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")
_LECCION = re.compile(r"^[a-z0-9][a-z0-9_-]*/[a-z0-9][a-z0-9_-]*$")
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Modelo(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


# --- cuentas ----------------------------------------------------------------------------------------------------

class Registro(Modelo):
    correo: str = Field(max_length=254)
    nombre_visible: str = Field(min_length=2, max_length=120)
    clave: str = Field(max_length=256)
    consentimiento: bool
    politica_version: str

    @field_validator("correo")
    @classmethod
    def _correo(cls, v: str) -> str:
        v = v.strip().lower()
        if not _CORREO.match(v):
            raise ValueError("correo no válido")
        return v

    @field_validator("nombre_visible")
    @classmethod
    def _nombre(cls, v: str) -> str:
        return " ".join(v.split())


class InicioSesion(Modelo):
    correo: str = Field(max_length=254)
    clave: str = Field(max_length=256)

    @field_validator("correo")
    @classmethod
    def _correo(cls, v: str) -> str:
        return v.strip().lower()


class Renovar(Modelo):
    renovacion: str = Field(max_length=200)


class CambioCuenta(Modelo):
    nombre_visible: str | None = Field(default=None, min_length=2, max_length=120)
    clave_actual: str | None = Field(default=None, max_length=256)
    clave_nueva: str | None = Field(default=None, max_length=256)


class Baja(Modelo):
    clave: str = Field(max_length=256)


class UsuarioSalida(Modelo):
    id: int
    correo: str
    nombre_visible: str
    rol_global: str
    creado_en: datetime


class Tokens(Modelo):
    acceso: str
    renovacion: str
    tipo: str = "bearer"
    expira_en_s: int


class SesionSalida(Tokens):
    usuario: UsuarioSalida


# --- clases -----------------------------------------------------------------------------------------------------

class ClaseNueva(Modelo):
    nombre: str = Field(min_length=2, max_length=160)
    curso_id: str
    pub: str
    periodo: str = Field(default="", max_length=40)

    @field_validator("curso_id", "pub")
    @classmethod
    def _ident(cls, v: str) -> str:
        if not _IDENT.match(v):
            raise ValueError("identificador en minúsculas, con guion o guion bajo")
        return v


class ClaseCambio(Modelo):
    nombre: str | None = Field(default=None, min_length=2, max_length=160)
    periodo: str | None = Field(default=None, max_length=40)
    archivada: bool | None = None


class ClaseSalida(Modelo):
    id: int
    nombre: str
    curso_id: str
    pub: str
    periodo: str
    archivada: bool
    mi_rol: str
    codigo: str | None = None  # solo para docentes


class Inscribirse(Modelo):
    codigo: str = Field(min_length=4, max_length=12)


class NuevoDocente(Modelo):
    correo: str


class Miembro(Modelo):
    usuario_id: int
    nombre_visible: str
    rol: str
    correo: str | None = None  # solo lo ve el docente


# --- anuncios ---------------------------------------------------------------------------------------------------

class AnuncioNuevo(Modelo):
    texto: str = Field(min_length=1, max_length=10_000)


class AnuncioSalida(Modelo):
    id: int
    clase_id: int
    autor: str | None
    texto: str
    creado_en: datetime


# --- tareas -----------------------------------------------------------------------------------------------------

class Criterio(Modelo):
    criterio: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(default="", max_length=2000)
    puntos: float = Field(gt=0)


class TareaNueva(Modelo):
    titulo: str = Field(min_length=2, max_length=200)
    consigna: str = Field(default="", max_length=20_000)
    fecha_limite: datetime | None = None
    puntaje_max: float = Field(default=20.0, gt=0, le=1000)
    rubrica: list[Criterio] | None = None
    acepta_archivo: bool = True
    publicada: bool = True

    @model_validator(mode="after")
    def _rubrica(self):
        if self.rubrica:
            nombres = [c.criterio for c in self.rubrica]
            if len(set(nombres)) != len(nombres):
                raise ValueError("los criterios de la rúbrica deben tener nombres distintos")
            if sum(c.puntos for c in self.rubrica) > self.puntaje_max + 1e-9:
                raise ValueError("la rúbrica suma más que el puntaje máximo")
        return self


class TareaCambio(Modelo):
    titulo: str | None = Field(default=None, min_length=2, max_length=200)
    consigna: str | None = Field(default=None, max_length=20_000)
    fecha_limite: datetime | None = None
    puntaje_max: float | None = Field(default=None, gt=0, le=1000)
    publicada: bool | None = None


class TareaSalida(Modelo):
    id: int
    clase_id: int
    titulo: str
    consigna: str
    fecha_limite: datetime | None
    puntaje_max: float
    rubrica: list | None
    acepta_archivo: bool
    publicada: bool
    creado_en: datetime


class CalificacionNueva(Modelo):
    puntaje: float | None = Field(default=None, ge=0)
    comentario: str = Field(default="", max_length=10_000)
    por_criterio: dict[str, float] | None = None


class CalificacionSalida(Modelo):
    puntaje: float
    comentario: str
    por_criterio: dict | None
    calificado_en: datetime


class EntregaSalida(Modelo):
    id: int
    tarea_id: int
    estudiante_id: int
    estudiante: str | None = None
    texto: str
    archivo_nombre: str | None
    archivo_bytes: int | None
    entregado_en: datetime
    tardia: bool
    calificacion: CalificacionSalida | None = None


# --- exámenes ---------------------------------------------------------------------------------------------------

class PreguntaNueva(Modelo):
    tipo: Literal["opcion", "vf", "numerica"]
    enunciado: str = Field(min_length=1, max_length=10_000)
    opciones: list[str] | None = None
    clave: int | bool | float
    tolerancia: float = Field(default=0.0, ge=0)
    puntos: float = Field(default=1.0, gt=0)

    @model_validator(mode="after")
    def _coherente(self):
        if self.tipo == "opcion":
            if not self.opciones or len(self.opciones) < 2:
                raise ValueError("una pregunta de opción necesita al menos dos opciones")
            if isinstance(self.clave, bool) or not isinstance(self.clave, int) or not 0 <= self.clave < len(self.opciones):
                raise ValueError("la clave de una pregunta de opción es el índice (desde 0) de la correcta")
        elif self.tipo == "vf":
            if not isinstance(self.clave, bool):
                raise ValueError("la clave de verdadero o falso es true o false")
            self.opciones = None
        else:
            if isinstance(self.clave, bool):
                raise ValueError("la clave numérica es un número")
            self.clave = float(self.clave)
            self.opciones = None
        return self


class ExamenNuevo(Modelo):
    titulo: str = Field(min_length=2, max_length=200)
    instrucciones: str = Field(default="", max_length=20_000)
    minutos: int | None = Field(default=None, gt=0, le=600)
    intentos_max: int = Field(default=1, ge=1, le=20)
    preguntas_por_intento: int | None = Field(default=None, ge=1)
    aleatorio: bool = True
    abre_en: datetime | None = None
    cierra_en: datetime | None = None
    publicado: bool = False
    revelar_claves: bool = False
    preguntas: list[PreguntaNueva] = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def _coherente(self):
        if self.preguntas_por_intento and self.preguntas_por_intento > len(self.preguntas):
            raise ValueError("preguntas_por_intento no puede ser mayor que el banco")
        if self.abre_en and self.cierra_en and self.cierra_en <= self.abre_en:
            raise ValueError("el examen debe cerrar después de abrir")
        return self


class ExamenCambio(Modelo):
    titulo: str | None = Field(default=None, min_length=2, max_length=200)
    instrucciones: str | None = None
    minutos: int | None = Field(default=None, gt=0, le=600)
    intentos_max: int | None = Field(default=None, ge=1, le=20)
    abre_en: datetime | None = None
    cierra_en: datetime | None = None
    publicado: bool | None = None
    revelar_claves: bool | None = None


class Respuestas(Modelo):
    # {"<id de pregunta>": índice | true/false | número o texto con coma decimal}
    respuestas: dict[str, int | bool | float | str | None] = Field(default_factory=dict)


# --- progreso ---------------------------------------------------------------------------------------------------

class Progreso(Modelo):
    # {"<curso>/<slug>": "AAAA-MM-DD" | null}; null desmarca
    completadas: dict[str, str | None]

    @field_validator("completadas")
    @classmethod
    def _claves(cls, v: dict) -> dict:
        if len(v) > 2000:
            raise ValueError("demasiadas lecciones en una sola sincronización")
        for k, f in v.items():
            if not _LECCION.match(k):
                raise ValueError(f"lección no válida: {k!r} (se espera <curso>/<slug>)")
            if f is not None and not _FECHA.match(f):
                raise ValueError(f"fecha no válida para {k!r}: se espera AAAA-MM-DD")
        return v


def validar_ident(v: str, que: str = "identificador") -> str:
    if not _IDENT.match(v):
        raise ValueError(f"{que} no válido")
    return v
