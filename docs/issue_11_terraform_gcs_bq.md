# Issue #11: Terraform — GCS Bucket + BigQuery Dataset

**Branch**: `feature/issue-11-terraform-gcs-bq` (based on `develop`)  
**Objective**: Implement the baseline Infrastructure-as-Code (IaC) using Terraform to provision a Google Cloud Storage (GCS) bucket and a BigQuery dataset.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-11-terraform-gcs-bq
```

---

## Step 2 — Create Terraform files

Create a new directory named `terraform/` at the root of the project, and add the following files:

1. **`terraform/variables.tf`**:
   - Define variables for `project_id`, `region` (e.g., `us-central1`), and `credentials_path`.

2. **`terraform/main.tf`**:
   - Configure the `google` provider utilizing the variables from `variables.tf`.

3. **`terraform/storage.tf`**:
   - Define a `google_storage_bucket` resource for archiving raw crypto data (e.g., `crypto-analytics-raw-archive`).
   - Configure it with `location` and `uniform_bucket_level_access = true`.

4. **`terraform/bigquery.tf`**:
   - Define a `google_bigquery_dataset` resource (e.g., `crypto_market_data`) to act as the container for future tables.

---

## Step 3 — Format and Validate Terraform code

Ensure the Terraform code is well-formatted and valid:

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
git add terraform/ docs/issue_11_terraform_gcs_bq.md
git commit -m "feat: Terraform config for GCS bucket and BigQuery dataset"
git push origin feature/issue-11-terraform-gcs-bq
```

---

## Step 5 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "feat: Issue #11 — Terraform GCS and BQ Dataset" \
  --body "Introduces Terraform baseline infrastructure for GCP." \
  --base develop \
  --head feature/issue-11-terraform-gcs-bq
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 11 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
