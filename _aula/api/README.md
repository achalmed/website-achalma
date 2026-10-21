---
tipo: readme
estado: borrador
---
# api/ — la API del aula con cuenta

La API que da a los 12 sitios (los pubs, estáticos en `*.netlify.app`) lo que un sitio estático no puede: cuentas,
clases con inscripción por código, anuncios, tareas con entrega y calificación (con rúbrica), exámenes calificados
en el servidor y progreso de lecciones sincronizado. FastAPI + SQLAlchemy 2 asíncrono + PostgreSQL 16 en Docker,
servida desde la laptop del autor (decisión A9 de `web/docs/plataforma-educativa.md`). Por qué está hecha así:
`../docs/decisiones.md` §1.9–§1.14. Qué datos guarda y cómo se borran: `docs/privacidad.md`.

## Uso

```bash
cd web/_aula/api                     # desde ~/Documents
./iniciar.sh                         # base (127.0.0.1:5442) + tablas + API (127.0.0.1:8040) en segundo plano
./iniciar.sh --primer-plano          # la API en esta terminal; --docker: la API también en contenedor; --dry-run simula
./detener.sh                         # detiene API y base; los datos se conservan
./respaldar.sh                       # simula; --aplicar escribe el respaldo cifrado en $RESPALDOS_DIR/aula/<fecha>/
```

La primera vez, `iniciar.sh` crea `.venv`, y `$XDG_CONFIG_HOME/aula/aula.env` (permisos 600) con una clave de base y
un secreto JWT al azar y `AULA_DATOS_DIR`. Toda la configuración va por variables `AULA_*` (`aula/config.py`):
duración del acceso (15 min) y de la renovación (30 días), límite de intentos (5 por 15 min y correo), tamaño máximo
de archivo (10 MB) y extensiones permitidas, orígenes extra de CORS, días de inactividad (730).

```bash
.venv/bin/python -m aula.cli rol <correo> docente --aplicar    # una cuenta nueva es estudiante; el docente se nombra así
.venv/bin/python -m aula.cli sembrar --aplicar                 # datos FICTICIOS (@ejemplo.test) solo en una base sin cuentas reales
.venv/bin/python -m aula.cli depurar [--dias N] [--aplicar]    # baja por inactividad y sesiones vencidas (privacidad §4)
.venv/bin/python -m aula.origenes --aplicar                    # regenera la lista blanca de CORS desde web/_pubs/pubs.yml
```

Las órdenes de la CLI necesitan `AULA_DATABASE_URL` (`iniciar.sh` la arma con los valores de `aula.env`). La
documentación interactiva queda en `http://127.0.0.1:8040/docs` mientras la API corre.

**Pruebas.** `.venv/bin/pip install -r requirements-dev.txt` y `.venv/bin/pytest` (58 pruebas, SQLite en memoria,
unos 30 s). Las mismas sobre PostgreSQL 16, con la base arriba:

```bash
set -a; source "${XDG_CONFIG_HOME:-$HOME/.config}/aula/aula.env"; set +a
AULA_PRUEBAS_DATABASE_URL="postgresql+asyncpg://aula:$AULA_POSTGRES_CLAVE@127.0.0.1:5442/aula_prueba" .venv/bin/pytest
```

**Publicarla** (lo decide el autor; ningún script lo hace): con la API arriba, `tailscale funnel --bg 8040` da un enlace
fijo `https://<laptop>.<red>.ts.net`, como `qillqa/enlace.sh`. Luego cada sitio se construye con
`AULA_API_URL=https://<laptop>.<red>.ts.net PUB=<pub> npm run build` (en `web/_aula`), que añade la página «Mi aula».

**Respaldo.** Declare en `aula.env` un destinatario: `AULA_RESPALDO_AGE=age1…` (si `age` está instalado:
`sudo apt install age`) o `AULA_RESPALDO_GPG=<clave>` (gpg ya está en la laptop). La clave privada vive fuera de la
laptop. Restaurar: `gpg -d base.dump.gpg | docker compose exec -T db pg_restore -U aula -d aula --clean` y
`gpg -d datos.tar.gz.gpg | tar -xzf - -C "$(dirname "$AULA_DATOS_DIR")"` (con `age -d -i <clave>` si es age).

## Estructura

| ruta | qué contiene |
|---|---|
| `aula/main.py` | la aplicación: CORS por lista blanca, límite de cuerpo, cabeceras y rutas |
| `aula/config.py` | variables `AULA_*` con defectos de desarrollo |
| `aula/modelos.py` | usuario, sesión de renovación, clase, inscripción, anuncio, tarea, entrega, calificación, examen, pregunta, intento, progreso |
| `aula/seguridad.py` | Argon2id, JWT de acceso, renovación rotativa con detección de reuso, límite de intentos |
| `aula/permisos.py` | miembro, docente y la regla «quien no es miembro recibe 404» |
| `aula/correccion.py` | arma cada intento desde el banco (azar de preguntas y opciones) y lo corrige |
| `aula/archivos.py` | entregas en `AULA_DATOS_DIR`, por trozos, con límite y fuera de todo repo |
| `aula/origenes.py`, `aula/origenes.generado.json` | lista blanca de CORS generada desde `web/_pubs/pubs.yml` (no se edita a mano) |
| `aula/rutas/` | `cuentas`, `clases` (y libro de notas), `anuncios`, `tareas`, `examenes`, `progreso` |
| `aula/cli.py` | tablas, roles, siembra ficticia, depuración |
| `tests/` | pytest + httpx contra la app: cuentas, permisos, entregas, exámenes, CORS, privacidad, progreso |
| `docker-compose.yml`, `Dockerfile` | PostgreSQL 16 (256 MB como mucho) y la imagen opcional de la API |
| `iniciar.sh`, `detener.sh`, `respaldar.sh` | operación local y respaldo cifrado |
| `docs/privacidad.md` | la política que aceptan las cuentas (Ley 29733) |

## Límite honesto

- Con la laptop apagada, dormida o sin internet, el aula no responde: la vitrina sigue en Netlify y «Mi aula» lo dice.
  Para disponibilidad continua, la misma receta Docker sube a un VPS (`plataforma-educativa.md` §7, B1).
- Sin dominio propio (B2) cada sitio guarda su propia sesión: se inicia sesión en cada uno con la misma cuenta.
- El límite de intentos vive en la memoria de un solo proceso: se reinicia con la API y no sirve con varios procesos.
- Las tablas se crean al arrancar (sin Alembic): un cambio de columna en una base con datos necesita una migración a
  mano hasta que el modelo se estabilice.
- No hay aún foros, certificados, liberación condicional, avisos por correo ni panel del docente: el docente crea
  tareas y exámenes y califica por la API (`/docs`); «Mi aula» de la vitrina solo inicia sesión, lista clases con sus
  anuncios, tareas y exámenes, une por código, sincroniza el progreso, cambia la contraseña y exporta o borra los datos.
- No hay recuperación de contraseña por correo (no hay servidor de correo): el autor da una temporal con
  `python -m aula.cli clave <correo> --aplicar` y la persona la cambia en «Mi aula».
- La política de privacidad es un borrador técnico con pendientes del autor (`docs/privacidad.md` §7).
