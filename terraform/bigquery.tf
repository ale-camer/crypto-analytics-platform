resource "google_bigquery_dataset" "crypto_market_data" {
  dataset_id  = "crypto_market_data"
  project     = var.project_id
  location    = var.region
  description = "Dataset for Cryptocurrency Analytics Platform"
}
