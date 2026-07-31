# Issue #21: Documentación Final (README y Arquitectura)

**Branch**: `chore/issue-21-final-documentation` (based on `develop`)  
**Objective**: Llegamos al final del proyecto. Este issue es para redactar el `README.md` final para que el repositorio sea un excelente caso de estudio en el portfolio, y terminar de pulir los diagramas o notas en `docs/architecture.md`. 

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b chore/issue-21-final-documentation
```

---

## Step 2 — Update README.md

Editá el archivo raíz `README.md`. Debería incluir:
- **Resumen del proyecto**: Qué hace (ETL de criptomonedas).
- **Arquitectura**: Airflow + GCP (BigQuery, GCS) + Polars.
- **Cómo ejecutarlo localmente**: Instrucciones con Docker/venv y variables de entorno.
- **Milestones logrados**: Resumen de las 3 fases que completaste.

---

## Step 3 — Update docs/architecture.md

Revisá `docs/architecture.md` (si existe) o el archivo correspondiente. 
Asegurate de que mencione la integración final del `GCSLoader` como capa de resiliencia y cómo interactúan las tareas a través de Airflow TaskFlow y XComs.

---

## Step 4 — Commit and Push

```bash
git add README.md docs/
git commit -m "docs: finalize README and project architecture documentation"
git push origin chore/issue-21-final-documentation
```

---

## Step 5 — Create PR, Merge and Close Issue

```bash
gh pr create \
  --title "docs: Issue #21 — Documentación Final del Proyecto" \
  --body "Actualiza el README y la documentación arquitectónica para el portfolio." \
  --base develop \
  --head chore/issue-21-final-documentation

gh pr merge <N> --squash --delete-branch
gh issue close 21 --comment "Documentación finalizada."
```

---

## Step 6 — Final Release (develop -> main)

¡Ahora sí! Promovemos todo el proyecto terminado a producción:

```bash
git checkout develop
git pull origin develop

gh pr create \
  --title "chore: Final Release v1.0" \
  --body "Release final a main con el proyecto completo y documentado." \
  --base main \
  --head develop
```

Una vez mergeado (con `--merge` desde la web o terminal), actualizá localmente:
```bash
git checkout main
git pull origin main
```
