# Issue #15: DAG tasks — BigQuery & GCS loading via XCom

**Branch**: `feature/issue-15-dag-xcom-tasks` (based on `develop`)  
**Objective**: Replace the `EmptyOperator` placeholders in our Airflow DAG with actual execution logic using the TaskFlow API (`@task`). We will integrate our existing modular components (`CoinGeckoExtractor`, `PriceTransformer`, `GCSLoader`, `BigQueryLoader`) and use XCom to pass data between them.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-15-dag-xcom-tasks
```

---

## Step 2 — Implement TaskFlow Logic

File: `src/dags/crypto_daily_pipeline.py`

Modify the DAG file to use `@task` decorators instead of `EmptyOperator`. The TaskFlow API automatically handles XCom serialization/deserialization for the returned values.

Replace the contents of `src/dags/crypto_daily_pipeline.py` with:

```python
import os
from datetime import datetime, timedelta

import polars as pl
from airflow.decorators import dag, task

# Import our custom modules
from src.extractors.coingecko import CoinGeckoExtractor
from src.transformers.price_transformer import PriceTransformer
# Note: Ensure GCSLoader and BigQueryLoader are implemented in their respective modules.
# We will mock their imports here if they are not yet fully available, but assuming they are:
from src.loaders.gcs_loader import GCSLoader
from src.loaders.bigquery_loader import BigQueryLoader

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
    schedule_interval="0 0 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["crypto", "daily", "etl"],
)
def crypto_pipeline():
    
    @task
    def extract_market_data():
        """Extracts data and passes it to downstream tasks via XCom."""
        # For a production app, we would pass a list of coins to extract
        extractor = CoinGeckoExtractor()
        # Mocking the extraction call for simplicity in this example
        raw_data = extractor.extract(coin_ids=["bitcoin", "ethereum"])
        return raw_data

    @task
    def load_raw_to_gcs(raw_data: list[dict]):
        """Saves the raw JSON payload to a GCS bucket."""
        project_id = os.environ.get("GCP_PROJECT_ID")
        bucket_name = f"{project_id}-crypto-raw-archive"
        loader = GCSLoader(bucket_name=bucket_name)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"raw_market_data_{timestamp}.json"
        
        # Ensure your GCSLoader has a method to load raw python objects/dicts
        loader.load_json(raw_data, destination_blob_name=blob_name)

    @task
    def transform_market_data(raw_data: list[dict]):
        """Transforms raw dicts into technical indicators using Polars."""
        transformer = PriceTransformer()
        df = transformer.transform(raw_data)
        
        # Return as list of dicts so Airflow XCom can serialize it easily
        return df.to_dicts()

    @task
    def load_transformed_to_bigquery(transformed_data: list[dict]):
        """Loads the processed data into the BigQuery table."""
        df = pl.DataFrame(transformed_data)
        
        project_id = os.environ.get("GCP_PROJECT_ID")
        dataset_id = "crypto_market_data"
        table_id = "prices"
        full_table_path = f"{project_id}.{dataset_id}.{table_id}"
        
        loader = BigQueryLoader(project_id=project_id)
        loader.load(df, full_table_path)

    # --- Topología del DAG ---
    # TaskFlow automatically sets dependencies based on function arguments
    raw_data = extract_market_data()
    
    # Branch 1: Save raw data to GCS
    load_raw_to_gcs(raw_data)
    
    # Branch 2: Transform and then save to BigQuery
    transformed_data = transform_market_data(raw_data)
    load_transformed_to_bigquery(transformed_data)


# Instantiate the DAG
dag_instance = crypto_pipeline()
```

---

## Step 3 — Format and Lint

Make sure imports and formatting are correct:
```bash
ruff check src/ --fix
ruff format src/
```

---

## Step 4 — Commit and Push

```bash
git add src/dags/crypto_daily_pipeline.py docs/issue_15_dag_xcom_tasks.md
git commit -m "feat: implement DAG logic using TaskFlow and XCom"
git push origin feature/issue-15-dag-xcom-tasks
```

---

## Step 5 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #15 — DAG tasks with XCom" \
  --body "Integrates extractor, transformer, and loaders into the DAG via TaskFlow XCom." \
  --base develop \
  --head feature/issue-15-dag-xcom-tasks
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 15 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
