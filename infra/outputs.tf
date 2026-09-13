output "public_ip" {
  description = "Dirección IP pública estática asignada a la instancia de Compute Engine."
  value       = google_compute_address.static_ip.address
}

output "frontend_url" {
  description = "URL para acceder a la aplicación web (Frontend Nuxt 4)."
  value       = "http://${google_compute_address.static_ip.address}:3000"
}

output "gateway_api_url" {
  description = "URL pública del API Gateway (Nginx)."
  value       = "http://${google_compute_address.static_ip.address}:8000/api/v1"
}

output "ssh_connection_command" {
  description = "Comando rápido para conectarse por SSH usando gcloud CLI."
  value       = "gcloud compute ssh --zone ${var.gcp_zone} ${google_compute_instance.app_vm.name} --project ${var.gcp_project_id}"
}

output "vm_instance_name" {
  description = "Nombre de la instancia de Compute Engine creada."
  value       = google_compute_instance.app_vm.name
}
