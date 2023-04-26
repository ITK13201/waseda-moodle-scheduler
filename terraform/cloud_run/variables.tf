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

variable "database_name" {}
variable "database_user" {}
variable "database_host" {}
variable "database_password" {}
variable "database_port" {
  default = "3306"
}
variable "prod_env_file_dir" {}
variable "local_env_file_path" {}
