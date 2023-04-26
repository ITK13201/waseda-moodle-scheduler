resource "google_secret_manager_secret" "secret" {
  project   = var.project
  secret_id = "waseda-moodle-scheduler-env"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret-version-data" {
  secret      = google_secret_manager_secret.secret.name
  secret_data = file(var.local_env_file_path)
}

resource "google_secret_manager_secret_iam_member" "secret-access" {
  secret_id  = google_secret_manager_secret.secret.id
  role       = "roles/secretmanager.secretAccessor"
  member     = "serviceAccount:${var.service_account}"
  depends_on = [google_secret_manager_secret.secret]
}
