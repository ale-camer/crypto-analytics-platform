import os

import polars as pl
import pytest

from src.loaders.bigquery_loader import BigQueryLoader


# Skip this test in CI environments where GCP credentials are not injected
@pytest.mark.skipif(
    "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ,
    reason="Requires GCP credentials to run integration tests",
)
def test_bigquery_loader_integration():
    """
    Integration test for BigQueryLoader.
    Requires a valid test table in the GCP project.
    """
    project_id = os.environ.get("GCP_PROJECT_ID", "test-project-id")
    dataset_id = "crypto_market_data"
    table_id = "prices_test"  # Use a dedicated test table

    loader = BigQueryLoader(project_id=project_id)

    # Create a small dummy dataframe
    df = pl.DataFrame(
        {
            "coin_id": ["integration-test-coin"],
            "symbol": ["itc"],
            "name": ["Integration Test Coin"],
            "current_price": [1.0],
            "market_cap": [100.0],
            "total_volume": [10.0],
            "price_change_24h": [0.0],
            "fetched_at": ["2026-01-01T00:00:00Z"],
            "macd": [0.0],
            "macd_signal": [0.0],
            "bb_upper": [0.0],
            "bb_lower": [0.0],
            "rsi_14": [0.0],
        }
    )

    # Cast fetched_at to proper timestamp
    df = df.with_columns(pl.col("fetched_at").str.to_datetime())

    # Attempt to load (will raise an exception if schema/connection fails)
    full_table_path = f"{project_id}.{dataset_id}.{table_id}"
    try:
        loader.load(df, full_table_path)
    except Exception as e:
        pytest.fail(f"Integration test failed with error: {e}")
