# Issue #5: Documentación de Arquitectura — Capa de Extracción y Modelos de Datos

**Rama**: `feature/issue-5-arch-extraction` (basada en `develop`)  
**Objetivo**: Documentar en `docs/architecture.md` la arquitectura de la capa de extracción (`CoinGeckoExtractor`) y los modelos de datos de validación (`PriceRecord`), incluyendo las decisiones de diseño (ADRs) adoptadas.

---

## Paso 1 — Crear la rama desde `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-5-arch-extraction
```

---

## Paso 2 — Escribir la documentación en `docs/architecture.md`

Completar `docs/architecture.md` detallando:

1. **Visión General de la Capa de Extracción**:
   - Rol del extractor HTTP `CoinGeckoExtractor` en el pipeline.
   - Endpoint consumido: `GET /coins/markets` (API v3 de CoinGecko).
   - Manejo de parámetros (`vs_currency`, `ids`) y `User-Agent`.
2. **Modelo de Datos (`PriceRecord`)**:
   - Uso de Pydantic v2 para validación estricta de esquema y tipos.
   - Definición de campos (`coin_id`, `symbol`, `name`, `current_price`, `market_cap`, `total_volume`, `price_change_24h`, `fetched_at`).
   - Normalización de marcas de tiempo a UTC (`timezone.utc`).
3. **Decisiones de Diseño (ADRs)**:
   - **ADR-001**: Uso de `httpx.Client` síncrono para simplicidad y compatibilidad con Airflow.
   - **ADR-002**: Validación explícita de entradas vía Pydantic antes de cualquier transformación.

---

## Paso 4 — Commit y Push

```bash
git add docs/architecture.md docs/issue_5_architecture_extraction.md
git commit -m "docs: architecture for extraction layer and price models"
git push origin feature/issue-5-arch-extraction
```

---

## Paso 5 — Crear y mergear el PR en GitHub

```bash
gh pr create \
  --title "docs: Issue #5 — Arquitectura capa de extracción y modelos" \
  --body "Closes #5. Documenta la capa de extracción CoinGeckoExtractor, el modelo PriceRecord y las decisiones de diseño." \
  --base develop \
  --head feature/issue-5-arch-extraction
```

Obtener el número del PR generado `<N>` y ejecutar:

```bash
gh pr merge <N> --squash --delete-branch
```

Actualizar la rama local:

```bash
git checkout develop
git pull origin develop
```
