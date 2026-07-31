from unittest.mock import MagicMock, patch

import polars as pl
from google.cloud import bigquery

from src.loaders.bigquery_loader import BigQueryLoader


@patch("src.loaders.bigquery_loader.bigquery.Client")
def test_bigquery_loader_success(mock_client_class):
    # Setup mock
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    # Create test data
    df = pl.DataFrame({"coin_id": ["bitcoin"], "current_price": [60000.0]})

    loader = BigQueryLoader(project_id="test-project")
    loader.load(df, "test-dataset.test-table")

    # Verify client initialization
    mock_client_class.assert_called_once_with(project="test-project")

    # Verify load_table_from_arrow was called correctly
    mock_client.load_table_from_arrow.assert_called_once()

    args, kwargs = mock_client.load_table_from_arrow.call_args
    # args[0] is the arrow table, args[1] is the table_id
    assert args[1] == "test-dataset.test-table"

    job_config = kwargs.get("job_config")
    assert job_config is not None
    assert job_config.write_disposition == bigquery.WriteDisposition.WRITE_APPEND


@patch("src.loaders.bigquery_loader.bigquery.Client")
def test_bigquery_loader_empty_df(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    df = pl.DataFrame(schema={"coin_id": pl.String, "current_price": pl.Float64})

    loader = BigQueryLoader(project_id="test-project")
    loader.load(df, "test-dataset.test-table")

    # Should not attempt to load an empty dataframe
    mock_client.load_table_from_arrow.assert_not_called()
