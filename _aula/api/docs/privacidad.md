---
tipo: doc
forma: referencia
titulo: "Política de privacidad del aula"
estado: borrador
version: 2026-10-20
---
# Política de privacidad del aula

Versión **2026-10-20** (`AULA_POLITICA_VERSION`). Es el texto que la vitrina resume antes del registro (`GET
/privacidad`) y que cada persona acepta al crear su cuenta; la API guarda la versión aceptada y la fecha. Marco: Ley
29733, de Protección de Datos Personales, y su reglamento vigente. Es un **borrador técnico**: describe con exactitud
lo que el código hace; los puntos marcados «al autor» (§7) los decide y completa el autor antes de abrir el aula a
estudiantes reales.

## 1. Quién trata los datos y para qué

El titular del aula (el autor, docente de los cursos de los 12 sitios) trata los datos con **una sola finalidad**: dar
el servicio educativo del aula (cuentas, clases, anuncios, tareas y entregas, calificaciones, exámenes y progreso de
lecciones). No hay publicidad, analítica, perfiles ni cesión a terceros, y la API no usa cookies.

## 2. Qué datos se guardan

| dato | para qué | dónde | cuánto tiempo |
|---|---|---|---|
| correo, nombre visible, rol | identificar la cuenta y mostrar el nombre al docente | base PostgreSQL | hasta la baja o 2 años sin actividad |
| contraseña | iniciar sesión; se guarda **solo su resumen Argon2id**, nunca la contraseña | base | ídem |
| versión y fecha del consentimiento, último acceso | probar el consentimiento; calcular la inactividad | base | ídem |
| sesiones (resumen SHA-256 del token de renovación, fechas) | mantener la sesión abierta y poder cerrarla | base | 30 días; las vencidas se borran con `depurar` |
| clases e inscripciones | saber en qué clases participa y con qué rol | base | hasta la baja o la salida de la clase |
| entregas: texto y archivo | que el docente las lea y califique | base; archivos en `AULA_DATOS_DIR` | hasta la baja |
| calificaciones y comentarios | la nota de cada tarea | base | hasta la baja |
| intentos de examen: respuestas y nota | corregir en el servidor y llevar el libro de notas | base | hasta la baja |
| lecciones completadas por sitio | sincronizar el progreso entre dispositivos | base | hasta la baja |

**No se guarda**: la dirección IP (el límite de intentos la usa solo en memoria y la API corre sin registro de
accesos, `--no-access-log`), el navegador, la ubicación ni la actividad de lectura fuera de lo que la persona marca.

## 3. Dónde viven y quién los ve

- En la laptop del autor, que sirve el aula (decisión A9): la base en un volumen de Docker y los archivos en
  `AULA_DATOS_DIR` (por omisión `$XDG_DATA_HOME/aula`, permisos 700/600). **Nunca dentro de un repositorio**: la API
  se niega a arrancar si esa carpeta cae dentro de uno, y `respaldar.sh` se niega a escribir en uno.
- Los respaldos van **cifrados con clave pública** (age o gpg) al disco de respaldos (`$RESPALDOS_DIR/aula/`).
- Acceso por internet: Tailscale Funnel con HTTPS; el sitio manda el token en una cabecera, no en cookies.
- Dentro del aula: cada estudiante ve solo lo suyo (entregas, notas, intentos, progreso) y, de su clase, solo el nombre
  de los docentes; el docente de una clase ve las entregas, intentos y notas de esa clase y los correos de sus
  miembros. Nadie ve datos de otra clase. Lo comprueban las pruebas (`_aula/api/tests/test_permisos.py`).

## 4. Cuánto tiempo

Mientras la cuenta se use. Una cuenta de estudiante sin actividad durante **730 días** (`AULA_DIAS_INACTIVIDAD`) se
borra con todo lo suyo al correr `python -m aula.cli depurar --aplicar` (simula sin `--aplicar`), que el autor
ejecuta en la revisión semestral del ecosistema. Las copias cifradas se conservan según la rotación del disco de
respaldos (§7).

## 5. Derechos: acceso, rectificación, cancelación y oposición

- **Acceso**: «Mi aula» → «Descargar mis datos» (`GET /cuentas/yo/datos`) entrega en JSON todo lo que el aula guarda
  de la persona, con el enlace de cada archivo.
- **Rectificación**: el nombre visible y la contraseña se cambian en la cuenta (`PATCH /cuentas/yo`); un correo mal
  escrito se corrige pidiéndolo al docente.
- **Cancelación**: «Mi aula» → «Borrar mi cuenta» (`DELETE /cuentas/yo`, con la contraseña) borra la cuenta, sus
  entregas y archivos, calificaciones, intentos, progreso e inscripciones. Los anuncios que un docente publicó y las
  notas que puso quedan en sus clases sin su nombre. Un docente que es el único de una clase con estudiantes debe
  sumar otro docente o retirarlos antes, para no borrar datos ajenos.
- **Oposición**: dejar de usar el aula y pedir la baja tiene el mismo efecto; no hay otro tratamiento al que oponerse.

## 6. Seguridad

Contraseñas con Argon2id; sesiones de acceso de 15 minutos y renovación rotativa que se revoca entera si alguien
reutiliza un token viejo; límite de intentos de inicio de sesión por correo; CORS solo para los 12 sitios; archivos
de entrega con límite de tamaño y tipos permitidos, guardados con nombre aleatorio y servidos siempre como descarga.

## 7. Al autor (antes de abrir el aula a estudiantes reales)

- Poner un medio de contacto para ejercer los derechos (correo del aula) en esta política y en «Mi aula».
- Verificar con la Autoridad Nacional de Protección de Datos Personales si el banco de datos del aula debe
  inscribirse en su registro, y cargar la ley y su reglamento en Calibre para citarlos.
- Decidir el consentimiento de padres o tutores si el aula recibirá menores de edad (preuniversitario).
- Fijar cuánto se conservan los respaldos cifrados y cuándo se rota la clave.
