resource "google_storage_bucket" "raw_archive" {
  name                        = "${var.project_id}-crypto-raw-archive"
  location                    = var.region
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  force_destroy               = false

  public_access_prevention = "enforced"
}
