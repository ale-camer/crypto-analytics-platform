import os
import logging
from datetime import datetime, timezone
from src.extractors.coingecko import CoinGeckoExtractor
from src.transformers.price_transformer import PriceTransformer
from src.loaders.gcs_loader import GCSLoader
from src.loaders.bigquery_loader import BigQueryLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("crypto_pipeline")

def run_pipeline():
    project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0887473308")
    bucket_name = os.getenv("DATA_LAKE_BUCKET", "gen-lang-client-0887473308-data-lake")
    dataset_name = os.getenv("BQ_DATASET", "crypto_market_data")
    prefix = os.getenv("DATA_LAKE_PREFIX", "p02/lakehouse")
    coins = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple"]

    logger.info(f"Starting crypto ETL pipeline for coins: {coins}")

    # 1. Extract from CoinGecko
    extractor = CoinGeckoExtractor()
    records = extractor.fetch(coins=coins)
    logger.info(f"Extracted {len(records)} price records from CoinGecko")

    # 2. Archive raw data to GCS Data Lake
    now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw_payload = [r.model_dump(mode="json") for r in records]
    blob_path = f"{prefix}/raw/{now_str}_prices.json"
    gcs_loader = GCSLoader(bucket_name=bucket_name, project_id=project_id)
    gcs_loader.load_json(raw_payload, blob_path)

    # 3. Transform with Polars (technical indicators: MACD, Bollinger Bands, RSI)
    transformer = PriceTransformer()
    transformed_df = transformer.transform(records)
    logger.info(f"Transformed DataFrame shape: {transformed_df.shape}")

    # 4. Load transformed metrics into BigQuery
    bq_loader = BigQueryLoader(project_id=project_id)
    table_id = f"{project_id}.{dataset_name}.prices"
    bq_loader.load(transformed_df, table_id)
    logger.info(f"Successfully loaded {len(transformed_df)} records into BigQuery table: {table_id}")

if __name__ == "__main__":
    run_pipeline()
