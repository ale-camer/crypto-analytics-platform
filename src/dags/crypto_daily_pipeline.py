import os
from datetime import datetime, timedelta

import polars as pl
from airflow.decorators import dag, task

# Import our custom modules
from src.extractors.coingecko import CoinGeckoExtractor
from src.loaders.bigquery_loader import BigQueryLoader

# Note: Ensure GCSLoader and BigQueryLoader are implemented in their respective modules.
# We will mock their imports here if they are not yet fully available, but assuming they are:
from src.loaders.gcs_loader import GCSLoader
from src.transformers.price_transformer import PriceTransformer

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
    schedule="0 0 * * *",  # Run daily at midnight UTC
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
