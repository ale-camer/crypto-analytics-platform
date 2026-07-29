# Issue #10: BigQuery Loader (WRITE_APPEND)

**Branch**: `feature/issue-10-bigquery-loader` (based on `develop`)  
**Objective**: Implement `BigQueryLoader` to load Polars DataFrames into Google Cloud BigQuery using the `WRITE_APPEND` strategy.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-10-bigquery-loader
```

---

## Step 2 — Add dependencies to `pyproject.toml`

Open `pyproject.toml` and add `google-cloud-bigquery` and `pyarrow` to the `dependencies` array:

```toml
[project]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "polars>=1.0",
    "google-cloud-bigquery>=3.0",
    "pyarrow>=14.0",
]
```

Install the new dependencies:
```bash
pip install -e ".[dev]"
```

---

## Step 3 — Create the `BigQueryLoader`

File: `src/loaders/bigquery_loader.py`

Create the class `BigQueryLoader`:
- It should use `google.cloud.bigquery.Client`.
- Implement a `load(self, df: pl.DataFrame, table_id: str)` method.
- The method must convert the Polars DataFrame to a PyArrow table using `df.to_arrow()`.
- Use a `LoadJobConfig` with `write_disposition="WRITE_APPEND"`.
- Execute `client.load_table_from_arrow(arrow_table, table_id, job_config=job_config)` and wait for the result.

---

## Step 4 — Write and Run unit tests

File: `tests/unit/test_loader.py`

Create tests that validate the behavior using `unittest.mock.patch` on the BigQuery Client:
- Verify that `load_table_from_arrow` is called with the correct `table_id` and the `WRITE_APPEND` configuration.
- Verify it handles empty DataFrames without crashing (or skips the API call entirely).

**Run the tests locally**:
```bash
pytest tests/unit/test_loader.py -v
```

---

## Step 5 — Lint and format

```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
```

---

## Step 6 — Commit and Push

```bash
git add pyproject.toml src/loaders/bigquery_loader.py tests/unit/test_loader.py docs/issue_10_bigquery_loader.md
git commit -m "feat: BigQueryLoader with WRITE_APPEND strategy"
git push origin feature/issue-10-bigquery-loader
```

---

## Step 7 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #10 — BigQuery loader" \
  --body "Implements BigQueryLoader using google-cloud-bigquery and pyarrow." \
  --base develop \
  --head feature/issue-10-bigquery-loader
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 10 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
