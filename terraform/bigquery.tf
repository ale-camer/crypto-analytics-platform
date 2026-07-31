resource "google_bigquery_dataset" "crypto_market_data" {
  dataset_id  = "crypto_market_data"
  project     = var.project_id
  location    = var.region
  description = "Dataset for Cryptocurrency Analytics Platform"
}

resource "google_bigquery_table" "crypto_prices" {
  dataset_id = google_bigquery_dataset.crypto_market_data.dataset_id
  table_id   = "prices"
  project    = var.project_id

  time_partitioning {
    type  = "DAY"
    field = "fetched_at"
  }

  clustering = ["coin_id"]

  schema = <<EOF
[
  {"name": "coin_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "symbol", "type": "STRING", "mode": "REQUIRED"},
  {"name": "name", "type": "STRING", "mode": "REQUIRED"},
  {"name": "current_price", "type": "FLOAT", "mode": "REQUIRED"},
  {"name": "market_cap", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "total_volume", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "price_change_24h", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "fetched_at", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "macd", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "macd_signal", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "bb_upper", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "bb_lower", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rsi_14", "type": "FLOAT", "mode": "NULLABLE"}
]
EOF
}
