# Chuleta: Flujo de trabajo para crear un Pull Request

Guía corta del proceso que se siguió para el PR #8 (`docs/add-claude-md`), para repetirlo en cambios futuros.

## Resumen del caso: CLAUDE.md vacío → PR mergeado

1. **Detectar el problema**
   `CLAUDE.md` existía pero estaba vacío (0 bytes).

2. **Generar el contenido**
   Se ejecutó `/init`, que analiza el repo (`README.md`, `_quarto.yml`, estructura de carpetas) y escribe el `CLAUDE.md` con comandos y arquitectura del proyecto.

3. **Crear una rama nueva** (no se puede abrir PR de `main` contra `main`)
   ```bash
   git checkout -b docs/add-claude-md
   ```

4. **Guardar el cambio (commit)**
   ```bash
   git add CLAUDE.md
   git commit -m "docs: add CLAUDE.md for Claude Code guidance"
   ```

5. **Subir la rama a GitHub**
   ```bash
   git push -u origin docs/add-claude-md
   ```

6. **Instalar y autenticar `gh`** (CLI de GitHub), si no está disponible
   ```bash
   sudo apt install gh
   gh auth login
   ```

7. **Crear el Pull Request**
   ```bash
   gh pr create --title "..." --body "..."
   ```
   Si falla con `you must first push the current branch to a remote`, forzar explícitamente:
   ```bash
   gh pr create --repo achalmed/website-achalma --head docs/add-claude-md --base main --title "..." --body "..."
   ```

8. **Revisar y mergear en GitHub**
   - Abrir el link del PR
   - Revisar el diff
   - Clic en "Merge pull request"
   - (Opcional) borrar la rama desde GitHub

9. **Actualizar el repo local**
   ```bash
   git checkout main
   git pull
   ```

## Plantilla rápida para el próximo cambio

```bash
git checkout main
git pull
git checkout -b <tipo>/<nombre-corto>        # ej: fix/typo-navbar
# ...hacer los cambios...
git add <archivos>
git commit -m "<tipo>: <qué cambió y por qué>"
git push -u origin <tipo>/<nombre-corto>
gh pr create --repo achalmed/website-achalma --head <tipo>/<nombre-corto> --base main \
  --title "<título corto>" --body "<qué cambió, por qué, notas para el revisor>"
```

Después: revisar en GitHub → Merge → `git checkout main && git pull`.
