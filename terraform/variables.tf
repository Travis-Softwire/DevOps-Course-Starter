variable "prefix" {
  description = "The prefix used for all resources in this environment"
  type        = string
}

variable "secret_key" {
  description = "Cache key used by Flask when storing data in session"
  type        = string
  sensitive   = true
}

variable "github_client_id" {
  description = "Client id for use with github OAuth"
  type        = string
  sensitive   = true
}

variable "github_client_secret" {
  description = "Client secret for use with github OAuth"
  type        = string
  sensitive   = true
}
