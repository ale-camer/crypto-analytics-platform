# Issue #1: Extractor CoinGecko + Modelos Pydantic

**Rama**: `feature/issue-1-coingecko-extractor`  
**Objetivo**: Implementar el cliente HTTP contra la API de CoinGecko y los modelos Pydantic que validan la respuesta.

---

## Paso 1 — Agregar dependencias al `pyproject.toml`

Abrir `pyproject.toml` y bajo `[project.dependencies]` agregar:

```toml
[project.dependencies]
httpx = ">=0.27"
pydantic = ">=2.0"
```

Luego instalar:

```bash
pip install -e ".[dev]"
```

**Verificación**:
```bash
python -c "import httpx, pydantic; print('OK')"
# → OK
```

---

## Paso 2 — Crear el modelo Pydantic `PriceRecord`

Archivo: `src/models/price_record.py`

El modelo debe representar un registro de precio de una crypto con los campos:
- `coin_id: str` — identificador de CoinGecko (ej: `"bitcoin"`)
- `symbol: str` — símbolo del activo (ej: `"btc"`)
- `name: str` — nombre legible
- `current_price: float` — precio actual en USD
- `market_cap: float`
- `total_volume: float`
- `price_change_24h: float | None` — puede ser nulo
- `fetched_at: datetime` — timestamp de extracción (UTC)

**Verificación**:
```bash
python -c "
from src.models.price_record import PriceRecord
from datetime import datetime, timezone
r = PriceRecord(coin_id='bitcoin', symbol='btc', name='Bitcoin',
                current_price=60000.0, market_cap=1e12,
                total_volume=5e10, price_change_24h=1.5,
                fetched_at=datetime.now(timezone.utc))
print(r.model_dump())
"
# → debe imprimir el dict con todos los campos
```

---

## Paso 3 — Crear el extractor `CoinGeckoExtractor`

Archivo: `src/extractors/coingecko.py`

La clase debe:
- Usar `httpx.Client` para hacer GET a `https://api.coingecko.com/api/v3/coins/markets`
- Aceptar parámetros: `vs_currency="usd"`, `ids: list[str]`
- Retornar una lista de `PriceRecord` validados por Pydantic
- Manejar errores HTTP con `response.raise_for_status()`

**Verificación** (requiere conexión a internet):
```bash
python -c "
from src.extractors.coingecko import CoinGeckoExtractor
ext = CoinGeckoExtractor()
records = ext.fetch(['bitcoin', 'ethereum'])
for r in records:
    print(r.coin_id, r.current_price)
"
# → bitcoin  <precio>
# → ethereum <precio>
```

---

## Paso 4 — Escribir los tests unitarios

Archivo: `tests/unit/test_extractor.py`

Tests con mock (sin llamadas reales a la API):
- `test_fetch_returns_price_records` — mock de `httpx`, verifica que retorna lista de `PriceRecord`
- `test_fetch_handles_null_price_change` — verifica que `price_change_24h=None` no rompe la validación
- `test_fetch_raises_on_http_error` — verifica que un 429/500 levanta excepción

**Verificación**:
```bash
pytest tests/unit/test_extractor.py -v
# → 3 passed
```

---

## Paso 5 — Lint y formato

```bash
ruff check src/extractors/ src/models/ tests/unit/test_extractor.py
ruff format src/extractors/ src/models/ tests/unit/test_extractor.py
```

**Verificación**:
```bash
ruff check src/ tests/
# → All checks passed.
```

---

## Paso 6 — Commit y push

```bash
git add pyproject.toml src/models/price_record.py src/extractors/coingecko.py tests/unit/test_extractor.py docs/issue_1_coingecko_extractor.md
git commit -m "feat: CoinGecko extractor and PriceRecord Pydantic model"
git push origin feature/issue-1-coingecko-extractor
```

**Verificación**:
```bash
git log --oneline -3
# → el commit aparece en el tope
```

---

## Paso 7 — Crear el PR y cerrar el issue

```bash
gh pr create \
  --title "feat: Issue #1 — CoinGecko extractor + modelos Pydantic" \
  --body "Closes #1. Implementa CoinGeckoExtractor con httpx y modelo PriceRecord con Pydantic v2." \
  --base main \
  --head feature/issue-1-coingecko-extractor

gh pr merge <N> --squash --delete-branch

git checkout main
git pull origin main
git branch -d feature/issue-1-coingecko-extractor
```

---

*P-02 Crypto Analytics Platform — Alejandro Camerlengo*
