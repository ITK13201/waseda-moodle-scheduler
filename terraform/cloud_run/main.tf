terraform {
  required_version = "~> 1.4.0"
  required_providers {
    google = ">= 4.60.0"
  }
  backend "gcs" {
    prefix = "terraform/state/cloud_run"
  }
}

data "google_iam_policy" "cloud_run_public" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_v2_job_iam_policy" "policy" {
  project = google_cloud_run_v2_job.default.project
  location = google_cloud_run_v2_job.default.location
  name = google_cloud_run_v2_job.default.name
  policy_data = data.google_iam_policy.cloud_run_public.policy_data
}
