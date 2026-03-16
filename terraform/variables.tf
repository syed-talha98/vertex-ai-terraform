variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
}

variable "pipeline_template_path" {
  description = "Path to compiled pipeline JSON"
  default     = "../pipeline.json"
}