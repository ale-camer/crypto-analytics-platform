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
    # Note: Removed include_examples=False to be compatible with Airflow 3.x
    return DagBag(dag_folder="src/dags")


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
