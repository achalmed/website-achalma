"""api/aula/cli.py — operación del aula desde la terminal: tablas, roles, siembra ficticia y depuración por inactividad.

Todo lo que escribe simula por defecto y pide `--aplicar` (normativa 5.10):

    python -m aula.cli tablas [--aplicar]                  crea las tablas que falten
    python -m aula.cli rol <correo> <rol> [--aplicar]      estudiante · docente · admin
    python -m aula.cli clave <correo> [--aplicar]          contraseña temporal al azar (no hay correo de recuperación)
    python -m aula.cli sembrar [--aplicar]                 datos FICTICIOS para probar (correos @ejemplo.test)
    python -m aula.cli depurar [--dias N] [--aplicar]      borra cuentas sin actividad (docs/privacidad.md §4)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import timedelta

from sqlalchemy import delete, func, inspect, select

from aula import db, seguridad, tiempo
from aula.config import config
from aula.modelos import ROLES_GLOBALES, Base, Clase, Examen, Inscripcion, Pregunta, SesionRenovacion, Tarea, Usuario

DOMINIO_FICTICIO = "@ejemplo.test"  # .test está reservado (RFC 2606): nunca es un correo real


async def _tablas(aplicar: bool) -> int:
    async with db.motor().connect() as conexion:
        existentes = set(await conexion.run_sync(lambda c: inspect(c).get_table_names()))
    faltan = [t for t in Base.metadata.tables if t not in existentes]
    print(f"tablas que faltan: {', '.join(faltan) or 'ninguna'}")
    if aplicar and faltan:
        await db.crear_tablas()
        print("creadas")
    elif faltan:
        print("[simulación] use --aplicar para crearlas")
    return 0


async def _rol(correo: str, rol: str, aplicar: bool) -> int:
    if rol not in ROLES_GLOBALES:
        print(f"rol no válido: {rol} ({', '.join(ROLES_GLOBALES)})", file=sys.stderr)
        return 2
    async with db.fabrica()() as sesion:
        usuario = (await sesion.execute(select(Usuario).where(Usuario.correo == correo.strip().lower()))).scalar_one_or_none()
        if usuario is None:
            print(f"no hay una cuenta con el correo {correo}", file=sys.stderr)
            return 1
        print(f"{usuario.correo}: {usuario.rol_global} → {rol}")
        if aplicar:
            usuario.rol_global = rol
            await sesion.commit()
            print("aplicado")
        else:
            print("[simulación] use --aplicar")
    return 0


async def _clave(correo: str, aplicar: bool) -> int:
    """Pone una contraseña temporal al azar y cierra todas las sesiones de la cuenta; la persona la cambia después."""
    import secrets

    async with db.fabrica()() as sesion:
        usuario = (await sesion.execute(select(Usuario).where(Usuario.correo == correo.strip().lower()))).scalar_one_or_none()
        if usuario is None:
            print(f"no hay una cuenta con el correo {correo}", file=sys.stderr)
            return 1
        if not aplicar:
            print(f"[simulación] {usuario.correo}: se pondría una contraseña temporal y se cerrarían sus sesiones (use --aplicar)")
            return 0
        temporal = secrets.token_urlsafe(9)
        usuario.clave_hash = seguridad.hashear_clave(temporal)
        await seguridad.revocar_todas(sesion, usuario.id)
        await sesion.commit()
        print(f"{usuario.correo}: contraseña temporal {temporal} (comuníquela por un canal privado; que la cambie en «Mi aula»)")
    return 0


async def _sembrar(aplicar: bool) -> int:
    """Una clase de prueba con una docente y dos estudiantes inventados, una tarea con rúbrica y un examen."""
    async with db.fabrica()() as sesion:
        reales = (
            await sesion.execute(select(func.count()).select_from(Usuario).where(~Usuario.correo.like(f"%{DOMINIO_FICTICIO}")))
        ).scalar_one()
        if reales:
            print(f"la base tiene {reales} cuenta(s) real(es): la siembra ficticia solo va en una base de prueba", file=sys.stderr)
            return 1
        personas = [
            ("docente" + DOMINIO_FICTICIO, "Docente Ficticia", "docente"),
            ("ana" + DOMINIO_FICTICIO, "Ana Prueba", "estudiante"),
            ("beto" + DOMINIO_FICTICIO, "Beto Ensayo", "estudiante"),
        ]
        print("se crearían:", ", ".join(p[0] for p in personas), "· clase «Clase de prueba» (methodica) · 1 tarea · 1 examen")
        if not aplicar:
            print("[simulación] use --aplicar (contraseña de las tres cuentas: clave-de-prueba)")
            return 0
        ahora = tiempo.ahora()
        usuarios = {}
        for correo, nombre, rol in personas:
            u = (await sesion.execute(select(Usuario).where(Usuario.correo == correo))).scalar_one_or_none()
            if u is None:
                u = Usuario(correo=correo, nombre_visible=nombre, clave_hash=seguridad.hashear_clave("clave-de-prueba"),
                            rol_global=rol, consentimiento_version=config.politica_version, consentimiento_en=ahora)
                sesion.add(u)
                await sesion.flush()
            usuarios[correo] = u
        clase = Clase(nombre="Clase de prueba", curso_id="metodologia-investigacion", pub="methodica", periodo="prueba", codigo="PRUEBA7")
        if (await sesion.execute(select(Clase).where(Clase.codigo == clase.codigo))).scalar_one_or_none():
            print("la clase de prueba ya existe")
            return 0
        sesion.add(clase)
        await sesion.flush()
        for correo, _, rol in personas:
            sesion.add(Inscripcion(clase_id=clase.id, usuario_id=usuarios[correo].id, rol="docente" if rol == "docente" else "estudiante"))
        sesion.add(Tarea(clase_id=clase.id, titulo="Ensayo breve", consigna="Escribe 300 palabras sobre el método científico.",
                         fecha_limite=ahora + timedelta(days=7), puntaje_max=20,
                         rubrica=[{"criterio": "argumento", "descripcion": "", "puntos": 12}, {"criterio": "redaccion", "descripcion": "", "puntos": 8}]))
        examen = Examen(clase_id=clase.id, titulo="Control de prueba", minutos=20, intentos_max=2, publicado=True)
        sesion.add(examen)
        await sesion.flush()
        sesion.add_all([
            Pregunta(examen_id=examen.id, orden=0, tipo="opcion", enunciado="¿Qué es una hipótesis?",
                     opciones=["Una certeza", "Una respuesta tentativa", "Un dato"], clave=1),
            Pregunta(examen_id=examen.id, orden=1, tipo="vf", enunciado="Una muestra es parte de la población.", clave=True),
            Pregunta(examen_id=examen.id, orden=2, tipo="numerica", enunciado="¿Cuánto es 0,5 × 8?", clave=4.0, tolerancia=0.001),
        ])
        await sesion.commit()
        print(f"sembrado: clase {clase.id}, código {clase.codigo}")
    return 0


async def _depurar(dias: int, aplicar: bool) -> int:
    limite = tiempo.ahora() - timedelta(days=dias)
    async with db.fabrica()() as sesion:
        viejas = (
            await sesion.execute(
                select(Usuario).where(func.coalesce(Usuario.ultimo_acceso_en, Usuario.creado_en) < limite, Usuario.rol_global == "estudiante")
            )
        ).scalars().all()
        vencidas = (
            await sesion.execute(select(func.count()).select_from(SesionRenovacion).where(SesionRenovacion.expira_en < tiempo.ahora()))
        ).scalar_one()
        print(f"cuentas de estudiante sin actividad desde hace más de {dias} días: {len(viejas)}")
        print(f"sesiones de renovación vencidas: {vencidas}")
        if not aplicar:
            if viejas or vencidas:
                print("[simulación] use --aplicar para borrarlas (las cuentas, con sus datos y archivos)")
            return 0
        await sesion.execute(delete(SesionRenovacion).where(SesionRenovacion.expira_en < tiempo.ahora()))
        await sesion.commit()
        from fastapi import HTTPException

        from aula import archivos
        from aula.rutas.cuentas import borrar_datos_de

        borradas = 0
        for u in viejas:
            try:
                rutas_archivos = await borrar_datos_de(sesion, u)
            except HTTPException as e:
                print(f"se conserva {u.id}: {e.detail}")
                continue
            await sesion.commit()
            for r in rutas_archivos:
                archivos.borrar(r)
            borradas += 1
        print(f"borradas: {borradas}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m aula.cli", description="Operación del aula (simula por defecto).")
    sub = ap.add_subparsers(dest="orden", required=True)
    p = sub.add_parser("tablas", help="crea las tablas que falten")
    p.add_argument("--aplicar", action="store_true")
    p = sub.add_parser("rol", help="cambia el rol global de una cuenta")
    p.add_argument("correo")
    p.add_argument("rol", choices=ROLES_GLOBALES)
    p.add_argument("--aplicar", action="store_true")
    p = sub.add_parser("clave", help="contraseña temporal al azar para una cuenta")
    p.add_argument("correo")
    p.add_argument("--aplicar", action="store_true")
    p = sub.add_parser("sembrar", help="datos ficticios para probar (solo en una base sin cuentas reales)")
    p.add_argument("--aplicar", action="store_true")
    p = sub.add_parser("depurar", help="borra cuentas de estudiante sin actividad")
    p.add_argument("--dias", type=int, default=config.dias_inactividad)
    p.add_argument("--aplicar", action="store_true")
    args = ap.parse_args(argv)
    if args.orden == "tablas":
        corrutina = _tablas(args.aplicar)
    elif args.orden == "rol":
        corrutina = _rol(args.correo, args.rol, args.aplicar)
    elif args.orden == "clave":
        corrutina = _clave(args.correo, args.aplicar)
    elif args.orden == "sembrar":
        corrutina = _sembrar(args.aplicar)
    else:
        corrutina = _depurar(args.dias, args.aplicar)

    async def correr():
        try:
            return await corrutina
        finally:
            await db.motor().dispose()

    return asyncio.run(correr())


if __name__ == "__main__":
    raise SystemExit(main())
