import os

import pytest

# Set up test environment variables for Airflow BEFORE importing DagBag
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"
os.environ["AIRFLOW_HOME"] = "/tmp/airflow_test"
os.environ["AIRFLOW__DATABASE__SQL_ALCHEMY_CONN"] = "sqlite:////tmp/airflow_test.db"

from airflow.models import DagBag


@pytest.fixture(scope="module")
def dagbag():
    return DagBag(dag_folder="src/dags")


def test_dag_loaded_without_errors(dagbag):
    """Verify that the DAG parses correctly without any import errors."""
    assert len(dagbag.import_errors) == 0, f"DAG import errors: {dagbag.import_errors}"
    assert "crypto_daily_pipeline" in dagbag.dags


def test_dag_topology(dagbag):
    """Verify that the DAG has the exact expected tasks."""
    dag = dagbag.dags["crypto_daily_pipeline"]
    expected_tasks = {
        "extract_market_data",
        "load_raw_to_gcs",
        "transform_market_data",
        "load_transformed_to_bigquery",
    }

    actual_tasks = set(dag.task_dict.keys())
    assert actual_tasks == expected_tasks, f"Expected tasks {expected_tasks} but got {actual_tasks}"


def test_task_dependencies(dagbag):
    """Verify the execution order and dependencies of the tasks."""
    dag = dagbag.dags["crypto_daily_pipeline"]

    extract_task = dag.get_task("extract_market_data")
    load_gcs_task = dag.get_task("load_raw_to_gcs")
    transform_task = dag.get_task("transform_market_data")
    load_bq_task = dag.get_task("load_transformed_to_bigquery")

    # Check extract_task downstream
    assert load_gcs_task.task_id in extract_task.downstream_task_ids
    assert transform_task.task_id in extract_task.downstream_task_ids

    # Check transform_task downstream
    assert load_bq_task.task_id in transform_task.downstream_task_ids

    # Verify load_bq has no downstream tasks (it is a leaf node)
    assert len(load_bq_task.downstream_task_ids) == 0


def test_dag_configuration(dagbag):
    """Verify DAG scheduling and catchup behavior."""
    dag = dagbag.dags["crypto_daily_pipeline"]

    assert dag.catchup is False
    assert dag.schedule == "0 0 * * *"
