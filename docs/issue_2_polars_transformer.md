# Issue #2: Transformer con Polars

**Rama**: `feature/issue-2-polars-transformer` (basada en `develop`)
**Objetivo**: Implementar un transformador de datos usando Polars que reciba una lista de `PriceRecord` y la convierta en un `DataFrame` limpio y enriquecido.

---

## Paso 1 — Crear la rama desde develop

Como trabajaremos sobre `develop`, asegúrate de estar en esa rama y actualizada antes de ramificar:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-2-polars-transformer
```

---

## Paso 2 — Agregar dependencias al `pyproject.toml`

Abrir `pyproject.toml` y agregar `polars` a la sección `[project]`:

```toml
[project]
# ... (mantener lo anterior) ...
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "polars>=1.0",
]
```

Luego, instalar la nueva dependencia en el entorno:

```bash
pip install -e ".[dev]"
```

**Verificación**:
```bash
python -c "import polars; print('Polars OK')"
# → Polars OK
```

---

## Paso 3 — Crear el transformador `PriceTransformer`

Archivo: `src/transformers/price_transformer.py`

Crea la clase `PriceTransformer` con un método `transform(self, records: list[PriceRecord]) -> pl.DataFrame`.

El método debe:
1. Convertir la lista de objetos `PriceRecord` (modelos Pydantic) a diccionarios usando `[r.model_dump() for r in records]`.
2. Crear un `pl.DataFrame` de Polars con esos diccionarios.
3. (Opcional/Recomendado) Asegurar que los tipos de datos en el DataFrame sean correctos (ej: que `fetched_at` sea Datetime).

**Verificación**:
```bash
python -c "
import polars as pl
from datetime import datetime, timezone
from src.models.price_record import PriceRecord
from src.transformers.price_transformer import PriceTransformer

r = PriceRecord(coin_id='bitcoin', symbol='btc', name='Bitcoin', current_price=60000.0, market_cap=1e12, total_volume=5e10, price_change_24h=1.5, fetched_at=datetime.now(timezone.utc))
df = PriceTransformer().transform([r])
print(df)
"
# → Debería imprimir el DataFrame de Polars mostrando 1 fila con los datos de Bitcoin.
```

---

## Paso 4 — Escribir los tests unitarios

Archivo: `tests/unit/test_transformer.py`

Crear tests que validen el comportamiento de `PriceTransformer`:
- `test_transform_creates_dataframe`: Verifica que si pasas una lista válida de `PriceRecord`, devuelve un `pl.DataFrame`.
- `test_transform_empty_list`: Verifica cómo se comporta al pasar una lista vacía `[]` (debería retornar un DataFrame vacío con el esquema correcto o manejarlo sin errores).

**Verificación**:
```bash
pytest tests/unit/test_transformer.py -v
# → Deberían pasar los tests
```

---

## Paso 5 — Lint y formato

Asegúrate de que el código cumple con los estándares del proyecto:

```bash
ruff check src/transformers/ tests/unit/test_transformer.py --fix
ruff format src/transformers/ tests/unit/test_transformer.py
```

**Verificación**:
```bash
ruff check src/ tests/
# → All checks passed.
```

---

## Paso 6 — Commit y push

```bash
git add pyproject.toml src/transformers/price_transformer.py tests/unit/test_transformer.py docs/issue_2_polars_transformer.md
git commit -m "feat: Polars PriceTransformer for data processing"
git push origin feature/issue-2-polars-transformer
```

---

## Paso 7 — Crear el PR hacia develop

Recuerda que ahora apuntamos a `develop` como base:

```bash
gh pr create \
  --title "feat: Issue #2 — Transformer con Polars" \
  --body "Closes #2. Implementa PriceTransformer usando Polars para procesar listas de PriceRecord." \
  --base develop \
  --head feature/issue-2-polars-transformer
```

Una vez revisado (y con CI en verde si hubiera), lo mergeas:

```bash
gh pr merge <N> --squash --delete-branch
```

Y finalmente actualizas tu `develop` local:

```bash
git checkout develop
git pull origin develop
```
