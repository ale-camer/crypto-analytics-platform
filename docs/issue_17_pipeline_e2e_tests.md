# Issue #17: Integration tests — pipeline end-to-end

**Branch**: `feature/issue-17-pipeline-e2e-tests` (based on `develop`)  
**Objective**: Write an end-to-end integration test that executes the entire Airflow DAG using the `dag.test()` feature. This test verifies the complete flow: Extraction (CoinGecko) -> Transformation (Polars) -> Loading (GCS & BigQuery). As this touches real external services, it will conditionally skip if GCP credentials are not present in the environment (making it safe for standard CI).

Completing this issue officially finalizes our Airflow + BigQuery infrastructure milestone!

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-17-pipeline-e2e-tests
```

---

## Step 2 — Create the E2E Integration Test

File: `tests/integration/test_pipeline_e2e.py`

This test uses Airflow's built-in `dag.test()` method, which executes all tasks in the DAG synchronously in a single process. It is the perfect tool for local E2E testing.

```python
import os
import pytest
from airflow.models import DagBag

# Setup environment variables needed for the DAG parsing
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"
os.environ["AIRFLOW_HOME"] = "/tmp/airflow_test"
os.environ["AIRFLOW__DATABASE__SQL_ALCHEMY_CONN"] = "sqlite:////tmp/airflow_test.db"

# We must check if the real environment has GCP credentials
HAS_GCP_CREDS = bool(os.environ.get("GCP_PROJECT_ID"))


@pytest.fixture(scope="module")
def dagbag():
    """Fixture to load the DAGs from the src/dags folder."""
    return DagBag(dag_folder="src/dags", include_examples=False)


@pytest.mark.skipif(
    not HAS_GCP_CREDS,
    reason="Skipping E2E pipeline test because GCP_PROJECT_ID is not set in the environment.",
)
def test_crypto_pipeline_e2e(dagbag):
    """
    Executes the entire DAG synchronously end-to-end.
    This will actually hit CoinGecko, GCS, and BigQuery.
    """
    dag = dagbag.dags.get("crypto_daily_pipeline")
    assert dag is not None, "DAG crypto_daily_pipeline not found"

    # Airflow 2.5+ allows running the DAG in a single process for testing
    # We execute for a specific execution date
    try:
        dag.test()
    except Exception as e:
        pytest.fail(f"E2E Pipeline execution failed: {e}")
```

---

## Step 3 — Run the Integration Test

Run `pytest` to execute the E2E test. If your `.env` file doesn't have `GCP_PROJECT_ID`, it will safely skip.

```bash
pytest tests/integration/test_pipeline_e2e.py -v
```

---

## Step 4 — Lint, Commit and Push

```bash
ruff check tests/ --fix
ruff format tests/

git add tests/integration/test_pipeline_e2e.py docs/issue_17_pipeline_e2e_tests.md
git commit -m "test: add E2E integration test for the full crypto pipeline"
git push origin feature/issue-17-pipeline-e2e-tests
```

---

## Step 5 — Create PR, Merge and Close Issue #17

Create the PR to `develop`:
```bash
gh pr create \
  --title "test: Issue #17 — E2E pipeline integration tests" \
  --body "Introduces full synchronous execution of the DAG using dag.test() for E2E validation." \
  --base develop \
  --head feature/issue-17-pipeline-e2e-tests
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 17 --comment "Completed E2E testing."
```

---

## Step 6 — Milestone Release (develop -> main)

Since this concludes the Milestone (BigQuery & Airflow Integration), we must promote our stable `develop` branch to `main`.

```bash
git checkout develop
git pull origin develop

# Create Release PR
gh pr create \
  --title "chore: Release Milestone 2 (Airflow & BigQuery)" \
  --body "Promoting develop to main after successfully implementing the Airflow DAG, GCP loaders, and passing all integration/validation tests." \
  --base main \
  --head develop
```

Approve and merge the PR in GitHub, then update local `main`:
```bash
git checkout main
git pull origin main
git checkout develop
```
