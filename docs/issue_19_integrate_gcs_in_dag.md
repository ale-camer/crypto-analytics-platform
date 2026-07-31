# Issue #19: Integrar GCS loader en DAG

**Branch**: `feature/issue-19-integrate-gcs-in-dag` (based on `develop`)  
**Objective**: Now that the resilient `GCSLoader` is fully implemented (Issue #18), we need to properly integrate its final form into the Airflow DAG. Although we had a placeholder task for it, we must now ensure it correctly passes the `project_id`, handles the boolean return value of `load_json` (True/False), and logs appropriately within the Airflow context if the resilient upload fails.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-19-integrate-gcs-in-dag
```

---

## Step 2 — Refine the DAG Task

File: `src/dags/crypto_daily_pipeline.py`

Update the `load_raw_to_gcs` task to properly instantiate the loader and handle its resilient response.

```python
# Modificar la tarea en src/dags/crypto_daily_pipeline.py
    @task
    def load_raw_to_gcs(raw_data: list[dict]):
        """Saves the raw JSON payload to a GCS bucket."""
        import logging
        logger = logging.getLogger("airflow.task")

        project_id = os.environ.get("GCP_PROJECT_ID")
        bucket_name = f"{project_id}-crypto-raw-archive"
        
        # Instantiate with both required arguments
        loader = GCSLoader(bucket_name=bucket_name, project_id=project_id)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"raw_market_data_{timestamp}.json"
        
        success = loader.load_json(raw_data, destination_blob_name=blob_name)
        
        if not success:
            logger.warning(
                "GCS Archive upload failed (resilient fallback triggered). "
                "The pipeline will continue with the BigQuery load."
            )
        else:
            logger.info("Successfully archived raw data to GCS.")
```

---

## Step 3 — Validate the DAG

Run the validation tests to ensure we haven't broken the topology or Airflow compilation:

```bash
pytest tests/unit/test_dag_validation.py -v
```

---

## Step 4 — Format, Lint, and Commit

```bash
ruff check src/ --fix
ruff format src/

git add src/dags/crypto_daily_pipeline.py docs/issue_19_integrate_gcs_in_dag.md
git commit -m "feat: properly integrate resilient GCSLoader into the DAG"
git push origin feature/issue-19-integrate-gcs-in-dag
```

---

## Step 5 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #19 — Integrate GCS Loader in DAG" \
  --body "Updates the DAG task to handle the resilient boolean response from GCSLoader." \
  --base develop \
  --head feature/issue-19-integrate-gcs-in-dag
```

Merge it and clean up:
```bash
gh pr merge <N> --squash --delete-branch
gh issue close 19 --comment "GCS Loader properly integrated and logging correctly in the DAG."
git checkout develop
git pull origin develop
```
