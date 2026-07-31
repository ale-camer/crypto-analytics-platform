# Issue #1: CoinGecko Extractor + Pydantic Models

**Branch**: `feature/issue-1-coingecko-extractor`  
**Objective**: Implement the HTTP client against the CoinGecko API and the Pydantic models to validate the response.

---

## Step 1 — Add dependencies to `pyproject.toml`

Open `pyproject.toml` and under `[project.dependencies]` add:

```toml
[project]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
]
```

Then install:

```bash
pip install -e ".[dev]"
```

**Verification**:
```bash
python -c "import httpx, pydantic; print('OK')"
# → OK
```

---

## Step 2 — Create the Pydantic model `PriceRecord`

File: `src/models/price_record.py`

The model must represent a crypto price record with the fields:
- `coin_id: str` — CoinGecko identifier (e.g. `"bitcoin"`)
- `symbol: str` — asset ticker (e.g. `"btc"`)
- `name: str` — human-readable name
- `current_price: float` — current price in USD
- `market_cap: float`
- `total_volume: float`
- `price_change_24h: float | None` — can be null
- `fetched_at: datetime` — extraction timestamp (UTC)

**Verification**:
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
# → should print the dict with all fields
```

---

## Step 3 — Create the extractor `CoinGeckoExtractor`

File: `src/extractors/coingecko.py`

The class must:
- Use `httpx.Client` to perform GET requests to `https://api.coingecko.com/api/v3/coins/markets`
- Accept parameters: `vs_currency="usd"`, `ids: list[str]`
- Return a list of `PriceRecord` objects validated by Pydantic
- Handle HTTP errors with `response.raise_for_status()`

**Verification** (requires internet connection):
```bash
python -c "
from src.extractors.coingecko import CoinGeckoExtractor
ext = CoinGeckoExtractor()
records = ext.fetch(['bitcoin', 'ethereum'])
for r in records:
    print(r.coin_id, r.current_price)
"
# → bitcoin  <price>
# → ethereum <price>
```

---

## Step 4 — Write unit tests

File: `tests/unit/test_extractor.py`

Mocked tests (without real API calls):
- `test_fetch_returns_price_records` — mocks `httpx`, verifies it returns a list of `PriceRecord`
- `test_fetch_handles_null_price_change` — verifies `price_change_24h=None` doesn't break validation
- `test_fetch_raises_on_http_error` — verifies a 429/500 raises an exception

**Verification**:
```bash
pytest tests/unit/test_extractor.py -v
# → 3 passed
```

---

## Step 5 — Lint and format

```bash
ruff check src/extractors/ src/models/ tests/unit/test_extractor.py
ruff format src/extractors/ src/models/ tests/unit/test_extractor.py
```

**Verification**:
```bash
ruff check src/ tests/
# → All checks passed.
```

---

## Step 6 — Commit and push

```bash
git add pyproject.toml src/models/price_record.py src/extractors/coingecko.py tests/unit/test_extractor.py docs/issue_1_coingecko_extractor.md
git commit -m "feat: CoinGecko extractor and PriceRecord Pydantic model"
git push origin feature/issue-1-coingecko-extractor
```

---

## Step 7 — Create PR and close the issue

```bash
gh pr create \
  --title "feat: Issue #1 — CoinGecko extractor + Pydantic models" \
  --body "Closes #1. Implements CoinGeckoExtractor with httpx and PriceRecord model with Pydantic v2." \
  --base main \
  --head feature/issue-1-coingecko-extractor

gh pr merge <N> --squash --delete-branch

git checkout main
git pull origin main
git branch -d feature/issue-1-coingecko-extractor
```

---

*P-02 Crypto Analytics Platform — Alejandro Camerlengo*
