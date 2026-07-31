import polars as pl
from google.cloud import bigquery


class BigQueryLoader:
    def __init__(self, project_id: str | None = None):
        """
        Initializes the BigQuery client.
        If project_id is None, it will be inferred from the environment.
        """
        self.client = bigquery.Client(project=project_id)

    def load(self, df: pl.DataFrame, table_id: str) -> None:
        """
        Loads a Polars DataFrame into a BigQuery table using the WRITE_APPEND strategy.

        Args:
            df: The Polars DataFrame to load.
            table_id: The destination table ID (e.g., 'my_project.my_dataset.my_table').
        """
        if df.is_empty():
            return

        arrow_table = df.to_arrow()

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        job = self.client.load_table_from_arrow(arrow_table, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete
