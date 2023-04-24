variable "project" {
  description = "A name of a GCP project"
  type        = string
  default     = null
}

variable "location" {
  description = "A location of a cloud run instance"
  type        = string
  default     = "asia-northeast1"
}

variable "container_image" {
  description = "docker container image"
  type        = string
  default     = ""
}

variable "service_account" {
  description = "Email address of the IAM service account"
  type        = string
  default     = ""
}

variable "user" {
  description = "Email address of User"
  type        = string
  default     = ""
}
