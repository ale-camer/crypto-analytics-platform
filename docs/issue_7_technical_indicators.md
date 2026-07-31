# Issue #7: Technical Indicators (RSI, MACD, Bollinger Bands)

**Branch**: `feature/issue-7-technical-indicators` (based on `develop`)  
**Objective**: Enhance `PriceTransformer` to calculate technical indicators (RSI, MACD, Bollinger Bands) using Polars expressions.

> **Note on Data Requirements**: Technical indicators require time-series data. This implementation assumes the input `pl.DataFrame` contains historical data sorted by time for each `coin_id`. If only one row per coin is provided (e.g., real-time snapshot), these calculations will naturally result in `null` values until enough historical data is accumulated.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-7-technical-indicators
```

---

## Step 2 — Update `PriceTransformer`

File: `src/transformers/price_transformer.py`

Update the `PriceTransformer` class to calculate indicators. You can use Polars built-in expressions (e.g., `ewm_mean` for Exponential Moving Average, `rolling_mean`, `rolling_std`).

The transformation should:
1. Ensure the DataFrame is sorted by `fetched_at`.
2. Group calculations by `coin_id` (using `pl.col("current_price").ewm_mean(...).over("coin_id")`).
3. Add the following columns:
   - `macd`: EMA(12) - EMA(26)
   - `macd_signal`: EMA(9) of the `macd`
   - `bb_upper` / `bb_lower`: Simple Moving Average (SMA 20) ± (2 * Rolling Standard Deviation 20)
   - `rsi_14`: Relative Strength Index (14 periods)

---

## Step 3 — Update Unit Tests

File: `tests/unit/test_transformer.py`

Add new tests to verify:
- The new indicator columns exist in the output schema.
- DataFrames with insufficient history (e.g., 1 row) handle the calculations gracefully by outputting `null` without crashing.

**Verification**:
```bash
pytest tests/unit/test_transformer.py -v
```

---

## Step 4 — Lint and Format

```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
```

---

## Step 5 — Commit, Push and PR

```bash
git add src/transformers/price_transformer.py tests/unit/test_transformer.py docs/issue_7_technical_indicators.md
git commit -m "feat: implement RSI, MACD and Bollinger Bands in PriceTransformer"
git push origin feature/issue-7-technical-indicators
```

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #7 — Technical Indicators" \
  --body "Closes #7. Adds RSI, MACD, and Bollinger Bands calculations using Polars." \
  --base develop \
  --head feature/issue-7-technical-indicators
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
