resource "google_cloud_run_v2_job" "default" {
  name     = "waseda-moodle-scheduler"
  project = var.project
  location = var.location
  launch_stage = "BETA"

  template {
    template {
      containers {
        image = var.container_image
      }
      service_account = var.service_account
    }
  }

  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}
