"""api/aula/modelos.py — el modelo de datos del aula con cuenta (SQLAlchemy 2, tipos portables PostgreSQL ⇄ SQLite).

Usuario → inscripciones en clases (docente o estudiante) → anuncios, tareas con entregas y calificaciones, exámenes
con banco de preguntas e intentos corregidos en el servidor; y el progreso de lecciones por pub y curso. Nada de
tipos propios de PostgreSQL (JSON genérico, `FechaUTC`): la misma suite de pruebas corre sobre las dos bases.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from aula import tiempo
from aula.tiempo import FechaUTC

ROLES_GLOBALES = ("estudiante", "docente", "admin")
ROLES_CLASE = ("docente", "estudiante")
TIPOS_PREGUNTA = ("opcion", "vf", "numerica")


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correo: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    nombre_visible: Mapped[str] = mapped_column(String(120))
    clave_hash: Mapped[str] = mapped_column(String(255))
    # estudiante (por omisión al registrarse) · docente (puede crear clases) · admin (cambia roles por la CLI)
    rol_global: Mapped[str] = mapped_column(String(20), default="estudiante")
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    consentimiento_version: Mapped[str] = mapped_column(String(20))
    consentimiento_en: Mapped[datetime] = mapped_column(FechaUTC())
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)
    ultimo_acceso_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)


class SesionRenovacion(Base):
    """Token de renovación: solo se guarda su resumen SHA-256; rota en cada uso y se revoca al salir."""

    __tablename__ = "sesiones_renovacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    resumen: Mapped[str] = mapped_column(String(64), unique=True)
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)
    expira_en: Mapped[datetime] = mapped_column(FechaUTC())
    revocado_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)


class Clase(Base):
    """Un grupo concreto de un curso de `docencia` (por su id) que se dicta en un pub."""

    __tablename__ = "clases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(160))
    curso_id: Mapped[str] = mapped_column(String(80), index=True)
    pub: Mapped[str] = mapped_column(String(60), index=True)
    periodo: Mapped[str] = mapped_column(String(40), default="")
    codigo: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    archivada: Mapped[bool] = mapped_column(Boolean, default=False)
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Inscripcion(Base):
    __tablename__ = "inscripciones"
    __table_args__ = (UniqueConstraint("clase_id", "usuario_id", name="uq_inscripcion"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clase_id: Mapped[int] = mapped_column(ForeignKey("clases.id", ondelete="CASCADE"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    rol: Mapped[str] = mapped_column(String(20))
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Anuncio(Base):
    __tablename__ = "anuncios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clase_id: Mapped[int] = mapped_column(ForeignKey("clases.id", ondelete="CASCADE"), index=True)
    autor_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    texto: Mapped[str] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clase_id: Mapped[int] = mapped_column(ForeignKey("clases.id", ondelete="CASCADE"), index=True)
    titulo: Mapped[str] = mapped_column(String(200))
    consigna: Mapped[str] = mapped_column(Text, default="")
    fecha_limite: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)
    puntaje_max: Mapped[float] = mapped_column(Float, default=20.0)
    # [{"criterio": "...", "descripcion": "...", "puntos": 5}, ...]; la suma no puede pasar de puntaje_max
    rubrica: Mapped[list | None] = mapped_column(JSON, nullable=True)
    acepta_archivo: Mapped[bool] = mapped_column(Boolean, default=True)
    publicada: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Entrega(Base):
    __tablename__ = "entregas"
    __table_args__ = (UniqueConstraint("tarea_id", "estudiante_id", name="uq_entrega"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tarea_id: Mapped[int] = mapped_column(ForeignKey("tareas.id", ondelete="CASCADE"), index=True)
    estudiante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    texto: Mapped[str] = mapped_column(Text, default="")
    # El archivo vive en AULA_DATOS_DIR; aquí solo su ruta relativa y su nombre original.
    archivo_ruta: Mapped[str | None] = mapped_column(String(300), nullable=True)
    archivo_nombre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    archivo_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    entregado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)
    tardia: Mapped[bool] = mapped_column(Boolean, default=False)


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entrega_id: Mapped[int] = mapped_column(ForeignKey("entregas.id", ondelete="CASCADE"), unique=True)
    puntaje: Mapped[float] = mapped_column(Float)
    comentario: Mapped[str] = mapped_column(Text, default="")
    # {"<criterio>": puntos} cuando la tarea tiene rúbrica
    por_criterio: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    calificado_por: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    calificado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Examen(Base):
    __tablename__ = "examenes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clase_id: Mapped[int] = mapped_column(ForeignKey("clases.id", ondelete="CASCADE"), index=True)
    titulo: Mapped[str] = mapped_column(String(200))
    instrucciones: Mapped[str] = mapped_column(Text, default="")
    minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    intentos_max: Mapped[int] = mapped_column(Integer, default=1)
    # Cuántas preguntas del banco toca a cada intento (None = todas) y si se barajan preguntas y opciones.
    preguntas_por_intento: Mapped[int | None] = mapped_column(Integer, nullable=True)
    aleatorio: Mapped[bool] = mapped_column(Boolean, default=True)
    abre_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)
    cierra_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    # Mostrar la clave al estudiante después del cierre del examen (nunca antes).
    revelar_claves: Mapped[bool] = mapped_column(Boolean, default=False)
    creado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)


class Pregunta(Base):
    """Una pregunta del banco del examen. `clave` y `tolerancia` nunca salen hacia un estudiante en curso."""

    __tablename__ = "preguntas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    examen_id: Mapped[int] = mapped_column(ForeignKey("examenes.id", ondelete="CASCADE"), index=True)
    orden: Mapped[int] = mapped_column(Integer, default=0)
    tipo: Mapped[str] = mapped_column(String(20))
    enunciado: Mapped[str] = mapped_column(Text)
    opciones: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # opcion: índice (desde 0) en `opciones` · vf: true/false · numerica: número
    clave: Mapped[object] = mapped_column(JSON)
    tolerancia: Mapped[float] = mapped_column(Float, default=0.0)
    puntos: Mapped[float] = mapped_column(Float, default=1.0)


class Intento(Base):
    __tablename__ = "intentos"
    __table_args__ = (UniqueConstraint("examen_id", "estudiante_id", "numero", name="uq_intento"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    examen_id: Mapped[int] = mapped_column(ForeignKey("examenes.id", ondelete="CASCADE"), index=True)
    estudiante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    numero: Mapped[int] = mapped_column(Integer)
    iniciado_en: Mapped[datetime] = mapped_column(FechaUTC(), default=tiempo.ahora)
    vence_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)
    entregado_en: Mapped[datetime | None] = mapped_column(FechaUTC(), nullable=True)
    # en_curso · entregado · vencido (se corrigió con lo guardado al vencer)
    estado: Mapped[str] = mapped_column(String(20), default="en_curso")
    # [{"id": <pregunta>, "opciones": [permutación] | null}] en el orden en que se le presentó
    orden: Mapped[list] = mapped_column(JSON)
    respuestas: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"<pregunta>": {"correcta": bool, "puntos": float}} tras corregir
    detalle: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    puntaje: Mapped[float | None] = mapped_column(Float, nullable=True)
    puntaje_max: Mapped[float] = mapped_column(Float, default=0.0)


class Progreso(Base):
    """Lección completada, el espejo en servidor de `aula:<pub>:completadas` de la vitrina."""

    __tablename__ = "progreso"
    __table_args__ = (UniqueConstraint("usuario_id", "pub", "leccion", name="uq_progreso"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    pub: Mapped[str] = mapped_column(String(60))
    # "<curso>/<slug>", la misma clave que usa el navegador
    leccion: Mapped[str] = mapped_column(String(200))
    completada_el: Mapped[str] = mapped_column(String(10))
