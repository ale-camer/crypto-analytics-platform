# Issue #13: Integration Tests — BigQuery Loader

**Branch**: `feature/issue-13-test-bq-integration` (based on `develop`)  
**Objective**: Implement integration tests for `BigQueryLoader` to verify that the DataFrame is correctly transformed and dispatched to the GCP BigQuery API. This issue concludes the current Milestone, culminating in a release PR to `main`.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-13-test-bq-integration
```

---

## Step 2 — Create the Integration Test

File: `tests/integration/test_bigquery_loader.py`

Create a new directory `tests/integration/` if it doesn't exist. 
In this test, we will verify the end-to-end functionality. Since running real GCP API calls in CI without credentials will fail, we will use `pytest.mark.skipif` to only run the test if `GOOGLE_APPLICATION_CREDENTIALS` is present in the environment.

```python
import os
import pytest
import polars as pl
from src.loaders.bigquery_loader import BigQueryLoader

# Skip this test in CI environments where GCP credentials are not injected
@pytest.mark.skipif(
    "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ,
    reason="Requires GCP credentials to run integration tests"
)
def test_bigquery_loader_integration():
    """
    Integration test for BigQueryLoader.
    Requires a valid test table in the GCP project.
    """
    project_id = os.environ.get("GCP_PROJECT_ID", "test-project-id")
    dataset_id = "crypto_market_data"
    table_id = "prices_test"  # Use a dedicated test table
    
    loader = BigQueryLoader(project_id=project_id)
    
    # Create a small dummy dataframe
    df = pl.DataFrame({
        "coin_id": ["integration-test-coin"],
        "symbol": ["itc"],
        "name": ["Integration Test Coin"],
        "current_price": [1.0],
        "market_cap": [100.0],
        "total_volume": [10.0],
        "price_change_24h": [0.0],
        "fetched_at": ["2026-01-01T00:00:00Z"],
        "macd": [0.0],
        "macd_signal": [0.0],
        "bb_upper": [0.0],
        "bb_lower": [0.0],
        "rsi_14": [0.0]
    })
    
    # Cast fetched_at to proper timestamp
    df = df.with_columns(pl.col("fetched_at").str.to_datetime())
    
    # Attempt to load (will raise an exception if schema/connection fails)
    full_table_path = f"{project_id}.{dataset_id}.{table_id}"
    try:
        loader.load(df, full_table_path)
    except Exception as e:
        pytest.fail(f"Integration test failed with error: {e}")
```

---

## Step 3 — Run the tests

Run the test suite to ensure the new file is collected:
```bash
pytest tests/ -v
```

*(Note: If you don't have GCP credentials exported locally, this test will explicitly show as `SKIPPED`, which is the intended safe behavior).*

---

## Step 4 — Lint, Commit and Push

```bash
ruff check src/ tests/ --fix
ruff format src/ tests/

git add tests/integration/ docs/issue_13_test_bq_integration.md
git commit -m "test: integration tests for BigQuery loader"
git push origin feature/issue-13-test-bq-integration
```

---

## Step 5 — Create PR, Merge and Close Issue #13

Create the PR to `develop`:
```bash
gh pr create \
  --title "test: Issue #13 — Integration tests BQ loader" \
  --body "Introduces BigQuery loader integration tests." \
  --base develop \
  --head feature/issue-13-test-bq-integration
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 13 --comment "Completed and integrated in develop"
```

---

## Step 6 — Release Milestone (Merge `develop` to `main`)

With the loading and infrastructure layer finished and tested, this milestone is complete! Open a Release PR to `main`:

```bash
git checkout develop
git pull origin develop

# Create a PR from develop to main
gh pr create \
  --title "chore(release): Milestone Completion (Data Loading & IaC)" \
  --body "Merges the completed features (Issue #7 to #13) into production." \
  --base main \
  --head develop
```

Once merged, your `main` branch will be fully updated with the production-ready code.
