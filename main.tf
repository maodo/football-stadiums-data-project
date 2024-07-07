terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.36.0"
    }
  }
}

provider "google" {
  project     = var.project_name
  region      = var.region
  credentials = file(var.credentials)
}

resource "google_storage_bucket" "football-bucket" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true
  storage_class = var.storage_class

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "football_dataset" {
  dataset_id = var.bq_dataset_id
  location   = var.location
}

resource "google_bigquery_table" "football_dataset" {
  dataset_id          = var.bq_dataset_id
  table_id            = "stadiums"
  deletion_protection = false
  schema              = <<EOF
    [
        {
            "name": "test",
            "type" : "STRING",
            "description" : "This is a test table"
        }
    ]
    EOF

}