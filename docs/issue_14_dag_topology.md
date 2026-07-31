# Issue #14: DAG crypto_daily_pipeline — Topology and Structure

**Branch**: `feature/issue-14-dag-topology` (based on `develop`)  
**Objective**: Establish the basic topology and structure of the main Airflow DAG (`crypto_daily_pipeline`) using dummy operators. Actual task implementations (passing data via XCom) will be handled in Issue #15.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-14-dag-topology
```

---

## Step 2 — Add Airflow Dependency

File: `pyproject.toml`

Add `apache-airflow` to the `dependencies` array so we can use Airflow's classes:

```toml
[project]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "polars>=1.0",
    "google-cloud-bigquery>=3.0",
    "pyarrow>=14.0",
    "apache-airflow>=2.9.0"
]
```

Install it:
```bash
pip install -e ".[dev]"
```

---

## Step 3 — Create the DAG Skeleton

File: `src/dags/crypto_daily_pipeline.py`

Create a new directory `src/dags/` and add the DAG file. We will use the TaskFlow API (`@dag`) and `EmptyOperator` to outline the pipeline's topology (Extract -> Transform -> Load).

```python
from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="crypto_daily_pipeline",
    default_args=default_args,
    description="Extracts, transforms, and loads crypto market data daily.",
    schedule_interval="0 0 * * *",  # Run daily at midnight UTC
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["crypto", "daily", "etl"],
)
def crypto_pipeline():
    # Define topology using EmptyOperators for now
    extract_task = EmptyOperator(task_id="extract_market_data")
    transform_task = EmptyOperator(task_id="transform_market_data")
    load_gcs_raw_task = EmptyOperator(task_id="load_raw_to_gcs")
    load_bq_task = EmptyOperator(task_id="load_transformed_to_bigquery")

    # Set dependencies (Topology)
    extract_task >> load_gcs_raw_task
    extract_task >> transform_task >> load_bq_task

# Instantiate the DAG
dag_instance = crypto_pipeline()
```

---

## Step 4 — Lint and Format

```bash
ruff check src/ --fix
ruff format src/
```

---

## Step 5 — Commit and Push

```bash
git add pyproject.toml src/dags/ docs/issue_14_dag_topology.md
git commit -m "feat: Airflow DAG structure and topology"
git push origin feature/issue-14-dag-topology
```

---

## Step 6 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #14 — DAG topology" \
  --body "Introduces basic Airflow DAG structure with EmptyOperators." \
  --base develop \
  --head feature/issue-14-dag-topology
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 14 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
