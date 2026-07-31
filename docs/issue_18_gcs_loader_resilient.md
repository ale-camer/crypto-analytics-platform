# Issue #18: GCS loader resiliente (never raises)

**Branch**: `feature/issue-18-gcs-loader-resilient` (based on `develop`)  
**Objective**: Implement the `GCSLoader` class so that it acts as a resilient fallback archive. If the upload to Google Cloud Storage fails for *any* reason (missing credentials, network failure, bucket not found), it should catch the exception, log the error clearly, and exit gracefully returning `False`. It must **never** raise an exception that causes the Airflow task (and the DAG) to crash. The main pipeline logic must continue unharmed.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-18-gcs-loader-resilient
```

---

## Step 2 — Implement the Resilient GCSLoader

File: `src/loaders/gcs_loader.py`

Write the `GCSLoader` class using the `google-cloud-storage` library. Wrap the `upload_from_string` logic in a broad `try-except Exception` block. 

```python
import json
import logging
from typing import Any

from google.cloud import storage

logger = logging.getLogger(__name__)


class GCSLoader:
    def __init__(self, bucket_name: str, project_id: str = None):
        self.bucket_name = bucket_name
        self.project_id = project_id

    def load_json(self, data: Any, destination_blob_name: str) -> bool:
        """
        Loads a Python object as JSON to GCS.
        Returns True if successful, False if it fails. NEVER raises an exception.
        """
        try:
            client = storage.Client(project=self.project_id)
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            json_data = json.dumps(data)
            blob.upload_from_string(json_data, content_type="application/json")
            
            logger.info(f"Successfully uploaded {destination_blob_name} to {self.bucket_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload to GCS bucket {self.bucket_name}: {str(e)}")
            return False
```

Add the dependency to `pyproject.toml` (if not already there):
```toml
"google-cloud-storage>=2.0.0",
```

---

## Step 3 — Create Unit Tests

File: `tests/unit/test_gcs_loader.py`

Write tests using `unittest.mock.patch` to verify:
1. `load_json` returns `True` when upload is successful.
2. `load_json` returns `False` and does **not** raise an exception when `storage.Client` or `upload_from_string` raises an exception.

---

## Step 4 — Format, Lint, and Run Tests

```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
pytest tests/unit/test_gcs_loader.py -v
```

---

## Step 5 — Commit and Push

```bash
git add src/loaders/gcs_loader.py tests/unit/test_gcs_loader.py pyproject.toml docs/issue_18_gcs_loader_resilient.md
git commit -m "feat: implement resilient GCSLoader that never raises exceptions"
git push origin feature/issue-18-gcs-loader-resilient
```

---

## Step 6 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #18 — Resilient GCS Loader" \
  --body "Implements GCSLoader with a try-except block so raw data archive failures don't crash the pipeline." \
  --base develop \
  --head feature/issue-18-gcs-loader-resilient
```

Merge it and clean up:
```bash
gh pr merge <N> --squash --delete-branch
gh issue close 18 --comment "GCS Loader is now resilient"
git checkout develop
git pull origin develop
```
