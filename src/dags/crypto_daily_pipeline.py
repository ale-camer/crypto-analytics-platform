import os
import logging
from datetime import datetime, timedelta, timezone

from airflow.decorators import dag, task
from src.extractors.coingecko import CoinGeckoExtractor
from src.transformers.price_transformer import PriceTransformer
from src.loaders.gcs_loader import GCSLoader
from src.loaders.bigquery_loader import BigQueryLoader

logger = logging.getLogger("airflow.task")

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple"]

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
    @task(task_id="extract_market_data")
    def extract_market_data() -> list[dict]:
        extractor = CoinGeckoExtractor()
        records = extractor.fetch(coins=COINS)
        logger.info(f"Extracted {len(records)} records from CoinGecko")
        return [r.model_dump(mode="json") for r in records]

    @task(task_id="load_raw_to_gcs")
    def load_raw_to_gcs(records: list[dict]):
        project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0887473308")
        bucket_name = os.getenv("DATA_LAKE_BUCKET", "gen-lang-client-0887473308-data-lake")
        prefix = os.getenv("DATA_LAKE_PREFIX", "p02/lakehouse")
        now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        blob_path = f"{prefix}/raw/{now_str}_prices.json"
        
        gcs_loader = GCSLoader(bucket_name=bucket_name, project_id=project_id)
        gcs_loader.load_json(records, blob_path)
        logger.info(f"Uploaded raw payload to GCS: {blob_path}")

    @task(task_id="transform_market_data")
    def transform_market_data(records: list[dict]) -> list[dict]:
        from src.models.price_record import PriceRecord
        parsed_records = [PriceRecord(**r) for r in records]
        transformer = PriceTransformer()
        transformed_df = transformer.transform(parsed_records)
        logger.info(f"Transformed DataFrame shape: {transformed_df.shape}")
        return transformed_df.to_dicts()

    @task(task_id="load_transformed_to_bigquery")
    def load_transformed_to_bigquery(transformed_dicts: list[dict]):
        import polars as pl
        project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0887473308")
        dataset_name = os.getenv("BQ_DATASET", "crypto_market_data")
        table_id = f"{project_id}.{dataset_name}.prices"
        
        df = pl.DataFrame(transformed_dicts)
        if "fetched_at" in df.columns:
            df = df.with_columns(pl.col("fetched_at").str.to_datetime())
            
        bq_loader = BigQueryLoader(project_id=project_id)
        bq_loader.load(df, table_id)
        logger.info(f"Loaded {len(df)} records into BigQuery table: {table_id}")

    # Orchestration graph
    raw_data = extract_market_data()
    raw_data >> load_raw_to_gcs(raw_data)
    transformed = transform_market_data(raw_data)
    transformed >> load_transformed_to_bigquery(transformed)

# Instantiate the DAG
dag_instance = crypto_pipeline()
