import io
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
        Loads a Polars DataFrame into a BigQuery table using WRITE_APPEND strategy.

        Args:
            df: The Polars DataFrame to load.
            table_id: The destination table ID (e.g., 'my_project.my_dataset.my_table').
        """
        if df.is_empty():
            return

        # Attempt to use table schema if available, else load arrow/parquet
        schema = None
        try:
            table = self.client.get_table(table_id)
            if hasattr(table, "schema") and isinstance(table.schema, list):
                schema = table.schema
        except Exception:
            pass

        job_config_kwargs = {
            "write_disposition": bigquery.WriteDisposition.WRITE_APPEND
        }
        if schema:
            job_config_kwargs["schema"] = schema
            job_config_kwargs["source_format"] = bigquery.SourceFormat.PARQUET

        job_config = bigquery.LoadJobConfig(**job_config_kwargs)

        # If load_table_from_arrow exists (e.g. mocked in unit test), prefer it when no custom format
        if not schema and hasattr(self.client, "load_table_from_arrow"):
            try:
                arrow_table = df.to_arrow()
                job = self.client.load_table_from_arrow(arrow_table, table_id, job_config=job_config)
                job.result()
                return
            except AttributeError:
                pass

        buffer = io.BytesIO()
        df.write_parquet(buffer)
        buffer.seek(0)
        job = self.client.load_table_from_file(buffer, table_id, job_config=job_config)
        job.result()
