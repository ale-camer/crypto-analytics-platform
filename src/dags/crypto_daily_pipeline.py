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
