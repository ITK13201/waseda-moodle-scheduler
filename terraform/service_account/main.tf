terraform {
  required_version = "~> 1.4.0"
  backend "gcs" {
    prefix = "terraform/state/service_account"
  }
}

locals {
  cloud_run_roles = [
    "roles/run.developer",
    "roles/iam.serviceAccountUser"
  ]
}

resource "google_project_service" "project" {
  project = var.project
  service = "iamcredentials.googleapis.com"
}

resource "google_service_account" "service_account" {
  project      = var.project
  account_id   = "terraform"
  display_name = "A service account for terraform"
  description  = "link to Workload Identity Pool used by github actions"
}

resource "google_iam_workload_identity_pool" "github" {
  provider                  = google-beta
  project                   = var.project
  workload_identity_pool_id = "github"
  display_name              = "github"
  description               = "Workload Identity Pool for GitHub Actions"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  provider                           = google-beta
  project                            = var.project
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "github actions provider"
  description                        = "OIDC identity pool provider for execute github actions"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.owner"      = "assertion.repository_owner"
    "attribute.refs"       = "assertion.ref"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "github-account-iam" {
  service_account_id = google_service_account.service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.repo_name}"
}

resource "google_project_iam_member" "service_account" {
  count   = length(local.cloud_run_roles)
  project = var.project
  role    = element(local.cloud_run_roles, count.index)
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

output "service_account_terraform_email" {
  description = "service account for terraform"
  value       = google_service_account.service_account.email
}

output "google_iam_workload_identity_pool_provider_github_name" {
  description = "Workload Identity Pool Provider ID"
  value       = google_iam_workload_identity_pool_provider.github.name
}
