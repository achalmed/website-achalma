"""api/aula/archivos.py — los archivos de las entregas, en AULA_DATOS_DIR y nunca dentro de un repo git.

Se guardan como `entregas/<tarea>/<estudiante>/<aleatorio>.<ext>`: el nombre original solo vive en la base (no se
usa como ruta, así que no hay recorrido de directorios). Se escriben por trozos y se cortan al pasar el límite.
"""

from __future__ import annotations

import os
import re
import secrets
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from aula.config import config

_TROZO = 1024 * 1024


class DatosEnRepo(RuntimeError):
    pass


def dentro_de_repo(ruta: Path) -> Path | None:
    """La raíz del repo git que contiene `ruta` (o la contendría), o None."""
    ruta = ruta.expanduser().resolve()
    for carpeta in (ruta, *ruta.parents):
        if (carpeta / ".git").exists():
            return carpeta
    return None


def raiz_datos() -> Path:
    """AULA_DATOS_DIR, creada con permisos 700. Se niega a usar una carpeta dentro de un repo (regla 8)."""
    raiz = Path(config.datos_dir).expanduser()
    repo = dentro_de_repo(raiz)
    if repo is not None:
        raise DatosEnRepo(f"AULA_DATOS_DIR ({raiz}) está dentro del repo {repo}: los datos de estudiantes nunca van a un repo.")
    raiz.mkdir(parents=True, exist_ok=True, mode=0o700)
    return raiz


def nombre_seguro(nombre: str) -> str:
    base = os.path.basename(nombre or "").strip() or "archivo"
    base = re.sub(r"[^\w.\- ]+", "_", base, flags=re.UNICODE)
    return base[:200]


def extension(nombre: str) -> str:
    return Path(nombre).suffix.lower().lstrip(".")


async def guardar(archivo: UploadFile, tarea_id: int, estudiante_id: int) -> tuple[str, str, int]:
    """Guarda la subida y devuelve (ruta relativa, nombre original saneado, bytes)."""
    nombre = nombre_seguro(archivo.filename or "")
    ext = extension(nombre)
    if ext not in config.extensiones_permitidas:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Tipo de archivo no permitido (.{ext or '?'}). Permitidos: {', '.join(sorted(config.extensiones_permitidas))}.",
        )
    raiz = raiz_datos()
    relativa = Path("entregas") / str(tarea_id) / str(estudiante_id) / f"{secrets.token_hex(12)}.{ext}"
    destino = raiz / relativa
    destino.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    total = 0
    try:
        with open(destino, "wb") as salida:
            while trozo := await archivo.read(_TROZO):
                total += len(trozo)
                if total > config.max_archivo_bytes:
                    raise HTTPException(
                        status.HTTP_413_CONTENT_TOO_LARGE,
                        f"El archivo pasa del límite de {config.max_archivo_mb} MB.",
                    )
                salida.write(trozo)
        os.chmod(destino, 0o600)
    except BaseException:
        destino.unlink(missing_ok=True)
        raise
    if total == 0:
        destino.unlink(missing_ok=True)
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "El archivo está vacío.")
    return str(relativa), nombre, total


def ruta_absoluta(relativa: str) -> Path:
    raiz = raiz_datos().resolve()
    ruta = (raiz / relativa).resolve()
    if raiz not in ruta.parents:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Archivo no encontrado.")
    return ruta


def borrar(relativa: str | None) -> None:
    if not relativa:
        return
    try:
        ruta_absoluta(relativa).unlink(missing_ok=True)
    except HTTPException:
        pass
