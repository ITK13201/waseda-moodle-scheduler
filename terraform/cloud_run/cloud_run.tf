resource "google_cloud_run_v2_job" "default" {
  name         = "waseda-moodle-scheduler"
  project      = var.project
  location     = var.location
  launch_stage = "BETA"

  template {
    template {
      containers {
        image = var.container_image
        volume_mounts {
          name       = "env-file-volume"
          mount_path = var.prod_env_file_dir
        }
        env {
          name  = "DATABASE_NAME"
          value = var.database_name
        }
        env {
          name  = "DATABASE_USER"
          value = var.database_user
        }
        env {
          name  = "DATABASE_HOST"
          value = var.database_host
        }
        env {
          name  = "DATABASE_PASSWORD"
          value = var.database_password
        }
        env {
          name  = "DATABASE_PORT"
          value = var.database_port
        }
        env {
          name  = "ENV_FILE_PATH"
          value = "${var.prod_env_file_dir}/.env"
        }
      }
      volumes {
        name = "env-file-volume"
        secret {
          secret       = google_secret_manager_secret.secret.secret_id
          default_mode = 292 # 0444
          items {
            version = "latest"
            path    = ".env"
            mode    = 256 # 0400
          }
        }
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
