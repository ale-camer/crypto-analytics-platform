# Issue #12: Terraform — BigQuery Tables (Partitioning & Clustering)

**Branch**: `feature/issue-12-terraform-bq-tables` (based on `develop`)  
**Objective**: Define the BigQuery table schema, partitioning, and clustering configurations in Terraform to optimize query performance and reduce storage costs.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-12-terraform-bq-tables
```

---

## Step 2 — Define the BigQuery Table in Terraform

File: `terraform/bigquery.tf`

Append a new `google_bigquery_table` resource to the file. This table will live inside the dataset created in the previous issue. 

We need to configure:
1. **Schema**: Matching our `PriceTransformer` output (including technical indicators).
2. **Time Partitioning**: By day, using the `fetched_at` timestamp.
3. **Clustering**: By `coin_id` for fast filtering.

Add the following to the bottom of the file:

```hcl
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
```

---

## Step 3 — Format and Validate Terraform code

Ensure the new Terraform configuration is valid:

```bash
cd terraform
terraform fmt
terraform init
terraform validate
cd ..
```

---

## Step 4 — Commit and Push

```bash
git add terraform/bigquery.tf docs/issue_12_terraform_bq_tables.md
git commit -m "feat: Terraform BigQuery table with partitioning and clustering"
git push origin feature/issue-12-terraform-bq-tables
```

---

## Step 5 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #12 — Terraform BigQuery tables" \
  --body "Introduces BigQuery table schema, partitioning (fetched_at), and clustering (coin_id)." \
  --base develop \
  --head feature/issue-12-terraform-bq-tables
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 12 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
