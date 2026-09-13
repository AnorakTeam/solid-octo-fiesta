variable "gcp_project_id" {
  description = "El ID del proyecto de Google Cloud donde se desplegarán los recursos."
  type        = string
}

variable "gcp_region" {
  description = "Región de Google Cloud (us-central1 es económica y suele calificar para free tier)."
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "Zona específica dentro de la región seleccionada."
  type        = string
  default     = "us-central1-a"
}

variable "app_name" {
  description = "Prefijo para los nombres de los recursos creados en GCP."
  type        = string
  default     = "solid-octo"
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "machine_type" {
  description = "Tipo de máquina en Compute Engine. e2-small (2GB RAM) o e2-medium (4GB RAM) ofrecen excelente relación costo-rendimiento para microservicios con Docker."
  type        = string
  default     = "e2-small"
}

variable "boot_disk_size_gb" {
  description = "Tamaño del disco de arranque en GB (GCP Free Tier incluye hasta 30GB de disco estándar)."
  type        = number
  default     = 25
}

variable "boot_disk_type" {
  description = "Tipo de disco de almacenamiento (pd-standard para menor costo, o pd-balanced)."
  type        = string
  default     = "pd-balanced"
}

variable "ssh_user" {
  description = "Nombre de usuario para acceso SSH a la instancia."
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key" {
  description = "Clave pública SSH (contenido de ~/.ssh/id_rsa.pub o similar) para inyectar en la VM. Opcional si usas 'gcloud compute ssh'."
  type        = string
  default     = ""
}

variable "allowed_ingress_cidrs" {
  description = "Rangos CIDR permitidos para acceder a la aplicación."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
