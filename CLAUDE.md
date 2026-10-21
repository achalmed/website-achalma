---
tipo: guia_ia
estado: activo
---
# CLAUDE.md — aula

El código de la plataforma de cursos de los pubs (vitrina estática con Astro; más adelante, la API del aula). No es
contenido. Léase antes: `README.md`, `estado.md`, `docs/README.md` y `web/docs/plataforma-educativa.md`.
Rigen las reglas del `CLAUDE.md` raíz de `~/Documents`: aquí solo lo que el raíz no dice.

## Reglas propias

- **Solo lee las fuentes; nunca las escribe**: `docencia` (currículo: `curso.yml`, `docencia/config/areas.yml`), los pubs
  (`web/_pubs/<pub>`), `simuladores` (`catalogo.json`). Rutas por `core/env.py` / `core/env.sh`.
- **Nada de datos de estudiantes en el repo** (regla 8): el aula con cuenta guarda sus datos fuera, con respaldo cifrado.
- **Identidad «Laboratorio abierto»**: los tokens vienen del design system del hub (`web/assets/scss/00-settings/`);
  un color nuevo entra por los tokens, nunca como hex suelto en un componente.
- **Accesible y primero 375 px**: claro y oscuro, `prefers-reduced-motion`, teclado.

## Dónde está cada cosa

| pregunta | documento |
|---|---|
| la arquitectura, las decisiones del autor y el plan | `web/docs/plataforma-educativa.md` |
| qué está en curso y qué queda | `estado.md` |
| por qué está hecho así | `docs/decisiones.md` |
| el resto de la documentación | `docs/README.md` (índice generado) |
