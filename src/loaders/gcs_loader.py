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
