variable "prefix" {
  description = "The prefix used for all resources in this environment"
  type        = string
}

variable "ip_ranges" {
  description = "The ip ranges to filter the database on"
  type        = list(any)
  default     = null
}