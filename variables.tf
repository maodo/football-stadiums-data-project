variable "project_name" {
  description = "This is the name of the project"
  default     = "football-stadium-de"
}

variable "region" {
  description = "This is the name of the region"
  default     = "us-central1"
}

variable "location" {
  description = "This is the name of the location"
  default     = "US"
}

variable "bucket_name" {
  description = "This is the name of the bucket"
  default     = "maodo-bkt-football-bucket"
}

variable "storage_class" {
  description = "This is the name of the storage class"
  default     = "STANDARD"
}

variable "credentials" {
  description = "This is the path to the credentials"
  default     = "./keys/football-gcp-credentials.json"
}

variable "bq_dataset_id" {
  description = "The dataset id"
  default     = "footbal_stadium_dataset"
}
