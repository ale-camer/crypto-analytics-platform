from unittest.mock import MagicMock, patch

from src.loaders.gcs_loader import GCSLoader


@patch("src.loaders.gcs_loader.storage.Client")
@patch("src.loaders.gcs_loader.logger")
def test_gcs_loader_success(mock_logger, mock_storage_client):
    """Test that GCSLoader returns True and logs success when upload works."""
    # Setup mock
    mock_client_instance = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.return_value = mock_client_instance
    mock_client_instance.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    # Initialize loader and call method
    loader = GCSLoader(bucket_name="test-bucket", project_id="test-project")
    result = loader.load_json({"key": "value"}, "test.json")

    # Asserts
    assert result is True
    mock_blob.upload_from_string.assert_called_once()
    mock_logger.info.assert_called_once_with("Successfully uploaded test.json to test-bucket")


@patch("src.loaders.gcs_loader.storage.Client")
@patch("src.loaders.gcs_loader.logger")
def test_gcs_loader_resilient_failure(mock_logger, mock_storage_client):
    """Test that GCSLoader catches exceptions, logs error, and returns False without raising."""
    # Setup mock to raise an exception
    mock_storage_client.side_effect = Exception("Simulated GCP connection error")

    # Initialize loader and call method
    loader = GCSLoader(bucket_name="test-bucket", project_id="test-project")

    # This should not raise an exception, but return False
    result = loader.load_json({"key": "value"}, "test.json")

    assert result is False
    mock_logger.error.assert_called_once()
    assert (
        "Failed to upload to GCS bucket test-bucket: Simulated GCP connection error"
        in mock_logger.error.call_args[0][0]
    )


@patch("src.loaders.gcs_loader.logger")
def test_gcs_loader_json_serialization_error(mock_logger):
    """Test that GCSLoader gracefully handles JSON encoding errors."""
    loader = GCSLoader(bucket_name="test-bucket", project_id="test-project")

    # Set cannot be serialized by json.dumps
    invalid_data = {"key": set([1, 2, 3])}

    # Should catch TypeError from json.dumps and return False
    result = loader.load_json(invalid_data, "test.json")

    assert result is False
    mock_logger.error.assert_called_once()
    assert "Failed to upload to GCS bucket test-bucket:" in mock_logger.error.call_args[0][0]
