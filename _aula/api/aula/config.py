"""api/aula/config.py — configuración de la API del aula: todo valor ajustable sale del entorno (prefijo AULA_).

Ningún módulo lee `os.environ` directamente: lo hace `config`. Los secretos y la contraseña de la base no viven en el
repo: `iniciar.sh` los guarda en `$XDG_CONFIG_HOME/aula/aula.env` (permisos 600) y los exporta antes de arrancar.
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Extensiones que una entrega puede llevar. Documentos, hojas, imágenes, código y datos de los cursos del autor;
# nada ejecutable del lado del docente (sin .exe, .sh, .html, .svg, que un navegador podría interpretar).
EXTENSIONES_POR_DEFECTO = (
    "pdf,docx,doc,odt,xlsx,xls,ods,pptx,odp,txt,md,csv,tsv,json,png,jpg,jpeg,webp,zip,"
    "py,r,rmd,qmd,ipynb,do,dta,sav,gdt,m,tex,bib"
)


def _datos_por_defecto() -> str:
    """`$XDG_DATA_HOME/aula` o, si no está definida, `~/.local/share/aula` (fuera de todo repo)."""
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return str(Path(base) / "aula")


class Configuracion(BaseSettings):
    """Valores del entorno con defectos de desarrollo local (nunca de producción)."""

    model_config = SettingsConfigDict(env_prefix="AULA_", extra="ignore")

    # Base de datos: PostgreSQL 16 del docker compose propio (puerto 5442, distinto del de Qillqa).
    database_url: str = "postgresql+asyncpg://aula:aula@127.0.0.1:5442/aula"
    # Crear las tablas que falten al arrancar (sin Alembic mientras el modelo se estabiliza; decisiones §1.10).
    crear_tablas: bool = True

    # Autenticación: acceso corto por JWT y renovación opaca guardada como resumen SHA-256.
    jwt_secreto: str = ""
    minutos_acceso: int = 15
    dias_renovacion: int = 30
    # Límite de intentos fallidos de inicio de sesión por correo, en una ventana deslizante.
    intentos_sesion: int = 5
    minutos_ventana_sesion: int = 15
    # Registros nuevos por dirección IP y hora (protege de altas en masa; detrás de un proxy, ver README).
    registros_por_hora: int = 20
    permitir_registro: bool = True

    # Archivos de las entregas: fuera del repo, con límite de tamaño y tipos permitidos.
    datos_dir: str = _datos_por_defecto()
    max_archivo_mb: int = 10
    extensiones: str = EXTENSIONES_POR_DEFECTO

    # Origen cruzado: la lista blanca sale de web/_pubs/pubs.yml (aula/origenes.generado.json); localhost para
    # desarrollo y orígenes extra (separados por coma) por entorno.
    cors_local: bool = True
    origenes_extra: str = ""

    # Privacidad: versión vigente de docs/privacidad.md; el registro exige aceptar esta versión.
    politica_version: str = "2026-10-20"
    # Días sin actividad tras los que una cuenta se propone para baja (`python -m aula.cli depurar`).
    dias_inactividad: int = 730

    # Exámenes: segundos de gracia tras el vencimiento para absorber la latencia de la red.
    gracia_examen_s: int = 30

    @property
    def extensiones_permitidas(self) -> set[str]:
        return {e.strip().lower().lstrip(".") for e in self.extensiones.split(",") if e.strip()}

    @property
    def max_archivo_bytes(self) -> int:
        return self.max_archivo_mb * 1024 * 1024


config = Configuracion()
