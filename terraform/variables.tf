variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "mlops-430311"
}

variable "region" {
  description = "The region the cluster in"
  default     = "us-central1-a"
}

variable "k8s" {
  description = "GKE for text image retrieval app"
  default     = "text-image-retrieval"
}
