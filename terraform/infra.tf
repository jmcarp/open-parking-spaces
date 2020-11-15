terraform {
  backend "gcs" {
    bucket = "open-parking-spaces-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  region  = "us-central1"
  project = var.project
}

variable "project" {
  default = "open-parking-spaces"
}

resource "google_bigquery_dataset" "spaces" {
  dataset_id = "spaces"

  // Default access
  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  access {
    role          = "READER"
    special_group = "projectReaders"
  }
  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }

  // Public read-only access
  access {
    role          = "READER"
    special_group = "allAuthenticatedUsers"
  }
}

resource "google_bigquery_table" "spaces" {
  dataset_id = google_bigquery_dataset.spaces.dataset_id
  table_id   = "lot_spaces"
  schema = jsonencode([
    {
      name = "timestamp",
      type = "TIMESTAMP",
      mode = "REQUIRED"
    },
    {
      name = "provider",
      type = "STRING",
      mode = "REQUIRED"
    },
    {
      name = "lot",
      type = "STRING",
      mode = "REQUIRED"
    },
    {
      name = "spaces",
      type = "INTEGER",
      mode = "REQUIRED"
    },
    {
      name = "capacity",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "id",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "url",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "address",
      type = "STRING",
      mode = "NULLABLE"
    },
  ])

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }
  clustering = ["provider"]
}

data "archive_file" "scrape" {
  type        = "zip"
  source_dir  = "${path.module}/../parking_scrapers"
  output_path = "${path.module}/scrape.zip"
}

resource "google_storage_bucket" "functions" {
  project = var.project
  name    = "open-parking-spaces-functions"
}

resource "google_storage_bucket_object" "scrape" {
  name   = "${data.archive_file.scrape.output_sha}.zip"
  bucket = google_storage_bucket.functions.name
  source = data.archive_file.scrape.output_path
}

resource "google_pubsub_topic" "scrape" {
  project = var.project
  name    = "scrape"
}

resource "google_cloudfunctions_function" "scrape" {
  project = var.project
  name    = "scrape"
  runtime = "python37"

  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.scrape.name
  entry_point           = "scrape"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.scrape.name
  }

  depends_on = [google_storage_bucket_object.scrape]
}

resource "google_cloud_scheduler_job" "scrape" {
  project  = var.project
  name     = "scrape"
  schedule = "*/15 * * * *"

  pubsub_target {
    topic_name = google_pubsub_topic.scrape.id
    attributes = {
      action = "scrape"
    }
  }
}
