variable "project" {
  description = "A name of a GCP project"
  type        = string
  default     = null
}
variable "repo_name" {
  description = "github repository name"
  default     = "user/repository"
}
