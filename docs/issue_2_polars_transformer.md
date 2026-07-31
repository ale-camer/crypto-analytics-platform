# Issue #2: Polars Transformer

**Branch**: `feature/issue-2-polars-transformer` (based on `develop`)
**Objective**: Implement a data transformer using Polars that takes a list of `PriceRecord`s and converts it into a clean and enriched `DataFrame`.

---

## Step 1 — Create the branch from develop

Since we are working on `develop`, make sure to be on that branch and updated before branching:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-2-polars-transformer
```

---

## Step 2 — Add dependencies to `pyproject.toml`

Open `pyproject.toml` and add `polars` to the `[project]` section:

```toml
[project]
# ... (keep previous content) ...
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "polars>=1.0",
]
```

Then, install the new dependency in the environment:

```bash
pip install -e ".[dev]"
```

**Verification**:
```bash
python -c "import polars; print('Polars OK')"
# → Polars OK
```

---

## Step 3 — Create the `PriceTransformer`

File: `src/transformers/price_transformer.py`

Create the `PriceTransformer` class with a `transform(self, records: list[PriceRecord]) -> pl.DataFrame` method.

The method must:
1. Convert the list of `PriceRecord` objects (Pydantic models) to dictionaries using `[r.model_dump() for r in records]`.
2. Create a Polars `pl.DataFrame` with those dictionaries.
3. (Optional/Recommended) Ensure correct data types in the DataFrame (e.g. `fetched_at` should be Datetime).

**Verification**:
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
# → Should print the Polars DataFrame showing 1 row with Bitcoin data.
```

---

## Step 4 — Write unit tests

File: `tests/unit/test_transformer.py`

Create tests that validate the behavior of `PriceTransformer`:
- `test_transform_creates_dataframe`: Verify that passing a valid list of `PriceRecord`s returns a `pl.DataFrame`.
- `test_transform_empty_list`: Verify how it behaves when passing an empty list `[]` (it should return an empty DataFrame with the correct schema or handle it without errors).

**Verification**:
```bash
pytest tests/unit/test_transformer.py -v
# → Tests should pass
```

---

## Step 5 — Lint and format

Ensure the code complies with the project standards:

```bash
ruff check src/transformers/ tests/unit/test_transformer.py --fix
ruff format src/transformers/ tests/unit/test_transformer.py
```

**Verification**:
```bash
ruff check src/ tests/
# → All checks passed.
```

---

## Step 6 — Commit and push

```bash
git add pyproject.toml src/transformers/price_transformer.py tests/unit/test_transformer.py docs/issue_2_polars_transformer.md
git commit -m "feat: Polars PriceTransformer for data processing"
git push origin feature/issue-2-polars-transformer
```

---

## Step 7 — Create the PR to develop

Remember that we now target `develop` as the base:

```bash
gh pr create \
  --title "feat: Issue #2 — Polars Transformer" \
  --body "Closes #2. Implements PriceTransformer using Polars to process lists of PriceRecord." \
  --base develop \
  --head feature/issue-2-polars-transformer
```

Once reviewed (and with green CI if any), merge it:

```bash
gh pr merge <N> --squash --delete-branch
```

And finally update your local `develop`:

```bash
git checkout develop
git pull origin develop
```
