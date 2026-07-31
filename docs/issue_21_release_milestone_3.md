# Issue #21: End of Milestone 3 Release

**Objective**: Milestone 3 ("GCS Fallback Archive") is completely finished! We have implemented a resilient GCS Loader, integrated it successfully into our Airflow TaskFlow DAG, and verified it with exhaustive unit tests that cover connection errors and JSON parsing edge cases.
Now, we must promote all these features from our `develop` branch into `main` to finalize the release.

---

## Step 1 — Create Release PR

Asegurate de estar en la rama `develop` y con los últimos cambios traídos desde origin:

```bash
git checkout develop
git pull origin develop
```

Creá el PR de release apuntando hacia `main`:

```bash
gh pr create \
  --title "chore: Release Milestone 3 (GCS Fallback Archive)" \
  --body "Promoting develop to main after successfully implementing the resilient GCSLoader, integrating it with the TaskFlow API, and ensuring 100% test coverage." \
  --base main \
  --head develop
```

---

## Step 2 — Merge Release PR

Mergeá el PR desde la terminal (o desde la web). Como es de `develop` a `main`, **NO** uses `--delete-branch` para no borrar `develop`!

```bash
gh pr merge <N> --merge
```
*(Nota: Cambiá `<N>` por el número del PR que te devolvió el comando anterior).*

---

## Step 3 — Close the Issue and Update Local `main`

Cerrá este último issue:

```bash
gh issue close 21 --comment "Milestone 3 successfully released to main."
```

Actualizá tu entorno local para que tu `main` tenga los cambios reflejados:

```bash
git checkout main
git pull origin main
git checkout develop
```
