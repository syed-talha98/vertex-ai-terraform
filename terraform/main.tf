provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "pipeline_bucket" {
  name          = "${var.project_id}-vertex-demo-bucket"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "pipeline_spec" {
  name   = "pipeline.json"
  bucket = google_storage_bucket.pipeline_bucket.name
  source = "../pipeline.json"
}